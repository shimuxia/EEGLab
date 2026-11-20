"""Local acceptance for the original homepage and light portrait sections."""
import os
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
from check_group_site import BASE

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(os.getenv("QA_OUTPUT_DIR", ROOT / "output")) / "portrait-checks"
OUT.mkdir(parents=True, exist_ok=True)


def run():
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
                if route == "/":
                    copy = page.locator(".home-hero-copy").bounding_box()
                    film = page.locator(".science-film").bounding_box()
                    if width == 1440:
                        assert copy["x"] + copy["width"] <= film["x"] + 1
                    else:
                        assert copy["y"] + copy["height"] <= film["y"] + 1
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
    print(f"PASS: {len(results)} original visual / portrait checks; desktop split and mobile stacked composition verified")


if __name__ == "__main__":
    run()
