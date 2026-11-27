# -*- coding: utf-8 -*-
"""musathegiant.com/cards/bellvercards/ follows bellveraffiliates.com automatically (MTG, 27 Nov 2026:
"Make sure all income stream pages on musathegiant.com are up to date as well ... Bellver pages aren't up to date").

bellveraffiliates.com is MTG's main Bellver guide (every copy names it as canonical). This script copies its 16 guide pages
into musathegiant.com/cards/bellvercards/, so the two can never drift apart again:
  * links between the guide's pages stay on musathegiant.com (/prices/ -> /cards/bellvercards/prices/)
  * styles, scripts, fonts, images, PDFs and team pages load from bellveraffiliates.com (always its newest files)
  * MTG's own pages (legal pages, dashboard, about) become musathegiant.com addresses again
  * the tab icon stays musathegiant.com's crown; Up and Down come from /assets/updown.js on this site
Run by .github/workflows/sync-from-mtgtribe.yml every hour, or by hand:
  python3 .github/sync/bellver.py                      (reads the live bellveraffiliates.com)
  python3 .github/sync/bellver.py /home/user/bellveraffiliates   (reads a local checkout)
If a page cannot be read or does not look like the guide, nothing is written and the job fails."""
import os, re, sys, urllib.request

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SRC = sys.argv[1] if len(sys.argv) > 1 else 'https://bellveraffiliates.com'
BVA = 'https://bellveraffiliates.com'
BASE = '/cards/bellvercards/'
PAGES = ['', 'learn/', 'get-started/', 'how-it-works/', 'prices/', 'rewards/', 'matrix/', 'partner/', 'rewards-calculator/',
         'payback-calculator/', 'videos/', 'explainers/', 'tutorials/', 'faq/', 'docs/', 'downloads/']
LOCAL = ('/favicon.svg', '/assets/updown.js')      # files musathegiant.com has itself


def get(p):
    if SRC.startswith('http'):
        req = urllib.request.Request(SRC + '/' + p, headers={'User-Agent': 'musathegiant-sync'})
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.read().decode('utf-8')
    return open(os.path.join(SRC, p, 'index.html'), encoding='utf-8').read()


def page_of(path):
    """'/prices/#x' -> 'prices/#x' when it is one of the guide's pages, else None."""
    bare = re.split(r'[?#]', path)[0].lstrip('/')
    if bare and not bare.endswith('/'):
        bare += '/'
    return path.lstrip('/') if (bare if bare != '/' else '') in PAGES else None


def fix(u, attr):
    if u.startswith('https://www.musathegiant.com/') and attr == 'href':
        return u[len('https://www.musathegiant.com'):]
    if u.startswith(BVA + '/') and attr == 'href':
        pg = page_of(u[len(BVA):])
        return BASE + pg if pg is not None else u
    if u.startswith('/') and not u.startswith('//'):
        if u.split('?')[0] in LOCAL:
            return u
        pg = page_of(u)
        if pg is not None and attr != 'src':
            return BASE + pg
        return BVA + u
    return u


def convert(s, p):
    def attr(m):
        a, v = m.group(1), m.group(2)
        if a == 'srcset':
            v = ', '.join(' '.join([fix(x.split(' ')[0], a)] + x.split(' ')[1:]) for x in re.split(r',\s*', v.strip()))
        else:
            v = fix(v, 'href' if a.startswith('data-') or a in ('href', 'action') else a)
        return f' {a}="{v}"'
    s = re.sub(r' (href|src|srcset|poster|action|data-[\w-]+)="([^"]*)"', attr, s)
    s = re.sub(r'url\((["\']?)(/[^)"\']+)\1\)', lambda m: f'url({m.group(1)}{fix(m.group(2), "src")}{m.group(1)})', s)
    # Up and Down on musathegiant.com load from this site (bellver.js asks for /assets/updown.js, which exists here)
    return s


out, problems = {}, []
for p in PAGES:
    try:
        s = get(p)
    except Exception as e:
        problems.append(f'{p or "home"}: could not read ({e})')
        continue
    if 'bv-own' not in s or 'rel="canonical"' not in s or '</html>' not in s:
        problems.append(f'{p or "home"}: does not look like the Bellver guide')
        continue
    t = convert(s, p)
    left = re.findall(r' (?:href|src|srcset)="(/(?!cards/bellvercards/|favicon\.svg|assets/updown\.js|about|dashboard|cards/|[\w-]+\.html)[^"]*)"', t)
    if left:
        problems.append(f'{p or "home"}: addresses left unchanged: {left[:5]}')
    if '—' in t or '–' in t:
        problems.append(f'{p or "home"}: has a long dash (MTG rule)')
    out[p] = t
if problems:
    print('STOPPED, nothing written:\n  ' + '\n  '.join(problems))
    sys.exit(1)
changed = []
for p, t in out.items():
    full = os.path.join(ROOT, BASE.strip('/'), p, 'index.html')
    b = t.encode('utf-8')
    if not os.path.exists(full) or open(full, 'rb').read() != b:
        os.makedirs(os.path.dirname(full), exist_ok=True)
        open(full, 'wb').write(b)
        changed.append(BASE + p)
print('bellver: changed', ', '.join(changed) if changed else 'nothing (already in sync)')
