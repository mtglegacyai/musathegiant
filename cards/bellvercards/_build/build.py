# -*- coding: utf-8 -*-
"""Build every Bellver Cards page.
   python3 build.py             -> writes the live pages into cards/bellvercards/
   python3 build.py preview DIR -> writes a preview copy with relative links into DIR"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bv
OUT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
if len(sys.argv) > 2 and sys.argv[1] == 'preview':
    bv.MODE = 'preview'; OUT = os.path.abspath(sys.argv[2])
import p_home, p_info, p_more, p_watch

PAGES = [('', p_home.build), ('learn/', p_watch.learn), ('get-started/', p_more.start), ('how-it-works/', p_info.how),
         ('prices/', p_info.prices), ('rewards/', p_info.rewards), ('videos/', p_watch.videos), ('tutorials/', p_watch.tutorials),
         ('faq/', p_more.faq), ('docs/', p_watch.docs)]

# old addresses that now live elsewhere: small redirect pages so shared links keep working
MOVED = {'downloads/': 'docs/', 'videos/bellver-card-explained/': 'videos/#explained',
         'videos/dashboard-walkthrough/': 'tutorials/#walkthrough', 'videos/launch-webinar/': 'videos/#webinar'}


def write(path, html):
    if '—' in html or '–' in html:
        raise SystemExit(f'Dash found in {path or "home"}: MTG rule is no em or en dashes')
    d = os.path.join(OUT, path); os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html)


for path, fn in PAGES:
    html = fn(path) if path else fn('')
    write(path, html)
    print('built', '/cards/bellvercards/' + path, len(html) // 1024, 'KB')

if bv.MODE == 'prod':
    for old, new in MOVED.items():
        to = bv.BASE + new; canon = bv.SITE + bv.BASE + new.split('#')[0]
        write(old, f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Moved | Bellver Cards by MTG</title>
<meta name="robots" content="noindex,follow"><link rel="canonical" href="{canon}">
<meta http-equiv="refresh" content="0; url={to}"><script>location.replace("{to}")</script></head>
<body style="background:#020c06;color:#eef5f1;font-family:system-ui,sans-serif;padding:40px">This page has moved. <a style="color:#34cc88" href="{to}">Continue to the new page</a>.</body></html>
''')
        print('redirect', old, '->', new)
