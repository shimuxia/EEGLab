"""Adversarial local acceptance: accessibility, narrow layouts, corrupt APIs and media failure."""
from __future__ import annotations

import copy
import json
import os
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
from check_group_site import BASE, ROUTES

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'output'
AXE = Path(os.getenv('AXE_PATH', OUT / 'accessibility/node_modules/axe-core/axe.min.js'))
PAYLOAD = {
    'version':'synthetic', 'updatedAt':'', 'total':1, 'offset':0, 'limit':500,
    'filterTags':['EEG'], 'fields':['EEG'], 'years':[2026],
    'researchers':[{'id':1,'slug':'synthetic','name':'Test','paperCount':1,'currentPaperCount':1}],
    'papers':[{'id':'test','num':'01','title':'合成边界测试','authors':'Test','journal':'Test',
               'year':2026,'type':'journal','citedByCount':0,'field':'EEG','tags':['EEG'],
               'isTop':False,'lead':True,'representative':True,
               'researchers':[{'id':1,'slug':'synthetic','name':'Test'}]}],
}


def run():
    assert AXE.is_file(), 'Install axe-core@4.14.0 in output/accessibility first'
    results=[]
    with sync_playwright() as pw:
        executable=os.getenv('CHROMIUM_PATH')
        browser=pw.chromium.launch(**({'executable_path':executable} if executable else {}))
        context=browser.new_context(reduced_motion='reduce')
        context.route('**/*', lambda route: route.continue_() if route.request.url.startswith(BASE) else route.abort())
        context.route('**/api/**', lambda route: route.fulfill(status=503,content_type='application/json',body='{}'))
        page=context.new_page()
        for width in (1440,390):
            page.set_viewport_size({'width':width,'height':950})
            for route in ROUTES:
                page.goto(BASE+route,wait_until='networkidle')
                page.add_script_tag(path=str(AXE))
                data=page.evaluate("""async()=>await axe.run(document,{
                    runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa','wcag22aa']}
                })""")
                failures=[{'id':v['id'],'impact':v['impact'],
                           'targets':[n['target'] for n in v['nodes']]} for v in data['violations']]
                results.append({'case':'axe WCAG','width':width,'route':route,'violations':failures})
        for width in (320,360,640,1024,1920):
            page.set_viewport_size({'width':width,'height':950})
            for route in ROUTES:
                page.goto(BASE+route,wait_until='networkidle')
                overflow=page.evaluate('document.documentElement.scrollWidth>innerWidth')
                results.append({'case':'narrow/zoom-equivalent/wide layout','width':width,'route':route,'overflow':overflow})
        for width in (1440,390):
            page.set_viewport_size({'width':width,'height':950})
            for route in ROUTES:
                page.goto(BASE+route,wait_until='networkidle')
                page.evaluate("""()=>{
                    const values=Array.from(document.querySelectorAll('body *'))
                      .filter(e=>!(e instanceof SVGElement))
                      .map(e=>[e,getComputedStyle(e).fontSize]);
                    values.forEach(([e,size])=>e.style.fontSize=(parseFloat(size)*2)+'px');
                }""")
                results.append({'case':'200 percent text enlargement','width':width,'route':route,
                                'overflow':page.evaluate('document.documentElement.scrollWidth>innerWidth')})
                if route=='/':
                    copy_box=page.locator('.home-hero-copy').bounding_box()
                    bottom=page.locator('.hero-bottom').bounding_box()
                    assert copy_box['y']+copy_box['height']<=bottom['y']+1, 'Enlarged hero text overlaps following content'
                    skip=page.locator('.skip-link').bounding_box()
                    assert skip['y']+skip['height']<=0, 'Hidden skip link leaks into viewport'
                    for link in page.locator('.hero-actions a').all():
                        box=link.bounding_box()
                        assert box['x']+box['width']<=width+1, 'Enlarged primary action is clipped'
        context.close()

        for variant in ('null researcher','null paper researcher','unsafe link','object tag','invalid JSON','markup'):
            context=browser.new_context(reduced_motion='reduce')
            context.route('**/*',lambda route:route.continue_() if route.request.url.startswith(BASE) else route.abort())
            payload=copy.deepcopy(PAYLOAD)
            if variant=='null researcher': payload['researchers']=[None]
            if variant=='null paper researcher': payload['papers'][0]['researchers']=[None]
            if variant=='unsafe link': payload['researchers'][0]['googleScholarUrl']='javascript:window.__payloadExecuted=true'
            if variant=='object tag': payload['papers'][0]['tags']=[{}]
            if variant=='markup': payload['papers'][0]['title']='<img src=x onerror="window.__payloadExecuted=true">'
            body='not-json' if variant=='invalid JSON' else json.dumps(payload)
            context.route('**/api/**',lambda route:route.fulfill(status=200,content_type='application/json',body=body))
            page=context.new_page();errors=[]
            page.on('pageerror',lambda error:errors.append(str(error)))
            page.add_init_script('window.__payloadExecuted=false')
            page.goto(BASE+'/achievements',wait_until='networkidle')
            if variant=='markup':
                expect(page.get_by_text(payload['papers'][0]['title'],exact=True)).to_be_visible()
                assert page.evaluate('window.__payloadExecuted') is False
                # Audit success state as well as the unavailable-API state.
                page.add_script_tag(path=str(AXE))
                data=page.evaluate("async()=>await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa','wcag22aa']}})")
                results.append({'case':'axe API success','violations':[
                    {'id':v['id'],'targets':[n['target'] for n in v['nodes']]} for v in data['violations']]})
            else:
                expect(page.get_by_text('已保留静态代表论文',exact=False)).to_be_visible()
            results.append({'case':variant,'errors':errors,'executed':page.evaluate('window.__payloadExecuted')})
            context.close()

        context=browser.new_context(reduced_motion='reduce')
        context.route('**/*',lambda route:route.continue_() if route.request.url.startswith(BASE) else route.abort())
        context.route('**/*.mp4',lambda route:route.abort())
        page=context.new_page();page.goto(BASE,wait_until='networkidle')
        expect(page.locator('[data-video-status]')).to_be_visible()
        expect(page.locator('[data-video-toggle]')).to_be_disabled()
        assert page.locator('[data-hero-video]').get_attribute('poster')
        results.append({'case':'video failure preserves poster and reports status','status':'PASS'})
        context.close()

        context=browser.new_context(reduced_motion='reduce')
        context.route('**/*',lambda route:route.continue_() if route.request.url.startswith(BASE) else route.abort())
        context.route('**/api/**',lambda route:None)
        page=context.new_page();page.goto(BASE+'/achievements',wait_until='domcontentloaded')
        expect(page.get_by_text('已保留静态代表论文',exact=False)).to_be_visible(timeout=12000)
        results.append({'case':'hung API aborts within bounded timeout and preserves fallback','status':'PASS'})
        context.close()

        context=browser.new_context(reduced_motion='reduce')
        phase={'ok':False}
        context.route('**/*',lambda route:route.continue_() if route.request.url.startswith(BASE) else route.abort())
        context.route('**/api/**',lambda route:route.fulfill(
            status=200 if phase['ok'] else 503,content_type='application/json',
            body=json.dumps(PAYLOAD) if phase['ok'] else '{}'))
        page=context.new_page();page.goto(BASE+'/achievements',wait_until='networkidle')
        expect(page.get_by_text('已保留静态代表论文',exact=False)).to_be_visible()
        phase['ok']=True
        page.get_by_role('button',name='重新加载').click()
        expect(page.get_by_text('合成边界测试',exact=True)).to_be_visible()
        results.append({'case':'API recovery retry replaces fallback with real response','status':'PASS'})
        context.close()

        context=browser.new_context(reduced_motion='reduce',java_script_enabled=False)
        page=context.new_page();page.goto(BASE,wait_until='networkidle')
        assert page.locator('h1').is_visible() and page.locator('a[href="/research"]').count()
        assert page.locator('#research-panel-0').is_visible()
        results.append({'case':'JavaScript disabled static content remains readable','status':'PASS'})
        context.close();browser.close()

    OUT.mkdir(exist_ok=True)
    (OUT/'adversarial-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
    failures=[r for r in results if r.get('violations') or r.get('overflow') or r.get('errors') or r.get('executed')]
    print(json.dumps(failures,ensure_ascii=False,indent=2) if failures else f'{len(results)} adversarial checks PASS')
    assert not failures, f'{len(failures)} adversarial cases need correction'


if __name__=='__main__':
    run()
