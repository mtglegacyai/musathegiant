#!/usr/bin/env python3
"""musathegiant.com stays at the same level as mtgtribe.com, automatically (MTG, 27 Nov 2026: "any new updates that I am
pushing onto mtgtribe.com, make sure that musathegiant.com syncs automatically while being its own website").

What it does, every run (GitHub Actions, every hour: .github/workflows/sync-from-mtgtribe.yml; or by hand):
  1. reads mtgtribe.com: the home page, the shared design files and the list of MTG's income streams
     (https://mtgtribe.com/assets/tribe/streams.json, the single source of truth, in MTG's order);
  2. builds musathegiant.com's home page from the mtgtribe.com home page: the same look, motion and sections, with
     musathegiant.com's own name, address, search details (title, description, canonical, structured data), its own
     Income Streams and Free Tools sections and its own footer;
  3. copies the shared design files the page needs (same look on both sites);
  4. refreshes every list of MTG's streams on musathegiant.com: the Income Streams column in every page footer and
     the streams line in llms.txt; and checks that the dashboard (dashboard.html) shows the streams in the same order.
It stops without writing anything when mtgtribe.com's page has changed so much that a step cannot be done safely, and
says which step (the Action then fails and GitHub emails MTG), so a broken page is never published.

Run by hand:  python3 .github/sync/sync.py            (reads the live mtgtribe.com)
              python3 .github/sync/sync.py ../mtgtribe (reads a local copy of the mtgtribe repo)
Never edit index.html by hand: change mtgtribe.com, or this script.
Lives in .github/ so GitHub Pages never publishes it.
"""
import html as H
import json
import os
import re
import sys
import urllib.request

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SRC = sys.argv[1] if len(sys.argv) > 1 else 'https://mtgtribe.com'
TRIBE = 'https://mtgtribe.com'
SITE = 'https://www.musathegiant.com'
MARK_A, MARK_B = '<!-- mtg-streams:start (written by .github/sync/sync.py) -->', '<!-- mtg-streams:end -->'
problems = []


def get(path):
    if SRC.startswith('http'):
        req = urllib.request.Request(SRC + path, headers={'User-Agent': 'musathegiant-sync/1.0'})
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.read()
    p = os.path.join(SRC, path.lstrip('/').split('?')[0])
    if p.endswith('/'):
        p += 'index.html'
    with open(p, 'rb') as f:
        return f.read()


def stop(msg):
    sys.exit('sync stopped, nothing written: ' + msg)


def need(s, old, new, what, count=1):
    """replace exactly; stop if mtgtribe.com's page no longer has it"""
    n = s.count(old)
    if n < count:
        stop(f'{what}: not found on the mtgtribe.com home page any more')
    return s.replace(old, new)


def sub(s, pat, rep, what, flags=re.S):
    s2, n = re.subn(pat, rep, s, flags=flags)
    if not n:
        stop(f'{what}: not found on the mtgtribe.com home page any more')
    return s2


def soft(s, old, new, what):
    """a nice-to-have tweak: skip it (and say so) if the words changed on mtgtribe.com"""
    if old not in s:
        problems.append('skipped: ' + what)
        return s
    return s.replace(old, new)


def esc(t):
    return H.escape(t, quote=True)


# ------------------------------------------------------------------ 1. read mtgtribe.com
data = json.loads(get('/assets/tribe/streams.json'))
streams = data['streams']
if not 3 <= len(streams) <= 12 or any(not s.get('name') or not s.get('url') for s in streams):
    stop('streams.json looks wrong')
page = get('/').decode('utf-8')
if '<section class="hero"' not in page or '</footer>' not in page:
    stop('the mtgtribe.com home page does not look like itself')


def surl(s):
    return s.get('mtg_url') or s['url']


def ext(u):
    return u.startswith('http')


def rel(s):
    return 'sponsored noopener' if s.get('sponsored') else 'noopener'


def link(s, cls='', label=None):
    u = surl(s)
    a = f'<a{" class=" + chr(34) + cls + chr(34) if cls else ""} href="{esc(u)}"'
    if ext(u):
        a += f' target="_blank" rel="{rel(s)}"'
    return a + f'>{esc(label or s["name"])}' + ('<span class="sr-only"> (opens in a new tab)</span>' if ext(u) else '') + '</a>'


# ------------------------------------------------------------------ 2. the home page
s = page

# 2a. search details: musathegiant.com's own
TITLE = 'MTG | Your Digital Architect: Multiple Streams of Income, Crypto &amp; AI | MusaTheGiant.com'
DESC = ('MTG, Your Digital Architect: ' + str(len(streams)) + ' income streams explained step by step, free crypto tools and calculators, and the MTG TRIBE. Learn first, then decide.')
OGT = 'MTG | Multiple Streams of Income, Explained Step by Step'
OGD = 'Your Digital Architect: ' + ', '.join(x['name'] for x in streams[:4]) + ' and more, plus free crypto tools. Learn first, then decide.'
s = sub(s, r'<title>.*?</title>', f'<title>{TITLE}</title>', 'title')
s = sub(s, r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{esc(DESC)}">', 'description')
s = sub(s, r'<meta name="author" content="[^"]*">', '<meta name="author" content="MTG (Musa The Giant)">', 'author')
s = sub(s, r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{SITE}/">', 'canonical')
s = sub(s, r'<meta property="og:site_name" content="[^"]*">', '<meta property="og:site_name" content="MusaTheGiant.com">', 'og:site_name')
s = sub(s, r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{esc(OGT)}">', 'og:title')
s = sub(s, r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{esc(OGD)}">', 'og:description')
s = sub(s, r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{SITE}/">', 'og:url')
OGI = SITE + '/images/og-mtg.jpg'
s = re.sub(r'<meta property="og:image(:secure_url)?" content="[^"]*">', lambda m: f'<meta property="og:image{m.group(1) or ""}" content="{OGI}">', s)
s = re.sub(r'<meta property="og:image:alt" content="[^"]*">', '<meta property="og:image:alt" content="MTG, Your Digital Architect: multiple streams of income, MusaTheGiant.com">', s)
s = re.sub(r'<meta name="twitter:title" content="[^"]*">', f'<meta name="twitter:title" content="{esc(OGT)}">', s)
s = re.sub(r'<meta name="twitter:description" content="[^"]*">', f'<meta name="twitter:description" content="{esc(OGD)}">', s)
s = re.sub(r'<meta name="twitter:image" content="[^"]*">', f'<meta name="twitter:image" content="{OGI}">', s)
s = re.sub(r'<meta name="twitter:image:alt" content="[^"]*">', '<meta name="twitter:image:alt" content="MTG, Your Digital Architect: multiple streams of income">', s)
s = re.sub(r'<link rel="icon"[^>]*>', '<link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="icon" type="image/png" href="/images/favicon.png">', s, count=1)
s = s.replace("location.hostname==='mtgtribe.com'", "location.hostname==='www.musathegiant.com'")

ld = {
    '@context': 'https://schema.org',
    '@graph': [
        {'@type': 'WebSite', '@id': SITE + '/#website', 'url': SITE + '/', 'name': 'MusaTheGiant.com',
         'alternateName': ['MTG', 'Musa The Giant', 'MTG | Your Digital Architect'], 'description': DESC, 'inLanguage': 'en-ZA',
         'publisher': {'@id': SITE + '/#mtg'}},
        {'@type': 'Person', '@id': SITE + '/#mtg', 'name': 'MTG', 'alternateName': ['MusaTheGiant', 'Musa The Giant'],
         'jobTitle': 'Your Digital Architect', 'url': SITE + '/', 'image': TRIBE + '/assets/tribe/mtg-photo-720.jpg?v=2',
         'description': 'MTG, Your Digital Architect: plain-English crypto education, step-by-step tutorials and free tools, and host of the MTG TRIBE.',
         'sameAs': [TRIBE + '/', 'https://www.tiktok.com/@joinmtgtribe', 'https://www.youtube.com/@mtgtribe', 'https://t.me/mtgtribe', 'https://www.facebook.com/mtgtribe'],
         'knowsAbout': ['Multiple streams of income', 'Bitcoin', 'Crypto portfolios', 'Crypto debit cards', 'AI tutorials', 'Affiliate marketing', 'Crypto safety']},
        {'@type': 'WebPage', '@id': SITE + '/#webpage', 'url': SITE + '/', 'name': TITLE.replace('&amp;', '&'), 'description': DESC,
         'inLanguage': 'en-ZA', 'isPartOf': {'@id': SITE + '/#website'}, 'about': {'@id': SITE + '/#mtg'}, 'author': {'@id': SITE + '/#mtg'},
         'dateModified': data.get('updated', ''), 'mainEntity': {'@id': SITE + '/#streams'},
         'primaryImageOfPage': {'@type': 'ImageObject', 'url': OGI, 'width': 1200, 'height': 630}},
        {'@type': 'ItemList', '@id': SITE + '/#streams', 'name': "MTG's income streams, in his order", 'numberOfItems': len(streams),
         'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': x['name'], 'description': x['tag'],
                              'url': (SITE + surl(x)) if not ext(surl(x)) else surl(x)} for i, x in enumerate(streams)]},
        {'@type': 'VideoObject', '@id': SITE + '/#invite', 'name': 'Join the MTG TRIBE: an invite from MTG',
         'description': 'MTG, Your Digital Architect, invites you into the MTG TRIBE, a WhatsApp community of action takers, and shows how to join at mtgtribe.com/group.',
         'thumbnailUrl': TRIBE + '/assets/mtg-tribe-invite-cover.webp', 'contentUrl': TRIBE + '/assets/mtg-tribe-invite.mp4',
         'uploadDate': '2026-10-26', 'duration': 'PT2M48S', 'inLanguage': 'en'},
    ]}
s = sub(s, r'<script type="application/ld\+json">.*?</script>',
        lambda m: '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/') + '</script>', 'structured data')

# 2b. addresses: pictures and videos play from mtgtribe.com; the scripts and styles are copied here (step 3)
LOCAL = ('/assets/tribe/tribe.css', '/assets/tribe/tribe-scene.js', '/assets/tribe/cntn-live.js', '/assets/tribe/to-top.js',
         '/assets/tribe/bottom-nav.js', '/assets/video-return.js', '/assets/wa-message.js', '/assets/zoom-cta.js', '/assets/updown.js')
MAP = {'/': '/', '/dashboard/': '/dashboard.html', '/dashboard/#streams': '/#streams', '/group/': TRIBE + '/group/'}


def addr(u):
    if not u.startswith('/') or u.startswith('//'):
        return u
    bare = u.split('?')[0]
    if u in MAP:
        return MAP[u]
    if bare in LOCAL:
        return u
    return TRIBE + u


def attr(m):
    name, q, val = m.group(1), m.group(2), m.group(3)
    if name == 'srcset':
        val = ', '.join(' '.join([addr(p.split(' ')[0])] + p.split(' ')[1:]) for p in (x.strip() for x in val.split(',')))
    else:
        val = addr(val)
    return f'{name}={q}{val}{q}'


s = re.sub(r'\b(href|src|srcset|poster|data-wide|data-tall|data-src|data-poster)=(["\'])(/[^"\']*)\2', attr, s)
s = re.sub(r'url\((["\']?)(/[^)"\'/][^)"\']*)\1\)', lambda m: 'url(' + m.group(1) + addr(m.group(2)) + m.group(1) + ')', s)

# 2c. the brand: MTG, Your Digital Architect (musathegiant.com is MTG's own site; the tribe lives on mtgtribe.com)
s = sub(s, r'(<a class="brand" href="/") aria-label="[^"]*">(<img[^>]*>)MTG TRIBE', r'\1 aria-label="MTG, Your Digital Architect: home">\2MTG', 'brand')
s = soft(s, '<span class="word gold-text">MTG TRIBE</span>', '<span class="word gold-text">MTG</span>', 'intro word')
s = soft(s, '<i class="dot" aria-hidden="true"></i>A tribe of action takers</p>',
         '<i class="dot" aria-hidden="true"></i>MTG 👑 Your Digital Architect</p>', 'hero pill')
# MTG, 28 Nov 2026: no "AI tutorials" (he makes the step-by-step tutorials himself); mtgtribe.com's hero says
# "Step-by-step videos that show you every tap", and musathegiant.com's own line says it the same way
s = soft(s, 'Multiple streams of income. A diversified crypto portfolio. Step-by-step videos that show you every tap. One tribe, building generational wealth together.',
         f'{len(streams)} income streams, explained in plain English. A diversified crypto portfolio. Free tools, and step-by-step videos that show you every tap. Learn first, then decide.', 'hero words')
s = soft(s, '>Enter the dashboard<', '>See my income streams<', 'dashboard button words')
s = s.replace('<a href="#code">The code</a><a href="#engine">The engine</a>', '<a href="#streams">Income streams</a><a href="#tools">Free tools</a>')
s = re.sub(r'<a href="#code"><span>02 The code</span><i></i></a>', '<a href="#streams"><span>02 Income streams</span><i></i></a>', s)
s = re.sub(r'(<a href="#engine"><span>03 The engine</span><i></i></a>)', r'\1<a href="#tools"><span>04 Free tools</span><i></i></a>', s)
s = s.replace('<span>04 Meet MTG</span>', '<span>05 Meet MTG</span>').replace('<span>05 Lead</span>', '<span>06 Lead</span>')

# 2d. musathegiant.com's own sections: the income streams in MTG's order, then the free tools
cards = []
for i, x in enumerate(streams):
    u = surl(x)
    tgt = f' target="_blank" rel="{rel(x)}"' if ext(u) else ''
    facts = ''.join(f'<li>{esc(f)}</li>' for f in x.get('facts', []))
    cards.append(
        f'<article class="ms-card glass rv{" ms-top" if i == 0 else ""}" style="--d:{i % 3}" id="s-{esc(x["id"])}">'
        f'<div class="ms-row"><span class="ms-n">#{i + 1}</span><span class="ms-badge">{esc(x.get("badge", ""))}</span></div>'
        f'<h3><span class="ms-name">{esc(x["name"])}</span>{esc(x["tag"])}</h3>'
        f'<p>{esc(x.get("blurb", ""))}</p><ul class="ms-facts">{facts}</ul>'
        f'<a class="btn {"btn-gold" if i == 0 else "btn-glass"} ring ms-go" href="{esc(u)}"{tgt}>{esc(x.get("cta", "Open the guide"))}'
        f'<svg class="ic" aria-hidden="true"><use href="#i-arrow"/></svg>{"<span class=sr-only> (opens in a new tab)</span>" if ext(u) else ""}</a></article>')
STREAMS = f'''{MARK_A}
<!-- MTG'S INCOME STREAMS, in his order (from mtgtribe.com/assets/tribe/streams.json) -->
<section class="sec ms-streams" id="streams" aria-labelledby="ms-s-h">
 <span class="seam" aria-hidden="true"></span>
 <div class="wrap">
  <div class="sec-head">
   <p class="eyebrow rv">My income streams, ranked</p>
   <h2 class="display rv" style="--d:1" id="ms-s-h"><span class="silver-text">{len(streams)} streams.</span> <span class="gold-text">One plan.</span></h2>
   <p class="lede rv" style="--d:2">Ranked by how much I use them right now. Read each guide first, then decide if it fits your budget and goals. A stream that stops performing makes way for the next best one.</p>
  </div>
  <div class="ms-grid">{"".join(cards)}</div>
  <div class="more rv"><a class="btn btn-gold ring" href="/dashboard.html"><span class="chip"><svg class="ic" aria-hidden="true"><use href="#i-dash"/></svg></span>Open the income streams dashboard<svg class="ic" aria-hidden="true"><use href="#i-arrow"/></svg></a></div>
 </div>
</section>
{MARK_B}
'''
TOOLS = [('/halving/', 'Crypto Halving Countdown', 'Bitcoin, Litecoin, Bittensor and more, live to the second.', 'i-trend'),
         ('/converter/', 'Dollar to Rand and Bitcoin Converter', 'Live USD/ZAR and BTC/ZAR rates, both ways.', 'i-coins'),
         ('/dca/', 'Bitcoin DCA Calculator', 'See what regular buying could have made, in rand or dollars.', 'i-calc'),
         ('/101/', 'Free Crypto 101 Crash Course', 'Learn the basics step by step and earn your certificate.', 'i-cap'),
         ('/cards/', 'Crypto Debit Cards Dashboard', 'Crypto cards side by side: fees, limits and coins.', 'i-card'),
         ('/tools/', 'Every tool in one place', 'All my free calculators and web tools, each on its own page.', 'i-globe')]
TOOLS_HTML = '''
<!-- FREE TOOLS: musathegiant.com's own calculators and courses -->
<section class="sec ms-tools" id="tools" aria-labelledby="ms-t-h">
 <span class="seam" aria-hidden="true"></span>
 <div class="wrap">
  <div class="sec-head">
   <p class="eyebrow rv">Free, on any phone</p>
   <h2 class="display rv" style="--d:1" id="ms-t-h"><span class="silver-text">Free tools.</span> <span class="gold-text">Real numbers.</span></h2>
   <p class="lede rv" style="--d:2">Calculators, countdowns and a free course that do the maths for you, so every decision starts with the facts.</p>
  </div>
  <div class="ms-tgrid">''' + ''.join(
    f'<a class="ms-tool glass rv" style="--d:{i % 3}" href="{u}"><span class="ms-ti"><svg class="ic" aria-hidden="true"><use href="#{ic}"/></svg></span>'
    f'<span><b>{esc(t)}</b><small>{esc(d)}</small></span><svg class="ic ms-ta" aria-hidden="true"><use href="#i-arrow"/></svg></a>'
    for i, (u, t, d, ic) in enumerate(TOOLS)) + '''</div>
 </div>
</section>
'''
s = need(s, '<!-- 03 THE ENGINE', STREAMS + '\n<!-- 03 THE ENGINE', 'the engine section')
s = need(s, '<!-- CANTON COIN LIVE', TOOLS_HTML + '\n<!-- CANTON COIN LIVE', 'the Canton Coin section')

CSS = '''<style>
/* musathegiant.com's own sections (written by .github/sync/sync.py), in the mtgtribe.com design */
.sr-only{position:absolute!important;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}
.ms-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,330px),1fr));gap:20px;margin-top:36px}
.ms-card{position:relative;display:flex;flex-direction:column;gap:12px;min-width:0;padding:24px;border-radius:24px;
  background:linear-gradient(160deg,rgba(255,255,255,.07),rgba(255,255,255,.02));box-shadow:inset 0 0 0 1px rgba(255,255,255,.1),inset 0 1px 0 rgba(255,255,255,.14),0 24px 50px rgba(0,0,0,.4)}
.ms-card.ms-top{box-shadow:inset 0 0 0 1px rgba(var(--gold-rgb),.55),inset 0 1px 0 rgba(255,255,255,.18),0 0 50px rgba(var(--gold-rgb),.14),0 24px 50px rgba(0,0,0,.45)}
.ms-row{display:flex;align-items:center;justify-content:space-between;gap:10px}
.ms-n{font:400 2.4rem/1 var(--f-d);color:transparent;-webkit-text-stroke:1px rgba(var(--gold-rgb),.75)}
.ms-badge{padding:6px 11px;border-radius:99px;font:700 11px/1 var(--f-m);letter-spacing:.12em;text-transform:uppercase;color:#ffd98e;background:rgba(var(--gold-rgb),.12);box-shadow:inset 0 0 0 1px rgba(var(--gold-rgb),.35)}
.ms-card h3{margin:0;font:800 1.25rem/1.25 var(--f-b);color:var(--text);overflow-wrap:anywhere}
.ms-name{display:block;margin-bottom:6px;font:400 1.7rem/1.05 var(--f-d);letter-spacing:.02em;text-transform:uppercase;background:linear-gradient(180deg,#fff3d6,#f2ad3c);-webkit-background-clip:text;background-clip:text;color:transparent}
.ms-card p{margin:0;color:var(--muted);line-height:1.6}
.ms-facts{display:flex;flex-wrap:wrap;gap:8px;margin:2px 0 0;padding:0;list-style:none}
.ms-facts li{padding:7px 11px;border-radius:99px;font-size:.84rem;font-weight:700;color:var(--champ,#efe2c6);background:rgba(255,255,255,.05);box-shadow:inset 0 0 0 1px var(--line-2,rgba(255,255,255,.14))}
.ms-go{margin-top:auto;align-self:flex-start;max-width:100%;white-space:normal;text-align:left}
.ms-streams .more{display:flex;justify-content:center;margin-top:40px}
.ms-tgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));gap:16px;margin-top:36px}
.ms-tool{display:flex;align-items:center;gap:14px;min-width:0;padding:18px;border-radius:20px;color:var(--text);text-decoration:none;
  background:linear-gradient(160deg,rgba(255,255,255,.06),rgba(255,255,255,.02));box-shadow:inset 0 0 0 1px rgba(255,255,255,.1);transition:box-shadow .25s,transform .25s}
.ms-tool:hover{box-shadow:inset 0 0 0 1px rgba(var(--gold-rgb),.6),0 0 30px rgba(var(--gold-rgb),.15);transform:translateY(-2px)}
.ms-tool:focus-visible{outline:3px solid #ffd98e;outline-offset:3px}
.ms-ti{flex:none;display:grid;place-items:center;width:48px;height:48px;border-radius:14px;color:#1a1002;background:linear-gradient(180deg,#ffd98e,#f2ad3c)}
.ms-ti .ic{width:22px;height:22px}
.ms-tool b{display:block;font-weight:800;line-height:1.3}
.ms-tool small{display:block;margin-top:3px;color:var(--muted);font-size:.88rem;line-height:1.45}
.ms-ta{flex:none;margin-left:auto;width:18px;height:18px;color:#ffd98e}
.ms-tool>span:nth-child(2){min-width:0}
@media (prefers-reduced-motion:reduce){.ms-tool{transition:none}.ms-tool:hover{transform:none}}
</style>
'''
s = need(s, '</head>', CSS + '</head>', 'the end of the page head')

# 2e. the footer: musathegiant.com's links, MTG's streams in his order, and the MTG TRIBE
s = s.replace('href="https://www.musathegiant.com" target="_blank" rel="noopener" aria-label="MusaTheGiant.com (opens in a new tab)"',
              f'href="{TRIBE}/" target="_blank" rel="noopener" aria-label="The MTG TRIBE, mtgtribe.com (opens in a new tab)"')
fl = (['<a href="/dashboard.html">Income Streams</a>'] + [link(x) for x in streams] +
      [f'<a href="{TRIBE}/canton-weekly/" target="_blank" rel="noopener">Canton weekly</a>', '<a href="/tools/">Free Tools</a>',
       '<a href="/about.html">About MTG</a>', '<a href="/contact.html">Contact</a>',
       f'<a href="{TRIBE}/" target="_blank" rel="noopener">MTG TRIBE</a>', '<a href="/risk-disclaimer.html">Disclaimer</a>',
       '<a href="/privacy-policy.html">Privacy</a>'])
s = sub(s, r'<div class="flinks">.*?</div>', lambda m: '<div class="flinks">' + ''.join(fl) + '</div>', 'footer links')
s = re.sub(r'(<p class="fine">)© (\d{4}) MTG\.', r'\1© \2 MTG (Musa The Giant). MusaTheGiant.com.', s)

s = ('<!-- Built automatically from the mtgtribe.com home page by .github/sync/sync.py. Do not edit by hand. -->\n' + s)
if 'mtgtribe.com/dashboard/"' in s or 'href="/dashboard/"' in s:
    problems.append('note: a link to the mtgtribe.com dashboard remains on the page')

# ------------------------------------------------------------------ 3. the shared design files
files = {}
for p in LOCAL:
    if p == '/assets/updown.js':
        continue                                   # already here (same file on every site)
    b = get(p)
    if p == '/assets/tribe/bottom-nav.js':
        t = b.decode('utf-8')
        t = t.replace("var onDash = /^\\/dashboard\\/?$/.test(path);", "var onDash = /^\\/dashboard(\\.html)?\\/?$/.test(path);")
        t = t.replace("'/dashboard/#streams'", "'/#streams'").replace("'/dashboard/'", "'/dashboard.html'")
        t = t.replace("'/group/'", "'" + TRIBE + "/group/'").replace("'/canton-weekly/'", "'" + TRIBE + "/canton-weekly/'")
        t = t.replace("a('/#invite',", "a(onHome ? '#invite' : '/#invite',")
        t = t.replace("'#totop,.mtg-up{bottom:", "'#totop,.totop,.mtg-up{bottom:")
        t = '/* Copied from mtgtribe.com by .github/sync/sync.py, with musathegiant.com addresses. */\n' + t
        b = t.encode('utf-8')
    files[p] = b

# ------------------------------------------------------------------ 4. every list of MTG's streams on musathegiant.com
FOOT = (MARK_A + '<nav aria-label="Income streams"><h2>Income Streams</h2><ul>' +
        ''.join(f'<li>{link(x)}</li>' for x in streams) +
        f'<li><a href="{TRIBE}/" target="_blank" rel="noopener">MTG TRIBE</a></li></ul></nav>' + MARK_B)
pages = {}
for dp, dn, fn in os.walk(ROOT):
    dn[:] = [x for x in dn if not x.startswith('.') and x not in ('cards', 'bellvercards', 'preview-v2', 'endotech', 'halvings')]
    for f in fn:
        if f.endswith('.html') and not (dp == ROOT and f == 'index.html'):
            pages[os.path.join(dp, f)] = None
for p in list(pages):
    t = open(p, encoding='utf-8').read()
    if MARK_A in t:
        t2 = re.sub(re.escape(MARK_A) + '.*?' + re.escape(MARK_B), lambda m: FOOT, t, flags=re.S)
    elif '<nav aria-label="Legal">' in t and 'foot-grid' in t:
        t2 = t.replace('<nav aria-label="Legal">', FOOT + '<nav aria-label="Legal">', 1)
    else:
        t2 = t
    pages[p] = t2 if t2 != t else None

llms_p = os.path.join(ROOT, 'llms.txt')
llms = open(llms_p, encoding='utf-8').read()
line = ("MTG's income streams, in his order (" + data.get('updated', '') + "): " +
        ', '.join(f'{i + 1}. {x["name"]} ({(SITE + surl(x)) if not ext(surl(x)) else surl(x)})' for i, x in enumerate(streams)) + '.')
LA, LB = '<!-- streams -->', '<!-- /streams -->'
if LA in llms:
    llms2 = re.sub(re.escape(LA) + '.*?' + re.escape(LB), LA + '\n' + line + '\n' + LB, llms, flags=re.S)
else:
    parts = llms.split('\n\n', 2)
    llms2 = '\n\n'.join(parts[:2] + [LA + '\n' + line + '\n' + LB] + parts[2:]) if len(parts) >= 2 else llms + '\n\n' + LA + '\n' + line + '\n' + LB + '\n'

# the dashboard keeps its own designed cards; check they follow MTG's order
dash = open(os.path.join(ROOT, 'dashboard.html'), encoding='utf-8').read()
want = [x['name'].split(' ')[0].lower() for x in streams]
pos = []
for x in streams:
    key = {'bellver': r'id="cryptocards"|id="bellver"', 'clickbaitpays': r'id="clickbait"|id="clickbaitpays"',
           'bitcoinwealth': r'id="bitcoin"|id="bitcoinwealth"'}.get(x['id'], f'id="{x["id"]}"')
    m = re.search(r'<(section|article|div)[^>]*(' + key + ')', dash)
    pos.append(m.start() if m else -1)
if -1 in pos or pos != sorted(pos):
    problems.append('CHECK dashboard.html: its stream cards are missing one or not in the order of streams.json ('
                    + ', '.join(x['name'] for x in streams) + ')')

# ------------------------------------------------------------------ write
changed = []


def write(p, b):
    full = os.path.join(ROOT, p.lstrip('/'))
    old = open(full, 'rb').read() if os.path.exists(full) else None
    if old != b:
        os.makedirs(os.path.dirname(full), exist_ok=True)
        open(full, 'wb').write(b)
        changed.append(p)


write('/index.html', s.encode('utf-8'))
if '/index.html' in changed:                      # tell search engines the home page is new
    import datetime
    sm_p = os.path.join(ROOT, 'sitemap.xml')
    sm = open(sm_p, encoding='utf-8').read()
    sm2 = re.sub(r'(<loc>https://www\.musathegiant\.com/</loc>\s*<lastmod>)[^<]*', r'\g<1>' + datetime.date.today().isoformat(), sm, count=1)
    if sm2 != sm:
        open(sm_p, 'w', encoding='utf-8').write(sm2); changed.append('/sitemap.xml')
for p, b in files.items():
    write(p, b)
for p, t in pages.items():
    if t is not None:
        write('/' + os.path.relpath(p, ROOT), t.encode('utf-8'))
if llms2 != llms:
    write('/llms.txt', llms2.encode('utf-8'))
print('changed:', ', '.join(changed) if changed else 'nothing (already in sync)')
for p in problems:
    print(p)
if any(p.startswith('CHECK') for p in problems):
    sys.exit(2)
