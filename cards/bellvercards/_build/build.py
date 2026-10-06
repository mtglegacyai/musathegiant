# -*- coding: utf-8 -*-
"""Build every Bellver Cards page.
   python3 build.py            -> writes the live pages into cards/bellvercards/
   python3 build.py preview DIR -> writes a self-contained preview copy (relative links) into DIR"""
import os, sys, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bv
OUT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
if len(sys.argv) > 2 and sys.argv[1] == 'preview':
    bv.MODE = 'preview'; OUT = os.path.abspath(sys.argv[2])
import p_home, p_info, p_more

PAGES = [('', p_home.build), ('how-it-works/', p_info.how), ('prices/', p_info.prices), ('rewards/', p_info.rewards),
         ('get-started/', p_more.start), ('videos/', p_more.videos), ('videos/bellver-card-explained/', p_more.v_explained),
         ('videos/dashboard-walkthrough/', p_more.v_dashboard), ('videos/launch-webinar/', p_more.v_webinar),
         ('faq/', p_more.faq), ('downloads/', p_more.downloads)]

for path, fn in PAGES:
    html = fn(path) if path else fn('')
    if '—' in html or '–' in html:
        raise SystemExit(f'Dash found in {path or "home"}: MTG rule is no em or en dashes')
    d = os.path.join(OUT, path); os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html)
    print('built', '/cards/bellvercards/' + path, len(html) // 1024, 'KB')
