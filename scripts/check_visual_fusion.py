"""Local presentation acceptance: footage, motion, keyboard and graceful fallbacks."""
from __future__ import annotations

import json
import os
from pathlib import Path
from playwright.sync_api import sync_playwright
from check_group_site import BASE

OUT = Path(__file__).resolve().parents[1] / "output/fusion"
OUT.mkdir(parents=True, exist_ok=True)


def run():
    results = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path=os.environ["CHROMIUM_PATH"])

        def context(**options):
            ctx = browser.new_context(**options)
            ctx.route("**/*", lambda r: r.continue_() if r.request.url.startswith(BASE) else r.abort())
            return ctx

        for width in (1440, 1024, 805, 800, 774, 605, 390, 320):
            ctx = context(viewport={"width": width, "height": 900}, reduced_motion="no-preference")
            page = ctx.new_page()
            errors = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.goto(BASE, wait_until="networkidle")
            page.wait_for_timeout(1100)
            video = page.locator("[data-hero-video]")
            frame = page.locator(".science-film").bounding_box()
            copy = page.locator(".home-hero-copy").bounding_box()
            caption = page.locator(".film-caption").bounding_box()
            assert video.is_visible() and frame["width"] >= 260
            assert abs(frame["width"] / frame["height"] - 16 / 9) < 0.03
            assert caption["y"] >= frame["y"] + frame["height"], "Caption covers footage"
            assert not page.evaluate("document.documentElement.scrollWidth > innerWidth")
            if width > 800:
                assert copy["x"] + copy["width"] <= frame["x"], "Hero columns overlap"
            else:
                assert copy["y"] + copy["height"] <= frame["y"], "Stacked footage overlaps copy"
            if width == 1440:
                assert frame["y"] + frame["height"] <= 900, "Desktop footage falls below fold"
                assert not video.evaluate("(v) => v.paused")
                before = video.evaluate("(v) => v.currentTime")
                page.wait_for_timeout(500)
                assert video.evaluate("(v) => v.currentTime") > before
            assert not errors, errors
            page.screenshot(path=str(OUT / f"hero-{width}.png"))
            results.append({"case": "responsive footage, full frame, separate caption, no overflow", "width": width, "status": "PASS"})
            ctx.close()

        ctx = context(viewport={"width": 1440, "height": 900}, reduced_motion="no-preference")
        page = ctx.new_page()
        page.goto(BASE, wait_until="networkidle")
        target = page.locator(".team-contact-sheet")
        assert target.get_attribute("data-motion-pending") is not None
        page.evaluate("document.documentElement.style.scrollBehavior='auto'")
        target.scroll_into_view_if_needed()
        page.wait_for_function("document.querySelector('.team-contact-sheet').classList.contains('is-visible')")
        page.wait_for_timeout(1100)
        assert target.locator("a").evaluate_all("(items) => items.every(e => +getComputedStyle(e).opacity === 1)")
        # Keyboard/programmatic focus reveals an offscreen destination immediately.
        page.goto(BASE, wait_until="networkidle")
        page.locator(".lab-copy a").first.focus()
        assert page.locator(".lab-copy").get_attribute("data-motion-pending") is None
        # A live OS preference change must reveal every pending section and pause footage.
        page.emulate_media(reduced_motion="reduce")
        page.wait_for_function("document.documentElement.dataset.motion === 'reduced' && !document.querySelector('[data-motion-pending]')")
        page.wait_for_function("document.querySelector('[data-hero-video]').paused")
        assert page.locator("[data-motion-pending]").count() == 0
        assert page.locator("[data-hero-video]").evaluate("(v) => v.paused")
        assert target.locator("a").evaluate_all("(items) => items.every(e => +getComputedStyle(e).opacity === 1)")
        results.append({"case": "stagger completion, focus visibility, live reduced motion", "status": "PASS"})
        # Capture final static layout only after every section is shown.
        page.goto(BASE, wait_until="networkidle")
        page.locator("img").evaluate_all("""async imgs => {
            imgs.forEach(img => img.loading = 'eager');
            await Promise.all(imgs.map(img => img.decode()));
        }""")
        assert page.locator("img").evaluate_all("(imgs) => imgs.every(img => img.naturalWidth > 0)")
        page.screenshot(path=str(OUT / "homepage-desktop-full.png"), full_page=True)
        for selector in (".advisor-editorial", ".home-team"):
            page.locator(selector).screenshot(path=str(OUT / (selector[1:] + ".png")))
        ctx.close()

        for mode in ("no-js", "no-observer"):
            ctx = context(viewport={"width": 390, "height": 844}, java_script_enabled=mode != "no-js")
            if mode == "no-observer":
                ctx.add_init_script("delete window.IntersectionObserver")
            page = ctx.new_page()
            page.goto(BASE, wait_until="networkidle")
            assert page.locator("h1").is_visible()
            assert page.locator("[data-motion-pending]").count() == 0
            assert page.locator("[data-reveal]").evaluate_all("(items) => items.every(e => +getComputedStyle(e).opacity === 1)")
            results.append({"case": mode + " content remains readable", "status": "PASS"})
            ctx.close()

        browser.close()
    (OUT / "results.json").write_text(json.dumps(results, ensure_ascii=False, indent=2))
    print(f"PASS: {len(results)} visual/motion cases; evidence: output/fusion")


if __name__ == "__main__":
    run()
