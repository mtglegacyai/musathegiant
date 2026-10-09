# -*- coding: utf-8 -*-
"""Get started, Videos (hub + 3 pages), FAQ, Downloads."""
from bv import *  # noqa
from p_info import phero, T


# ------------------------------------------------------------------ GET STARTED
def start(H='get-started/'):
    trail = T(('Get Started', abs_url(H)))
    top = phero(H, trail, ['Order your card,', 'step by step'], 'From sign-up to your first payment in seven short steps. Keep this page open next to your dashboard and follow along.', None,
                order_btn('Open the registration page') + f'<a class="btn btn-ghost" href="{L("tutorials/#walkthrough", H)}"><span class="play">{ic("play")}</span>Watch the dashboard tour</a>')
    S = [
     ('Register with MTG\'s link', f'''<p>Open <a class="inl" href="{REF}" target="_blank" rel="sponsored noopener">the registration page</a> and create your account. Using this link places you in my team, so I can see your sign-up and help you if you get stuck.</p><p>Your dashboard opens with a Fireblocks wallet already set up for you.</p>'''),
     ('Secure your account first', '''<ul><li>Go to <span class="path">Settings</span> and switch on the <b>authenticator app</b> for two-factor login.</li><li>Go to <span class="path">My Wallet › Settings › Account and security</span>, set a <b>transaction password</b>, then use <b>Export private key</b>.</li><li>Write the key down, store it offline and never share it. If you lose it, nobody can recover your funds.</li><li>Change your password today and switch on <b>two-factor login or a passkey</b>. Bellver never emails links to its login page, so ignore any message that sends you to one. Type app.bellvercards.com yourself or use your bookmark.</li><li>You may see an extra access code on <span class="path">My Wallet</span> and <span class="path">My Cards</span>. Bellver added it temporarily after three phishing incidents and said it would be removed in 7 days.</li></ul>'''),
     ('Fund your wallet', '''<p>Open <span class="path">My Wallet › Deposit</span>.</p><ul><li><b>Best:</b> send USDT or USDC on BNB Smart Chain from any wallet or exchange.</li><li><b>Add gas:</b> send about $10 to $20 of BNB (or TRX if you use Tron) for network fees.</li><li><b>No crypto?</b> Use Buy crypto to pay by credit card, or SEPA and PayPal in Europe.</li></ul><p>The deposit page has a calculator that shows how much you need for your card. Add a little extra: it stays your money.</p>'''),
     ('Order your card', '''<p>Open <span class="path">My Cards</span> and choose:</p><ul><li>Your level: Basic, Premium, Business or Gold</li><li>Virtual (instant, no shipping, Mastercard) or physical (Visa)</li><li>Optional Special Edition (+$370 when you buy, or $470 to upgrade a regular card you already own) and your printed name (+$49)</li><li>Physical card? Enter a <b>complete, accurate shipping address</b> and a <b>valid mobile number from the delivery country</b>. The courier uses it, and without both your card cannot be delivered.</li></ul><p>Pay from your wallet. Your new card can take a few minutes to appear. Once it does, you receive the next free place in the 2x2 matrix.</p>'''),
     ('Load it and pay', '''<p>Move the amount you want to spend from your wallet to your card. Then add the card to Apple Pay or Google Pay, or start paying online right away.</p><p>If you want to receive rewards, load at least $100 onto your card each month. It is not a fee. It is your own money to spend.</p>'''),
     ('Share your link, if you want to', '''<p>Sharing is entirely optional, and you do not need a card of your own to earn direct commissions: Bellver pays them on personal referrals in all cases. Your personal referral link sits at the top of your dashboard. Share it with people who would value the card. You earn a direct commission for every card ordered through it.</p><p>Keep it honest: large-scale campaigns or public advertising on social media need Bellver's prior approval, and false or misleading statements or income promises can lead to suspension.</p><p>The easiest way: send them to a page like this one with the words "Take a look at the two videos, it's worth it."</p><p>Going live on TikTok? Show the card working, say that you earn a commission, and read <a class="inl" href="{L("partner/#tiktok", H)}">the rules for sharing it on TikTok</a> first.</p>'''),
     ('Get paid', '''<p>Your current month's commissions and rewards show in the green fields. On the 15th they move to <b>Earnings available</b>.</p><p>Open <span class="path">Withdraw</span>, enter the amount (minimum $100) and request it. It shows as pending, then arrives in My Wallet.</p>'''),
    ]
    TUT = ['01', '01', '02', '02', '03', None, None]
    steps = ''.join(f'<article class="gstep rv" id="step-{i+1}"><span class="gn">{i+1}</span><div><h2>{t}</h2>{b}{(f'<p class="gtut"><a class="tlink" href="{L("tutorials/#tut-" + TUT[i], H)}">{ic("play-c")}Watch the tutorial</a></p>' if TUT[i] else '')}</div></article>' for i, (t, b) in enumerate(S))
    body = top + f'''<section class="sec-tight"><div class="wrap"><div class="split guide-split">
 <div class="guide">{steps}</div>
 <aside class="rv" style="position:sticky;top:96px;display:grid;gap:16px">
  <figure class="media" style="margin:0"><img src="{L('images/bellver-card-dashboard-login.webp', H)}" alt="Bellver Card dashboard login page with username and password fields" width="1024" height="933" loading="lazy"><figcaption class="cap">Already registered? Log in at app.bellvercards.com</figcaption></figure>
  <div class="box"><h3 class="h3">Before you start</h3><ul><li>A phone with an authenticator app</li><li>USDT or USDC, or a credit card</li><li>A little BNB or TRX for gas</li><li>Pen and paper for your private key</li></ul><div class="btn-row" style="margin-top:18px">{order_btn('Register now', 'btn btn-go btn-sm')}<a class="btn btn-ghost btn-sm" href="{LOGIN}" target="_blank" rel="noopener">Member login</a></div></div>
 </aside>
</div></div></section>''' + news_band(H, compact=True) + checklist_band(H) + help_band(H)
    howto = {"@type": "HowTo", "name": "How to order a Bellver Card", "totalTime": "PT20M",
             "supply": [{"@type": "HowToSupply", "name": "USDT or USDC"}, {"@type": "HowToSupply", "name": "BNB or TRX for gas fees"}],
             "step": [{"@type": "HowToStep", "position": i + 1, "name": t, "url": abs_url(H) + f"#step-{i+1}"} for i, (t, _) in enumerate(S)]}
    return page(H, 'start', 'How to Order a Bellver Card: Step-by-Step Setup Guide | MTG',
                'Order your Bellver Card in seven steps: register, secure your account, fund your Fireblocks wallet with USDT or USDC, choose your card, load it, share your link and withdraw.',
                'images/og/og-bellver-get-started.jpg', 'How to order a Bellver Card step by step', body, ld_extra=[howto], trail=trail)


# ------------------------------------------------------------------ FAQ
FAQ = [
 ('The card', [
  ('What is the Bellver Card?', 'A crypto-funded payment card with a US dollar account. The physical card is a Visa and the virtual card is a Mastercard. Bellver calls it the world\'s first network card because it also has an optional rewards program. It is a product of Bellver Markets Ltd.'),
  ('How much does it cost?', 'A one-time $99 (Basic), $270 (Premium), $490 (Business) or $990 (Gold). Add-ons: Special Edition +$370 (or $470 to upgrade a regular card you already own), printed name +$49. Physical cards add shipping: $85 Europe, $149 rest of world. <a class="inl" href="{PL}" download>Download the price list</a>'),
  ('Is there a monthly or annual fee?', 'The official price list shows no monthly or annual card fee. You pay usage fees: 3.9% when you top up the card (cut from 4.95% in October 2026), 1.75% per transaction and 2% for ATM withdrawals. The top-up fee helps Bellver cover its running costs, so the company stays profitable and around for the long term.'),
  ('What are the daily and per-transaction limits?', 'Basic $1,000 a day and $500 per transaction. Premium $10,000 and $5,000. Business $50,000 and $10,000. Gold $250,000 and $20,000.'),
  ('What do I need to give when I order a physical card?', 'A complete and accurate shipping address and a valid mobile phone number from the country where the card will be delivered. The delivery service uses the number to contact you about the delivery. Bellver says it is used only by the courier and is not stored. If anything is missing or wrong, the card cannot be delivered. Tell anyone you refer who orders a physical card.'),
  ('Physical or virtual: which should I choose?', 'Virtual if you want to start today: no shipping wait, no shipping fee, and it works with Apple Pay, Google Pay and NFC rings. Choose physical if you need cash from ATMs.'),
  ('Can I use it with Apple Pay and Google Pay?', 'Yes. You can also connect it to an NFC ring or wristband and pay with a tap.'),
  ('Where can I use it?', 'Worldwide, in shops and online, in any local currency. The card account itself is in US dollars.'),
  ('How long does the physical card take to arrive?', 'Bellver\'s terms allow up to four weeks. At launch, early users reported receiving their cards in about five days.'),
  ('Can I upgrade later?', 'Yes, at any time. You pay only the difference and keep the same card. Note that monthly rewards are not back-dated to before your upgrade. Upgrading a regular card to the Special Edition costs $470.'),
  ('What is the Special Edition?', 'An add-on for any level that Bellver positions as its highest level of security and privacy, available physical or virtual. It costs $370 when you choose it at purchase (down from $390), or $470 to upgrade a regular card you already own. Bellver has said it may not be offered forever. Ask MTG for the details before you choose it.'),
 ]),
 ('Money and security', [
  ('Why is there an extra access code on My Wallet and My Cards?', 'Bellver added it as a temporary security measure after three reported phishing incidents, where criminals used fake login pages to get users\' passwords. Bellver said the code would be removed in 7 days. It never sends emails containing links to its login page. Change your password, and where you can, switch on two-factor login or set up a passkey.'),
  ('Do I need crypto to get one?', 'No, but it is the cheapest route. Card balances use USDT or USDC. Without crypto you can buy it by credit card inside the dashboard, and in Europe pay by SEPA bank transfer or PayPal.'),
  ('Which coins and networks can I deposit?', 'USDT and USDC on BNB Smart Chain (recommended), Tron or Ethereum. Bitcoin, Ethereum, BNB, Solana and others are accepted too, but must be swapped to USDT or USDC before you top up the card.'),
  ('What is the gas fee and how much do I need?', 'A small network fee paid in the chain\'s own coin: BNB on BNB Smart Chain, TRX on Tron. About $10 to $20 worth is enough to start.'),
  ('Who controls my money?', 'You. Deposits go to your own non-custodial Fireblocks wallet protected by your private key. Bellver cannot freeze or access it. You can export the key at any time. If you lose it, nobody can recover your funds.'),
  ('Where is the card registered?', 'In Singapore. At launch Bellver said its card provider is licensed by the Monetary Authority of Singapore. Bellver Markets Ltd, the company running the program, is based in Malta.'),
  ('Is this an investment?', 'No. Bellver presents it as a product: a payment card. The card price and fees are real costs, and rewards depend entirely on real card activity in your matrix.'),
 ]),
 ('Rewards', [
  ('Do I have to refer anyone?', 'No. Using a card is never dependent on or tied to referring new cardholders, and customers who do not refer anyone are just as welcome. Participation in the Reward Program is entirely voluntary. If you do want to take part, you need your own Premium card or higher and two new personal referrals who each buy a Premium card or higher, which earns your first star. Basic cardholders earn direct commissions only.'),
  ('What changed in the Bellver ranks?', 'Since Bellver\'s October 2026 update, everyone starts as a Member. You earn your first star when you hold a Premium card yourself and directly refer two new participants who each buy a Premium card. The old intermediate Premium status has been removed, which Bellver says makes the first star clearer to reach.'),
  ('Do I need to own a card to earn commissions?', 'No. Bellver pays a referral commission for personal referrals in all cases, whether or not you have purchased a Visa or Mastercard yourself. Purchasing a card is not a requirement. Monthly rewards are different: they need a card of your own, as explained below.'),
  ('Can I run ads or a big social media campaign?', 'Only with Bellver\'s approval. Any large-scale promotional campaign or public advertising on social media requires Bellver\'s prior approval. False or misleading statements, or promises of income, may result in suspension. <a class="inl" href="{PT}#bellver-rules">Read the promotion rules</a>'),
  ('Who is the rewards program for?', 'Anyone with people who trust them: TikTok LIVE hosts and other creators, YouTubers and streamers, community and group admins, network marketers, affiliate marketers and side hustlers. It is optional, and you can use the card without ever referring anyone. <a class="inl" href="{PT}">See the partner page</a>'),
  ('Can I share the card on TikTok LIVE?', 'Many people share products on TikTok LIVE, but you must follow TikTok\'s rules for your country. TikTok\'s advertising policy (updated June 2026) restricts crypto promotion in many markets and lists crypto debit cards as not allowed in some. Disclose that you earn a commission, never promise income, and check the current rules before you go live. This is general information, not legal advice. <a class="inl" href="{PTT}">Read the partner page guidance</a>'),
  ('How much do I earn per referral?', 'A one-time commission of $10 for Basic, $100 for Premium, $200 for Business or $400 for Gold. With the Special Edition: $150, $300 or $500. Upgrades pay an extra 50% of the new level\'s commission.'),
  ('How do monthly rewards work?', '0.1% of every completed card top-up by cardholders in your 2x2 matrix, on each level you qualify for: up to 12 levels with Premium, 15 with Business and 18 to 20 with Gold, depending on your star rank.'),
  ('What do I need to stay qualified?', 'Load at least $100 onto your own card every month. This is not a subscription fee: it is your own money, and it stays yours to spend. Miss a month and that month\'s rewards are forfeited. Miss three months in a row and you permanently lose your matrix position. <a class="inl" href="{CP}" download>Download the compensation plan</a>'),
  ('When and how am I paid?', 'In USDT. Direct commissions arrive within seven business days of the payment. Monthly rewards are paid on the 15th. The minimum withdrawal is $100.'),
  ('Is income guaranteed?', 'No. Bellver\'s own examples state they are not a guarantee of income. What you earn depends on how many cardholders are placed in your levels and how much they load.'),
 ]),
 ('Getting help', [
  ('How do I get help ordering?', f'Message MTG on WhatsApp for personal help, or use the Support area inside your Bellver dashboard. The <a class="inl" href="{{GS}}">step-by-step guide</a> covers the whole process.'),
  ('Where do I log in?', f'At app.bellvercards.com/login. The Member login link is in the menu on every page of this site. Bellver never sends emails with links to its login page, so do not log in from an email.'),
 ]),
]

GLOSSARY = [
 ('Non-custodial wallet', 'A wallet where only you hold the private key. No company can freeze or move your funds.'),
 ('Fireblocks dynamic wallet', 'The wallet technology behind every Bellver account. It lets you export your own private key.'),
 ('Private key', 'The secret that controls your wallet. Lose it and the funds cannot be recovered.'),
 ('USDT and USDC', 'Stablecoins worth one US dollar each. Card balances run on them.'),
 ('BNB Smart Chain', 'The recommended network for sending USDT or USDC: fast and low-cost.'),
 ('Gas fee', 'The small network fee for sending tokens, paid in BNB, TRX or ETH depending on the chain.'),
 ('Top-up (deposit)', 'Moving money onto your card balance. Carries a 3.9% fee (cut from 4.95% in October 2026), which helps keep the company sustainable, and is what rewards are calculated on.'),
 ('Direct commission', 'A one-time payment for each card ordered through your referral link.'),
 ('Rewards', 'Your monthly 0.1% share of top-ups by cardholders on your qualified levels.'),
 ('2x2 matrix', 'Your team structure: two places under each person, filled top to bottom, left to right.'),
 ('Spillover', 'Extra referrals from you or your upline that fill the next free places in your matrix.'),
 ('Member', 'Where every new participant starts. Your first star comes from your own Premium card plus two new participants you refer directly, who each buy a Premium card.'),
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
            a2 = a.replace('{GS}', L('get-started/', H)).replace('{PL}', L(DOCS_PDF['price'], H)).replace('{CP}', L(DOCS_PDF['plan'], H)).replace('{PTT}', L('partner/#tiktok', H)).replace('{PT}', L('partner/', H))
            items += f'<details class="qa"><summary>{q}<span class="pm" aria-hidden="true"></span></summary><div class="ans"><p>{a2}</p></div></details>'
            ld_q.append({"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": __import__('re').sub('<[^>]+>', '', a2)}})
        slug = g.lower().replace(' ', '-')
        blocks += f'<section class="sec-tight" id="faq-{slug}"><div class="wrap"><div class="faq-cols"><div class="sticky rv"><h2 class="h2" style="font-size:clamp(1.8rem,3.4vw,2.6rem)">{g}</h2></div><div class="faq rv">{items}</div></div></div></section>'
    gl = ''.join(f'<div class="lg rv"><i style="background:linear-gradient(135deg,var(--green),#0d4f2f)"></i><div><b>{t}</b><span>{d}</span></div></div>' for t, d in GLOSSARY)
    body = top + f'''{blocks}
<section class="sec-tight" id="glossary"><div class="wrap"><div class="sec-head rv"><h2 class="h2">Glossary</h2><p class="lead">The words you will meet in the dashboard and the videos.</p></div><div class="legend">{gl}</div></div></section>''' + help_band(H, 'Question not here?', 'Ask me on WhatsApp. I read every message and I will answer you personally.')
    dt = [{"@type": "DefinedTermSet", "name": "Bellver Card glossary", "hasDefinedTerm": [{"@type": "DefinedTerm", "name": t, "description": d} for t, d in GLOSSARY]}]
    return page(H, 'faq', 'Bellver Card FAQ: Fees, Limits, Wallet and Rewards Answered | MTG',
                'Answers to common Bellver Card questions: cost, monthly fees, limits, funding with crypto, who controls your money, Apple Pay, upgrades, rewards, payouts, plus a glossary.',
                'images/og/og-bellver-faq.jpg', 'Bellver Card frequently asked questions', body,
                ld_extra=[{"@type": "FAQPage", "mainEntity": ld_q}] + dt, trail=trail)


