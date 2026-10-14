"""Build index.html (the GitHub Pages site) from src/safelight.html.

src/safelight.html is the page body as published to the Claude artifact, which adds its own
<!doctype>/<head> wrapper. This script adds the same wrapper so the page works as a plain website.
Run from the repo root:  python3 tools/build_page.py
"""
import pathlib

root = pathlib.Path(__file__).resolve().parent.parent
src = (root / 'src' / 'safelight.html').read_text()
cut = src.index('</style>') + len('</style>')          # title, fonts, JSZip and styles go in <head>
head, body = src[:cut], src[cut:]
page = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
        '<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}'
        'body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>\n'
        + head + '\n</head>\n<body>' + body + '\n</body>\n</html>\n')
(root / 'index.html').write_text(page)
print('wrote index.html', len(page), 'bytes')
