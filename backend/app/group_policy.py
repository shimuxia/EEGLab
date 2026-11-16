"""Read-only, researcher-scoped publication policy for the unified group website."""
from __future__ import annotations

from .database import normalize_doi, normalize_title

POLICY_VERSION = 'group-scholar-v1'
# Approved historical false positives; a seed edit cannot revoke this baseline.
PROTECTED_EXCLUSIONS = (
    ('W7163642400', '10.1117/12.3116350',
     'Research on repeated quantum error detection based on surface codes'),
    ('W7163778240', '10.48550/arxiv.2606.05405', "Agents' Last Exam"),
)


def matches(paper, *, oid=None, doi=None, title=None) -> bool:
    return bool(
        (oid and (paper['openalex_id'] or '').rsplit('/', 1)[-1] == oid.rsplit('/', 1)[-1])
        or (doi and normalize_doi(paper['doi']) == normalize_doi(doi))
        or (title and normalize_title(paper['title']) == normalize_title(title))
    )


def public_association(link, paper, rules) -> bool:
    if link['slug'] == 'ying-yan' and any(
        matches(paper, oid=oid, doi=doi, title=title)
        for oid, doi, title in PROTECTED_EXCLUSIONS
    ):
        return False
    applicable = [rule for rule in rules if rule['researcher_id'] == link['researcher_id']]
    for rule in applicable:
        if rule['decision'] == 'exclude' and (
            (link['scholar_citation_id'] and rule['citation_id'] == link['scholar_citation_id'])
            or matches(paper, oid=rule['target_openalex_id'], doi=rule['target_doi'],
                       title=rule['target_normalized_title'])
        ):
            return False
    if link['source_match_status'] in ('excluded', 'review'):
        return False
    # Other researchers keep their own source policy; no name-based global exclusion.
    return link['slug'] != 'ying-yan' or link['source_match_status'] == 'confirmed'


def validate_recovery_rules(connection) -> None:
    """Migration preflight on a backup copy; never seeds or repairs missing decisions."""
    rows = connection.execute(
        "SELECT rr.* FROM scholar_review_rules rr JOIN researchers r "
        "ON r.id=rr.researcher_id WHERE r.slug='ying-yan'"
    ).fetchall()
    for oid, doi, title in PROTECTED_EXCLUSIONS:
        target = {'openalex_id': oid, 'doi': doi, 'title': title}
        matching = [r for r in rows if matches(
            target, oid=r['target_openalex_id'], doi=r['target_doi'],
            title=r['target_normalized_title'])]
        if any(r['decision'] == 'accept' for r in matching) or not any(
            r['decision'] == 'exclude'
            and (r['target_openalex_id'] or '').rsplit('/', 1)[-1] == oid
            and normalize_doi(r['target_doi']) == normalize_doi(doi)
            and r['target_normalized_title'] == normalize_title(title)
            for r in matching
        ):
            raise ValueError('Approved recovery exclusion baseline missing or conflicting')
