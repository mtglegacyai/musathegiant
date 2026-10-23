# -*- coding: utf-8 -*-
"""Team pages: member list, the text that changes on a member's copy, and the safety scan.
Every team page goes through finalize(): if anything still points at MTG's referral link, WhatsApp,
socials or website, the build stops and names the problem, so nothing leaks onto a live page."""
import json, os, re
import bv
from team_shell import NOWA, TEAM_DIR, MTG_ASSETS, TEAM_FAV, socials

HERE = os.path.dirname(os.path.abspath(__file__))


def _all():
    with open(os.path.join(HERE, 'team.json'), encoding='utf-8') as f:
        return json.load(f)['members']


def members(target=None):
    """Team members built for a site: 'bva' = bellveraffiliates.com/<slug>, 'mtg' = musathegiant.com/bellvercards/<slug>.
    A member's "sites" in team.json lists where they live (new members: bellveraffiliates.com only)."""
    target = target or bv.TARGET
    return [m for m in _all() if target in m.get('sites', ['bva'])]


# folder names MTG's own guide uses at the root of bellveraffiliates.com: a team member can never take one of these
RESERVED = {'learn', 'get-started', 'how-it-works', 'prices', 'rewards', 'matrix', 'partner', 'rewards-calculator', 'payback-calculator',
            'videos', 'explainers', 'tutorials', 'faq', 'docs', 'downloads', 'assets', 'images', 'og', 'cards', 'bellvercards', 'index.html'}


def member(slug):
    if slug in RESERVED:
        raise SystemExit(f'"{slug}" is a page name on MTG\'s guide: choose another address for this team member')
    for m in _all():
        if m['slug'] == slug:
            return m
    raise SystemExit(f'No team member called {slug} in team.json')


# ---- text that speaks as MTG, rewritten for the member. {n} = full name, {f} = first name.
# Each phrase must still be found, so a wording change on MTG's pages can never slip through unnoticed.
TEXT = [
 # home
 ('Ask MTG about it', 'Ask {f} about it'),
 ("Register with MTG's link", "Register with {f}'s link"),
 # how it works
 ('Ask MTG what it includes', 'Ask {f} what it includes'),
 # get started
 ('Using this link places you in my team, so I can see your sign-up and help you if you get stuck.',
  'Using this link places you in {f}\'s team, so {f} can see your sign-up and help you if you get stuck.'),
 # faq
 ('Ask MTG for the details before you choose it.', 'Ask {f} for the details before you choose it.'),
 ('Message MTG on WhatsApp for personal help, or use', 'Message {f} on WhatsApp for personal help, or use'),
 # partner page
 ('Ask MTG a question', 'Ask {f} a question'),
 ('Do I need to talk to MTG or apply to become a partner?', 'Do I need to talk to {f} or apply to become a partner?'),
 ('There is no application and no approval from MTG. You are welcome to message MTG with questions, but you never have to.',
  'There is no application and no approval from {f}. You are welcome to message {f} with questions, but you never have to.'),
 # page titles and descriptions
 ('Step-by-step Bellver Card tutorials by MTG:', 'Step-by-step Bellver Card tutorials:'),
 ('Your complete Bellver Card guide by MTG:', 'Your complete Bellver Card guide, shared by {n}:'),
 ('Bellver Card guide by MTG', 'Bellver Card guide by {n}'),
 # MTG's own work, described in his voice: say it neutrally so it is not claimed as the member's
 ('Watch it explained in under 9 minutes, in my own voice', 'Watch it explained in under 9 minutes'),
 ('plus my plain-words 2x2 matrix guide', 'plus a plain-words 2x2 matrix guide'),
 # links to MTG's own legal pages: the member's footer carries the disclaimer instead
 ('Earnings are never guaranteed: read the <a class="inl" href="/earnings-disclaimer.html">Earnings Disclaimer</a>.', 'Earnings are never guaranteed.'),
 (' Read the <a href="/earnings-disclaimer.html">Earnings Disclaimer</a>.', ''),
 (' Read the <a class="inl" href="/earnings-disclaimer.html">Earnings Disclaimer</a> and the <a class="inl" href="/risk-disclaimer.html">Risk Disclaimer</a>.', ''),
 # structured data: MTG's matrix page author becomes the member; MTG stays the named author of his own videos, without his links
 ('"@id": "https://www.musathegiant.com/#mtg"', '"@id": "{site}{base}#partner"'),
 ('"name": "MTG",\n    "jobTitle": "Your Digital Architect",\n    "url": "https://www.musathegiant.com/"', '"name": "MTG"'),
]

# MTG's own creations stay credited to him where the work is his (his videos and his PDF guide are shared exactly as they are).
# These are the only places his name may appear on a team page.
CREDITS = [
 'Explainer by MTG', '"name": "MTG"', 'Narrated by MTG with his AI voice', "MTG's own 2x2 matrix explainer", "MTG's own explainers", 'Short explainer videos by MTG', 'Explainers by MTG, narrated with his AI voice', "in MTG's own voice", 'explainer video by MTG',
 '2x2 matrix guide by MTG', 'Made by MTG from Bellver', 'by-mtg.pdf',
]


def _remove_no_whatsapp(html, f):
    """Partner gave no WhatsApp: drop every button or link that would have used it, and the words that promised it."""
    if bv.WA != NOWA:
        return html
    html = re.sub(r'<a\b[^>]*href="' + re.escape(NOWA) + r'[^"]*"[^>]*>.*?</a>', '', html, flags=re.S)
    html = html.replace(f'Message {f} on WhatsApp for personal help, or use the Support area', 'Use the Support area')
    # the "Questions? Ask me" box on the partner page: point it at another link they gave, or leave the box out
    k = '<h3 class="h3">Questions? Ask me</h3>'
    if k in html:
        i = html.rfind('<div class="box rv"', 0, html.index(k)); j = html.index('<div class="btn-row" style="margin-top:12px"></div></div>', i)
        end = j + len('<div class="btn-row" style="margin-top:12px"></div></div>')
        soc = socials()
        if soc:
            key, lab, url = soc[0]
            html = html[:j] + f'<div class="btn-row" style="margin-top:12px"><a class="btn btn-ghost btn-sm" href="{url}" target="_blank" rel="noopener">{bv.ic(key)}Ask {f} on {lab}</a></div></div>' + html[end:]
        else:
            html = html[:i] + html[end:]
    return html


USED = set()


def check_all_used():
    """After a member's pages are built: every rewrite must have found its phrase. If MTG's wording changed, update TEXT."""
    missing = [old for old, new in TEXT if old not in USED]
    if missing:
        raise SystemExit('team.py TEXT phrases no longer found on MTG\'s pages (update them):\n  ' + '\n  '.join(missing))


def _swap_checklist(html):
    """MTG's Starter Checklist is his personal offer: on team pages that box points to the tutorials instead."""
    k = '<h3 class="h3">Starter Checklist</h3>'
    if k not in html:
        return html
    i = html.rfind('<div class="box rv"', 0, html.index(k)); j = html.index('</a></div></div>', i) + len('</a></div></div>')
    box = (f'<div class="box rv" style="--d:.06s">{bv.ped(bv.ic("play-c"), '')}<h3 class="h3">Tutorial videos</h3>'
           '<p>Short step-by-step videos: register, secure your account, back up your key, fund your wallet and order your card.</p>'
           f'<div class="btn-row" style="margin-top:12px"><a class="btn btn-ghost btn-sm" href="{bv.BASE}tutorials/">Watch the tutorials</a></div></div>')
    return html[:i] + box + html[j:]


def finalize(html, m, path):
    n, f = m['name'], (m.get('short') or m['name'].split()[0])
    if bv.TARGET == 'bva':   # on bellveraffiliates.com MTG's legal links are absolute: match them like the site paths TEXT expects
        html = html.replace('href="' + bv.MTG_SITE + '/', 'href="/')
    for old, new in TEXT:
        if old in html:
            USED.add(old)
            html = html.replace(old, new.format(n=n, f=f, site=bv.SITE, base=bv.BASE))
    html = _swap_checklist(html)
    html = _remove_no_whatsapp(html, f)
    problems = scan(html, m)
    if problems:
        where = TEAM_DIR + m['slug'] + '/' + path
        if os.environ.get('TEAM_SCAN_REPORT'):
            print('LEAKS', where, *problems, sep='\n  '); return html
        raise SystemExit(f'Team page {where} still points at MTG:\n  ' + '\n  '.join(problems))
    return html


MTG_MARKERS = ['ref=mtg', '27721714626', 'Musa.TheMTG', 'tiktok.com/@musathegiant', 'youtube.com/@MusaTheGiant', 'mtg-profile', 'Musa The Giant',
               'Musa the Giant', 'Crypto-Regards', "Let's Get This Crypto", 'Your Digital Architect', '#mtg"',
               'VAKM6VZY', 'ref=11139868', 'clickbaitpaysus.com']


def scan(html, m):
    """Return a list of leaks. Videos' own transcripts are checked separately (they are MTG's narration, shared as is)."""
    out = []
    body = strip_transcripts(html)
    for k in MTG_MARKERS:
        if k in body:
            i = body.index(k); out.append(f'"{k}" near: {body[max(0, i - 60):i + 60]!r}')
    # links: only this member's pages, MTG's shared files (images, styles, videos, PDFs) and outside sites
    base = TEAM_DIR + m['slug'] + '/'
    for href in re.findall(r'href="([^"]+)"', html):
        h = href.replace(bv.SITE, '')
        if h.startswith('/') and not (h.startswith(base) or h.startswith(MTG_ASSETS + 'assets/') or h.startswith(MTG_ASSETS + 'docs/')
                                       or h.startswith(MTG_ASSETS + 'images/') or h.startswith(MTG_ASSETS + 'videos/') or h == TEAM_FAV):
            out.append(f'link to MTG\'s site: {href}')
        if 'musathegiant' in h:
            out.append(f'link to MTG\'s site: {href}')
    # MTG's name: only in the credits for his own videos and guide
    text = body
    for c in CREDITS:
        text = text.replace(c, '')
    for mt in re.finditer(r'\bMTG\b', text):
        out.append(f'"MTG" near: {text[max(0, mt.start() - 70):mt.end() + 50]!r}')
    return out[:40]


def strip_transcripts(html):
    """Video transcripts (MTG's narration word for word) and video data are part of the videos, which are shared as they are."""
    html = re.sub(r'<details class="qa more"><summary>Read the transcript.*?</details>', '', html, flags=re.S)
    html = re.sub(r'"transcript": "(?:[^"\\]|\\.)*"', '"transcript": ""', html)
    return html


def write_index(root):
    """/bellvercards/ itself: forwards to MTG's guide, so nobody lands on an empty folder.
    On bellveraffiliates.com MTG's guide is the root itself, so only the team tab icon is written."""
    to = MTG_ASSETS
    d = os.path.join(root, TEAM_DIR.strip('/')); os.makedirs(d, exist_ok=True)
    if bv.TARGET == 'bva':
        _team_favicon(os.path.join(root, TEAM_FAV.strip('/'))); return
    with open(os.path.join(d, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Bellver Card guide</title>
<meta name="robots" content="noindex,follow"><link rel="canonical" href="{bv.SITE}{to}">
<meta http-equiv="refresh" content="0; url={to}"><script>location.replace("{to}")</script></head>
<body style="background:#020c06;color:#eef5f1;font-family:system-ui,sans-serif;padding:40px"><a style="color:#34cc88" href="{to}">Continue to the Bellver Card guide</a>.</body></html>
''')
    print('redirect', TEAM_DIR, '->', to)
    # a neutral tab icon for team pages (MTG's crown stays on his own site): a green card on Bellver's dark green
    _team_favicon(os.path.join(d, 'favicon.svg'))


def _team_favicon(path):
    with open(path, 'w', encoding='utf-8') as f:
        f.write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="100" height="100" rx="20" fill="#020c06"/>'
                '<rect x="16" y="28" width="68" height="46" rx="8" fill="#34b070"/><rect x="16" y="39" width="68" height="8" fill="#020c06"/>'
                '<rect x="24" y="58" width="16" height="6" rx="2" fill="#020c06"/></svg>\n')
