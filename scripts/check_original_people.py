"""Local acceptance for the original homepage and light portrait sections."""
import os
import json
import subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright
from check_group_site import BASE

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output/original-people"
OUT.mkdir(parents=True, exist_ok=True)


def run():
    for path in ("frontend/src/pages/index.astro", "frontend/src/components/Nav.astro"):
        original = subprocess.check_output(["git", "show", f"405f7a9:{path}"], cwd=ROOT)
        assert (ROOT / path).read_bytes() == original, f"Original composition changed: {path}"
    results = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path=os.environ["CHROMIUM_PATH"])
        for width in (1440, 390):
            ctx = browser.new_context(viewport={"width": width, "height": 950}, reduced_motion="reduce")
            ctx.route("**/*", lambda r: r.continue_() if r.request.url.startswith(BASE) else r.abort())
            page = ctx.new_page()
            for route, selector in (("/", ".home-advisor, .home-team"), ("/about", ".people-surface"), ("/team", ".people-surface")):
                page.goto(BASE + route, wait_until="networkidle")
                page.locator("img").evaluate_all("async imgs => {imgs.forEach(i => i.loading='eager');await Promise.all(imgs.map(i => i.decode()))}")
                assert page.evaluate("getComputedStyle(document.body).backgroundColor") == "rgb(16, 19, 16)"
                for surface in page.locator(selector).all():
                    assert surface.evaluate("(e) => getComputedStyle(e).backgroundColor") == "rgb(255, 255, 255)"
                    assert surface.locator("img").evaluate_all("(imgs) => imgs.every(i => i.naturalWidth > 0 && getComputedStyle(i).filter === 'none')")
                assert not page.evaluate("document.documentElement.scrollWidth > innerWidth")
                if route == "/":
                    page.screenshot(path=str(OUT / f"hero-{width}.png"))
                    page.locator(".home-advisor").screenshot(path=str(OUT / f"advisor-{width}.png"))
                    page.locator(".home-team").screenshot(path=str(OUT / f"team-{width}.png"))
                results.append({"route": route, "width": width, "status": "PASS"})
            ctx.close()
        ctx = browser.new_context(viewport={"width": 1440, "height": 950}, reduced_motion="no-preference")
        ctx.route("**/*", lambda r: r.continue_() if r.request.url.startswith(BASE) else r.abort())
        page = ctx.new_page()
        page.goto(BASE, wait_until="networkidle")
        page.wait_for_function("!document.querySelector('[data-hero-video]').paused")
        before = page.locator("video").evaluate("(v) => v.currentTime")
        page.wait_for_timeout(800)
        assert page.locator("video").evaluate("(v) => v.currentTime") > before
        results.append({"case": "original hero footage actually plays", "status": "PASS"})
        browser.close()
    (OUT / "results.json").write_text(json.dumps(results, ensure_ascii=False, indent=2))
    print(f"PASS: {len(results)} original visual / portrait checks; homepage and navigation match 405f7a9")


if __name__ == "__main__":
    run()
