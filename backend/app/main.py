from __future__ import annotations

import asyncio
import hmac
import json
import sqlite3
from contextlib import asynccontextmanager

from starlette.applications import Starlette
from starlette.concurrency import run_in_threadpool
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.routing import Route

from .analytics import (
    get_analytics_summary,
    initialize_analytics,
    make_analytics_etag,
    normalize_public_path,
    record_pageview,
)
from .api_contract import publication_filters, public_sync_status
from .budget import SyncDeadlineExceeded, sync_budget
from .config import get_settings
from .database import initialize
from .repository import (
    create_researcher,
    get_publications,
    get_sync_status,
    list_scholar_candidates,
    list_researchers,
    make_etag,
)
from .sync_service import SnapshotChanged, sync_all_researchers


settings = get_settings()
sync_lock = asyncio.Lock()


@asynccontextmanager
async def lifespan(_: Starlette):
    await run_in_threadpool(initialize, settings)
    await run_in_threadpool(initialize_analytics, settings)
    yield


async def health(_: Request) -> JSONResponse:
    return JSONResponse({'status': 'ok'})


async def researchers(_: Request) -> JSONResponse:
    data = await run_in_threadpool(list_researchers, settings)
    return _public_json({'researchers': data})


async def papers(request: Request) -> Response:
    if len(request.scope['query_string']) > 8192:
        return _error('论文查询过长', 400)
    try:
        filters = publication_filters(
            request.query_params.getlist, group_policy=request.url.path == '/api/group/papers',
        )
    except ValueError:
        return _error('无效的论文查询参数', 400)
    try:
        data = await run_in_threadpool(get_publications, settings, filters)
    except (sqlite3.Error, ValueError):
        return _error('论文服务暂时不可用', 503)
    etag = make_etag(data['version'], request.url.path + '?' + request.url.query)
    if request.headers.get('if-none-match') == etag:
        return Response(status_code=304, headers={
            'ETag': etag, 'Cache-Control': settings.cache_control,
        })
    return _public_json(data, headers={'ETag': etag})


async def papers_version(_: Request) -> JSONResponse:
    status = await run_in_threadpool(get_sync_status, settings)
    return _public_json({
        'version': status.get('snapshotVersion'),
        'updatedAt': status.get('lastSyncAt'),
    })


async def sync_status(_: Request) -> JSONResponse:
    return _public_json(public_sync_status(await run_in_threadpool(get_sync_status, settings)))


async def analytics_pageview(request: Request) -> Response:
    if not _analytics_origin_allowed(request):
        return JSONResponse(
            {'error': '不允许的请求来源'},
            status_code=403,
            headers={'Cache-Control': 'no-store'},
        )
    try:
        payload = await _bounded_json(request, 1024)
        path = normalize_public_path(payload.get('path') if isinstance(payload, dict) else None)
        if path is None:
            raise ValueError('无效的页面路径')
    except BodyTooLarge:
        return _error('请求体过大', 413)
    except ValueError:
        return JSONResponse(
            {'error': '无效的访问记录'},
            status_code=400,
            headers={'Cache-Control': 'no-store'},
        )

    await run_in_threadpool(
        record_pageview,
        settings,
        path=path,
        client_ip=_analytics_client_ip(request),
        user_agent=request.headers.get('user-agent', ''),
    )
    return Response(status_code=204, headers={'Cache-Control': 'no-store'})


async def analytics_summary(request: Request) -> Response:
    data = await run_in_threadpool(get_analytics_summary, settings)
    etag = make_analytics_etag(data)
    headers = {'ETag': etag, 'Cache-Control': settings.analytics_cache_control}
    if request.headers.get('if-none-match') == etag:
        return Response(status_code=304, headers=headers)
    return JSONResponse(data, headers=headers)


async def trigger_sync(request: Request) -> JSONResponse:
    unauthorized = _require_admin(request)
    if unauthorized:
        return unauthorized
    if sync_lock.locked():
        return _error('同步任务正在运行', 409)
    async with sync_lock:
        try:
            with sync_budget(70):
                result = await run_in_threadpool(sync_all_researchers, settings)
            return JSONResponse(result.as_dict(), headers={'Cache-Control': 'no-store'})
        except SnapshotChanged:
            return _error('其他任务已更新数据，请重试', 409)
        except SyncDeadlineExceeded:
            return _error('同步超时，已保留上次完整快照', 504)
        except Exception:
            return _error('论文同步失败，已保留上次完整快照', 502)


async def add_researcher(request: Request) -> JSONResponse:
    unauthorized = _require_admin(request)
    if unauthorized:
        return unauthorized
    try:
        payload = await _bounded_json(request, 8192)
        researcher = await run_in_threadpool(create_researcher, settings, payload)
        return JSONResponse(researcher, status_code=201, headers={'Cache-Control': 'no-store'})
    except BodyTooLarge:
        return _error('请求体过大', 413)
    except ValueError:
        return _error('无效的研究者数据', 400)
    except sqlite3.IntegrityError:
        return _error('研究者已存在或标识冲突', 409)


async def scholar_candidates(request: Request) -> JSONResponse:
    unauthorized = _require_admin(request)
    if unauthorized:
        return unauthorized
    data = await run_in_threadpool(list_scholar_candidates, settings)
    return JSONResponse({'candidates': data}, headers={'Cache-Control': 'no-store'})


def _error(message: str, status: int) -> JSONResponse:
    return JSONResponse({'error': message}, status_code=status, headers={'Cache-Control': 'no-store'})


class BodyTooLarge(ValueError):
    pass


async def _bounded_json(request: Request, limit: int) -> dict:
    body = bytearray()
    async for chunk in request.stream():
        if len(body) + len(chunk) > limit:
            raise BodyTooLarge()
        body.extend(chunk)
    payload = json.loads(body)
    if not isinstance(payload, dict):
        raise ValueError('JSON 请求体必须是对象')
    return payload


def _require_admin(request: Request) -> JSONResponse | None:
    if not settings.sync_token or len(settings.sync_token) < 32:
        return _error('管理接口暂不可用', 503)
    actual = request.headers.get('authorization', '')
    expected = f'Bearer {settings.sync_token}'
    if not hmac.compare_digest(actual.encode(), expected.encode()):
        return _error('Unauthorized', 401)
    return None


def _analytics_origin_allowed(request: Request) -> bool:
    origin = (request.headers.get('origin') or '').rstrip('/')
    if not origin:
        return request.headers.get('sec-fetch-site', '') in ('', 'same-origin', 'same-site')
    request_origin = f'{request.url.scheme}://{request.url.netloc}'.rstrip('/')
    allowed = {value.rstrip('/') for value in settings.allowed_origins}
    return origin == request_origin or origin in allowed


def _analytics_client_ip(request: Request) -> str:
    cloudflare_ip = request.headers.get('cf-connecting-ip')
    if cloudflare_ip:
        return cloudflare_ip.strip()
    forwarded = request.headers.get('x-forwarded-for')
    if forwarded:
        return forwarded.split(',', 1)[0].strip()
    real_ip = request.headers.get('x-real-ip')
    if real_ip:
        return real_ip.strip()
    return request.client.host if request.client else 'unknown'


def _public_json(payload: dict, *, headers: dict | None = None) -> JSONResponse:
    response_headers = {'Cache-Control': settings.cache_control, **(headers or {})}
    return JSONResponse(payload, headers=response_headers)


routes = [
    Route('/health', health),
    Route('/api/researchers', researchers),
    Route('/api/papers', papers),
    Route('/api/group/papers', papers),
    Route('/api/papers/version', papers_version),
    Route('/api/sync/status', sync_status),
    Route('/api/analytics/pageview', analytics_pageview, methods=['POST']),
    Route('/api/analytics/summary', analytics_summary),
    Route('/api/admin/sync', trigger_sync, methods=['POST']),
    Route('/api/admin/researchers', add_researcher, methods=['POST']),
    Route('/api/admin/scholar-candidates', scholar_candidates),
]

app = Starlette(routes=routes, lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=list(settings.allowed_origins),
    allow_methods=['GET', 'POST'],
    allow_headers=['Authorization', 'Content-Type', 'If-None-Match'],
    expose_headers=['ETag'],
)
