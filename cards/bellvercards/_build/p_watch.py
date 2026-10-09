# -*- coding: utf-8 -*-
"""Overview (learn/), Presentation Videos, Tutorial Videos, Documents."""
from bv import *  # noqa
from p_info import phero, T

# (id, title, kind, duration label, type, source, thumb, description, iso duration)
PRES = [
 ('overview', 'Bellver Card in 3 minutes', 'Quick overview', '3 min', 'mp4', MP4_3MIN, 'images/bellver-card-3-minute-video-thumbnail',
  'The fastest way to understand the card: limits, privacy, physical and virtual cards, and how two referrals open the rewards program.', 'PT3M31S'),
 ('explained', 'Bellver Card explained in 27 minutes', 'Full presentation', '27 min', 'yt', YT_27, 'images/bellver-card-explained-27-minutes-thumbnail',
  'The complete presentation: the Fireblocks wallet, funding, all four levels, the 2x2 matrix, ranks and the $100 monthly rule.', None),
 ('webinar', 'Bellver Card launch webinar', 'Launch webinar', 'Full talk', 'yt', YT_WEBINAR, 'images/bellver-card-launch-webinar-thumbnail',
  'The English launch webinar with the founder and the head of operations in Singapore: the story, the partners, early numbers and the roadmap.', None),
]
WALK = ('walk', 'Bellver dashboard walkthrough', 'Back office tour', '11:53', 'mp4', MP4_DASH, 'images/bellver-card-dashboard-walkthrough-thumbnail',
        'A guided tour of the Bellver back office: every coloured field, your wallet, deposits, withdrawals, cards and the referral area.', 'PT11M53S')

# Tutorial placeholders. Upload an MP4 with exactly this name into cards/bellvercards/videos/tutorials/
# and the matching tile switches from "Coming soon" to a playable video by itself.
TUTS = [
 ('01-register-and-secure-your-account.mp4', 'Register and secure your account', 'Sign up with MTG\'s link, switch on two-factor login and save your private key.', 'login', 1),
 ('02-fund-your-wallet-and-order-your-card.mp4', 'Fund your wallet and order your card', 'Deposit USDT or USDC, choose your level and pay from your wallet.', 'card', 3),
 ('03-top-up-and-pay-with-your-phone.mp4', 'Top up and pay with your phone', 'Load your card, add it to Apple Pay or Google Pay and start paying.', 'nfc', 5),
]


def live_thumb(v, H, local_suffix, w, h, load, alt):
    """Webinar only: pull the thumbnail straight from YouTube so it always matches the video; fall back to the local copy."""
    vid, typ, src, img = v[0], v[4], v[5], v[6]
    if vid != 'webinar' or typ != 'yt':
        return None
    local = L(img + local_suffix, H)
    onerr = "this.onerror=null;this.src='" + local + "'"
    return (f'<img src="https://i.ytimg.com/vi/{src}/maxresdefault.jpg" alt="{alt}" width="{w}" height="{h}"{load} '
            f'referrerpolicy="no-referrer" onerror="{onerr}">')


def pplayer(v, H, eager=False, more=None):
    vid, title, kind, dur, typ, src, img, desc, iso = v
    data = f'data-yt="{src}"' if typ == 'yt' else f'data-src="{L(src, H)}"'
    m = f' data-more="{more}"' if more else ''
    load = '' if eager else ' loading="lazy"'
    pimg = live_thumb(v, H, '.webp', 1280, 720, load, title + ', video thumbnail') or (
        f'<img src="{L(img + "-640.webp", H)}" srcset="{L(img + "-640.webp", H)} 640w, {L(img + ".webp", H)} 1280w" sizes="(max-width:860px) 100vw, 820px" alt="{title}, video thumbnail" width="1280" height="720"{load}>')
    return f'''<div class="player" id="p-{vid}" role="button" tabindex="0" aria-label="Play: {title}" {data} data-title="{title}"{m}>
{pimg}
 <span class="pbtn">{ic('play')}</span><span class="plabel">{dur}</span></div>'''


def vld(v, page_path):
    vid, title, kind, dur, typ, src, img, desc, iso = v
    d = {"@type": "VideoObject", "name": title, "description": desc, "thumbnailUrl": (f"https://i.ytimg.com/vi/{src}/maxresdefault.jpg" if vid == "webinar" else abs_url(img + ".webp")), "inLanguage": "en", "url": abs_url(page_path) + '#' + vid}
    if typ == 'yt':
        d["embedUrl"] = f"https://www.youtube.com/embed/{src}"
    else:
        d["contentUrl"] = abs_url(src); d["uploadDate"] = "2026-10-06"
    if iso:
        d["duration"] = iso
    return d


# ------------------------------------------------------------------ PRESENTATION VIDEOS
def videos(H='videos/'):
    trail = T(('Presentation Videos', abs_url(H)))
    top = phero(H, trail, ['Presentation', 'videos'], 'Bellver\'s official presentations in one place. Pick a video from the list, press play, and read the short summary underneath.')

    s_overview = f'''<div class="split vsum">
 <div class="prose">
  <h3>What you will hear</h3>
  <ul>
   <li>A US dollar card account you can spend worldwide in any local currency</li>
   <li>Limits up to $250,000 a day and $20,000 per payment on Gold</li>
   <li>A physical Visa or a virtual Mastercard, with Apple Pay and Google Pay</li>
   <li>Four levels: Basic, Premium, Business and Gold. Most people choose Business</li>
   <li>Own Premium or higher and recommend it to two people who also choose Premium or higher to qualify for monthly rewards</li>
  </ul>
 </div>
 <div class="box"><div class="ico">{ic('info')}</div><h3 class="h3">Next step</h3><p>Liked what you saw? The 27-minute presentation covers every detail, or jump straight to <a class="inl" href="{L('prices/', H)}">prices and limits</a>.</p></div>
</div>'''
    s_explained = f'''<div class="split vsum">
 <div class="prose">
  <h3>What you will learn</h3>
  <ul>
   <li>Why your money sits in your own Fireblocks wallet, not on the card</li>
   <li>Every way to fund it: USDT and USDC first, other crypto, credit card, SEPA and PayPal</li>
   <li>Physical vs virtual card, Apple Pay, Google Pay and NFC rings</li>
   <li>The four levels, their limits and their prices</li>
   <li>How the 2x2 matrix fills itself with spillover</li>
   <li>The star ranks that unlock 12, 15 or 18 levels of rewards</li>
   <li>The one catch: a $100 minimum monthly top-up to qualify for rewards</li>
  </ul>
  <h3>Three ideas worth remembering</h3>
  <p><b>Earn like a bank.</b> Banks earn small fees on every transaction. Bellver shares part of its fees with cardholders instead of spending on advertising.</p>
  <p><b>Premium is where rewards start.</b> Basic only earns direct commissions. Bellver recommends Premium at minimum, and says most people pick Business.</p>
  <p><b>Your card can cost nothing.</b> Buy Business, refer three Business cardholders and the commissions cover your card.</p>
 </div>
 <div class="box warn"><div class="ico">{ic('alert')}</div><h3 class="h3">A fair reading of the numbers</h3>
  <p>The video's monthly examples ($2,457, about $20,000 and $157,286) assume every matrix place is filled and every cardholder loads $300 a month. A full 12 levels is 8,190 cardholders. Treat these as illustrations, not forecasts.</p>
  <p>This video was recorded before Bellver's October 2026 update, so its 4.95% top-up fee, $390 Special Edition and Premium rank step have since changed. <a class="inl" href="{L('learn/#bellver-news', H)}">See what changed</a>.</p>
  <p><a class="inl" href="{L('rewards/#estimate', H)}">Run your own numbers</a></p></div>
</div>'''
    road = [('Sep 2026', 'Testing phase from 9 September, then the official launch of version 1.0'), ('End of 2026', 'Dashboard version 2.0, in development as announced in October 2026'), ('Jan 2027', 'Version 2.0 of the platform'), ('Mar 2027', 'NFC rings and other products in the shop'),
            ('May 2027', 'Platinum unlimited metal card with extra benefits'), ('Jun 2027', 'Bellver\'s own app'), ('Oct 2027', 'Plans for Bellver\'s own licence'), ('Dec 2027', 'Version 3.0')]
    rd = ''.join(f'<tr><td><b>{d}</b></td><td>{t}</td></tr>' for d, t in road)
    s_webinar = f'''<div class="split vsum">
 <div class="prose">
  <h3>An honest start</h3><p>The founder opened by calling the launch version 1.0: "good, but not perfect". The platform had taken about ten months to build, small problems were still being fixed, and he advised anyone expecting perfection to wait for later versions.</p>
  <h3>Why he built it</h3><p>He had used the card himself for four to five years. The goal was a real product rather than an investment, so nobody would be left behind having lost money.</p>
  <h3>The partners</h3><p>The head of operations in Singapore explained the choice of card provider: licensed by the Monetary Authority of Singapore, serving major banks and businesses. Wallets use Fireblocks' dynamic wallet, which lets users export their own private keys. His advice: keep funds in your wallet and only top up the card with what you need.</p>
  <h3>The fees, openly</h3><p>Both speakers said the card's fees are higher than a normal bank card, because the top-up is the only place commissions can be funded. If you only want a cheap card, they said, your bank's card may suit you better.</p>
  <h3>Early numbers, as reported at launch</h3><p>Over 1,000 cards sold during testing, about half Business or Gold and 40% Premium, around $210,000 in pending commissions, and the first commissions already paid on 15 September.</p>
 </div>
 <div><h3 class="h3" style="margin-bottom:12px">Announced roadmap</h3><div class="tbl-wrap"><table class="tbl" style="min-width:0"><tbody>{rd}</tbody></table></div><p class="fine">Plans as presented at launch, plus Bellver's October 2026 update. Not promises. Dates may change.</p></div>
</div>'''
    sums = {'overview': s_overview, 'explained': s_explained, 'webinar': s_webinar}

    panels = ''; items = ''
    for i, v in enumerate(PRES):
        vid, title, kind, dur, typ, src, img, desc, iso = v
        panels += f'''<article class="vpanel" id="{vid}" data-panel="{vid}" aria-labelledby="t-{vid}">
  {pplayer(v, H, i == 0)}
  <div class="vhead"><span class="badge green">{kind}, {dur}</span><h2 id="t-{vid}">{title}</h2><p class="muted">{desc}</p></div>
  {sums[vid]}
 </article>'''
        lthumb = live_thumb(v, H, '-640.webp', 640, 360, ' loading="lazy"', '') or f'<img src="{L(img + "-640.webp", H)}" alt="" width="640" height="360" loading="lazy">'
        items += f'''<button class="vitem" type="button" data-show="{vid}" aria-controls="{vid}"{' aria-current="true"' if i == 0 else ''}>
  <span class="vthumb">{lthumb}<span class="vdur">{dur}</span></span>
  <span class="vtx"><b>{title}</b><small>{kind}</small></span></button>'''
    lib = f'''<section class="sec-tight" style="padding-top:0"><div class="wrap">
 <div class="vlib">
  <div class="vstage">{panels}</div>
  <aside class="vlist" aria-label="Choose a video"><p class="slabel">Playlist</p>{items}
   <a class="vtut" href="{L('tutorials/', H)}">{ic('play-c')}<span><b>Looking for how-to videos?</b><small>Open the tutorial videos</small></span></a>
  </aside>
 </div>
 <p class="vnote" style="margin-top:16px">Official Bellver videos. Parts of the voice-over and graphics were created with AI.</p>
</div></section>'''
    body = top + lib + help_band(H)
    return page(H, 'videos', 'Bellver Card Presentation Videos: 3 Minute, 27 Minute and Launch Webinar | MTG',
                'Watch the official Bellver Card presentations in English: the 3-minute overview, the 27-minute presentation and the launch webinar, each with a short written summary.',
                'images/og/og-bellver-videos.jpg', 'Bellver Card presentation videos', body, ld_extra=[vld(v, H) for v in PRES], trail=trail)


# ------------------------------------------------------------------ TUTORIAL VIDEOS
def tutorials(H='tutorials/'):
    trail = T(('Tutorial Videos', abs_url(H)))
    top = phero(H, trail, ['Tutorial', 'videos'], 'Short step-by-step videos that show you exactly where to click. Pick a video from the playlist, press play, and follow along. New tutorials appear here as soon as they are ready.')
    F = [('#fcbe25', 'Yellow: wallet balance', 'Your USDT and USDC balance in your dynamic wallet. Other coins are not shown here. You pay for cards from this balance.'),
         ('#21c06c', 'Green: this month\'s earnings', 'Direct commissions and rewards earned in the current billing month.'),
         ('#e5484d', 'Red: missed rewards', 'Rewards you did not receive because you were not qualified in time. Ideally always zero.'),
         ('#1aa3d1', 'Blue: card balance', 'The money currently on your card, or on all your cards combined.'),
         ('#8a96a0', 'Grey: lifetime totals', 'Everything you have ever earned in commissions and rewards.'),
         ('#3b6fd6', 'Dark blue: earnings available', 'Once a month the green fields move here, ready to withdraw. Payout day is the 15th.')]
    lg = ''.join(f'<div class="lg"><i style="background:{c}"></i><div><b>{t}</b><span>{d}</span></div></div>' for c, t, d in F)
    walk_det = f'''<details class="qa more"><summary>What each coloured field means<span class="pm" aria-hidden="true"></span></summary><div class="ans"><div class="legend">{lg}</div></div></details>
  <details class="qa more"><summary>Menu by menu<span class="pm" aria-hidden="true"></span></summary><div class="ans prose">
   <p><b>My Wallet:</b> your Fireblocks wallet. Swap currencies, send funds, set a transaction password and export your private key under Settings, then Account and security.</p>
   <p><b>Deposit:</b> fund with crypto (USDT or USDC recommended, plus BNB or TRX for gas), credit card, or SEPA and PayPal in Europe. A calculator shows how much you need.</p>
   <p><b>Withdraw:</b> request payouts of $100 or more. They show as pending, then appear in My Wallet.</p>
   <p><b>My Cards:</b> order cards and see each card's balance and transactions. When your card appears you get the next free place in the 2x2 matrix.</p>
   <p><b>Referral:</b> your matrix, direct referrals, people per level, card levels and ranks in your team, including spillover.</p>
   <p><b>Settings:</b> switch on two-factor authentication. Bellver strongly recommends it.</p>
  </div></details>'''
    vid, title, kind, dur, typ, src, img, desc, iso = WALK
    panels = f'''<article class="vpanel" id="walkthrough" data-panel="walkthrough" aria-labelledby="t-walkthrough">
  {pplayer(WALK, H, True)}
  <div class="vhead"><span class="badge green">{ic('star')}Start here, {dur}</span><h2 id="t-walkthrough">Dashboard <em>walkthrough</em></h2><p class="muted">Watch this once after you register and you will know where everything is in your back office.</p></div>
  <div class="vsum-d">{walk_det}</div>
 </article>'''
    items = f'''<button class="vitem" type="button" data-show="walkthrough" aria-controls="walkthrough" aria-current="true">
  <span class="vthumb"><img src="{L(img + "-640.webp", H)}" alt="" width="640" height="360" loading="lazy"><span class="vdur">{dur}</span></span>
  <span class="vtx"><b>{title}</b><small>Start here, back office tour</small></span></button>'''
    for i, (f, t, d, icn, step) in enumerate(TUTS):
        n = f[:2]
        panels += f'''<article class="vpanel" id="tut-{n}" data-panel="tut-{n}" aria-labelledby="t-tut-{n}">
  <div class="player tplayer soon" data-wait="{L('videos/tutorials/' + f, H)}" data-title="{t}">
   <div class="tposter"><span class="tnum">{n}</span><span class="tic">{ic(icn)}</span></div>
   <span class="pbtn">{ic('play')}</span><span class="plabel">Coming soon</span>
  </div>
  <div class="vhead"><span class="badge green">Tutorial {i + 1} of {len(TUTS)}</span><h2 id="t-tut-{n}">{t}</h2><p class="muted">{d}</p><p class="vwait"><a class="tlink" href="{L('get-started/#step-' + str(step), H)}">Read the written steps {ic('arrow')}</a></p></div>
 </article>'''
        items += f'''<button class="vitem" type="button" data-show="tut-{n}" aria-controls="tut-{n}">
  <span class="vthumb"><span class="tposter"><span class="tnum">{n}</span><span class="tic">{ic(icn)}</span></span><span class="vdur">Soon</span></span>
  <span class="vtx"><b>{t}</b><small>Tutorial {i + 1}</small></span></button>'''
    lib = f'''<section class="sec-tight" style="padding-top:0"><div class="wrap">
 <div class="vlib">
  <div class="vstage">{panels}</div>
  <aside class="vlist" aria-label="Choose a video"><p class="slabel">Playlist</p>{items}
   <a class="vtut" href="{L('videos/', H)}">{ic('play-c')}<span><b>Looking for the presentations?</b><small>Open the presentation videos</small></span></a>
  </aside>
 </div>
</div></section>'''
    body = top + lib + help_band(H, 'Need a tutorial that is not here?', 'Tell me what you are stuck on and I will make a video for it, or walk you through it on WhatsApp.')
    return page(H, 'tutorials', 'Bellver Card Tutorial Videos: Step-by-Step How-To Guides | MTG',
                'Step-by-step Bellver Card tutorial videos: the dashboard walkthrough, registering, securing your account, depositing USDT, ordering a virtual card, topping up and withdrawing.',
                'images/og/og-bellver-tutorials.jpg', 'Bellver Card tutorial videos', body, ld_extra=[vld(WALK, H)], trail=trail)


# ------------------------------------------------------------------ OVERVIEW
MORE = {
 'start': 'Seven short steps from sign-up to your first payment, with matching tutorial videos.',
 'how': 'Where your money sits, how it reaches the card, physical vs virtual, and who is behind Bellver.',
 'prices': 'All four levels side by side, every published fee, add-ons, shipping and upgrades.',
 'rewards': 'Direct commissions, the 2x2 matrix, the six ranks and the rules for staying qualified.',
 'partner': 'Who it suits, what you earn, a first-week plan and the honest way to share the card.',
 'videos': 'The 3-minute overview, the 27-minute presentation and the launch webinar, with summaries.',
 'tutorials': 'The dashboard walkthrough plus short how-to videos for every step.',
 'faq': 'Two dozen straight answers and a plain-words glossary.',
 'docs': 'The official price list, compensation plan and presentation slides as PDFs.',
}


def learn(H='learn/'):
    trail = T(('Card guide', abs_url(H)))
    top = phero(H, trail, ['Your Bellver', 'card guide'], 'Everything you need before and after you order, in one place. New here? Start with How It Works. Ready to go? Follow Get Started.', None,
                f'<a class="btn btn-go" href="{L("how-it-works/", H)}">{ic("layers")}Start with How It Works</a><a class="btn btn-ghost" href="{L("get-started/", H)}">{ic("rocket")}I am ready to order</a>')
    facts = f'''<section class="sec-tight" style="padding-top:0"><div class="wrap"><div class="facts rv" style="margin-top:0">
  <div class="fact"><span class="ic">{ic('tag')}</span><div><b>From $99</b><span>one-time, four levels</span></div></div>
  <div class="fact"><span class="ic">{ic('bolt')}</span><div><b>Up to $250,000</b><span>daily limit on Gold</span></div></div>
  <div class="fact"><span class="ic">{ic('key')}</span><div><b>Your own key</b><span>non-custodial wallet</span></div></div>
  <div class="fact"><span class="ic">{ic('gift')}</span><div><b>Two referrals</b><span>Premium or higher, for rewards</span></div></div>
 </div></div></section>'''
    tiles = ''
    for i, (k, path, label, sub, icn, g) in enumerate([n for n in NAV if n[0] != 'learn']):
        tiles += f'''<a class="gtile rv" href="{L(path, H)}" style="--d:{(i % 4) * 0.05:.2f}s"><span class="gic">{ic(icn)}</span><span class="gg">{g}</span><b>{label}</b><p>{MORE[k]}</p><span class="go">Open {ic('arrow')}</span></a>'''
    grid = f'''<section class="sec-tight"><div class="wrap"><div class="sec-head rv"><h2 class="h2">Everything <em>inside</em></h2></div><div class="ggrid">{tiles}</div></div></section>'''
    docs = f'''<section class="sec-tight"><div class="wrap"><div class="panel docband rv">
  <div><h2 class="h3" style="font-size:1.3rem">Official documents</h2><p class="muted" style="margin:4px 0 0">Version 08/2026, straight from Bellver. Save them or share them.</p></div>
  <div class="btn-row">{dl_btn('price', H, 'Price list')}{dl_btn('plan', H, 'Compensation plan')}{dl_btn('slides', H, 'Presentation')}</div>
 </div></div></section>'''
    body = top + facts + news_band(H) + audience_band(H) + grid + docs + help_band(H)
    return page(H, 'learn', 'Bellver Card Guide: Everything About the Card in One Place | MTG',
                'Your complete Bellver Card guide by MTG: how it works, prices and fees, the rewards program, a setup guide, presentation and tutorial videos, FAQ and official PDFs.',
                'images/og/og-bellver-guide.jpg', 'Bellver Card guide by MTG', body, trail=trail)


# ------------------------------------------------------------------ DOCUMENTS
DOCS = [
 ('price', 'images/bellver-card-price-list-preview.webp', 'Price list', 'All four levels, limits, shipping, upgrades, add-ons and transaction fees on one page.', '1 page, 2.3 MB'),
 ('plan', 'images/bellver-card-compensation-plan-preview.webp', 'Compensation plan', 'Commissions, monthly rewards, the six ranks and the qualification rules.', '1 page, 0.4 MB'),
 ('slides', 'images/bellver-card-presentation-preview.webp', 'Presentation slides', 'The official 20-slide presentation, ideal for sharing or presenting the card yourself.', '20 slides, 8.8 MB'),
]


def docs(H='docs/'):
    trail = T(('Documents', abs_url(H)))
    top = phero(H, trail, ['Official', 'documents'], 'Bellver\'s official documents, version 08/2026. Open them in your browser, save them, or share them with someone you are introducing to the card.')
    cards = ''
    for i, (k, img, t, d, m) in enumerate(DOCS):
        href = L(DOCS_PDF[k], H)
        cards += f'''<article class="doc rv" style="--d:{i*0.08:.2f}s"><a class="thumb" href="{href}" target="_blank" rel="noopener"><img src="{L(img, H)}" alt="Bellver Card {t.lower()} PDF, first page" width="800" height="600" loading="lazy"><span class="ext">PDF</span></a>
 <div class="body"><h2>{t}</h2><p>{d}</p><span class="meta">{m}</span><div class="btn-row" style="margin-top:auto;gap:8px"><a class="btn btn-ghost btn-sm" href="{href}" download>{ic('download')}Download</a><a class="btn btn-ghost btn-sm" href="{href}" target="_blank" rel="noopener">{ic('eye')}Open</a></div></div></article>'''
    body = top + f'<section class="sec-tight" style="padding-top:0"><div class="wrap"><div class="dl">{cards}</div><p class="fine rv" style="margin-top:18px">These documents form part of Bellver Markets\' terms and conditions and can be updated by Bellver at any time. The newest versions are always in the PDFs section of your Bellver back office.</p></div></section>' + help_band(H)
    ld = [{"@type": "DigitalDocument", "name": f"Bellver Card {t}", "encodingFormat": "application/pdf", "url": abs_url(DOCS_PDF[k])} for k, img, t, d, m in DOCS]
    return page(H, 'docs', 'Bellver Card PDF Documents: Price List, Compensation Plan, Slides | MTG',
                'Download the official Bellver Card price list, compensation plan and 20-slide presentation (version 08/2026) as PDFs.',
                'images/og/og-bellver-downloads.jpg', 'Bellver Card official documents', body, ld_extra=ld, trail=trail)
