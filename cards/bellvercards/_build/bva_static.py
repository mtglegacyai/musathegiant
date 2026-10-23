# -*- coding: utf-8 -*-
"""bellveraffiliates.com: the files the pages need besides the HTML (styles, scripts, images, videos, PDFs, tab icon, social images).
build.py calls copy() after building MTG's pages with BV_TARGET=bva. Source of truth stays in musathegiant/cards/bellvercards."""
import os, shutil, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.abspath(os.path.join(HERE, '..'))                 # musathegiant/cards/bellvercards
SITE_ROOT = os.path.abspath(os.path.join(SRC, '..', '..'))      # musathegiant
TEAM_SRC = os.path.join(SITE_ROOT, 'bellvercards')              # team photos on musathegiant.com


def _sync(a, b):
    """Copy a folder, only files that changed (videos are large)."""
    for dp, dn, fn in os.walk(a):
        rel = os.path.relpath(dp, a); od = os.path.join(b, rel); os.makedirs(od, exist_ok=True)
        for f in fn:
            if f == 'index.html':
                continue      # pages are built, never copied
            s, d = os.path.join(dp, f), os.path.join(od, f)
            if not os.path.exists(d) or os.path.getsize(d) != os.path.getsize(s) or os.path.getmtime(d) < os.path.getmtime(s):
                shutil.copy2(s, d)


def copy(out):
    for folder in ('assets', 'images', 'videos', 'docs'):
        _sync(os.path.join(SRC, folder), os.path.join(out, folder))
    shutil.copy2(os.path.join(SITE_ROOT, 'favicon.svg'), os.path.join(out, 'favicon.svg'))
    shutil.copy2(os.path.join(SITE_ROOT, 'images', 'mtg-profile.jpg'), os.path.join(out, 'images', 'mtg-profile.jpg'))
    open(os.path.join(out, '.nojekyll'), 'w').close()
    # social preview images that show bellveraffiliates.com instead of musathegiant.com
    sys.path.insert(0, HERE); import og
    for args in og.PAGES:
        og.make(*args[:4], *(args[4:] or ['card']), url='bellveraffiliates.com', out=os.path.join(out, 'images', 'og'))
    _seo(out)
    print('static files copied to', out)


def _seo(out):
    """robots.txt, sitemap.xml (MTG's pages only: team pages are noindex) and a friendly 404 page."""
    import datetime, team, bv
    skip = {m['slug'] for m in team.members()}
    today = datetime.date.today().isoformat()
    urls = []
    for dp, dn, fn in os.walk(out):
        dn[:] = [d for d in dn if not d.startswith('.') and d not in skip and d not in ('assets', 'images', 'videos')]
        if 'index.html' in fn:
            rel = os.path.relpath(dp, out); rel = '' if rel == '.' else rel + '/'
            if 'noindex' not in open(os.path.join(dp, 'index.html'), encoding='utf-8').read(3000):
                urls.append(bv.SITE + '/' + rel)
    urls.sort(key=lambda u: (u.count('/'), u))
    xml = ''.join(f'  <url><loc>{u}</loc><lastmod>{today}</lastmod></url>\n' for u in urls)
    open(os.path.join(out, 'sitemap.xml'), 'w').write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{xml}</urlset>\n')
    open(os.path.join(out, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\n\nSitemap: {bv.SITE}/sitemap.xml\n')
    open(os.path.join(out, '404.html'), 'w', encoding='utf-8').write('''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Page not found | Bellver Cards</title><meta name="robots" content="noindex"><link rel="icon" type="image/svg+xml" href="/team-favicon.svg"></head>
<body style="margin:0;min-height:100vh;display:grid;place-items:center;background:#020c06;color:#eef5f1;font:16px/1.6 system-ui,sans-serif;text-align:center;padding:24px">
<div><p style="font-size:3rem;margin:0">404</p><h1 style="font-size:1.4rem;margin:8px 0 12px">This page does not exist</h1>
<p style="color:#8ea39a;margin:0 0 22px">The link may be old or mistyped.</p>
<a href="/" style="display:inline-block;padding:12px 22px;border-radius:12px;background:#34b070;color:#04180e;font-weight:800;text-decoration:none">Go to the Bellver Card guide</a></div></body></html>
''')
    print('sitemap', len(urls), 'pages')


def team_files(out, slug):
    """A team member's photo (made once by team_assets.py on musathegiant.com) and their social images."""
    src = os.path.join(TEAM_SRC, slug); dst = os.path.join(out, slug); os.makedirs(dst, exist_ok=True)
    for f in ('photo.webp', 'photo.jpg'):
        if os.path.exists(os.path.join(src, f)):
            shutil.copy2(os.path.join(src, f), os.path.join(dst, f))
    if os.path.isdir(os.path.join(src, 'og')):
        _sync(os.path.join(src, 'og'), os.path.join(dst, 'og'))
