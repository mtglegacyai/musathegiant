# -*- coding: utf-8 -*-
"""Get started, Videos (hub + 3 pages), FAQ, Downloads."""
from bv import *  # noqa
from p_info import phero, T


# ------------------------------------------------------------------ GET STARTED
def start(H='get-started/'):
    trail = T(('Get Started', abs_url(H)))
    top = phero(H, trail, ['Order your card,', 'step by step'], 'From sign-up to your first payment in seven short steps. Keep this page open next to your dashboard and follow along.', None,
                order_btn('Open the registration page') + f'<a class="btn btn-ghost" href="{L("videos/dashboard-walkthrough/", H)}"><span class="play">{ic("play")}</span>Watch the dashboard tour</a>')
    S = [
     ('Register with MTG\'s link', f'''<p>Open <a class="inl" href="{REF}" target="_blank" rel="sponsored noopener">the registration page</a> and create your account. Using this link places you in my team, so I can see your sign-up and help you if you get stuck.</p><p>Your dashboard opens with a Fireblocks wallet already set up for you.</p>'''),
     ('Secure your account first', '''<ul><li>Go to <span class="path">Settings</span> and switch on the <b>authenticator app</b> for two-factor login.</li><li>Go to <span class="path">My Wallet › Settings › Account and security</span>, set a <b>transaction password</b>, then use <b>Export private key</b>.</li><li>Write the key down, store it offline and never share it. If you lose it, nobody can recover your funds.</li></ul>'''),
     ('Fund your wallet', '''<p>Open <span class="path">My Wallet › Deposit</span>.</p><ul><li><b>Best:</b> send USDT or USDC on BNB Smart Chain from any wallet or exchange.</li><li><b>Add gas:</b> send about $10 to $20 of BNB (or TRX if you use Tron) for network fees.</li><li><b>No crypto?</b> Use Buy crypto to pay by credit card, or SEPA and PayPal in Europe.</li></ul><p>The deposit page has a calculator that shows how much you need for your card. Add a little extra: it stays your money.</p>'''),
     ('Order your card', '''<p>Open <span class="path">My Cards</span> and choose:</p><ul><li>Your level: Basic, Premium, Business or Gold</li><li>Virtual (instant, no shipping) or physical Visa</li><li>Optional Special Edition (+$390) and your printed name (+$49)</li></ul><p>Pay from your wallet. Your new card can take a few minutes to appear. Once it does, you receive the next free place in the 2x2 matrix.</p>'''),
     ('Load it and pay', '''<p>Move the amount you want to spend from your wallet to your card. Then add the card to Apple Pay or Google Pay, or start paying online right away.</p><p>Remember the $100 monthly top-up if you want to receive rewards.</p>'''),
     ('Share your link, if you want to', '''<p>Your personal referral link sits at the top of your dashboard. Share it with people who would value the card. You earn a direct commission for every card ordered through it.</p><p>The easiest way: send them to a page like this one with the words "Take a look at the two videos, it's worth it."</p>'''),
     ('Get paid', '''<p>Your current month's commissions and rewards show in the green fields. On the 15th they move to <b>Earnings available</b>.</p><p>Open <span class="path">Withdraw</span>, enter the amount (minimum $100) and request it. It shows as pending, then arrives in My Wallet.</p>'''),
    ]
    steps = ''.join(f'<article class="gstep rv" id="step-{i+1}"><span class="gn">{i+1}</span><div><h2>{t}</h2>{b}</div></article>' for i, (t, b) in enumerate(S))
    body = top + f'''<section class="sec-tight"><div class="wrap"><div class="split guide-split">
 <div class="guide">{steps}</div>
 <aside class="rv" style="position:sticky;top:96px;display:grid;gap:16px">
  <figure class="media" style="margin:0"><img src="{L('images/bellver-card-dashboard-login.webp', H)}" alt="Bellver Card dashboard login page with username and password fields" width="1024" height="933" loading="lazy"><figcaption class="cap">Already registered? Log in at app.bellvercards.com</figcaption></figure>
  <div class="box"><h3 class="h3">Before you start</h3><ul><li>A phone with an authenticator app</li><li>USDT or USDC, or a credit card</li><li>A little BNB or TRX for gas</li><li>Pen and paper for your private key</li></ul><div class="btn-row" style="margin-top:18px">{order_btn('Register now', 'btn btn-go btn-sm')}<a class="btn btn-ghost btn-sm" href="{LOGIN}" target="_blank" rel="noopener">Member login</a></div></div>
 </aside>
</div></div></section>''' + help_band(H) + final_cta(H)
    howto = {"@type": "HowTo", "name": "How to order a Bellver Card", "totalTime": "PT20M",
             "supply": [{"@type": "HowToSupply", "name": "USDT or USDC"}, {"@type": "HowToSupply", "name": "BNB or TRX for gas fees"}],
             "step": [{"@type": "HowToStep", "position": i + 1, "name": t, "url": abs_url(H) + f"#step-{i+1}"} for i, (t, _) in enumerate(S)]}
    return page(H, 'start', 'How to Order a Bellver Card: Step-by-Step Setup Guide | MTG',
                'Order your Bellver Card in seven steps: register, secure your account, fund your Fireblocks wallet with USDT or USDC, choose your card, load it, share your link and withdraw.',
                'images/og/og-bellver-get-started.jpg', 'How to order a Bellver Card step by step', body, ld_extra=[howto], trail=trail)


# ------------------------------------------------------------------ VIDEOS
VIDS = [
 ('v3', 'Bellver Card in 3 minutes', 'Quick overview', '3:31', 'mp4', MP4_3MIN, 'images/bellver-card-3-minute-video-thumbnail', 'The fastest way to understand the card: limits, privacy, physical and virtual cards, and how two referrals open the rewards program.', None, 'PT3M31S'),
 ('v27', 'Bellver Card explained in 27 minutes', 'Full presentation', '27 min', 'yt', YT_27, 'images/bellver-card-explained-27-minutes-thumbnail', 'The complete presentation: the Fireblocks wallet, funding, all four levels, the 2x2 matrix, ranks and the $100 monthly rule.', 'videos/bellver-card-explained/', None),
 ('vd', 'Bellver dashboard walkthrough', 'Back office tour', '11:53', 'mp4', MP4_DASH, 'images/bellver-card-dashboard-walkthrough-thumbnail', 'A guided tour of your back office: every coloured field, your wallet, deposits, withdrawals, cards and the referral area.', 'videos/dashboard-walkthrough/', 'PT11M53S'),
 ('vw', 'Bellver Card launch webinar', 'Launch webinar', 'Full length', 'yt', YT_WEBINAR, 'images/bellver-card-launch-webinar-thumbnail', 'The English launch webinar with the founder and the head of operations in Singapore: the story, the partners, early numbers and the roadmap.', 'videos/launch-webinar/', None),
]


def player(v, H, eager=False):
    vid, title, kind, dur, typ, src, img, desc, link, iso = v
    data = f'data-yt="{src}"' if typ == 'yt' else f'data-src="{L(src, H)}"'
    lab = f'{dur} on YouTube' if typ == 'yt' and dur != 'Full length' else (f'Watch on YouTube' if typ == 'yt' else dur)
    load = '' if eager else ' loading="lazy"'
    return f'''<div class="player" id="{vid}" role="button" tabindex="0" aria-label="Play: {title}" {data} data-title="{title}">
 <img src="{L(img + '-640.webp', H)}" srcset="{L(img + '-640.webp', H)} 640w, {L(img + '.webp', H)} 1280w" sizes="(max-width:860px) 100vw, 760px" alt="{title}, video thumbnail" width="1280" height="720"{load}>
 <span class="pbtn">{ic('play')}</span><span class="plabel">{lab}</span></div>'''


def videos(H='videos/'):
    trail = T(('Videos', abs_url(H)))
    top = phero(H, trail, ['Watch &', 'learn'], 'Four official Bellver videos, from a 3-minute overview to a full tour of your dashboard. Each longer video has its own page with a short written summary.')
    tiles = ''
    for i, v in enumerate(VIDS):
        link = f'<a class="tlink" href="{L(v[8], H)}">Read the summary {ic("arrow")}</a>' if v[8] else f'<a class="tlink" href="{L("", H)}#watch">Also on the home page {ic("arrow")}</a>'
        tiles += f'<article class="vtile rv" style="--d:{(i%2)*0.08:.2f}s">{player(v, H, i < 2)}<div class="txt"><span class="badge green" style="margin-bottom:10px">{v[2]}, {v[3]}</span><h2>{v[1]}</h2><p>{v[7]}</p>{link}</div></article>'
    body = top + f'<section class="sec-tight"><div class="wrap"><div class="vhub">{tiles}</div><p class="vnote rv" style="margin-top:18px">Official Bellver videos. Parts of the voice-over and graphics were created with AI.</p></div></section>' + help_band(H) + final_cta(H)
    ld = [video_ld(v) for v in VIDS]
    return page(H, 'videos', 'Bellver Card Videos: Overview, Full Presentation and Dashboard Tour | MTG',
                'Watch the official Bellver Card videos in English: the 3-minute overview, the 27-minute presentation, the dashboard walkthrough and the launch webinar, with written summaries.',
                'images/og/og-bellver-videos.jpg', 'Bellver Card videos', body, ld_extra=ld, trail=trail)


def video_ld(v):
    vid, title, kind, dur, typ, src, img, desc, link, iso = v
    d = {"@type": "VideoObject", "name": title, "description": desc, "thumbnailUrl": abs_url(img + '.webp'), "inLanguage": "en"}
    if typ == 'yt':
        d["embedUrl"] = f"https://www.youtube.com/embed/{src}"
    else:
        d["contentUrl"] = abs_url(src); d["uploadDate"] = "2026-10-06"
    if iso: d["duration"] = iso
    if link: d["url"] = abs_url(link)
    return d


def vpage(H, v, key_title, desc, og, lines, lead, sections, extra_ld=None):
    trail = T(('Videos', abs_url('videos/')), (v[1], abs_url(H)))
    top = phero(H, trail, lines, lead)
    body = top + f'''<section class="sec-tight" style="padding-top:0"><div class="wrap" style="max-width:980px">{player(v, H, True)}<p class="vnote" style="margin-top:12px">Official Bellver video. Parts of the voice-over and graphics may have been created with AI.</p></div></section>''' + sections + help_band(H) + final_cta(H)
    return page(H, 'videos', key_title, desc, og, v[1], body, ld_extra=[video_ld(v)] + (extra_ld or []), trail=trail)


def v_explained(H='videos/bellver-card-explained/'):
    v = VIDS[1]
    s = f'''<section class="sec-tight"><div class="wrap split" style="align-items:start">
 <div class="prose rv">
  <h2>The short version</h2>
  <p>Bellver calls it the world's first network card: a crypto-funded card you spend like any other, with a rewards program that pays you a share of card fees when people you recommend use their cards.</p>
  <h3>What you will learn</h3>
  <ul>
   <li>Why your money sits in your own Fireblocks wallet, not on the card</li>
   <li>Every way to fund it: USDT and USDC first, other crypto, credit card, SEPA and PayPal</li>
   <li>Physical Visa vs virtual card, Apple Pay, Google Pay and NFC rings</li>
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
 <div class="box warn rv" style="--d:.1s;position:sticky;top:96px">
  <div class="ico">{ic('alert')}</div><h3 class="h3">A fair reading of the numbers</h3>
  <p>The video's monthly examples ($2,457, about $20,000 and $157,286) assume every matrix place is filled and every cardholder loads $300 a month. A full 12 levels is 8,190 cardholders. Bellver also says even 5% of the top example would be a good income. Treat these as illustrations, not forecasts.</p>
  <p><a class="inl" href="{L('rewards/#estimate', H)}">Run your own numbers</a></p>
 </div>
</div></section>'''
    return vpage(H, v, 'Bellver Card Explained in 27 Minutes: Video and Summary | MTG',
                 'Watch the official 27-minute Bellver Card presentation and read a clear summary: Fireblocks wallet, funding, card levels, the 2x2 matrix, ranks and the $100 monthly rule.',
                 'images/og/og-bellver-video-explained.jpg', ['Explained in', '27 minutes'],
                 'The complete official presentation of the Bellver Card. Watch it below, or read the summary if you are short on time.', s)


def v_dashboard(H='videos/dashboard-walkthrough/'):
    v = VIDS[2]
    F = [('#fcbe25', 'Yellow: wallet balance', 'Your USDT and USDC balance in your dynamic wallet. Other coins are not shown here. You pay for cards from this balance.'),
         ('#21c06c', 'Green: this month\'s earnings', 'Direct commissions and rewards earned in the current billing month.'),
         ('#e5484d', 'Red: missed rewards', 'Rewards you did not receive because you were not qualified in time. Ideally always zero.'),
         ('#1aa3d1', 'Blue: card balance', 'The money currently on your card, or on all your cards combined.'),
         ('#8a96a0', 'Grey: lifetime totals', 'Everything you have ever earned in commissions and rewards.'),
         ('#3b6fd6', 'Dark blue: earnings available', 'Once a month the green fields move here, ready to withdraw. Payout day is the 15th.')]
    lg = ''.join(f'<div class="lg rv"><i style="background:{c}"></i><div><b>{t}</b><span>{d}</span></div></div>' for c, t, d in F)
    s = f'''<section class="sec-tight"><div class="wrap">
 <div class="sec-head rv"><h2 class="h2">What the <em>colours</em> mean</h2><p class="lead">The top of your dashboard shows your rank, your referral link, your qualified levels and your team's card users and deposits. Below that, six colour-coded fields.</p></div>
 <div class="legend">{lg}</div>
</div></section>
<section class="sec-tight"><div class="wrap split" style="align-items:start">
 <div class="prose rv">
  <h2>Menu by menu</h2>
  <h3>My Wallet</h3><p>Your Fireblocks wallet: swap currencies, send funds anywhere, set a transaction password and export your private key under Settings, then Account and security. "The dynamic wallet is essentially your own bank."</p>
  <h3>Deposit</h3><p>Fund with crypto (USDT or USDC recommended, plus BNB or TRX for gas), credit card, or SEPA and PayPal in Europe. A calculator shows how much you need for your card.</p>
  <h3>Withdraw</h3><p>Request payouts of $100 or more. They show as pending, then appear in My Wallet.</p>
  <h3>My Cards</h3><p>Order cards and see each card's balance and transactions. When your card appears you get the next free place in the 2x2 matrix.</p>
  <h3>Referral</h3><p>Your growing matrix, your direct referrals, people per level, the card levels and ranks in your team, and a visual of your first levels, including spillover.</p>
  <h3>Videos, PDFs, Support, Notifications, Settings</h3><p>Presentations, the price list and compensation plan, help requests, confirmations and news from Bellver, and two-factor authentication, which Bellver strongly recommends.</p>
 </div>
 <div class="rv" style="--d:.1s;position:sticky;top:96px;display:grid;gap:16px">
  <div class="note g">{ic('info')}<span><b>Numbers not showing yet?</b> Transactions can appear with a short delay when volume is high. Wait a few minutes, refresh, or log out and back in.</span></div>
  <div class="note">{ic('key')}<span><b>Buy your card before you share your link.</b> You still earn the commission either way, but only cardholders are placed in your matrix.</span></div>
  <a class="btn btn-ghost" href="{LOGIN}" target="_blank" rel="noopener">{ic('login')}Open the member login</a>
 </div>
</div></section>'''
    return vpage(H, v, 'Bellver Card Dashboard Walkthrough: Video and Guide | MTG',
                 'Tour the Bellver Card back office: what each coloured field means, how to deposit, withdraw, order cards, secure your wallet and read your 2x2 matrix.',
                 'images/og/og-bellver-video-dashboard.jpg', ['Dashboard', 'walkthrough'],
                 'A 12-minute tour of the Bellver back office. Watch it once after you register and you will know where everything is.', s)


def v_webinar(H='videos/launch-webinar/'):
    v = VIDS[3]
    road = [('Sep 2026', 'Testing phase from 9 September, then the official launch of version 1.0'), ('Jan 2027', 'Version 2.0 of the platform'), ('Mar 2027', 'NFC rings and other products in the shop'),
            ('May 2027', 'Platinum unlimited metal card with extra benefits'), ('Jun 2027', 'Bellver\'s own app'), ('Oct 2027', 'Plans for Bellver\'s own licence'), ('Dec 2027', 'Version 3.0')]
    rd = ''.join(f'<tr><td><b>{d}</b></td><td>{t}</td></tr>' for d, t in road)
    s = f'''<section class="sec-tight"><div class="wrap split" style="align-items:start">
 <div class="prose rv">
  <h2>What was said</h2>
  <h3>An honest start</h3><p>The founder opened by calling the launch version 1.0: "good, but not perfect". The platform had taken about ten months to build, small problems were still being fixed, and he advised anyone expecting perfection to wait for later versions.</p>
  <h3>Why he built it</h3><p>He had used the card himself for four to five years. The goal was a real product rather than an investment, so nobody would be left behind having lost money.</p>
  <h3>The partners</h3><p>The head of operations in Singapore explained the choice of card provider: licensed by the Monetary Authority of Singapore, serving major banks and businesses. Wallets use Fireblocks' dynamic wallet, which lets users export their own private keys. His advice: keep funds in your wallet and only top up the card with what you need.</p>
  <h3>The fees, openly</h3><p>Both speakers said the card's fees are higher than a normal bank card, because the top-up is the only place commissions can be funded. If you only want a cheap card, they said, your bank's card may suit you better.</p>
  <h3>Early numbers, as reported at launch</h3><p>Over 1,000 cards sold during testing, about half Business or Gold and 40% Premium, around $210,000 in pending commissions, and the first commissions already paid on 15 September.</p>
 </div>
 <div class="rv" style="--d:.1s;position:sticky;top:96px">
  <h2 class="h2" style="font-size:2rem;margin-bottom:14px">Announced <em>roadmap</em></h2>
  <div class="tbl-wrap"><table class="tbl" style="min-width:0"><tbody>{rd}</tbody></table></div>
  <p class="fine">Plans as presented at launch, not promises. Dates may change.</p>
 </div>
</div></section>'''
    return vpage(H, v, 'Bellver Card Launch Webinar: Video, Partners and Roadmap | MTG',
                 'The English Bellver Card launch webinar summarised: why it was built, the Singapore card provider and Fireblocks wallet, open talk about fees, early numbers and the 2027 roadmap.',
                 'images/og/og-bellver-video-webinar.jpg', ['Launch', 'webinar'],
                 'The full English launch webinar with the founder and the head of operations in Singapore. Here is what matters, in two minutes of reading.', s)


# ------------------------------------------------------------------ FAQ
FAQ = [
 ('The card', [
  ('What is the Bellver Card?', 'A crypto-funded payment card, physical Visa or virtual, with a US dollar account. Bellver calls it the world\'s first network card because it also has an optional rewards program. It is a product of Bellver Markets Ltd.'),
  ('How much does it cost?', 'A one-time $99 (Basic), $270 (Premium), $490 (Business) or $990 (Gold). Add-ons: Special Edition +$390, printed name +$49. Physical cards add shipping: $85 Europe, $149 rest of world.'),
  ('Is there a monthly or annual fee?', 'The official price list shows no monthly or annual card fee. You pay usage fees: 4.95% when you top up the card, 1.75% per transaction and 2% for ATM withdrawals.'),
  ('What are the daily and per-transaction limits?', 'Basic $1,000 a day and $500 per transaction. Premium $10,000 and $5,000. Business $50,000 and $10,000. Gold $250,000 and $20,000.'),
  ('Physical or virtual: which should I choose?', 'Virtual if you want to start today: no shipping wait, no shipping fee, and it works with Apple Pay, Google Pay and NFC rings. Choose physical if you need cash from ATMs.'),
  ('Can I use it with Apple Pay and Google Pay?', 'Yes. You can also connect it to an NFC ring or wristband and pay with a tap.'),
  ('Where can I use it?', 'Worldwide, in shops and online, in any local currency. The card account itself is in US dollars.'),
  ('How long does the physical card take to arrive?', 'Bellver\'s terms allow up to four weeks. At launch, early users reported receiving their cards in about five days.'),
  ('Can I upgrade later?', 'Yes, at any time. You pay only the difference and keep the same card. Note that monthly rewards are not back-dated to before your upgrade.'),
  ('What is the Special Edition?', 'A $390 add-on for any level that Bellver positions as its highest level of security and privacy, available physical or virtual. Bellver has said it may not be offered forever. Ask MTG for the details before you choose it.'),
 ]),
 ('Money and security', [
  ('Do I need crypto to get one?', 'No, but it is the cheapest route. Card balances use USDT or USDC. Without crypto you can buy it by credit card inside the dashboard, and in Europe pay by SEPA bank transfer or PayPal.'),
  ('Which coins and networks can I deposit?', 'USDT and USDC on BNB Smart Chain (recommended), Tron or Ethereum. Bitcoin, Ethereum, BNB, Solana and others are accepted too, but must be swapped to USDT or USDC before you top up the card.'),
  ('What is the gas fee and how much do I need?', 'A small network fee paid in the chain\'s own coin: BNB on BNB Smart Chain, TRX on Tron. About $10 to $20 worth is enough to start.'),
  ('Who controls my money?', 'You. Deposits go to your own non-custodial Fireblocks wallet protected by your private key. Bellver cannot freeze or access it. You can export the key at any time. If you lose it, nobody can recover your funds.'),
  ('Where is the card registered?', 'In Singapore. At launch Bellver said its card provider is licensed by the Monetary Authority of Singapore. Bellver Markets Ltd, the company running the program, is based in Malta.'),
  ('Is this an investment?', 'No. Bellver presents it as a product: a payment card. The card price and fees are real costs, and rewards depend entirely on real card activity in your matrix.'),
 ]),
 ('Rewards', [
  ('Do I have to refer anyone?', 'No. The rewards program is optional. If you do want to take part, two referrals who order a card are enough to qualify.'),
  ('How much do I earn per referral?', 'A one-time commission of $10 for Basic, $100 for Premium, $200 for Business or $400 for Gold. With the Special Edition: $150, $300 or $500. Upgrades pay an extra 50% of the new level\'s commission.'),
  ('How do monthly rewards work?', '0.1% of every completed card top-up by cardholders in your 2x2 matrix, on each level you qualify for: up to 12 levels with Premium, 15 with Business and 18 to 20 with Gold, depending on your star rank.'),
  ('What do I need to stay qualified?', 'Top up your own card with at least $100 every month. Miss a month and that month\'s rewards are forfeited. Miss three months in a row and you permanently lose your matrix position.'),
  ('When and how am I paid?', 'In USDT. Direct commissions arrive within seven business days of the payment. Monthly rewards are paid on the 15th. The minimum withdrawal is $100.'),
  ('Is income guaranteed?', 'No. Bellver\'s own examples state they are not a guarantee of income. What you earn depends on how many cardholders are placed in your levels and how much they load.'),
 ]),
 ('Getting help', [
  ('How do I get help ordering?', f'Message MTG on WhatsApp for personal help, or use the Support area inside your Bellver dashboard. The <a class="inl" href="{{GS}}">step-by-step guide</a> covers the whole process.'),
  ('Where do I log in?', f'At app.bellvercards.com/login. The Member login link is in the menu on every page of this site.'),
 ]),
]

GLOSSARY = [
 ('Non-custodial wallet', 'A wallet where only you hold the private key. No company can freeze or move your funds.'),
 ('Fireblocks dynamic wallet', 'The wallet technology behind every Bellver account. It lets you export your own private key.'),
 ('Private key', 'The secret that controls your wallet. Lose it and the funds cannot be recovered.'),
 ('USDT and USDC', 'Stablecoins worth one US dollar each. Card balances run on them.'),
 ('BNB Smart Chain', 'The recommended network for sending USDT or USDC: fast and low-cost.'),
 ('Gas fee', 'The small network fee for sending tokens, paid in BNB, TRX or ETH depending on the chain.'),
 ('Top-up (deposit)', 'Moving money onto your card balance. Carries a 4.95% fee and is what rewards are calculated on.'),
 ('Direct commission', 'A one-time payment for each card ordered through your referral link.'),
 ('Rewards', 'Your monthly 0.1% share of top-ups by cardholders on your qualified levels.'),
 ('2x2 matrix', 'Your team structure: two places under each person, filled top to bottom, left to right.'),
 ('Spillover', 'Extra referrals from you or your upline that fill the next free places in your matrix.'),
 ('Star rank', 'Your qualification level, from 1 to 5 stars. Higher ranks unlock deeper reward levels.'),
 ('Settlement day', 'The 15th of each month, when the previous month\'s rewards become available to withdraw.'),
 ('NFC', 'Near-field communication: the contactless tech that lets a phone, ring or wristband pay at a terminal.'),
]


def faq(H='faq/'):
    trail = T(('FAQ & Glossary', abs_url(H)))
    top = phero(H, trail, ['Questions,', 'answered'], 'Straight answers taken from Bellver\'s official price list, compensation plan and presentations. Plus a plain-words glossary at the end.')
    blocks = ''; ld_q = []
    for gi, (g, qs) in enumerate(FAQ):
        items = ''
        for q, a in qs:
            a2 = a.replace('{GS}', L('get-started/', H))
            items += f'<details class="qa"><summary>{q}<span class="pm" aria-hidden="true"></span></summary><div class="ans"><p>{a2}</p></div></details>'
            ld_q.append({"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": __import__('re').sub('<[^>]+>', '', a2)}})
        blocks += f'<div class="faq-cols" style="margin-bottom:56px"><div class="sticky rv"><h2 class="h2" style="font-size:clamp(1.8rem,3.4vw,2.6rem)">{g}</h2></div><div class="faq rv">{items}</div></div>'
    gl = ''.join(f'<div class="lg rv"><i style="background:linear-gradient(135deg,var(--green),#0d4f2f)"></i><div><b>{t}</b><span>{d}</span></div></div>' for t, d in GLOSSARY)
    body = top + f'''<section class="sec-tight"><div class="wrap">{blocks}</div></section>
<section class="sec-tight" id="glossary"><div class="wrap"><div class="sec-head rv"><h2 class="h2">Glossary</h2><p class="lead">The words you will meet in the dashboard and the videos.</p></div><div class="legend">{gl}</div></div></section>''' + help_band(H, 'Question not here?', 'Ask me on WhatsApp. I read every message and I will answer you personally.') + final_cta(H)
    dt = [{"@type": "DefinedTermSet", "name": "Bellver Card glossary", "hasDefinedTerm": [{"@type": "DefinedTerm", "name": t, "description": d} for t, d in GLOSSARY]}]
    return page(H, 'faq', 'Bellver Card FAQ: Fees, Limits, Wallet and Rewards Answered | MTG',
                'Answers to common Bellver Card questions: cost, monthly fees, limits, funding with crypto, who controls your money, Apple Pay, upgrades, rewards, payouts, plus a glossary.',
                'images/og/og-bellver-faq.jpg', 'Bellver Card frequently asked questions', body,
                ld_extra=[{"@type": "FAQPage", "mainEntity": ld_q}] + dt, trail=trail)


# ------------------------------------------------------------------ DOWNLOADS
DOCS = [
 ('bellver-card-price-list.pdf', 'images/bellver-card-price-list-preview.webp', 'Price list', 'All four levels, limits, shipping, upgrades, add-ons and transaction fees on one page.', '1 page, 2.3 MB'),
 ('bellver-card-compensation-plan.pdf', 'images/bellver-card-compensation-plan-preview.webp', 'Compensation plan', 'Commissions, monthly rewards, the six ranks and the qualification rules.', '1 page, 0.4 MB'),
 ('bellver-card-presentation.pdf', 'images/bellver-card-presentation-preview.webp', 'Presentation slides', 'The official 20-slide presentation, ideal for sharing or presenting the card yourself.', '20 slides, 8.8 MB'),
]


def downloads(H='downloads/'):
    trail = T(('Downloads', abs_url(H)))
    top = phero(H, trail, ['Official', 'downloads'], 'Bellver\'s official documents, version 08/2026. Save them, share them, or keep them open while you order.')
    cards = ''
    for i, (f, img, t, d, m) in enumerate(DOCS):
        cards += f'''<article class="doc rv" style="--d:{i*0.08:.2f}s"><div class="thumb"><img src="{L(img, H)}" alt="Bellver Card {t.lower()} PDF, first page" width="800" height="600" loading="lazy"><span class="ext">PDF</span></div>
 <div class="body"><h2>{t}</h2><p>{d}</p><span class="meta">{m}</span><a class="btn btn-ghost" href="{L('downloads/' + f, H)}" download>{ic('download')}Download</a></div></article>'''
    body = top + f'<section class="sec-tight"><div class="wrap"><div class="dl">{cards}</div><p class="fine rv" style="margin-top:18px">These documents form part of Bellver Markets\' terms and conditions and can be updated by Bellver at any time. The newest versions are always in the PDFs section of your dashboard.</p></div></section>' + help_band(H) + final_cta(H)
    return page(H, 'downloads', 'Bellver Card PDF Downloads: Price List, Compensation Plan, Slides | MTG',
                'Download the official Bellver Card price list, compensation plan and 20-slide presentation (version 08/2026) as PDFs.',
                'images/og/og-bellver-downloads.jpg', 'Bellver Card official downloads', body, trail=trail)
