#!/usr/bin/env python3
"""QA · varredura playwright: dual-width, slow-scroll, console/pageerrors, overflow, screenshots."""
import sys, json
from playwright.sync_api import sync_playwright

URL = sys.argv[1] if len(sys.argv) > 1 else "file:///mnt/agents/output/gramatica-iconocracia/index.html"
OUT = sys.argv[2] if len(sys.argv) > 2 else "/tmp/qa"

report = {}
with sync_playwright() as p:
    for width in (1680, 1280):
        browser = p.chromium.launch(executable_path="/usr/bin/chromium", args=["--no-sandbox"])
        pg = browser.new_page(viewport={"width": width, "height": 900})
        errors, console_errs = [], []
        pg.on("pageerror", lambda e: errors.append(str(e)))
        pg.on("console", lambda m: console_errs.append(m.text) if m.type == "error" else None)
        pg.goto(URL, wait_until="networkidle")
        pg.wait_for_timeout(1200)
        # slow-scroll para disparar IOs
        h = pg.evaluate("document.body.scrollHeight")
        ypos = 0
        while ypos < h:
            pg.evaluate(f"scrollTo(0,{ypos})")
            pg.wait_for_timeout(140)
            ypos += 700
        pg.evaluate("scrollTo(0,0)")
        pg.wait_for_timeout(900)
        overflow = pg.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
        fonts = pg.evaluate("document.fonts.check('16px \"Crimson Pro\"') && document.fonts.check('16px \"Instrument Serif\"') && document.fonts.check('700 12px \"JetBrains Mono\"')")
        pg.screenshot(path=f"{OUT}/cover_{width}.png")
        for sec in ["sec-exec", "sec-timeline", "sec-matrix", "sec-flow", "sec-verdict", "sec-sources"]:
            el = pg.locator(f"#{sec}")
            el.scroll_into_view_if_needed()
            pg.wait_for_timeout(1300)
            el.screenshot(path=f"{OUT}/{sec}_{width}.png")
        report[width] = {"errors": errors, "console": console_errs, "overflow_px": overflow, "fonts": fonts, "scroll_h": h}
        browser.close()

print(json.dumps(report, indent=1, ensure_ascii=False))
