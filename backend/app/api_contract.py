"""Shared request and response rules for the two HTTP adapters."""
from __future__ import annotations

import re


def publication_filters(getlist, *, group_policy: bool) -> dict:
    def scalar(name: str, *, size: int = 256) -> str | None:
        values = getlist(name)
        if len(values) > 1 or (values and len(values[0]) > size):
            raise ValueError('无效的论文查询参数')
        return (values[0].strip() or None) if values else None

    def integer(name: str, default: int | None, minimum: int, maximum: int) -> int | None:
        value = scalar(name, size=9)
        if value is None:
            return default
        if not re.fullmatch('[0-9]+', value) or not minimum <= int(value) <= maximum:
            raise ValueError('无效的论文查询参数')
        return int(value)

    raw_researchers = getlist('researcher')
    if len(raw_researchers) > 20 or any(len(value) > 1024 for value in raw_researchers):
        raise ValueError('无效的研究者筛选参数')
    slugs = {slug.strip() for value in raw_researchers for slug in value.split(',') if slug.strip()}
    if len(slugs) > 20 or any(len(slug) > 64 for slug in slugs):
        raise ValueError('无效的研究者筛选参数')
    representative = (scalar('representative', size=5) or '').lower()
    if representative not in ('', 'true', 'false'):
        raise ValueError('无效的论文查询参数')
    return {
        'group_policy': group_policy,
        'researchers': slugs,
        'tag': scalar('tag'),
        'field': scalar('field'),
        'query': scalar('q'),
        'year': integer('year', None, 1, 9999),
        'representative': representative == 'true',
        'limit': integer('limit', 500, 1, 999_999),
        'offset': integer('offset', 0, 0, 1_000_000),
    }


def public_sync_status(status: dict) -> dict:
    """Expose state and counts, without historical diagnostic strings."""
    public = dict(status)
    if status.get('error'):
        public['error'] = '论文同步失败，已保留上次完整快照'
    sources = status.get('sources')
    if isinstance(sources, dict) and 'warnings' in sources:
        public['sources'] = {
            **sources,
            'warnings': ['Google Scholar 同步异常，已保留上次核验数据'] if sources['warnings'] else [],
        }
    attempt = status.get('lastAttempt')
    if isinstance(attempt, dict):
        public['lastAttempt'] = public_sync_status(attempt)
    return public
