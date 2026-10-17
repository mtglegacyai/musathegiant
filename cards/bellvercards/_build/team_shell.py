# -*- coding: utf-8 -*-
"""Team pages: the shell pieces (header, menu, footer, help band, page head) for a business partner's copy of the guide.
Only used when bv.PARTNER is set by configure(). MTG's own pages never touch this file.

Rules (MTG, Oct 2026):
 - only the links a partner gave appear: no link, no icon, no button, never MTG's as a fallback
 - slogan on every team page: The Card That Can Pay Your Bills (none of MTG's slogans)
 - nothing on a team page leads to MTG's referral link, socials or website
 - videos and PDFs are shared exactly as they are
"""
import json, urllib.parse
import re
import bv

__all__ = ['configure', 'team_header', 'team_sidebar', 'team_footer', 'team_dash_footer', 'team_help_band', 'team_page',
           'SLOGAN', 'NOWA', 'socials', 'TEAM_DIR', 'MTG_ASSETS']

SLOGAN = 'The Card That Can Pay Your Bills'
NOWA = 'https://no-whatsapp.invalid/'      # placeholder for "partner gave no WhatsApp": every link to it is removed after the build
TEAM_DIR = '/bellvercards/'                # team pages live at /bellvercards/<slug>/ (later: their own domain)
MTG_ASSETS = '/cards/bellvercards/'        # shared images, styles, scripts, videos and PDFs

# small brand icons for the socials a partner may give (24x24, filled)
SOCIAL_ICONS = {
 'telegram': '<path d="M21.6 3.4 2.9 10.6c-1.3.5-1.3 1.2-.2 1.6l4.8 1.5 1.8 5.6c.2.6.4.8.9.8.4 0 .6-.2.9-.5l2.3-2.2 4.8 3.5c.9.5 1.5.2 1.7-.8l3.1-14.7c.3-1.3-.5-1.9-1.4-1.5ZM9.8 14.4l-.4 4 -1.4-4.6 10.1-6.4-8.3 7Z" fill="currentColor" stroke="none"/>',
 'tiktok': '<path d="M16.6 2h-3.3v13.4a2.9 2.9 0 1 1-2.9-2.9c.3 0 .6 0 .9.1V9.2a6.2 6.2 0 1 0 5.3 6.2V8.6a7.8 7.8 0 0 0 4.4 1.4V6.7a4.4 4.4 0 0 1-4.4-4.7Z" fill="currentColor" stroke="none"/>',
 'facebook': '<path d="M13.6 21.5v-8h2.7l.4-3.2h-3.1V8.3c0-.9.3-1.5 1.6-1.5h1.6V3.9c-.3 0-1.3-.1-2.4-.1-2.4 0-4 1.5-4 4.1v2.4H7.7v3.2h2.7v8h3.2Z" fill="currentColor" stroke="none"/>',
 'instagram': '<rect x="3.5" y="3.5" width="17" height="17" rx="4.5"/><circle cx="12" cy="12" r="3.8"/><circle cx="17.2" cy="6.8" r=".6" fill="currentColor"/>',
 'youtube': '<path d="M21.6 7.2a2.6 2.6 0 0 0-1.8-1.8C18.2 5 12 5 12 5s-6.2 0-7.8.4A2.6 2.6 0 0 0 2.4 7.2 27 27 0 0 0 2 12a27 27 0 0 0 .4 4.8 2.6 2.6 0 0 0 1.8 1.8C5.8 19 12 19 12 19s6.2 0 7.8-.4a2.6 2.6 0 0 0 1.8-1.8A27 27 0 0 0 22 12a27 27 0 0 0-.4-4.8ZM10 15V9l5.2 3L10 15Z" fill="currentColor" stroke="none"/>',
 'x': '<path d="M17.8 3h3.1l-6.8 7.8 8 10.6h-6.3l-4.9-6.4-5.6 6.4H2.2l7.3-8.3L1.8 3h6.4l4.4 5.9L17.8 3Zm-1.1 16.5h1.7L7.4 4.8H5.6l11.1 14.7Z" fill="currentColor" stroke="none"/>',
}
SOCIAL_LABELS = {'telegram': 'Telegram', 'tiktok': 'TikTok', 'facebook': 'Facebook', 'instagram': 'Instagram', 'youtube': 'YouTube', 'x': 'X'}


def _open_all(html):
    """Team pages open every section straight away (William's request, 16 Oct 2026; default for all team pages).
    A member can keep MTG's tap-to-open sections with "open_all_sections": false in team.json."""
    want = '99' if MEMBER_OPTS.get('open_all_sections', True) else '2'
    html = re.sub(r'<main id="main" data-open="\d+">', f'<main id="main" data-open="{want}">', html, count=1)
    return html



def team_clean_url():
    """Keep the address bar clean on team pages (William's request, 16 Oct 2026): no #section, ?tracking
    or #:~:text= after the page has opened, and the home page shows exactly .../bellvercards/<name>.
    Links that point at a section or video still work; only the address bar is tidied afterwards."""
    home = bv.BASE  # e.g. /bellvercards/william/
    return ('''<script>(function(){try{var H=history,rs=H.replaceState.bind(H),ps=H.pushState.bind(H),HOME="%s";
function clean(){var p=location.pathname;if(p===HOME||p===HOME+"index.html")p=HOME.slice(0,-1);return p;}
H.replaceState=function(s,t){return rs(s,t,clean());};H.pushState=function(s,t){return ps(s,t,clean());};
function tidy(){if(location.pathname+location.search+location.hash!==clean()||location.href.indexOf("#")>=0)rs(H.state,"",clean());}
if(!location.hash)tidy();addEventListener("DOMContentLoaded",function(){setTimeout(tidy,300);});addEventListener("load",function(){setTimeout(tidy,300);});addEventListener("pageshow",function(e){if(e.persisted)tidy();});
addEventListener("hashchange",function(){setTimeout(tidy,60);});}catch(e){}})();</script>''' % home)


MEMBER_OPTS = {}


def configure(p):
    """Point every shared link at this partner. Call before the page modules are imported."""
    bv.PARTNER = p
    MEMBER_OPTS.clear(); MEMBER_OPTS.update(p)
    bv.BASE = TEAM_DIR + p['slug'] + '/'
    bv.ASSET_BASE = MTG_ASSETS
    bv.REF = p['ref']
    for k, v in SOCIAL_ICONS.items():
        bv.I.setdefault(k, v)
    first = p.get('short') or p['name'].split()[0]
    digits = ''.join(ch for ch in (p.get('whatsapp') or '') if ch.isdigit())
    if digits:
        wa = 'https://wa.me/' + digits
        q = lambda t: wa + '?text=' + urllib.parse.quote(t, safe='')
        bv.WA = wa
        bv.WA_MSG = q(f'Hi {first}, I am interested in the Bellver Card. Can you help me get started?')
        bv.PARTNER_MSG = q(f'Hi {first}, I have a question about the Bellver Card.')
        bv.CHECKLIST_MSG = bv.WA_MSG
    else:
        bv.WA = bv.WA_MSG = bv.PARTNER_MSG = bv.CHECKLIST_MSG = NOWA
    bv.PERSON = person()


def first():
    return bv.PARTNER.get('short') or bv.PARTNER['name'].split()[0]


def socials():
    """(key, label, url) for every link the partner actually gave, WhatsApp first."""
    p = bv.PARTNER; out = []
    if bv.WA != NOWA:
        out.append(('wa', 'WhatsApp ' + first(), bv.WA_MSG))
    if p.get('whatsapp_group'):
        out.append(('users', 'WhatsApp group', p['whatsapp_group']))
    for k, lab in SOCIAL_LABELS.items():
        if p.get(k):
            out.append((k, lab, p[k]))
    return out


def photo_url(here=''):
    p = bv.PARTNER
    return (bv.BASE + p['photo'] + '.webp') if p.get('photo') else ''


def person():
    p = bv.PARTNER
    d = {"@type": "Person", "@id": bv.SITE + bv.BASE + "#partner", "name": p['name'], "url": bv.SITE + bv.BASE}
    if p.get('photo'):
        d["image"] = bv.SITE + bv.BASE + p['photo'] + '.jpg'
    same = [p[k] for k in SOCIAL_LABELS if p.get(k)]
    if same:
        d["sameAs"] = same
    return d


def team_header(here, key):
    L, ic, order_btn = bv.L, bv.ic, bv.order_btn
    return f'''<a class="skip" href="#main">Skip to content</a>
<div class="progress" aria-hidden="true"></div>
<header class="hdr">
 <div class="wrap hdr-in">
  <a class="brand" href="{L('', here)}" aria-label="Bellver Cards by {bv.PARTNER['name']}, home">
   <img src="{L('images/bellver-cards-logo-white-360.webp', here)}" alt="Bellver Card logo" width="360" height="106">
   <span class="by">Bellver Cards<b>by <span class="aff-l">Affiliate</span><abbr class="aff-s" title="Affiliate">AFF</abbr> {first()}</b></span>
  </a>
  <div class="hdr-act">
   <a class="btn btn-ghost btn-sm learn-btn" href="{L('learn/', here)}">{ic('book')}Learn more</a>
   {order_btn('Order your card', 'btn btn-go btn-sm')}
  </div>
 </div>
</header>'''


def team_sidebar(here, key):
    L, ic, order_btn = bv.L, bv.ic, bv.order_btn
    groups = []; cur_g = None; items = ''
    for k, path, label, sub, icn, g in bv.NAV:
        if g != cur_g:
            if cur_g is not None:
                groups.append((cur_g, items))
            cur_g, items = g, ''
        on = ' aria-current="page"' if k == key else ''
        items += f'<a class="snav" href="{L(path, here)}"{on}><span class="ic">{ic(icn)}</span><span class="tx"><b>{label}</b><small>{sub}</small></span></a>'
    groups.append((cur_g, items))
    nav = ''.join(f'<div class="sgroup"><p class="slabel">{g}</p>{it}</div>' for g, it in groups)
    links = [f'<a class="slink" href="{bv.LOGIN}" target="_blank" rel="noopener">{ic("login")}Member Login</a>',
             f'<a class="slink" href="{bv.REF}" target="_blank" rel="sponsored noopener">{ic("home")}Bellver Home</a>']
    short = {'wa': 'WhatsApp', 'users': 'Join group'}   # the menu is narrow: short labels, full names in the footer
    links += [f'<a class="slink" href="{u}" target="_blank" rel="noopener" aria-label="{lab}">{ic(k)}{short.get(k, lab)}</a>' for k, lab, u in socials()]
    rows = ''.join(f'<div class="srow">{"".join(links[i:i + 2])}</div>' for i in range(0, len(links), 2))
    return f'''<aside class="side" id="bv-menu" aria-label="Bellver Card guide">
 <div class="side-top">
  <a class="sbrand" href="{L('', here)}" aria-label="Bellver Cards home"><img src="{L('images/bellver-cards-logo-white-360.webp', here)}" alt="Bellver Card logo" width="360" height="106"></a>
  <span class="sby">Card guide by Affiliate {bv.PARTNER['name']}</span>
 </div>
 <nav class="snavs">{nav}</nav>
 <div class="side-bot">
  {order_btn('Order your card', 'btn btn-go btn-sm sorder')}
  {rows}
 </div>
</aside>
<button class="side-toggle" type="button" aria-controls="bv-menu" aria-expanded="true" aria-label="Collapse menu" title="Collapse menu">{ic('chev-l')}</button>
<div class="scrim" aria-hidden="true"></div>'''


def disclaimer(where='guide'):
    n = bv.PARTNER['name']
    return (f'Bellver Card is a product of Bellver Markets Ltd. This {where} is shared independently by {n} and is not the official Bellver website or back office. '
            f'Order buttons link to app.bellvercards.com with {first()}\'s referral code, so {first()} may earn a commission if you order, at no extra cost to you. '
            'Prices, fees and the compensation plan come from Bellver\'s official documents (version 08/2026) and can change. '
            'Rewards depend on real card activity and are never guaranteed. Nothing here is financial, tax or legal advice.')


def bottom():
    return f'<div class="ftr-bot"><span>© <span data-year>2026</span> {bv.PARTNER["name"]}</span><span class="sig">{SLOGAN}</span></div>'


def team_dash_footer(here):
    return f'''<footer class="dfoot"><div class="wrap">
  <div class="disc">{disclaimer('guide')}</div>
  {bottom()}
 </div></footer>'''


def team_footer(here):
    L, ic = bv.L, bv.ic
    cols = [
     ('The card', [('Overview', 'learn/'), ('How It Works', 'how-it-works/'), ('Prices & Limits', 'prices/'), ('Rewards Program', 'rewards/'), ('2x2 Matrix Explained', 'matrix/'), ('Get Started', 'get-started/')]),
     ('Learn', [('Presentation Videos', 'videos/'), ('Tutorial Videos', 'tutorials/'), ('FAQ & Glossary', 'faq/'), ('Documents', 'docs/')]),
    ]
    html = ''
    for t, items in cols:
        lis = ''.join(f'<li><a href="{L(p, here)}">{n}</a></li>' for n, p in items)
        html += f'<div><h3>{t}</h3><ul>{lis}</ul></div>'
    soc = socials()
    if soc:
        lis = ''.join(f'<li><a href="{u}" target="_blank" rel="noopener">{lab}</a></li>' for k, lab, u in soc)
        html += f'<div><h3>Contact {first()}</h3><ul>{lis}</ul></div>'
    return f'''<footer class="ftr">
 <div class="wrap">
  <div class="ftr-top">
   <div class="logo"><img src="{L('images/bellver-cards-logo-white-360.webp', here)}" alt="Bellver Card logo" width="360" height="106" loading="lazy">
    <p class="tag">THE CARD THAT CAN <em>PAY YOUR BILLS</em></p>
    <p>An independent Bellver Card guide shared by {bv.PARTNER['name']}. Clear facts, honest numbers and personal help to get you started.</p>
   </div>
   {html}
  </div>
  <div class="disc">{disclaimer('site')}</div>
  {bottom()}
 </div>
</footer>
<a class="mobile-cta" href="{bv.REF}" target="_blank" rel="sponsored noopener" aria-hidden="true" tabindex="-1"><span class="btn btn-go">Order your Bellver Card</span></a>
<button class="totop" type="button" aria-label="Back to top"><svg class="ring" viewBox="0 0 54 54" aria-hidden="true"><circle class="bg" cx="27" cy="27" r="25"/><circle class="fg" cx="27" cy="27" r="25"/></svg>{ic('up','arr')}</button>
<script src="{bv.asset('assets/bellver.js', here)}" defer></script>'''


def team_help_band(here, title="Stuck? I'll walk you through it."):
    ic = bv.ic; p = bv.PARTNER
    has_wa = bv.WA != NOWA; grp = p.get('whatsapp_group')
    if not has_wa and not grp:
        return ''
    btns = ''
    if has_wa:
        btns += f'<a class="btn btn-wa" href="{bv.WA_MSG}" target="_blank" rel="noopener">{ic("wa")}WhatsApp {first()}</a>'
    if grp:
        btns += f'<a class="btn btn-ghost" href="{grp}" target="_blank" rel="noopener">{ic("users")}Join my WhatsApp group</a>'
    if has_wa:
        text = f"I'm {first()}. Message me on WhatsApp and I'll help you register, fund your wallet and choose the right card for you."
    else:
        text = f"I'm {first()}. Join my WhatsApp group to ask questions and learn alongside other cardholders."
    face = (f'<div class="face"><img src="{photo_url(here)}" alt="{p["name"]}" width="88" height="88" loading="lazy"></div>' if p.get('photo')
            else f'<div class="face team-initials" aria-hidden="true">{"".join(w[0] for w in p["name"].split()[:2]).upper()}</div>')
    return f'''<section class="sec-tight"><div class="wrap"><div class="panel help rv">
  {face}
  <div><h2>{title}</h2><p>{text}</p></div>
  <div class="team-btns">{btns}</div>
 </div></div></section>'''


TEAM_CSS = '''<style>
.side .srow{grid-template-columns:repeat(2,minmax(0,1fr))}
.team-btns{display:flex;flex-direction:column;gap:12px;align-items:stretch}
.team-btns .btn{justify-content:center}
.team-initials{display:grid;place-items:center;border-radius:50%;background:rgba(52,176,112,.16);border:2px solid rgba(252,190,37,.6);color:#fff;font:400 1.9rem/1 var(--display)}
@media (max-width:760px){.help .team-btns{grid-column:1/-1;flex-direction:row;flex-wrap:wrap}}
</style>'''


def team_page(here, key, title, desc, og_img, og_alt, body, ld_extra, trail, preload, dash):
    p = bv.PARTNER; SITE = bv.SITE
    url = bv.abs_url(here)
    title = title.replace(' | MTG', ' | ' + p['name'])
    og = SITE + bv.BASE + 'og/' + og_img.rsplit('/', 1)[-1] + '?v=' + bv.OG_V
    trail = trail or [('Bellver Cards', SITE + bv.BASE)]
    graph = [{"@type": "WebPage", "@id": url + "#page", "url": url, "name": title, "description": desc, "inLanguage": "en",
              "author": {"@id": SITE + bv.BASE + "#partner"}, "dateModified": bv.UPDATED,
              "primaryImageOfPage": {"@type": "ImageObject", "url": og}, "breadcrumb": bv.crumbs_ld(trail)},
             bv.PERSON]
    graph += (ld_extra or [])
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)
    pre = f'<link rel="preload" as="image" href="{bv.L(preload, here)}" fetchpriority="high">' if preload else ''
    site_name = 'Bellver Card guide by ' + p['name']
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<script>document.documentElement.classList.add('js')</script>
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="noindex,follow">
<link rel="canonical" href="{url}">
<meta name="author" content="{p['name']}">
<meta name="theme-color" content="#020c06">
<link rel="icon" type="image/svg+xml" href="{TEAM_DIR}favicon.svg">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{site_name}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og}">
<meta property="og:image:secure_url" content="{og}">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{og_alt}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{og}">
<script type="application/ld+json">
{ld}
</script>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Anton&family=Manrope:wght@400;700;800&display=swap" rel="stylesheet">
{pre}
<link rel="stylesheet" href="{bv.asset('assets/bellver.css', here)}">
{TEAM_CSS}
{team_clean_url()}
</head>
<body{' class="is-dash"' if dash else ''}>
{_open_all(bv.shell(here, key, body, dash))}
</body>
</html>
'''
