# -*- coding: utf-8 -*-
"""Build every Bellver Cards page.
   python3 build.py               -> writes MTG's live pages into cards/bellvercards/, then every team page (team.json) into bellvercards/<slug>/
   python3 build.py preview DIR   -> writes a preview copy of MTG's pages with relative links into DIR
   python3 build.py --member SLUG -> builds one team member's pages only
   BV_TARGET=bva python3 build.py -> the same for bellveraffiliates.com (MTG at the root, clones at /<slug>/)
   To publish, use publish.py: it builds BOTH sites and pushes both repositories in one go."""
import os, sys, json, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bv
OUT = os.path.abspath(os.path.join(HERE, '..'))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
MEMBER = None
if bv.TARGET == 'bva':     # bellveraffiliates.com: its own repository (BV_OUT), MTG's guide at the root, team pages at /<slug>/
    OUT = ROOT = os.path.abspath(os.environ.get('BV_OUT', '/home/claude/bellveraffiliates'))
if len(sys.argv) > 2 and sys.argv[1] == 'preview':
    bv.MODE = 'preview'; OUT = os.path.abspath(sys.argv[2])
elif len(sys.argv) > 2 and sys.argv[1] == '--member':
    import team, team_shell
    MEMBER = team.member(sys.argv[2])
    team_shell.configure(MEMBER)
    OUT = os.path.join(ROOT, bv.BASE.strip('/'))
import p_home, p_info, p_more, p_watch, p_partner, p_matrix, p_tools

PAGES = [('', p_home.build), ('learn/', p_watch.learn), ('get-started/', p_more.start), ('how-it-works/', p_info.how),
         ('prices/', p_info.prices), ('rewards/', p_info.rewards), ('matrix/', p_matrix.matrix), ('partner/', p_partner.partner), ('rewards-calculator/', p_tools.rewards_page), ('payback-calculator/', p_tools.payback_page), ('videos/', p_watch.videos), ('explainers/', p_watch.explainers), ('tutorials/', p_watch.tutorials),
         ('faq/', p_more.faq), ('docs/', p_watch.docs)]

# old addresses that now live elsewhere: small redirect pages so shared links keep working
MOVED = {'downloads/': 'docs/', 'videos/bellver-card-explained/': 'videos/#explained',
         'videos/dashboard-walkthrough/': 'tutorials/#walkthrough', 'videos/launch-webinar/': 'videos/#webinar'}


def write(path, html):
    if MEMBER:
        html = team.finalize(html, MEMBER, path)
    if '—' in html or '–' in html:
        raise SystemExit(f'Dash found in {path or "home"}: MTG rule is no em or en dashes')
    d = os.path.join(OUT, path); os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html)


for path, fn in PAGES:
    html = fn(path) if path else fn('')
    write(path, html)
    print('built', bv.BASE + path, len(html) // 1024, 'KB')

if MEMBER:
    team.check_all_used()
    if bv.TARGET == 'bva':
        import bva_static
        bva_static.team_files(ROOT, MEMBER['slug'])
    sys.exit(0)

if bv.MODE == 'prod' and bv.TARGET == 'bva':
    import bva_static
    bva_static.copy(OUT)

if bv.MODE == 'prod' and bv.TARGET != 'bva':
    for old, new in MOVED.items():
        to = bv.BASE + new; canon = bv.SITE + bv.BASE + new.split('#')[0]
        write(old, f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Moved | Bellver Cards by MTG</title>
<meta name="robots" content="noindex,follow"><link rel="canonical" href="{canon}">
<meta http-equiv="refresh" content="0; url={to}"><script>location.replace("{to}")</script></head>
<body style="background:#020c06;color:#eef5f1;font-family:system-ui,sans-serif;padding:40px">This page has moved. <a style="color:#34cc88" href="{to}">Continue to the new page</a>.</body></html>
''')
        print('redirect', old, '->', new)

# ---- team pages: one copy of the guide per business partner (team.json), rebuilt every time MTG's pages are
if bv.MODE == 'prod':
    import team
    for m in team.members():
        subprocess.run([sys.executable, os.path.abspath(__file__), '--member', m['slug']], check=True)
    team.write_index(ROOT)
