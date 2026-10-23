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
    import team                       # tab icon: the same green card as the team clones (MTG, 23 Oct 2026); the crown stays on musathegiant.com
    team._team_favicon(os.path.join(out, 'favicon.svg'))
    shutil.copy2(os.path.join(SITE_ROOT, 'images', 'mtg-profile.jpg'), os.path.join(out, 'images', 'mtg-profile.jpg'))
    open(os.path.join(out, '.nojekyll'), 'w').close()
    # IndexNow: the key file Bing checks, and the GitHub workflow that tells Bing what changed after each publish
    gh = os.path.join(HERE, 'bva_github'); key = open(os.path.join(gh, 'indexnow.py')).read().split("KEY = '")[1].split("'")[0]
    open(os.path.join(out, key + '.txt'), 'w').write(key)
    os.makedirs(os.path.join(out, '.github', 'workflows'), exist_ok=True)
    shutil.copy2(os.path.join(gh, 'indexnow.py'), os.path.join(out, '.github', 'indexnow.py'))
    shutil.copy2(os.path.join(gh, 'indexnow.yml'), os.path.join(out, '.github', 'workflows', 'indexnow.yml'))
    # social preview images that show bellveraffiliates.com instead of musathegiant.com
    sys.path.insert(0, HERE); import og
    for args in og.PAGES:
        og.make(*args[:4], *(args[4:] or ['card']), url='bellveraffiliates.com', out=os.path.join(out, 'images', 'og'))
    _seo(out)
    print('static files copied to', out)


AI_BOTS = ['GPTBot', 'OAI-SearchBot', 'ChatGPT-User', 'ClaudeBot', 'Claude-SearchBot', 'Claude-User', 'PerplexityBot', 'Perplexity-User',
           'Google-Extended', 'Gemini-Deep-Research', 'Applebot-Extended', 'meta-externalagent', 'Meta-WebIndexer', 'DuckAssistBot',
           'Amazonbot', 'MistralAI-User', 'Bytespider', 'CCBot', 'cohere-ai']


def _pages(out, skip):
    """(url, html) for MTG's indexable pages on bellveraffiliates.com (clones are noindex and left out)."""
    import bv
    res = []
    for dp, dn, fn in os.walk(out):
        dn[:] = sorted(d for d in dn if not d.startswith('.') and d not in skip and d not in ('assets', 'images'))
        if 'index.html' in fn:
            h = open(os.path.join(dp, 'index.html'), encoding='utf-8').read()
            if 'noindex' in h[:4000]:
                continue
            rel = os.path.relpath(dp, out); rel = '' if rel == '.' else rel + '/'
            res.append((bv.BVA_SITE + '/' + rel, h))
    res.sort(key=lambda x: (x[0].count('/'), x[0]))
    return res


def _videos(h):
    """VideoObjects from a page's structured data, for the video sitemap."""
    import json, re
    out = []
    for blk in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
        try:
            data = json.loads(blk)
        except ValueError:
            continue
        stack = [data]
        while stack:
            x = stack.pop()
            if isinstance(x, dict):
                if x.get('@type') == 'VideoObject' and x.get('contentUrl') and x.get('thumbnailUrl'):
                    out.append(x)
                stack.extend(x.values())
            elif isinstance(x, list):
                stack.extend(x)
    seen = set(); res = []
    for v in out:
        if v['contentUrl'] not in seen:
            seen.add(v['contentUrl']); res.append(v)
    return res


def _secs(iso):
    import re
    m = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', iso or '')
    return (int(m.group(1) or 0) * 3600 + int(m.group(2) or 0) * 60 + int(m.group(3) or 0)) if m else 0


def _x(t):
    return (t or '').replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


def _seo(out):
    """Search and AI discovery for bellveraffiliates.com: robots.txt, sitemap.xml (with videos), llms.txt and a friendly 404.
    MTG's pages are the only ones offered to search engines and AI tools. Team clones are noindex for search engines,
    and AI crawlers are asked to skip them, so a clone never competes with MTG's own pages (MTG, 23 Oct 2026)."""
    import datetime, re, team, bv
    slugs = sorted(m['slug'] for m in team.members('bva'))
    today = datetime.date.today().isoformat()
    pages = _pages(out, set(slugs))
    # ---- sitemap with video entries
    rows = []
    for u, h in pages:
        vids = ''
        for v in _videos(h):
            secs = _secs(v.get('duration'))
            thumb = v['thumbnailUrl'] if isinstance(v['thumbnailUrl'], str) else v['thumbnailUrl'][0]
            vids += (f'\n    <video:video><video:thumbnail_loc>{_x(thumb)}</video:thumbnail_loc><video:title>{_x(v.get("name"))}</video:title>'
                     f'<video:description>{_x((v.get("description") or v.get("name"))[:2000])}</video:description>'
                     f'<video:content_loc>{_x(v["contentUrl"])}</video:content_loc>' + (f'<video:duration>{secs}</video:duration>' if secs else '') +
                     (f'<video:publication_date>{v["uploadDate"]}</video:publication_date>' if v.get('uploadDate') else '') + '</video:video>')
        rows.append(f'  <url><loc>{u}</loc><lastmod>{today}</lastmod>{vids}\n  </url>\n')
    open(os.path.join(out, 'sitemap.xml'), 'w', encoding='utf-8').write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
        'xmlns:video="http://www.google.com/schemas/sitemap-video/1.1">\n' + ''.join(rows) + '</urlset>\n')
    # ---- robots.txt: everyone welcome on MTG's pages; AI crawlers skip the clones (search engines read their noindex instead)
    clone_rules = ''.join(f'Disallow: /{s}/\n' for s in slugs)
    robots = ('# bellveraffiliates.com: the Bellver Card guide by MTG\n'
              '# Search engines and AI assistants are welcome on every page of the guide.\n'
              '# Team copies (/name/) are personal pages for MTG\'s partners: they are noindex for search engines, and AI crawlers skip them.\n\n'
              'User-agent: *\nAllow: /\n\n')
    robots += ''.join(f'User-agent: {b}\n' for b in AI_BOTS) + 'Allow: /\n' + clone_rules + '\n'
    robots += f'Sitemap: {bv.BVA_SITE}/sitemap.xml\n'
    open(os.path.join(out, 'robots.txt'), 'w').write(robots)
    # ---- llms.txt: a plain map of the guide for AI assistants (llmstxt.org format)
    def meta(h, name):
        m = re.search(r'<meta name="%s" content="([^"]*)"' % name, h); return m.group(1) if m else ''
    def title(h):
        m = re.search(r'<title>(.*?)</title>', h, re.S); return m.group(1).split(' | ')[0].strip() if m else ''
    lines = ['# Bellver Affiliates by MTG', '',
             '> An independent, plain-words guide to the Bellver Card, a crypto-funded payment card (fund it with USDT or USDC, spend in any currency), '
             'written by MTG (Musa The Giant), a Bellver affiliate. It covers how the card works, every price and fee, '
             'the rewards program (one-time referral commissions and the 2x2 matrix monthly rewards with the $100 a month rule), '
             'step-by-step video tutorials and short explainer videos. It is not the official Bellver website.', '',
             'Key facts (from Bellver\'s official price list and compensation plan, version 08/2026, and Bellver\'s October 2026 update):', '',
             '- Four card levels, one-time price: Basic $99, Premium $270, Business $490, Gold $990. No monthly or annual fee listed.',
             '- Fees: 3.9% card top-up fee (added on top of the amount loaded), 1.75% per transaction, 2% ATM withdrawal.',
             '- Physical card: Visa (ATM cash, shipping $85 Europe, $149 rest of world). Virtual card: Mastercard, usable the same day.',
             '- Funds sit in the cardholder\'s own non-custodial Fireblocks wallet, protected by their private key.',
             '- Referral commissions (one-time): $10 Basic, $100 Premium, $200 Business, $400 Gold; Special Edition $150, $300, $500.',
             '- Monthly rewards: 0.1% of completed top-ups in the cardholder\'s 2x2 matrix, for those holding Premium or higher with two direct Premium+ referrals, '
             'who load at least $100 onto their own card that month. Missing it three months in a row loses the matrix position. Rewards are never guaranteed.',
             '', f'Order link used on this site (MTG\'s referral link): {bv.REF}', '', '## Guide pages', '']
    for u, h in pages:
        t, d = title(h), meta(h, 'description')
        if t:
            lines.append(f'- [{t}]({u}): {d}')
    names = {'bellver-card-price-list.pdf': 'Bellver Card price list (official, version 08/2026)',
             'bellver-card-compensation-plan.pdf': 'Bellver Card compensation plan (official, version 08/2026)',
             'bellver-card-presentation.pdf': 'Bellver Card presentation slides (official)',
             'bellver-2x2-matrix-explained-by-mtg.pdf': 'The Bellver 2x2 matrix explained (by MTG)',
             'bellver-starter-checklist.pdf': 'Bellver Starter Checklist (by MTG)'}
    lines += ['', '## PDF documents', '']
    for f in sorted(os.listdir(os.path.join(out, 'docs'))):
        if f.endswith('.pdf'):
            lines.append(f'- [{names.get(f, f[:-4].replace("-", " "))}]({bv.BVA_SITE}/docs/{f})')
    lines += ['', '## Optional', '', f'- [About MTG]({bv.MTG_SITE}/about.html): who writes this guide',
              f'- [Earnings disclaimer]({bv.MTG_SITE}/earnings-disclaimer.html)', '']
    open(os.path.join(out, 'llms.txt'), 'w', encoding='utf-8').write('\n'.join(lines))
    # ---- friendly 404
    open(os.path.join(out, '404.html'), 'w', encoding='utf-8').write('''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Page not found | Bellver Cards</title><meta name="robots" content="noindex"><link rel="icon" type="image/svg+xml" href="/team-favicon.svg"></head>
<body style="margin:0;min-height:100vh;display:grid;place-items:center;background:#020c06;color:#eef5f1;font:16px/1.6 system-ui,sans-serif;text-align:center;padding:24px">
<div><p style="font-size:3rem;margin:0">404</p><h1 style="font-size:1.4rem;margin:8px 0 12px">This page does not exist</h1>
<p style="color:#8ea39a;margin:0 0 22px">The link may be old or mistyped.</p>
<a href="/" style="display:inline-block;padding:12px 22px;border-radius:12px;background:#34b070;color:#04180e;font-weight:800;text-decoration:none">Go to the Bellver Card guide</a></div></body></html>
''')
    print('sitemap', len(pages), 'pages,', sum(len(_videos(h)) for _, h in pages), 'video entries; robots.txt; llms.txt')


def team_files(out, slug):
    """A team member's photo (made once by team_assets.py on musathegiant.com) and their social images."""
    src = os.path.join(HERE, 'team_media', slug)                 # made by team_assets.py
    if not os.path.isdir(src):
        src = os.path.join(TEAM_SRC, slug)                         # older members: their files on musathegiant.com
    dst = os.path.join(out, slug); os.makedirs(dst, exist_ok=True)
    for f in ('photo.webp', 'photo.jpg'):
        if os.path.exists(os.path.join(src, f)):
            shutil.copy2(os.path.join(src, f), os.path.join(dst, f))
    if os.path.isdir(os.path.join(src, 'og')):
        _sync(os.path.join(src, 'og'), os.path.join(dst, 'og'))
