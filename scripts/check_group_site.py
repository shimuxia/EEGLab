"""Local-only browser acceptance. Requires built frontend and localhost preview."""
from __future__ import annotations
import json
import os
from pathlib import Path
from urllib.parse import urlparse, unquote
from html.parser import HTMLParser
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'frontend/dist'
OUT = Path(os.getenv('QA_OUTPUT_DIR', ROOT / 'output'))
BASE = 'http://127.0.0.1:' + str(int(os.getenv('QA_PREVIEW_PORT', '4327')))
ROUTES = ['/', '/about', '/research', '/team', '/achievements', '/join', '/contact',
          '/research/brain-computer-interface',
          *['/research/'+s for s in ['diagnosis','arm','drone','hand','glove']]]
class References(HTMLParser):
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        for key in ('src','poster','href'):
            value=attrs.get(key,'')
            parsed=urlparse(value)
            if value.startswith('/') and not value.startswith('//') and not parsed.path.startswith('/api/'):
                target=DIST / unquote(parsed.path).lstrip('/')
                assert target.exists() or target.with_suffix('.html').exists(), f'Broken reference {value}'

def run():
    OUT.mkdir(exist_ok=True)
    for file in DIST.rglob('*.html'):
        References().feed(file.read_text())
    checks=[]
    with sync_playwright() as pw:
        executable=os.getenv('CHROMIUM_PATH')
        browser=pw.chromium.launch(**({'executable_path':executable} if executable else {}),headless=True)
        for width in (1440,390,768):
            context=browser.new_context(viewport={'width':width,'height':950},reduced_motion='reduce')
            context.route('**/*', lambda route: route.continue_() if route.request.url.startswith(BASE) else route.abort())
            context.route('**/api/**', lambda route: route.fulfill(status=503,content_type='application/json',body='{}'))
            page=context.new_page()
            errors=[];missing=[]
            page.on('pageerror',lambda err:errors.append(str(err)))
            page.on('response',lambda res:missing.append(res.url) if res.status==404 else None)
            for route in ROUTES:
                response=page.goto(BASE+route,wait_until='networkidle')
                assert response.status==200,(route,response.status)
                assert page.locator('h1').count()==1,route
                assert page.evaluate('document.documentElement.scrollWidth<=window.innerWidth'),(width,route,'overflow')
                assert page.locator('h1').is_visible(),route
                page.locator('img').evaluate_all("async imgs=>{imgs.forEach(i=>i.loading='eager');await Promise.all(imgs.map(i=>i.decode().catch(()=>{})))}")
                broken=page.locator('img').evaluate_all('(imgs)=>imgs.filter(i=>i.complete&&i.naturalWidth===0).map(i=>i.src)')
                assert not broken,(route,broken)
                if width<=768:
                    toggle=page.locator('#nav-toggle')
                    toggle.click()
                    assert toggle.get_attribute('aria-expanded')=='true'
                    assert page.locator('#nav-links a[href="/join"]').is_visible()
                    page.locator('#nav-links a[href="/join"]').click()
                    assert page.url.endswith('/join')
                if route=='/achievements':
                    page.goto(BASE+route,wait_until='networkidle')
                    assert page.get_by_text('已保留静态代表论文').is_visible()
                    assert page.get_by_role('button',name='重新加载').is_visible()
                    chip=page.locator('.gf-chip').first
                    chip.click()
                    assert 'active' in chip.get_attribute('class')
                checks.append({'width':width,'route':route,'status':'PASS'})
            assert not errors,errors
            assert not missing,missing
            page.goto(BASE,wait_until='networkidle')
            page.locator('img').evaluate_all("imgs=>imgs.forEach(i=>i.loading='eager')")
            page.wait_for_timeout(300)
            page.screenshot(path=str(OUT/f'home-{width}.png'),full_page=True)
            page.goto(BASE+'/team',wait_until='networkidle')
            page.locator('img').evaluate_all("imgs=>imgs.forEach(i=>i.loading='eager')")
            page.wait_for_timeout(300)
            page.screenshot(path=str(OUT/f'team-{width}.png'),full_page=True)
            context.close()
        # New homepage interactions, both responsive layouts and motion preferences.
        for width in (1440, 390):
            context=browser.new_context(viewport={'width':width,'height':950},reduced_motion='reduce')
            context.route('**/*',lambda route:route.continue_() if route.request.url.startswith(BASE) else route.abort())
            page=context.new_page()
            page.goto(BASE,wait_until='networkidle')
            tabs=page.get_by_role('tab')
            assert tabs.count()==7
            for i in range(7):
                tabs.nth(i).click()
                assert tabs.nth(i).get_attribute('aria-selected')=='true'
                panel=page.locator(f'#research-panel-{i}')
                assert panel.is_visible()
                assert page.locator('[role="tabpanel"]:visible').count()==1
                artwork=panel.locator('.research-art').bounding_box()
                copy=panel.locator('.research-panel-copy').bounding_box()
                assert artwork['y']+artwork['height'] <= copy['y']+1, 'Artwork overlaps copy'
            tabs.nth(6).press('Home')
            assert tabs.nth(0).get_attribute('aria-selected')=='true'
            tabs.nth(0).press('ArrowDown')
            assert tabs.nth(1).get_attribute('aria-selected')=='true'
            video=page.locator('[data-hero-video]')
            assert video.evaluate('(v)=>v.paused'), 'Reduced motion should pause video'
            video.scroll_into_view_if_needed()
            page.get_by_role('button',name='播放实验视频').click()
            page.wait_for_function("!document.querySelector('[data-hero-video]').paused")
            page.get_by_role('button',name='暂停实验视频').click()
            assert video.evaluate('(v)=>v.paused')
            if width==390:
                page.locator('#nav-toggle').click()
                page.keyboard.press('Escape')
                assert page.locator('#nav-toggle').get_attribute('aria-expanded')=='false'
            checks.append({'case':'research tabs/keyboard, artwork separation, video control/reduced motion, menu Escape','width':width,'status':'PASS'})
            context.close()
        context=browser.new_context(viewport={'width':1440,'height':950},reduced_motion='no-preference')
        context.route('**/*',lambda route:route.continue_() if route.request.url.startswith(BASE) else route.abort())
        page=context.new_page();page.goto(BASE,wait_until='networkidle')
        page.locator('.home-intro').scroll_into_view_if_needed()
        page.wait_for_function("document.querySelector('.home-intro').classList.contains('is-visible')")
        checks.append({'case':'normal motion scroll reveal','status':'PASS'})
        context.close()
        # Synthetic API success and interactive filtering are explicitly isolated.
        context=browser.new_context(viewport={'width':1440,'height':950})
        payload={'version':'synthetic','updatedAt':'2026-11-15T00:00:00Z','total':1,
                 'offset':0,'limit':500,'fields':['EEG'],'filterTags':['EEG'],'years':[2026],
                 'researchers':[{'id':1,'slug':'synthetic','name':'测试研究者','paperCount':1,'currentPaperCount':1}],
                 'papers':[{'id':'synthetic','num':'01','year':2026,'title':'合成论文用于本地验收',
                            'authors':'Synthetic Author','journal':'Synthetic Journal','type':'journal',
                            'citedByCount':0,'field':'EEG','tags':['EEG'],'isTop':False,'lead':True,
                            'representative':True,'researchers':[{'id':1,'slug':'synthetic','name':'测试研究者'}]}]}
        context.route('**/*',lambda route:route.continue_() if route.request.url.startswith(BASE) else route.abort())
        context.route('**/api/**',lambda route:route.fulfill(status=200,content_type='application/json',body=json.dumps(payload)))
        page=context.new_page();page.goto(BASE+'/achievements',wait_until='networkidle')
        assert page.get_by_text('合成论文用于本地验收',exact=True).is_visible()
        page.get_by_role('button',name='测试研究者').click()
        page.get_by_placeholder('搜索标题、作者或期刊').fill('不会匹配')
        assert page.get_by_text('当前条件下暂无论文').is_visible()
        page.get_by_placeholder('搜索标题、作者或期刊').fill('合成论文')
        assert page.get_by_text('合成论文用于本地验收',exact=True).is_visible()
        checks.append({'case':'synthetic API success/researcher/search and API 503 fallback','status':'PASS'})
        browser.close()
    (OUT/'browser-results.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2))
    print(f'{len(checks)} browser checks passed; local assets and links passed')
if __name__=='__main__':run()
