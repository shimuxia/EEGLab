from __future__ import annotations
import unittest
from unittest.mock import patch
from starlette.testclient import TestClient
import test_backend as base
from app.database import connect, normalize_title
from app.group_policy import PROTECTED_EXCLUSIONS, validate_recovery_rules
from app.repository import get_publications, create_researcher

class GroupPolicyTests(unittest.TestCase):
    def setUp(self):
        self.fixture = base.BackendTestCase()
        self.fixture.setUp()
        self.settings = self.fixture.settings
        with connect(self.settings.database_path) as db:
            db.execute("UPDATE researcher_papers SET source_match_status='confirmed'")
            self.ids = [r['id'] for r in db.execute('SELECT id FROM papers ORDER BY id LIMIT 2')]
            for pid, (oid, doi, title) in zip(self.ids, PROTECTED_EXCLUSIONS):
                db.execute('UPDATE papers SET openalex_id=?,doi=?,title=?,normalized_title=? WHERE id=?',
                           (oid, doi, title, normalize_title(title), pid))

    def tearDown(self):
        self.fixture.tearDown()

    def test_exclusion_before_pagination_and_counts_even_if_confirmed(self):
        result = get_publications(self.settings, {'group_policy': True, 'limit': 1})
        self.assertEqual(result['total'], 134)
        self.assertEqual(result['researchers'][0]['currentPaperCount'], 134)
        self.assertEqual(len(result['papers']), 1)
        result = get_publications(self.settings, {'group_policy': True, 'limit': 500})
        self.assertFalse({p['id'] for p in result['papers']} & {x[0] for x in PROTECTED_EXCLUSIONS})

    def test_shared_paper_remains_for_other_researcher(self):
        other = create_researcher(self.settings, {'slug':'independent','name':'Synthetic','openalexAuthorId':'A222222'})
        with connect(self.settings.database_path) as db:
            db.execute("INSERT INTO researcher_papers(researcher_id,paper_id,source_match_status) VALUES (?,?,'confirmed')",
                       (other['id'],self.ids[0]))
        all_data = get_publications(self.settings, {'group_policy':True})
        shared = next(p for p in all_data['papers'] if p['id']==PROTECTED_EXCLUSIONS[0][0])
        self.assertEqual([r['slug'] for r in shared['researchers']], ['independent'])
        self.assertEqual(get_publications(self.settings, {'group_policy':True,'researchers':{'ying-yan'}})['total'],134)

    def test_openalex_only_review_and_excluded_links_are_hidden(self):
        for state in ('openalex_only','review','excluded'):
            with connect(self.settings.database_path) as db:
                db.execute('UPDATE researcher_papers SET source_match_status=?',(state,))
            self.assertEqual(get_publications(self.settings, {'group_policy':True})['total'],0)

    def test_recovery_missing_or_accept_alias_fails_without_writes(self):
        with connect(self.settings.database_path) as db:
            before = db.total_changes
            with self.assertRaises(ValueError): validate_recovery_rules(db)
            self.assertEqual(before, db.total_changes)
            for oid,doi,title in PROTECTED_EXCLUSIONS:
                db.execute("INSERT INTO scholar_review_rules(researcher_id,citation_id,decision,target_openalex_id,target_doi,target_normalized_title,reviewed_at) VALUES (1,?,'exclude',?,?,?,'synthetic')",
                           ('manual:'+oid,oid,doi,normalize_title(title)))
            validate_recovery_rules(db)
            db.execute("INSERT INTO scholar_review_rules(researcher_id,citation_id,decision,target_doi,reviewed_at) VALUES(1,'alias','accept',?,'synthetic')",(PROTECTED_EXCLUSIONS[0][1],))
            with self.assertRaises(ValueError): validate_recovery_rules(db)

    def test_api_policy_etag_filters_and_read_only_manual_fields(self):
        from app import main
        with connect(self.settings.database_path) as db:
            before = [tuple(r) for r in db.execute('SELECT * FROM paper_overrides')]
        with patch.object(main, 'settings', self.settings):
            with TestClient(main.app) as client:
                response = client.get('/api/group/papers?researcher=ying-yan&limit=1')
                self.assertEqual(response.status_code,200)
                self.assertEqual(response.json()['total'],134)
                self.assertEqual(client.get('/api/group/papers?researcher=ying-yan&limit=1',
                                 headers={'If-None-Match':response.headers['etag']}).status_code,304)
                self.assertNotEqual(response.headers['etag'],client.get('/api/papers?researcher=ying-yan&limit=1').headers['etag'])
        with connect(self.settings.database_path) as db:
            self.assertEqual(before,[tuple(r) for r in db.execute('SELECT * FROM paper_overrides')])

    def test_exclude_rule_overrides_confirmed_link_without_touching_paper(self):
        with connect(self.settings.database_path) as db:
            target = db.execute('SELECT * FROM papers WHERE id NOT IN (?,?) LIMIT 1',self.ids).fetchone()
            db.execute("INSERT INTO scholar_review_rules(researcher_id,citation_id,decision,target_normalized_title,reviewed_at) VALUES(1,'synthetic-exclude','exclude',?,'synthetic')",(target['normalized_title'],))
        result=get_publications(self.settings,{'group_policy':True})
        self.assertEqual(result['total'],133)
        self.assertNotIn(target['title'],[p['title'] for p in result['papers']])

    def test_counts_cover_more_than_api_page_limit(self):
        with connect(self.settings.database_path) as db:
            for i in range(510):
                cursor = db.execute("INSERT INTO papers(normalized_title,title,created_at,updated_at) VALUES(?,?,'synthetic','synthetic')",
                                    (f'synthetic{i}',f'Synthetic {i}'))
                db.execute("INSERT INTO researcher_papers(researcher_id,paper_id,source_match_status) VALUES(1,?,'confirmed')",
                           (cursor.lastrowid,))
        result=get_publications(self.settings,{'group_policy':True,'limit':500})
        self.assertEqual(result['total'],644)
        self.assertEqual(len(result['papers']),500)
        self.assertEqual(result['researchers'][0]['currentPaperCount'],644)

    def test_cloud_adapter_uses_same_policy_without_real_cos(self):
        from app.cloud_api import dispatch
        from test_cloud import MemoryStore, settings
        import json
        code, headers, body = dispatch('GET','/api/group/papers',{'host':'lab.example.cn'},b'',
                                      store=MemoryStore(),settings=settings())
        self.assertEqual(code,200)
        data=json.loads(body)
        self.assertTrue(data['version'].endswith(':group-scholar-v1'))
        self.assertTrue(all(r['sourceMatchStatus']=='confirmed'
                            for p in data['papers'] for r in p['researchers'] if r['slug']=='ying-yan'))
