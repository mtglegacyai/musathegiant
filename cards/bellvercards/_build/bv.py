# -*- coding: utf-8 -*-
"""Bellver Cards by MTG: shared config, icons and page shell.
Edit links here once and every page updates when you run build.py."""
import json, os, posixpath

# ---- one place for every link ----
SITE = 'https://www.musathegiant.com'
BASE = '/cards/bellvercards/'
REF = 'https://app.bellvercards.com?ref=mtg'            # MTG affiliate link (every order button)
LOGIN = 'https://app.bellvercards.com/login'            # member login
WA = 'https://wa.me/27721714626'                        # MTG WhatsApp
WA_MSG = WA + '?text=' + 'Hi%20MTG%2C%20I%20am%20interested%20in%20the%20Bellver%20Card.%20Can%20you%20help%20me%20get%20started%3F'
YT_27 = '_Ptm2Bj6gm4'
YT_WEBINAR = 'jeB_kZinnCg'
MP4_3MIN = 'videos/bellvercard-in-3minutes.mp4'
MP4_DASH = 'videos/bellvercards-dashboard-walkthrough.mp4'
UPDATED = '2026-10-09'
ASSET_BASE = BASE       # where images, styles, scripts, videos and PDFs live (team pages share MTG's files)
PARTNER = None          # set by configure() when building a team member's page (see team.json)
# Analytics: leave None until MTG creates a free GoatCounter site, then set e.g. 'musathegiant' (the site code).
ANALYTICS_GOATCOUNTER = None
CHECKLIST_MSG = WA + '?text=' + 'Hi%20MTG%2C%20please%20send%20me%20the%20free%20Bellver%20Starter%20Checklist.'
PARTNER_MSG = WA + '?text=' + 'Hi%20MTG%2C%20I%20have%20a%20question%20about%20the%20Bellver%20Card.'
# ---- MTG's other referral links (exchanges for onboarding, traffic for builders). Team pages only show a member's own links.
VALR = 'https://www.valr.com/invite/VAKM6VZY'
BINANCE = 'https://account.binance.com/register?ref=11139868&?registerChannel=user_center'
CBP = 'https://clickbaitpaysus.com'

import hashlib, os


def asset(name, here=''):
    """Asset URL with a content hash, so phones and browsers never keep serving a stale stylesheet or script."""
    f = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', name)
    v = hashlib.md5(open(f, 'rb').read()).hexdigest()[:8]
    return L(name, here) + '?v=' + v


MODE = 'prod'   # set by build.py: 'prod' writes site paths, 'preview' writes relative links for the preview copy


def L(target, here=''):
    """Link helper. target: '' or 'prices/' (inside Bellver), 'images/x.webp', '/about.html' (site), or full URL."""
    if target.startswith(('http://', 'https://', 'mailto:', '#')):
        return target
    if target.startswith('/'):
        return target if MODE == 'prod' else SITE + target
    if MODE == 'prod':
        return (BASE if _is_page(target) else ASSET_BASE) + target
    if target.startswith('videos/') and target.endswith('.mp4'):
        return SITE + BASE + target
    frag = ''
    if '#' in target:
        target, frag = target.split('#', 1); frag = '#' + frag
    rel = posixpath.relpath(target or '.', here or '.') if (target or here) else '.'
    if target == '' or target.endswith('/'):
        rel = (rel.rstrip('/') + '/index.html') if rel != '.' else 'index.html'
        rel = rel.replace('./', '') if rel.startswith('./') else rel
    return rel + frag


def _is_page(target):
    p = target.split('#', 1)[0]
    return p == '' or p.endswith('/')


def abs_url(target):
    return SITE + (BASE if _is_page(target) else ASSET_BASE) + target


I = {
 'card': '<rect x="2.5" y="5" width="19" height="14" rx="2.5"/><path d="M2.5 10h19M6.5 15h4"/>',
 'shield': '<path d="M12 3l7.5 3v5.5c0 4.6-3.2 8.3-7.5 9.5-4.3-1.2-7.5-4.9-7.5-9.5V6L12 3z"/><path d="M8.8 12.2l2.2 2.2 4.4-4.6"/>',
 'globe': '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.6 2.6 3.9 5.6 3.9 9s-1.3 6.4-3.9 9c-2.6-2.6-3.9-5.6-3.9-9S9.4 5.6 12 3z"/>',
 'gift': '<rect x="3.5" y="8" width="17" height="4" rx="1"/><path d="M5 12v8h14v-8M12 8v12M12 8c-1.5-3.5-5.5-3.5-5.5-1S10 8 12 8zm0 0c1.5-3.5 5.5-3.5 5.5-1S14 8 12 8z"/>',
 'wallet': '<path d="M19 7V5.5A1.5 1.5 0 0 0 17.5 4h-12A2.5 2.5 0 0 0 3 6.5v11A2.5 2.5 0 0 0 5.5 20h13a1.5 1.5 0 0 0 1.5-1.5V15"/><path d="M3 6.5A2.5 2.5 0 0 0 5.5 9H20a1 1 0 0 1 1 1v4a1 1 0 0 1-1 1h-3.5a2.5 2.5 0 0 1 0-5"/>',
 'key': '<circle cx="8" cy="15" r="4"/><path d="M10.8 12.2L20 3M16.5 6.5l2.5 2.5M14 9l2 2"/>',
 'bolt': '<path d="M13 2.5L4.5 13.5H11l-1 8 8.5-11H12l1-8z"/>',
 'phone': '<rect x="6.5" y="2.5" width="11" height="19" rx="2.5"/><path d="M10.5 18.5h3"/>',
 'nfc': '<path d="M8.5 8a5.5 5.5 0 0 1 0 8M12 5.5a9 9 0 0 1 0 13M15.5 3a12.5 12.5 0 0 1 0 18"/><circle cx="5" cy="12" r="1.2"/>',
 'play': '<path d="M7 4.5v15l12.5-7.5L7 4.5z" fill="currentColor"/>',
 'coins': '<ellipse cx="9" cy="7" rx="6" ry="2.8"/><path d="M3 7v4c0 1.5 2.7 2.8 6 2.8s6-1.3 6-2.8V7M9 13.8v3.4c0 1.5 2.7 2.8 6 2.8s6-1.3 6-2.8v-5c0-1.5-2.7-2.8-6-2.8"/>',
 'arrow': '<path d="M5 12h14M13 6l6 6-6 6"/>',
 'ext': '<path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/>',
 'wa': '<path d="M20.5 3.5A11.8 11.8 0 0 0 12.1 0C5.6 0 .3 5.3.3 11.8c0 2.1.5 4.1 1.6 5.9L0 24l6.5-1.7a11.7 11.7 0 0 0 5.6 1.4h.1c6.5 0 11.8-5.3 11.8-11.8 0-3.2-1.2-6.1-3.5-8.4Zm-8.4 18.2h-.1a9.8 9.8 0 0 1-5-1.4l-.4-.2-3.9 1 1-3.8-.2-.4a9.8 9.8 0 1 1 8.6 4.8Zm5.4-7.3c-.3-.1-1.7-.8-2-.9-.3-.1-.5-.1-.7.2-.2.3-.8.9-.9 1.1-.2.2-.4.2-.7.1-.3-.1-1.3-.5-2.4-1.5-.9-.8-1.5-1.8-1.7-2.1-.2-.3 0-.5.1-.7.1-.1.3-.4.4-.5.1-.2.2-.3.3-.5.1-.2 0-.4 0-.5-.1-.1-.7-1.7-1-2.3-.3-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.5s1.1 2.9 1.2 3.1c.1.2 2.1 3.2 5.1 4.5.7.3 1.3.5 1.7.6.7.2 1.4.2 1.9.1.6-.1 1.7-.7 1.9-1.4.2-.7.2-1.3.2-1.4-.1-.1-.3-.2-.6-.3Z" fill="currentColor" stroke="none"/>',
 'home': '<path d="M3.5 11L12 4l8.5 7M6 9.5V20h12V9.5"/>',
 'grid': '<rect x="3.5" y="3.5" width="7" height="7" rx="1.5"/><rect x="13.5" y="3.5" width="7" height="7" rx="1.5"/><rect x="3.5" y="13.5" width="7" height="7" rx="1.5"/><rect x="13.5" y="13.5" width="7" height="7" rx="1.5"/>',
 'help': '<circle cx="12" cy="12" r="9"/><path d="M9.5 9.3a2.6 2.6 0 0 1 5 .9c0 1.8-2.5 2.2-2.5 3.8M12 17.2h.01"/>',
 'download': '<path d="M12 3.5v12M7 10.5l5 5 5-5M4.5 20h15"/>',
 'book': '<path d="M4 4.5A1.5 1.5 0 0 1 5.5 3H19v15H5.5A1.5 1.5 0 0 0 4 19.5v-15zM4 19.5A1.5 1.5 0 0 0 5.5 21H19"/><path d="M8 7h7"/>',
 'video': '<rect x="2.5" y="5.5" width="14" height="13" rx="2.5"/><path d="M16.5 10.5l5-3v9l-5-3"/>',
 'star': '<path d="M12 3.2l2.7 5.5 6 .9-4.4 4.2 1 6-5.3-2.8-5.4 2.8 1-6L3.3 9.6l6-.9L12 3.2z"/>',
 'users': '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c.6-3.6 3.2-5.5 6.5-5.5s5.9 1.9 6.5 5.5"/><circle cx="17" cy="9" r="2.8"/><path d="M16.5 14.6c2.8.2 4.5 2 5 4.9"/>',
 'tag': '<path d="M3.5 12.3V4.5a1 1 0 0 1 1-1h7.8l8.2 8.2a1.5 1.5 0 0 1 0 2.1l-6.7 6.7a1.5 1.5 0 0 1-2.1 0L3.5 12.3z"/><circle cx="8" cy="8" r="1.4"/>',
 'layers': '<path d="M12 3l9 5-9 5-9-5 9-5z"/><path d="M3 13l9 5 9-5"/>',
 'login': '<path d="M14 4h4.5A1.5 1.5 0 0 1 20 5.5v13a1.5 1.5 0 0 1-1.5 1.5H14M10 8l4 4-4 4M14 12H3.5"/>',
 'lock': '<rect x="4.5" y="10.5" width="15" height="10" rx="2"/><path d="M8 10.5V7.5a4 4 0 0 1 8 0v3"/>',
 'info': '<circle cx="12" cy="12" r="9"/><path d="M12 11v5.5M12 7.6h.01"/>',
 'alert': '<path d="M12 3.5l9.5 16.5h-19L12 3.5z"/><path d="M12 10v4.5M12 17.4h.01"/>',
 'chevron': '<path d="M6 9l6 6 6-6"/>',
 'chev-r': '<path d="M9 6l6 6-6 6"/>',
 'chev-l': '<path d="M15 6l-6 6 6 6"/>',
 'up': '<path d="M12 19V5M6 11l6-6 6 6"/>',
 'check': '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
 'play-c': '<circle cx="12" cy="12" r="9"/><path d="M10 8.5v7l6-3.5-6-3.5z" fill="currentColor"/>',
 'rocket': '<path d="M5 15c-1.5 1-2 3.5-2 6 2.5 0 5-.5 6-2M14.5 4.5c3-1.5 5.5-1.5 5.5-1.5s0 2.5-1.5 5.5L12 15l-3-3 5.5-7.5z"/><path d="M9 12l-3.5-.5L8 8.5h4M12 15l.5 3.5L15.5 16v-4"/>',
 'calendar': '<rect x="3.5" y="5" width="17" height="15.5" rx="2"/><path d="M3.5 10h17M8 3v4M16 3v4"/>',
 'pin': '<path d="M12 21s-6.5-6.2-6.5-11a6.5 6.5 0 0 1 13 0c0 4.8-6.5 11-6.5 11z"/><circle cx="12" cy="10" r="2.3"/>',
 'swap': '<path d="M4 8h13l-3.5-3.5M20 16H7l3.5 3.5"/>',
 'eye': '<path d="M2.5 12S6 5.5 12 5.5 21.5 12 21.5 12 18 18.5 12 18.5 2.5 12 2.5 12z"/><circle cx="12" cy="12" r="3"/>',
 'tree': '<circle cx="12" cy="5" r="2.6"/><circle cx="5.5" cy="18" r="2.6"/><circle cx="18.5" cy="18" r="2.6"/><path d="M10.7 7.3L6.8 15.6M13.3 7.3l3.9 8.3"/>',
 'down': '<path d="M12 4v15M6 13l6 6 6-6"/>',
 'calc': '<rect x="5" y="3" width="14" height="18" rx="2.5"/><rect x="8" y="6" width="8" height="4" rx="1"/><path d="M8.5 13.5h.01M12 13.5h.01M15.5 13.5h.01M8.5 17h.01M12 17h.01M15.5 17h.01"/>',
 'building': '<path d="M4 21V5.5A1.5 1.5 0 0 1 5.5 4h7A1.5 1.5 0 0 1 14 5.5V21M14 10h4.5A1.5 1.5 0 0 1 20 11.5V21M3 21h18M8 8h2M8 12h2M8 16h2"/>',
}


def ic(name, cls=''):
    c = f' class="{cls}"' if cls else ''
    return f'<svg{c} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{I[name]}</svg>'


def order_btn(label='Order your card', cls='btn btn-go', here='', icon=True):
    return f'<a class="{cls}" href="{REF}" target="_blank" rel="sponsored noopener">{label}</a>'


# guide pages: (key, path, label, sub, icon, group). Sidebar and Previous/Next follow this order.
NAV = [
 ('learn', 'learn/', 'Overview', 'Everything in one place', 'grid', 'Start here'),
 ('start', 'get-started/', 'Get Started', 'Order your card step by step', 'rocket', 'Start here'),
 ('how', 'how-it-works/', 'How It Works', 'Wallet, funding and security', 'layers', 'The card'),
 ('prices', 'prices/', 'Prices & Limits', 'Four levels, fees, add-ons', 'tag', 'The card'),
 ('rewards', 'rewards/', 'Rewards Program', 'Commissions, matrix, ranks', 'users', 'Earn'),
 ('matrix', 'matrix/', '2x2 Matrix Explained', 'The rewards plan, made simple', 'tree', 'Earn'),
 ('partner', 'partner/', 'Become a Partner', 'Share the card, step by step', 'rocket', 'Earn'),
 ('rcalc', 'rewards-calculator/', 'Rewards Calculator', 'Your 0.1% in your own numbers', 'calc', 'Tools'),
 ('pcalc', 'payback-calculator/', 'Payback Calculator', 'Can referrals cover your card?', 'coins', 'Tools'),
 ('videos', 'videos/', 'Presentation Videos', '3 min, 27 min and the full talk', 'video', 'Watch'),
 ('explainers', 'explainers/', 'Explainer Videos', 'Big topics, explained simply', 'eye', 'Watch'),
 ('tutorials', 'tutorials/', 'Tutorial Videos', 'Short how-to guides', 'play-c', 'Watch'),
 ('faq', 'faq/', 'FAQ & Glossary', 'Straight answers, plain words', 'help', 'Help'),
 ('docs', 'docs/', 'Documents', 'Price list, plan, slides (PDF)', 'download', 'Help'),
]
DOCS_PDF = {'matrix': 'docs/bellver-2x2-matrix-explained-by-mtg.pdf', 'price': 'docs/bellver-card-price-list.pdf', 'plan': 'docs/bellver-card-compensation-plan.pdf', 'slides': 'docs/bellver-card-presentation.pdf'}


def dl_btn(kind, here, label, cls='btn btn-ghost'):
    return f'<a class="{cls}" href="{L(DOCS_PDF[kind], here)}" download>{ic("download")}{label}</a>'


def header(here, key):
    """Landing page header: logo, Learn more, Order."""
    if PARTNER:
        return team_header(here, key)
    return f'''<a class="skip" href="#main">Skip to content</a>
<div class="progress" aria-hidden="true"></div>
<header class="hdr">
 <div class="wrap hdr-in">
  <a class="brand" href="{L('', here)}" aria-label="Bellver Cards by MTG, home">
   <img src="{L('images/bellver-cards-logo-white-360.webp', here)}" alt="Bellver Card logo" width="360" height="106">
   <span class="by">Bellver Cards<b>by <span class="aff-l">Affiliate</span><abbr class="aff-s" title="Affiliate">AFF</abbr> MTG 👑</b></span>
  </a>
  <div class="hdr-act">
   <a class="btn btn-ghost btn-sm learn-btn" href="{L('learn/', here)}">{ic('book')}Learn more</a>
   {order_btn('Order your card', 'btn btn-go btn-sm')}
  </div>
 </div>
</header>'''


def sidebar(here, key):
    if PARTNER:
        return team_sidebar(here, key)
    groups = []; cur_g = None; items = ''
    for k, path, label, sub, icn, g in NAV:
        if g != cur_g:
            if cur_g is not None:
                groups.append((cur_g, items))
            cur_g, items = g, ''
        on = ' aria-current="page"' if k == key else ''
        items += f'<a class="snav" href="{L(path, here)}"{on}><span class="ic">{ic(icn)}</span><span class="tx"><b>{label}</b><small>{sub}</small></span></a>'
    groups.append((cur_g, items))
    nav = ''.join(f'<div class="sgroup"><p class="slabel">{g}</p>{it}</div>' for g, it in groups)
    return f'''<aside class="side" id="bv-menu" aria-label="Bellver Card guide">
 <div class="side-top">
  <a class="sbrand" href="{L('', here)}" aria-label="Bellver Cards home"><img src="{L('images/bellver-cards-logo-white-360.webp', here)}" alt="Bellver Card logo" width="360" height="106"></a>
  <span class="sby">Card guide by Affiliate MTG 👑</span>
 </div>
 <nav class="snavs">{nav}</nav>
 <div class="side-bot">
  {order_btn('Order your card', 'btn btn-go btn-sm sorder')}
  <div class="srow">
   <a class="slink" href="{LOGIN}" target="_blank" rel="noopener">{ic('login')}Member Login</a>
   <a class="slink" href="{WA_MSG}" target="_blank" rel="noopener">{ic('wa')}WhatsApp MTG</a>
  </div>
  <div class="srow">
   <a class="slink" href="{REF}" target="_blank" rel="sponsored noopener">{ic('home')}Bellver Home</a>
   <a class="slink" href="{L('/cards/', here)}">{ic('card')}All Cards</a>
  </div>
 </div>
</aside>
<button class="side-toggle" type="button" aria-controls="bv-menu" aria-expanded="true" aria-label="Collapse menu" title="Collapse menu">{ic('chev-l')}</button>
<div class="scrim" aria-hidden="true"></div>'''


def topbar(here, key):
    label = next(n[2] for n in NAV if n[0] == key)
    return f'''<header class="dtop">
 <button class="menu-btn" type="button" aria-expanded="false" aria-controls="bv-menu"><span class="bars" aria-hidden="true"></span><span class="lbl">Menu</span></button>
 <nav class="dcrumb" aria-label="You are here"><a href="{L('learn/', here)}">Card guide</a>{ic('chev-r')}<span aria-current="page">{label}</span></nav>
 <div class="dtop-act"><a class="btn btn-ghost btn-sm gohome" href="{L('', here)}" aria-label="Go Home: back to the Bellver Cards home page"><span class="emo" aria-hidden="true">🏡</span>Go Home</a>{order_btn('Order your card', 'btn btn-go btn-sm orderbtn')}</div>
</header>'''


def pager(here, key):
    keys = [n[0] for n in NAV]
    i = keys.index(key)
    prev = NAV[i - 1] if i > 0 else None
    nxt = NAV[i + 1] if i < len(NAV) - 1 else None

    def cell(n, cls, lab):
        if not n:
            return f'<a class="pg {cls}" href="{L("", here)}"><small>{lab}</small><b>Bellver Card Home</b></a>'
        return f'<a class="pg {cls}" href="{L(n[1], here)}"><small>{lab}</small><b>{n[2]}</b></a>'
    return f'<section class="sec-tight pager-sec"><div class="wrap"><nav class="pager" aria-label="Previous and next page">{cell(prev, "prev", "Previous")}{cell(nxt, "next", "Next")}</nav></div></section>'


def dash_footer(here):
    if PARTNER:
        return team_dash_footer(here)
    return f'''<footer class="dfoot"><div class="wrap">
  <div class="disc">Bellver Card is a product of Bellver Markets Ltd. This guide is run independently by MTG and is not the official Bellver website or back office. Order buttons link to app.bellvercards.com with MTG's referral code, and the VALR, Binance and ClickBaitPays buttons are MTG's referral links too, so MTG may earn a commission at no extra cost to you. Prices, fees and the compensation plan come from Bellver's official documents (version 08/2026) and can change. Rewards depend on real card activity and are never guaranteed. Nothing here is financial, tax or legal advice. Read the <a href="{L('/affiliate-disclosure.html', here)}">Affiliate Disclosure</a>, <a href="{L('/earnings-disclaimer.html', here)}">Earnings Disclaimer</a> and <a href="{L('/risk-disclaimer.html', here)}">Risk Disclaimer</a>.</div>
  <div class="ftr-bot"><span>© <span data-year>2026</span> MTG | Musa The Giant. <a href="{L('/privacy-policy.html', here)}">Privacy</a> &nbsp; <a href="{L('/terms-of-use.html', here)}">Terms</a></span><span class="sig">Let's Get This Crypto! 💰 Crypto-Regards, MTG 👑</span></div>
 </div></footer>'''


# Every section is open when a page loads (MTG, 17 Oct 2026: no tap-to-open section buttons).
# Set to 2 to bring back the tap-to-open sections (first 2 sections shown, the rest behind buttons).
OPEN_SECTIONS = 99


def shell(here, key, body, dash):
    if not dash:
        return f'{header(here, key)}\n<main id="main" data-open="{OPEN_SECTIONS}">\n{body}\n</main>\n{footer(here)}'
    tail = footer(here).split('</footer>', 1)[1]
    return f'''<a class="skip" href="#main">Skip to content</a>
<div class="progress" aria-hidden="true"></div>
<div class="dash">
<script>try{{if(localStorage.getItem("bv-side")==="off"&&innerWidth>1060)document.querySelector(".dash").classList.add("side-off")}}catch(e){{}}</script>
{sidebar(here, key)}
<div class="dmain">
{topbar(here, key)}
<main id="main" data-open="{OPEN_SECTIONS}">
{body}
{pager(here, key)}
</main>
{dash_footer(here)}
</div>
</div>{tail}'''


def help_band(here, title="Stuck? I'll walk you through it.", text="I'm MTG. Message me on WhatsApp and I'll help you register, fund your wallet and choose the right card for you."):
    if PARTNER:
        return team_help_band(here, title)
    return f'''<section class="sec-tight"><div class="wrap"><div class="panel help rv">
  <div class="face"><img src="{L('/images/mtg-profile.jpg', here)}" alt="MTG, Musa The Giant" width="88" height="88" loading="lazy"></div>
  <div><h2>{title}</h2><p>{text}</p></div>
  <a class="btn btn-wa" href="{WA_MSG}" target="_blank" rel="noopener">{ic('wa')}WhatsApp MTG</a>
 </div></div></section>'''


def checklist_band(here, title='Not ready to order yet? <em>Take the free checklist.</em>', text='A two-page Bellver Starter Checklist: what to prepare, how to secure your wallet, how to fund it, which level to pick and the rules that decide whether you get paid. Message me on WhatsApp and I will send it to you personally.'):
    if PARTNER:
        return ''   # MTG's personal checklist offer: not part of team pages
    return f'''<section class="sec-tight" id="checklist"><div class="wrap"><div class="panel checklist rv">
  <div class="ck-ico">{ic('book')}</div>
  <div class="ck-tx"><h2 class="h2">{title}</h2><p>{text}</p>
   <ul class="ck-pts"><li>{ic('check')}Free, no obligation</li><li>{ic('check')}Plain words, two pages</li><li>{ic('check')}Sent to you on WhatsApp</li></ul></div>
  <a class="btn btn-wa" data-track="checklist" href="{CHECKLIST_MSG}" target="_blank" rel="noopener">{ic('wa')}Get the checklist on WhatsApp</a>
 </div></div></section>'''


def news_band(here, compact=False):
    """Good to know before you start: the current fees and rules a newcomer needs (from Bellver's October 2026 update, stated as they apply today)."""
    items = [
     ('coins', 'Top-up fee: 3.9%, added on top', 'The fee is added to the amount you load, so load $100 and $103.90 leaves your wallet. The minimum top-up is $10, so always keep a little extra in your wallet.'),
     ('star', 'Special Edition: $370', 'Choose it when you buy your card and it costs $370. Upgrading a regular card to the Special Edition later costs $470, so decide at the start.'),
     ('users', 'Your first star', 'Everyone starts as a Member. Your first star comes when you hold a Premium card and directly refer two new participants who each buy a Premium card.'),
     ('shield', 'Keep your account safe', 'Bellver never emails links to its login page. Use a strong password and switch on two-factor login or a passkey from day one.'),
     ('pin', 'Physical cards: two must-haves', 'Give a complete, accurate shipping address and a valid mobile number from the country where the card will be delivered. The courier uses both, and without them the card cannot be delivered.'),
     ('wallet', 'Keep a little BNB for fees', 'Network fees on BNB Chain are paid in BNB. Keep about $10 worth in your wallet so every step goes through.'),
    ]
    cards = ''.join(f'<div class="box rv" style="--d:{(i % 3) * 0.06:.2f}s"><div class="ico">{ic(k)}</div><h3 class="h3">{t}</h3><p>{d}</p></div>' for i, (k, t, d) in enumerate(items))
    sub = '' if compact else '<p class="lead">The fees and rules that matter most when you start, in plain words.</p>'
    return f'''<section class="sec-tight" id="good-to-know"><div class="wrap">
 <span id="bellver-news" aria-hidden="true"></span>
 <div class="sec-head rv"><span class="badge green">{ic('info')}Current fees and rules</span><h2 class="h2" style="margin-top:14px">Good to know <em>before you start</em></h2>{sub}</div>
 <div class="grid3">{cards}</div>
 <p class="fine rv" style="margin-top:16px">Bellver's PDFs in the documents section (version 08/2026) still show some older figures. The numbers above are the current ones. Earnings are never guaranteed: read the <a class="inl" href="{L('/earnings-disclaimer.html', here)}">Earnings Disclaimer</a>.</p>
</div></section>'''


def audience_band(here, chips=True, cta=True):
    """Featured audience block: TikTok LIVE hosts first, then the other people the card and rewards suit."""
    others = ['YouTubers and streamers', 'Instagram and Facebook creators', 'WhatsApp and Telegram group admins', 'Network marketers', 'Affiliate marketers', 'Community leaders', 'Side hustlers']
    chip = ''.join(f'<li>{o}</li>' for o in others)
    chips_html = f'<ul class="aud-chips" aria-label="Other people the card suits">{chip}</ul>' if chips else ''
    link = f'<a class="btn btn-ghost" href="{L("partner/#tiktok", here)}">{ic("shield")}Going live? Read this first</a>' if cta else ''
    return f'''<section class="sec-tight" id="audience"><div class="wrap">
 <div class="sec-head rv"><h2 class="h2">Built for people who <em>go live</em></h2><p class="lead">If you host TikTok LIVEs, your audience already knows how you talk about products and services. That trust took you years to build, and it is the hardest part of sharing anything.</p></div>
 <div class="aud rv">
  <div class="aud-main">
   <span class="badge gold">{ic('star')}One of the best fits</span>
   <h3 class="h3">TikTok LIVE hosts and creators</h3>
   <ul class="checks">
    <li><b>Show it, do not just say it.</b> Pay for something live, add the card to your phone, show the dashboard (never your private key).</li>
    <li><b>Your viewers already trust you.</b> People who watch you regularly believe what you tell them, so honesty matters most.</li>
    <li><b>Something real to offer.</b> A card with high limits and a wallet they control, plus a clear commission table and a link that tracks.</li>
    <li><b>Stay within the rules.</b> Disclose that you earn a commission and check TikTok's current rules for your country first.</li>
   </ul>
   <div class="btn-row">{order_btn('Order your card')}{link}</div>
  </div>
  {chips_html}
 </div>
</div></section>'''


def final_cta(here, title='Let\'s make it <span class="hap">happen</span>', text='Order your Bellver Card from $99. Go virtual and you can start paying today.', second=None):
    sec = second or f'<a class="btn btn-ghost" href="{L("get-started/", here)}">See the setup guide</a>'
    return f'''<section class="sec-tight"><div class="wrap"><div class="panel final rv rv-scale">
  <img class="mini" src="{L('images/bellver-card-black-visa-640.webp', here)}" alt="Black Bellver Visa Business card" width="640" height="385" loading="lazy">
  <h2>{title}</h2>
  <p class="lead">{text}</p>
  <div class="btn-row">{order_btn('Order your card')}{sec}</div>
 </div></div></section>'''


def footer(here):
    if PARTNER:
        return team_footer(here)
    cols = [
     ('The card', [('Overview', 'learn/'), ('How It Works', 'how-it-works/'), ('Prices & Limits', 'prices/'), ('Rewards Program', 'rewards/'), ('2x2 Matrix Explained', 'matrix/'), ('Get Started', 'get-started/')]),
     ('Tools', [('Rewards Calculator', 'rewards-calculator/'), ('Payback Calculator', 'payback-calculator/')]),
     ('Learn', [('Presentation Videos', 'videos/'), ('Explainer Videos', 'explainers/'), ('Tutorial Videos', 'tutorials/'), ('FAQ & Glossary', 'faq/'), ('Documents', 'docs/')]),
     ('MTG', [('All Crypto Cards', '/cards/'), ('About MTG', '/about.html')]),
    ]
    html = ''
    for t, items in cols:
        lis = ''.join(f'<li><a href="{L(p, here)}">{n}</a></li>' for n, p in items)
        html += f'<div><h3>{t}</h3><ul>{lis}</ul></div>'
    return f'''<footer class="ftr">
 <div class="wrap">
  <div class="ftr-top">
   <div class="logo"><img src="{L('images/bellver-cards-logo-white-360.webp', here)}" alt="Bellver Card logo" width="360" height="106" loading="lazy">
    <p class="tag">LET'S MAKE IT <em>HAPPEN</em></p>
    <p>An independent Bellver Card information site by MTG (Musa The Giant), Durban, South Africa. Clear facts, honest numbers and personal help to get you started.</p>
   </div>
   {html}
  </div>
  <div class="disc">Bellver Card is a product of Bellver Markets Ltd. This site is run independently by MTG and is not the official Bellver website. Order buttons link to app.bellvercards.com with MTG's referral code, and the VALR, Binance and ClickBaitPays buttons are MTG's referral links too, so MTG may earn a commission at no extra cost to you. Prices, fees and the compensation plan come from Bellver's official documents (version 08/2026) and can change. Rewards depend on real card activity and are never guaranteed. Nothing here is financial, tax or legal advice. Read the <a href="{L('/affiliate-disclosure.html', here)}">Affiliate Disclosure</a>, <a href="{L('/earnings-disclaimer.html', here)}">Earnings Disclaimer</a> and <a href="{L('/risk-disclaimer.html', here)}">Risk Disclaimer</a>.</div>
  <div class="ftr-bot"><span>© <span data-year>2026</span> MTG | Musa The Giant. <a href="{L('/privacy-policy.html', here)}">Privacy</a> &nbsp; <a href="{L('/terms-of-use.html', here)}">Terms</a></span><span class="sig">Let's Get This Crypto! 💰 Crypto-Regards, MTG 👑</span></div>
 </div>
</footer>
<a class="mobile-cta" href="{REF}" target="_blank" rel="sponsored noopener" aria-hidden="true" tabindex="-1"><span class="btn btn-go">Order your Bellver Card</span></a>
<button class="totop" type="button" aria-label="Back to top"><svg class="ring" viewBox="0 0 54 54" aria-hidden="true"><circle class="bg" cx="27" cy="27" r="25"/><circle class="fg" cx="27" cy="27" r="25"/></svg>{ic('up','arr')}</button>
<script src="{asset('assets/bellver.js', here)}" defer></script>'''


PERSON = {"@type": "Person", "@id": SITE + "/#mtg", "name": "Musa The Giant", "alternateName": ["MTG", "Musa the Giant"], "url": SITE + "/", "image": SITE + "/images/mtg-profile.jpg",
          "sameAs": ["https://www.facebook.com/Musa.TheMTG", "https://www.tiktok.com/@musathegiant", "https://www.youtube.com/@MusaTheGiant"]}


def team_trail(trail):
    """Team pages: keep only the crumbs inside the member's own guide, so nothing leads to MTG's site."""
    if not PARTNER:
        return trail
    out = [(n, u) for n, u in trail if u.startswith(SITE + BASE)]
    return out or [('Home', SITE + BASE)]


def crumbs_ld(trail):
    trail = team_trail(trail)
    items = [{"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(trail)]
    return {"@type": "BreadcrumbList", "itemListElement": items}


def crumbs_html(trail, here):
    trail = team_trail(trail)
    out = []
    for i, (n, u) in enumerate(trail):
        if i == len(trail) - 1:
            out.append(f'<span aria-current="page">{n}</span>')
        else:
            path = u.replace(SITE + BASE, '') if u.startswith(SITE + BASE) else u.replace(SITE, '')
            out.append(f'<a href="{L(path, here)}">{n}</a>{ic("chev-r")}')
    return '<nav class="crumbs" aria-label="Breadcrumb">' + ''.join(out) + '</nav>'


def gc_snippet():
    if not ANALYTICS_GOATCOUNTER:
        return ''
    return f'<script data-goatcounter="https://{ANALYTICS_GOATCOUNTER}.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>'


OG_V = '20261023'  # bump when the social preview images change, so WhatsApp and others fetch the new ones


def page(here, key, title, desc, og_img, og_alt, body, ld_extra=None, trail=None, preload=None, robots='index,follow,max-image-preview:large,max-video-preview:-1', dash=True):
    url = abs_url(here)
    trail = trail or [('Home', SITE + '/'), ('Cards', SITE + '/cards/'), ('Bellver Cards', SITE + BASE)]
    if PARTNER:
        return team_page(here, key, title, desc, og_img, og_alt, body, ld_extra, trail, preload, dash)
    graph = [{"@type": "WebPage", "@id": url + "#page", "url": url, "name": title, "description": desc, "inLanguage": "en",
              "isPartOf": {"@id": SITE + "/#website"}, "author": {"@id": SITE + "/#mtg"}, "dateModified": UPDATED,
              "primaryImageOfPage": {"@type": "ImageObject", "url": abs_url(og_img)}, "breadcrumb": crumbs_ld(trail)},
             {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": "MTG | Musa The Giant", "publisher": {"@id": SITE + "/#mtg"}},
             PERSON]
    graph += (ld_extra or [])
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)
    pre = f'<link rel="preload" as="image" href="{L(preload, here)}" fetchpriority="high">' if preload else ''
    canonical = url
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<script>document.documentElement.classList.add('js')</script>
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canonical}">
<meta name="author" content="Musa The Giant (MTG)">
<meta name="theme-color" content="#020c06">
<link rel="icon" type="image/svg+xml" href="{L('/favicon.svg', here)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="MTG | Musa The Giant">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{abs_url(og_img)}?v={OG_V}">
<meta property="og:image:secure_url" content="{abs_url(og_img)}?v={OG_V}">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{og_alt}">
<meta property="og:locale" content="en_ZA">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{abs_url(og_img)}?v={OG_V}">
<script type="application/ld+json">
{ld}
</script>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Anton&family=Manrope:wght@400;700;800&display=swap" rel="stylesheet">
{pre}
<link rel="stylesheet" href="{asset('assets/bellver.css', here)}">
{gc_snippet()}
</head>
<body{' class="is-dash"' if dash else ''}>
{shell(here, key, body, dash)}
</body>
</html>
'''


# ------------------------------------------------------------------ 10 REASONS (from MTG's "10 Reasons Why I Joined BellverCard", facts checked against the site)
REASONS = [
 ('wallet', 'Your keys', 'Self-custodial crypto spending',
  'Spend your crypto without handing it to anyone. Your USDT and USDC stay in your own Fireblocks wallet, protected by your private key. You move only what you need onto the card, when you need it.', 'how-it-works/', 'How your wallet works'),
 ('card', 'Today', 'Instant virtual or mailed physical card',
  'Choose a virtual Mastercard and start paying online and with your phone the same day, or a physical Visa delivered to your door ($85 shipping in Europe, $149 to the rest of the world).', 'prices/#levels', 'Virtual or physical'),
 ('tag', '$99', 'Pay once: $99 to $990',
  'A one-time card price, not a monthly subscription: Basic $99, Premium $270, Business $490 and the top Gold card at $990. Pick the limits you need.', 'prices/', 'Compare the four levels'),
 ('shield', '2 ways', 'With or without an identity check',
  'Complete a quick identity check (KYC) for the regular card, or order a card without the check for a surcharge. Once you are verified, you skip that surcharge.', 'get-started/#step-3', 'How ordering works'),
 ('bolt', '$250K', '$20,000 per payment, $250,000 a day',
  'Gold cards spend up to $20,000 per transaction and $250,000 a day, in any local currency. Even Basic gives you $1,000 a day.', 'prices/', 'See every limit'),
 ('nfc', 'Tap', 'Apple Pay, Google Pay and ATM cash',
  'Add the card to Apple Pay or Google Pay and pay with a tap, shop online, or withdraw cash at an ATM when you need it (2% ATM fee).', 'how-it-works/', 'How paying works'),
 ('users', 'Up to $500', '$10 to $500 per direct referral',
  'Earn a one-time commission each time someone orders through your link: $10 Basic, $100 Premium, $200 Business, $400 Gold, and up to $500 with the Special Edition. You do not even need your own card for this.', 'rewards/', 'The commission table'),
 ('coins', '0.1%', 'A share of the fees your network pays',
  'Every time a cardholder in your paid levels tops up their card, you earn 0.1% per level, paid from Bellver\'s top-up fee. That is $1 for every $1,000 loaded, month after month.', 'rewards/', 'How rewards are paid'),
 ('tree', '2x2', 'Spillover in the 2x2 matrix',
  'Only two seats sit under you. When the people above you refer more than two, the extras flow down into the next free seats, and some land under you. Nobody builds alone.', 'matrix/', 'See spillover in action'),
 ('star', 'Monthly', 'Monthly rewards that grow with your team',
  'As your matrix fills, your monthly rewards grow. Bellver\'s own full-matrix examples run from about $2,457 a month on 12 levels to $157,286 on 18 levels, with everyone loading $300. These are examples, not promises: early on, direct commissions are the bigger money.', 'rewards/#estimate', 'Run your own numbers'),
]
REASONS_SHORT = ['Your crypto stays in your own wallet, protected by your private key.',
 'Pay with a virtual card today, or get a physical Visa posted to you.',
 'A one-time card price, never a monthly subscription.',
 'Order with an identity check (KYC), or without one for a surcharge.',
 'Gold limits for big payments, and $1,000 a day even on Basic.',
 'Tap to pay with your phone, shop online, or draw cash at an ATM.',
 'A one-time commission each time someone orders through your link.',
 'Earn 0.1% per level when cardholders in your paid levels top up.',
 'Extra referrals from above flow down into free seats under you.',
 'Rewards grow as your matrix fills. Examples, never promises.']
REASONS_LEAD = ('More than 1,000 cards were sold in the testing phase alone, about half of them Business or Gold (as reported at launch). '
                'Here are the 10 reasons people keep choosing Bellver Card.')


def reasons_band(here, variant='full', title=None, lead=None, sid='why'):
    """MTG's 10 reasons, explained. 'full': numbered cards with a short explanation each. 'compact': numbered list linking to the full version on the home page."""
    title = title or 'Bellver Card in numbers: <em>10 reasons</em> people are joining'
    lead = lead or REASONS_LEAD
    home_why = (L('', here) + '#why') if variant != 'full' else '#why'
    if variant == 'full':
        items = ''.join(f'''<article class="why-card rv" style="--d:{(i % 2) * .06:.2f}s"><span class="why-n">{i + 1:02d}</span><span class="ped{' ped-gold' if i >= 6 else ''}" aria-hidden="true"><span class="ped-obj">{ic(icn)}</span></span>
   <span class="why-big">{big}</span><h3 class="h3">{t}</h3><p>{d}</p><a class="tlink" href="{L(href, here)}">{lab} {ic('arrow')}</a></article>''' for i, (icn, big, t, d, href, lab) in enumerate(REASONS))
        return f'''<section class="sec" id="{sid}" style="padding-top:0"><div class="wrap">
 <div class="sec-head rv"><span class="kicker"><i>{ic('users')}</i>Why people are joining</span><h2 class="h2">{title}</h2><p class="lead">{lead}</p></div>
 <div class="why-grid">{items}</div>
 <div class="why-cta rv"><div><b>Ready to see it for yourself?</b><span>Start with a virtual card from $99 and pay today, or watch the 3-minute video first.</span></div><div class="btn-row">{order_btn('Order your card')}<a class="btn btn-ghost" href="{L('videos/#overview', here)}">{ic('play')}Watch the 3-minute video</a></div></div>
 <p class="fine rv" style="margin-top:16px">Prices, limits and commissions from Bellver's official price list and compensation plan. Rewards depend on real card activity and are never guaranteed.</p>
</div></section>'''
    items = ''.join(f'<li><span class="why-n">{i + 1:02d}</span><span class="why-ic">{ic(icn)}</span><span class="why-t"><b>{t}</b><small>{REASONS_SHORT[i]}</small></span></li>' for i, (icn, big, t, d, href, lab) in enumerate(REASONS))
    return f'''<section class="sec-tight" id="{sid}"><div class="wrap">
 <div class="sec-head rv"><h2 class="h2">{title}</h2><p class="lead">{lead}</p></div>
 <ol class="why-list rv">{items}</ol>
 <p class="rv btn-row" style="margin-top:22px;gap:22px"><a class="tlink" href="{home_why}">Read all 10 reasons, explained {ic('arrow')}</a><a class="tlink" href="{L('explainers/#ten-reasons-explained', here)}">{ic('play')}Watch the 10 reasons explained</a></p>
</div></section>'''


def reasons_ld(page_url):
    return {"@type": "ItemList", "name": "10 reasons people are joining Bellver Card", "url": page_url + "#why", "numberOfItems": len(REASONS),
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": t, "description": d} for i, (icn, big, t, d, href, lab) in enumerate(REASONS)]}


from team_shell import *  # noqa  (team member versions of the shell: only used when PARTNER is set)


# ---------------------------------------------------------------- referral helpers (exchanges and traffic)
def aff(key):
    """MTG's referral links. MTG's rule (17 Oct 2026): these links appear ONLY on MTG's own pages, never on team or client pages."""
    if PARTNER is not None:
        return ''
    return {'valr': VALR, 'binance': BINANCE, 'clickbaitpays': CBP}[key]


def _href(u):
    return u.replace('&', '&amp;')


def exch_btns(cls='btn btn-ghost btn-sm'):
    out = ''
    if aff('valr'):
        out += f'<a class="{cls}" data-track="valr" href="{_href(aff("valr"))}" target="_blank" rel="sponsored noopener">{ic("swap")}Open a VALR account</a>'
    if aff('binance'):
        out += f'<a class="{cls}" data-track="binance" href="{_href(aff("binance"))}" target="_blank" rel="sponsored noopener">{ic("swap")}Open a Binance account</a>'
    return out


def exch_note(style=''):
    """'No exchange yet?' box with the two exchange buttons (generic advice only, if there are no links)."""
    b = exch_btns()
    tail = ('<div class="btn-row" style="margin-top:12px">' + b + '</div><p class="fine" style="margin-top:8px">Referral links: I may earn a small reward if you sign up, at no extra cost to you.</p>') if b else ''
    return (f'<div class="note exch rv"{(" style=" + chr(34) + style + chr(34)) if style else ""}>{ic("wallet")}<div><b>No exchange account yet?</b> Open one, buy USDT there, then send it to your Bellver wallet on BNB Smart Chain (BEP20). '
            f'VALR is the easy choice in South Africa, because you can deposit rand by EFT. Binance works in most other countries.{tail}</div></div>')


def exch_inline():
    """One sentence with inline links, for FAQ answers."""
    v, b = aff('valr'), aff('binance')
    if v and b:
        return (f'No exchange account yet? Open one with <a class="inl" href="{_href(v)}" target="_blank" rel="sponsored noopener">VALR</a> (easy in South Africa, deposit rand by EFT) '
                f'or <a class="inl" href="{_href(b)}" target="_blank" rel="sponsored noopener">Binance</a> (most other countries), buy USDT and send it on BNB Smart Chain.')
    return 'No exchange account yet? Open one on a trusted exchange in your country, buy USDT and send it on BNB Smart Chain.'


def cbp_section(here):
    """Partner page: gentle recommendation of ClickBaitPays as a traffic source for builders. Left out when there is no link."""
    u = aff('clickbaitpays')
    if not u:
        return ''
    return f'''<section class="sec-tight" id="traffic" data-title="More eyes on your link"><div class="wrap">
 <div class="panel cbp rv">
  <div class="cbp-tx">
   <span class="kick">{ic('rocket')}For builders</span>
   <h2 class="h2">Want more eyes on <em>your link?</em></h2>
   <p class="lead">A good link still needs people to see it. If you want to build your team a little faster, ClickBaitPays is the traffic source I recommend to builders.</p>
   <ul class="checks">
    <li>Put your page in front of active viewers with an Ad Campaign, or a $20 login ad that runs for 30 days.</li>
    <li>Send them to an honest page like this guide, so they can learn before they decide.</li>
    <li>Traffic creates opportunity, not certainty. Test your message and keep what works.</li>
   </ul>
   <div class="btn-row" style="margin-top:20px"><a class="btn btn-go" data-track="clickbaitpays" href="{_href(u)}" target="_blank" rel="sponsored noopener">See how ClickBaitPays traffic works{ic('arrow')}</a></div>
  </div>
  <div class="cbp-rule">
   <div class="note warn">{ic('alert')}<span><b>Bellver's rule first.</b> Public advertising and large campaigns need Bellver's prior approval. Ask Bellver support before you advertise your referral link, and never promise income.</span></div>
   <p class="fine">ClickBaitPays is a separate platform with its own rules, fees and risks. Nothing is guaranteed: learn how it works first. I may earn a referral reward if you join.</p>
  </div>
 </div>
</div></section>'''


def cbp_band(here, title='Building your matrix faster?'):
    """Compact reminder for builder pages (matrix, payback). Left out when there is no link."""
    u = aff('clickbaitpays')
    if not u:
        return ''
    return f'''<section class="sec-tight" data-title="More eyes on your link"><div class="wrap"><div class="note cbp-band rv">{ic('rocket')}<div><b>{title}</b> More people seeing your link means more chances to fill your seats. ClickBaitPays is the traffic source I recommend to builders, with $20 login ads and Ad Campaigns. Check <a class="inl" href="{L('partner/#traffic', here)}">Bellver's advertising rule</a> first.
<div class="btn-row" style="margin-top:12px"><a class="btn btn-ghost btn-sm" data-track="clickbaitpays" href="{_href(u)}" target="_blank" rel="sponsored noopener">Get more eyes on your link{ic('arrow')}</a></div></div></div></div></section>'''

