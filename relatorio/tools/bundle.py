#!/usr/bin/env python3
"""Bundle do site em HTML único (abre sobre file://). Inline css + js na ordem do index."""
import re, sys, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
html = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()

def css_repl(m):
    css = open(os.path.join(ROOT, m.group(1)), encoding="utf-8").read()
    # fontes: converter url(../fonts/x.woff2) em base64
    def font_repl(fm):
        path = os.path.join(ROOT, fm.group(1))
        import base64
        b64 = base64.b64encode(open(path, "rb").read()).decode()
        return f'url(data:font/woff2;base64,{b64})'
    css = re.sub(r'url\("\.\./(fonts/[^"]+)"\)', font_repl, css)
    css = re.sub(r"url\('\.\./(fonts/[^']+)'\)", font_repl, css)
    return "<style>\n" + css + "\n</style>"
html = re.sub(r'<link rel="stylesheet" href="(css/[^"]+)">', css_repl, html)

def repl(m):
    code = open(os.path.join(ROOT, m.group(1)), encoding="utf-8").read()
    return "<script>\n" + code + "\n</script>"
html = re.sub(r'<script src="([^"]+)"></script>', repl, html)

out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "dist-single.html")
open(out, "w", encoding="utf-8").write(html)
print(out, len(html), "bytes")
