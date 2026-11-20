from __future__ import annotations

from dataclasses import replace
import unittest
from unittest.mock import patch

from starlette.testclient import TestClient

from app import main
from app.cloud_api import dispatch
from app.database import connect, initialize
from app.repository import get_publications
from app.sync_service import _upsert_work, sync_all_researchers
import test_backend as fixtures
from test_cloud import MemoryStore, settings as cloud_settings


class UnifiedContractTests(unittest.TestCase):
    def setUp(self):
        fixture = fixtures.BackendTestCase()
        fixture.setUp()
        self.addCleanup(fixture.tearDown)
        self.settings = fixture.settings
        self.cloud = cloud_settings()
        self.store = MemoryStore()
        patcher = patch.object(main, 'settings', self.settings)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.client = TestClient(main.app, raise_server_exceptions=False)
        self.addCleanup(self.client.close)

    def test_invalid_paper_queries_have_consistent_status(self):
        for query in ('year=bad', 'representative=maybe', 'limit=0', 'offset=-1', 'q=' + 'a' * 300):
            with self.subTest(query=query[:35]):
                path = '/api/group/papers?' + query
                local = self.client.get(path)
                remote = dispatch('GET', path, store=self.store, settings=self.cloud)
                self.assertEqual((local.status_code, remote[0]), (400, 400))
                self.assertEqual(local.headers['cache-control'], 'no-store')

    def test_admin_json_shape_and_duplicates(self):
        path = '/api/admin/researchers'
        local = {'Authorization': 'Bearer ' + self.settings.sync_token}
        remote = {'Authorization': 'Bearer ' + self.cloud.sync_token}
        for payload, expected in [(b'[]', 400), (b'{', 400), (b' ' * 8193, 413),
                                  (b'{"slug":"extra","name":["Invalid"],"openalexAuthorId":"A123"}', 400),
                                  (b'{"slug":"extra","name":"Fixture","openalexAuthorId":"A123"}', 201),
                                  (b'{"slug":"extra","name":"Fixture","openalexAuthorId":"A123"}', 409)]:
            with self.subTest(status=expected, payload=payload[:40]):
                a = self.client.post(path, content=payload, headers=local)
                b = dispatch('POST', path, remote, payload, store=self.store, settings=self.cloud)
                self.assertEqual((a.status_code, b[0]), (expected, expected))
                self.assertEqual(a.headers['cache-control'], 'no-store')

    def test_sync_failure_keeps_version_and_public_status_omits_details(self):
        before = self.client.get('/api/papers/version').json()
        unpublished_detail = 'synthetic upstream detail'
        with patch('app.sync_service.fetch_author_works', side_effect=RuntimeError(unpublished_detail)):
            with self.assertRaises(RuntimeError):
                sync_all_researchers(self.settings)
        self.assertEqual(self.client.get('/api/papers/version').json(), before)
        response = self.client.get('/api/sync/status')
        self.assertEqual(response.json()['status'], 'failed')
        self.assertNotIn(unpublished_detail, response.text)

    def test_group_current_count_omits_historical_associations(self):
        with connect(self.settings.database_path) as connection:
            connection.execute("""
                UPDATE researcher_papers SET source_match_status='confirmed', missing_since='historical'
                WHERE paper_id=(SELECT MIN(id) FROM papers)
            """)
        data = get_publications(self.settings, {'group_policy': True})
        count = data['researchers'][0]
        self.assertEqual(count['paperCount'], 1)
        self.assertEqual(count['currentPaperCount'], 0)

    def test_title_collision_does_not_reassign_a_distinct_identified_paper(self):
        paper = get_publications(self.settings, {})['papers'][0]
        original = fixtures._fake_work(paper, 0)
        other = {**original, 'id': 'https://openalex.org/W9999901', 'doi': None,
                 'publication_year': original['publication_year'] - 3}
        with connect(self.settings.database_path) as connection:
            first, _ = _upsert_work(connection, original, 'synthetic')
            second, inserted = _upsert_work(connection, other, 'synthetic')
        self.assertTrue(inserted)
        self.assertNotEqual(first, second)

    def test_reinitialization_preserves_review_decisions(self):
        review_settings = cloud_settings()
        review_settings = replace(review_settings, database_path=self.settings.database_path)
        initialize(review_settings)
        with connect(self.settings.database_path) as connection:
            row = connection.execute('SELECT researcher_id,citation_id FROM scholar_review_rules LIMIT 1').fetchone()
            connection.execute("""
                UPDATE scholar_review_rules SET decision='exclude', notes='local review'
                WHERE researcher_id=? AND citation_id=?
            """, tuple(row))
        initialize(review_settings)
        with connect(self.settings.database_path) as connection:
            review = connection.execute("""
                SELECT decision,notes FROM scholar_review_rules WHERE researcher_id=? AND citation_id=?
            """, tuple(row)).fetchone()
        self.assertEqual(tuple(review), ('exclude', 'local review'))

    def test_standalone_backup_preflight_is_read_only(self):
        from hashlib import sha256
        from pathlib import Path
        import subprocess
        import sys
        import os

        reviewed = replace(cloud_settings(), database_path=self.settings.database_path)
        initialize(reviewed)
        root = Path(__file__).resolve().parents[2]
        def check():
            return subprocess.run(
                [sys.executable, str(root / 'scripts/check_publication_recovery.py'), str(reviewed.database_path)],
                env={**os.environ, 'PYTHONPATH': str(root / 'backend')}, capture_output=True,
            )
        before = sha256(reviewed.database_path.read_bytes()).digest()
        self.assertEqual(check().returncode, 0)
        self.assertEqual(before, sha256(reviewed.database_path.read_bytes()).digest())
        with connect(reviewed.database_path) as db:
            db.execute("DELETE FROM scholar_review_rules WHERE citation_id LIKE 'manual:openalex:%'")
        before = sha256(reviewed.database_path.read_bytes()).digest()
        self.assertNotEqual(check().returncode, 0)
        self.assertEqual(before, sha256(reviewed.database_path.read_bytes()).digest())

    def test_duplicate_rows_cannot_satisfy_upstream_minimum(self):
        snapshot = get_publications(self.settings, {})
        row = fixtures._fake_work(snapshot['papers'][0], 1)
        with patch('app.sync_service.fetch_author_works', return_value=[row] * 20):
            with self.assertRaises(RuntimeError):
                sync_all_researchers(self.settings)
        self.assertEqual(get_publications(self.settings, {})['version'], snapshot['version'])

    def test_short_or_absent_admin_credentials_fail_closed(self):
        for short in (None, 'short'):
            with patch.object(main, 'settings', replace(self.settings, sync_token=short)):
                path = '/api/admin/scholar-candidates'
                local = self.client.get(path)
                cloud = dispatch('GET', path, store=self.store, settings=replace(self.cloud, sync_token=short))
                self.assertEqual((local.status_code, cloud[0]), (503, 503))

    def test_repeat_initialization_cannot_override_manual_visibility(self):
        reviewed = replace(cloud_settings(), database_path=self.settings.database_path)
        with connect(reviewed.database_path) as db:
            target = db.execute("SELECT id FROM papers WHERE doi IS NOT NULL LIMIT 1").fetchone()[0]
            db.execute("UPDATE paper_overrides SET hidden=1,notes=NULL WHERE paper_id=?", (target,))
        initialize(reviewed)
        with connect(reviewed.database_path) as db:
            self.assertEqual(db.execute("SELECT hidden FROM paper_overrides WHERE paper_id=?", (target,)).fetchone()[0], 1)

    def test_sync_cannot_publish_after_a_concurrent_catalog_edit(self):
        from app.repository import create_researcher
        catalog = get_publications(self.settings, {})
        works = [fixtures._fake_work(paper, i) for i, paper in enumerate(catalog['papers'][:20])]
        versions = []
        def edit_during_fetch(*args):
            create_researcher(self.settings, {'slug': 'edited', 'name': 'Test', 'openalexAuthorId': 'A321'})
            versions.append(get_publications(self.settings, {})['version'])
            return works
        with patch('app.sync_service.fetch_author_works', side_effect=edit_during_fetch):
            with self.assertRaisesRegex(RuntimeError, '版本'):
                sync_all_researchers(self.settings)
        self.assertEqual(get_publications(self.settings, {})['version'], versions[0])

    def test_retry_after_http_date_retries_without_network_or_sleep(self):
        import io
        from email.utils import formatdate
        import time
        from urllib.error import HTTPError
        from app import openalex
        failure = HTTPError('https://example.invalid', 429, 'rate limit',
                            {'Retry-After': formatdate(time.time() + 10, usegmt=True)}, io.BytesIO(b''))
        with patch('urllib.request.urlopen', side_effect=[failure, io.BytesIO(b'{}')]) as mock_open:
            with patch.object(openalex, 'retry_sleep') as wait:
                self.assertEqual(openalex._request_json('https://example.invalid', timeout=5, max_attempts=2), {})
        self.assertEqual(mock_open.call_count, 2)
        self.assertTrue(0 <= wait.call_args.args[0] <= 10)


if __name__ == '__main__':
    unittest.main()
