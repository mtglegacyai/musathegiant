# -*- coding: utf-8 -*-
"""Become a partner: the page for people who want to share the card and earn commissions."""
from bv import *  # noqa
from p_info import phero, T


def partner(H='partner/'):
    trail = T(('Become a Partner', abs_url(H)))
    top = phero(H, trail, ['Share the card,', 'the honest way'],
                'You become a Bellver affiliate partner when you use the card and share it with two or more people. There is nothing to apply for and nobody to sign up with: your referral link is your partnership. It suits TikTok LIVE hosts and other creators whose audiences already trust them.',
                None,
                order_btn('Order your card') +
                f'<a class="btn btn-ghost" href="{L("rewards/", H)}">See the rewards plan</a>')

    # (name, icon, categories, on Bellver's list, why, show/say)
    wrows = [
        ("TikTok LIVE hosts", 'video', 'creators', 'live', "You go live often and your followers trust you.", "Show the card paying for something live, and say you earn a commission."),
        ("Influencers and content creators", 'star', 'creators', 'yes', "You make videos, posts or a community and want a spending product your audience can use.", "Walk through the app, the limits and the fees on camera."),
        ("Community leaders", 'users', 'creators', '', "People trust you and a card with a wallet they control is useful to them.", f'The <a class="inl" href="{L("videos/", H)}">overview videos</a> and this guide, so people can decide for themselves.'),
        ("Cardholders who like it", 'card', 'everyday', '', "You use the card and friends already ask about it.", "Your own real use: a payment, a top-up, Apple Pay or Google Pay."),
        ("Everyday individuals", 'wallet', 'everyday', 'yes', "You want one card that pays your bills, with limits you choose.", f'The four card levels on the <a class="inl" href="{L("prices/", H)}">prices page</a>.'),
        ("Cryptocurrency holders", 'coins', 'everyday', 'yes', "You hold crypto and want to spend it in shops and online, in your own non-custodial wallet.", "How the wallet and private key work, and the top-up fee."),
        ("People who pay internationally", 'globe', 'everyday', 'yes', "You pay abroad, travel or send money worldwide and want it in real time.", "Worldwide acceptance, local currencies and the transfer feature."),
        ("Sales people", 'tag', 'business', 'yes', "You talk to people all day and need something clear to offer.", f'The <a class="inl" href="{L("prices/", H)}">price list</a> and the commission table, with the real numbers.'),
        ("Companies and business owners", 'building', 'business', 'yes', "You want high limits for business spending, up to $250,000 a day on Gold.", "The Business and Gold levels, with limits and shipping costs."),
        ("Network marketers", 'layers', 'business', '', "You already build teams and want a modern product with clear numbers.", f'The <a class="inl" href="{L("rewards/", H)}">rewards plan</a> and the monthly qualification rule.'),
        ("Affiliate marketers", 'swap', 'business', '', "You send traffic and want a clear commission table and a link that tracks.", "Direct commissions from $10 to $500 per card."),
        ("Side hustlers", 'bolt', 'business', '', "You want a second income stream next to a job and will do the explaining.", "Your honest first week and the starter checklist."),
    ]
    mark = {'yes': '<span class="bl" title="Named on Bellver\'s own slide">✅</span>', 'live': '<span class="bl" title="A natural fit for Bellver\'s Influencers">🎥</span>', '': '<span class="bl off">·</span>'}
    tr = ''.join(f'<tr data-cat="{c}" data-bl="{1 if s == "yes" else 0}"><th scope="row"><span class="wn"><span class="wi">{ic(i)}</span><span>{n}</span></span></th><td data-label="On Bellver\'s list" class="ctr">{mark[s]}</td><td data-label="Why the card fits">{w}</td><td data-label="What to show or say">{h}</td></tr>' for n, i, c, s, w, h in wrows)
    who = f'''<section class="sec-tight"><div class="wrap">
 <div class="sec-head rv"><h2 class="h2">Who this is <em>for</em></h2><p class="lead">The people who do well sharing a product are the ones who use it and explain it plainly. ✅ marks groups named on Bellver's own "Who is it suitable for" slide. 🎥 marks creators who sell live, a natural fit for Bellver's "Influencers".</p></div>
 <div class="who-filter rv" role="group" aria-label="Filter the table" data-who-filter>
  <button type="button" class="on" data-f="all">All 12</button><button type="button" data-f="creators">Creators and communities</button><button type="button" data-f="everyday">Everyday and crypto users</button><button type="button" data-f="business">Business, sales and networks</button><button type="button" data-f="bl">On Bellver's list</button>
 </div>
 <div class="tbl-wrap rv"><table class="tbl who-tbl" data-who-table>
  <caption class="sr">Who the Bellver Card suits, why, and what to show them</caption>
  <thead><tr><th scope="col">Who it is for</th><th scope="col" class="ctr">On Bellver's list</th><th scope="col">Why the card fits</th><th scope="col">What to show or say</th></tr></thead>
  <tbody>'''+tr+'''</tbody>
 </table></div>
 <p class="fine who-count" data-who-count aria-live="polite"></p>
 <div class="btn-row" style="margin-top:18px">'''+order_btn('Order your card')+f'''<a class="btn btn-ghost" href="{L("rewards/", H)}">See the rewards plan</a></div>
 <div class="box warn rv" style="margin-top:22px"><div class="ico">{ic('alert')}</div><h3 class="h3">Who it is not for</h3><p>Anyone looking for guaranteed or effortless income. Commissions depend on real people ordering real cards, and nothing is promised. If that is what you want to hear, this is not the right fit.</p></div>
</div></section>'''

    earn = f'''<section class="sec-tight"><div class="wrap">
 <div class="sec-head rv"><h2 class="h2">What you <em>earn</em></h2><p class="lead">One-time direct commissions when someone orders through your link, from Bellver's compensation plan (version 08/2026).</p></div>
 <div class="comm rv">
  <div style="--m1:var(--basic-1);--m2:var(--basic-2)"><span>Basic</span><b>$10</b><small>per referral</small></div>
  <div style="--m1:var(--prem-1);--m2:var(--prem-2)"><span>Premium</span><b>$100</b><small>$150 Special Edition</small></div>
  <div style="--m1:var(--biz-1);--m2:var(--biz-2)"><span>Business</span><b>$200</b><small>$300 Special Edition</small></div>
  <div style="--m1:var(--gold-1);--m2:var(--gold-2)"><span>Gold</span><b>$400</b><small>$500 Special Edition</small></div>
 </div>
 <div class="grid3" style="margin-top:22px">
  <div class="box rv"><div class="ico">{ic('gift')}</div><h3 class="h3">Monthly rewards, on top</h3><p>Everyone starts as a Member. Hold a Premium card or higher and directly refer two new participants who each buy Premium or higher, and you earn your first star and qualify for monthly rewards: 0.1% of completed card top-ups in your 2x2 matrix, on every level your rank unlocks. <a class="inl" href="{L('rewards/', H)}">How the matrix works</a></p></div>
  <div class="box rv" style="--d:.06s"><div class="ico">{ic('lock')}</div><h3 class="h3">The rule that decides payment</h3><p>To receive monthly rewards you load at least $100 a month onto your own card. Miss it three months in a row and you lose your matrix position for good.</p></div>
  <div class="box rv" style="--d:.12s"><div class="ico">{ic('info')}</div><h3 class="h3">Order your own card first</h3><p>You need at least a Basic card before you share your link. You get your matrix position when your own card appears. Someone you refer who buys before you still earns you the commission, but is not placed in your matrix.</p></div>
 </div>
 <p class="fine rv" style="margin-top:16px">Results vary and are never guaranteed. Read the <a class="inl" href="{L('/earnings-disclaimer.html', H)}">Earnings Disclaimer</a> and the <a class="inl" href="{L('/risk-disclaimer.html', H)}">Risk Disclaimer</a>.</p>
</div></section>'''

    days = [('1', 'Register and secure', 'Register with my link, switch on the authenticator app and write your private key on paper. <a class="inl" href="%s">Follow the setup guide</a>.' % L('get-started/', H)),
            ('2', 'Fund and order your own card', 'Send USDT or USDC to your wallet, choose your level and order. Going virtual means you can pay the same day.'),
            ('3', 'Use it for real', 'Pay for something with it and load your $100 for the month. Real use gives you something true to talk about.'),
            ('4', 'Learn the numbers', 'Watch the presentation videos and read Prices and Rewards, so you can answer plain questions without guessing.'),
            ('5', 'Pick your first two people', 'Think of two people who would value the card, then show them how it works. Do not push.'),
            ('6', 'Help them get set up', 'Send them the tutorial videos and the free Starter Checklist, and stay close while they register and fund. If they order a physical card, remind them to give a complete address and a valid local mobile number, or it cannot be delivered.'),
            ('7', 'Check your dashboard', 'See your registrations, orders and commissions, then tell me what is working and where you got stuck.')]
    wk = ''.join(f'<div class="day rv"><b class="d"><small>DAY</small>{n}</b><div><h3>{t}</h3><p>{p}</p></div></div>' for n, t, p in days)
    week = f'''<section class="sec-tight"><div class="wrap">
 <div class="sec-head rv"><h2 class="h2">Your <em>first week</em></h2><p class="lead">A simple plan. Move at your own speed, and skip nothing that protects your money.</p></div>
 <div class="wk">{wk}</div>
</div></section>'''

    tiktok = f'''<section class="sec-tight" id="tiktok"><div class="wrap">
 <div class="sec-head rv"><h2 class="h2">Going live on <em>TikTok</em></h2><p class="lead">Live selling works because people trust the host. Keep that trust, and keep your account safe, by following these rules.</p></div>
 <div class="dd">
  <div class="box do rv"><div class="ico">{ic('check')}</div><h3 class="h3">Do</h3><ul class="checks"><li>Say on screen and out loud that you earn a commission if people order through your link.</li><li>Use TikTok's branded content disclosure where it applies to your account and country.</li><li>Show the card working: a real payment, the app, the limits and the fees.</li><li>Pin a short note that points viewers to this guide for prices, fees and rules.</li><li>Read TikTok's current rules for your country before every campaign.</li></ul></div>
  <div class="box dont rv" style="--d:.08s"><div class="ico">{ic('alert')}</div><h3 class="h3">Do not</h3><ul class="checks"><li>Promise or hint at income, or say "passive", "risk free" or "guaranteed".</li><li>Show your private key, your full balance or any login screen.</li><li>Ask viewers to send you money or crypto for any reason.</li><li>Lead with recruiting. Lead with the card and what it does.</li><li>Pressure anyone with countdowns, "last chance" or "limited spots".</li></ul></div>
 </div>
 <div class="box warn rv" style="margin-top:22px"><div class="ico">{ic('info')}</div><h3 class="h3">Check TikTok's rules for your country</h3><p>TikTok's advertising policy (updated June 2026) restricts cryptocurrency promotion in many markets, lists crypto debit cards as not allowed in some, and restricts multi-level marketing. Organic live content and paid ads follow different rules, and the rules change, so read the current policy for your country. This is general information, not legal advice.</p></div>
</div></section>'''

    honest = f'''<section class="sec-tight"><div class="wrap">
 <div class="sec-head rv"><h2 class="h2">How to share it <em>honestly</em></h2><p class="lead">Trust is what makes people order. It also keeps you on the right side of advertising rules.</p></div>
 <div class="dd">
  <div class="box do rv"><div class="ico">{ic('check')}</div><h3 class="h3">Do</h3><ul class="checks"><li>Say plainly that you earn a commission if they order.</li><li>Show your own card and how you actually use it.</li><li>Give real numbers: prices, fees, limits and the $100 monthly rule.</li><li>Tell people to keep their private key safe, because nobody can recover it.</li><li>Point people to the official documents and this guide.</li></ul></div>
  <div class="box dont rv" style="--d:.08s"><div class="ico">{ic('alert')}</div><h3 class="h3">Do not</h3><ul class="checks"><li>Promise income, or say "passive", "risk free" or "guaranteed".</li><li>Quote the biggest examples as if they are typical.</li><li>Pressure anyone, or tell them to buy now or miss out.</li><li>Say Bellver is a bank, or that your money is insured.</li><li>Claim a link to Bellver beyond being an independent affiliate.</li></ul></div>
 </div>
</div></section>'''

    tools = f'''<section class="sec-tight"><div class="wrap">
 <div class="sec-head rv"><h2 class="h2">What you get <em>from me</em></h2><p class="lead">Everything on this guide is yours to point people to.</p></div>
 <div class="grid3">
  <div class="box rv"><div class="ico">{ic('video')}</div><h3 class="h3">Videos</h3><p>The 3-minute overview, the 27-minute presentation and the launch webinar, plus short tutorials. <a class="inl" href="{L('videos/', H)}">Presentation videos</a></p></div>
  <div class="box rv" style="--d:.06s"><div class="ico">{ic('book')}</div><h3 class="h3">Starter Checklist</h3><p>A free two-page checklist for new cardholders. Message me on WhatsApp and I will send it.</p><div class="btn-row" style="margin-top:12px"><a class="btn btn-ghost btn-sm" data-track="checklist" href="{CHECKLIST_MSG}" target="_blank" rel="noopener">Get the checklist</a></div></div>
  <div class="box rv" style="--d:.12s"><div class="ico">{ic('wa')}</div><h3 class="h3">Questions? Ask me</h3><p>You do not need my permission to partner. If you get stuck on registration, funding or your first referral, you are welcome to message me.</p><div class="btn-row" style="margin-top:12px"><a class="btn btn-ghost btn-sm" data-track="partner-whatsapp" href="{PARTNER_MSG}" target="_blank" rel="noopener">Ask MTG a question</a></div></div>
 </div>
</div></section>'''

    faq = [('Can I share it on TikTok LIVE?', 'Many people share products on TikTok LIVE, but you must follow TikTok\'s rules for your country. TikTok\'s advertising policy (updated June 2026) restricts crypto promotion in many markets and lists crypto debit cards as not allowed in some. Disclose that you earn a commission, never promise income and check the current rules before you go live.'),
           ('Do I need to talk to MTG or apply to become a partner?', 'No. Partner simply means you are an affiliate of Bellver Cards. Once you have your own card and share it with two or more people through your referral link, you are an affiliate partner. There is no application and no approval from MTG. You are welcome to message MTG with questions, but you never have to.'),
           ('Do I need to buy a card to become a partner?', 'Yes. You need at least a Basic card before you start sharing your referral link. Bellver\'s compensation plan ranks you by the card you have personally bought, and the official steps are: request your registration link, order and load your card, then spread the word. Basic earns direct commissions only. Monthly rewards need your own card at Premium or higher plus two new personal referrals who each buy Premium or higher, which earns your first star.'),
           ('Do I have to refer anyone?', 'No. The rewards program is optional. Many people just want a crypto card with high limits.'),
           ('When are commissions paid?', 'This month\'s commissions show in your dashboard. On the 15th they move to Earnings available, and you can withdraw from $100.'),
           ('Is it guaranteed income?', 'No. Commissions depend on real people ordering real cards. Read the Earnings Disclaimer before you decide.')]
    fq = ''.join(f'<details class="qa"><summary>{q}<span class="pm" aria-hidden="true"></span></summary><div class="ans"><p>{a}</p></div></details>' for q, a in faq)
    faqs = f'''<section class="sec-tight"><div class="wrap">
 <div class="sec-head rv"><h2 class="h2">Quick <em>answers</em></h2></div>
 <div class="faq rv">{fq}</div>
</div></section>'''

    cta = final_cta(H, 'Ready to <span class="hap">start?</span>', 'You need at least a Basic card before you share your link. Order yours first, then share it when you are ready.',
                    second=f'<a class="btn btn-ghost" href="{L("rewards/", H)}">See the rewards plan</a>')
    mean = f'''<section class="sec-tight"><div class="wrap">
 <div class="sec-head rv"><h2 class="h2">What "partner" <em>means</em></h2><p class="lead">No forms, no approval, no call with me.</p></div>
 <div class="grid3">
  <div class="box rv"><div class="ico">{ic('card')}</div><h3 class="h3">1. Use the card</h3><p>Order at least a Basic card and load it.</p></div>
  <div class="box rv" style="--d:.06s"><div class="ico">{ic('users')}</div><h3 class="h3">2. Share it</h3><p>Share your referral link with two or more people.</p></div>
  <div class="box rv" style="--d:.12s"><div class="ico">{ic('check')}</div><h3 class="h3">3. You are a partner</h3><p>You are now an affiliate partner of Bellver Cards. Commissions follow the plan.</p></div>
 </div>
</div></section>'''
    body = top + mean + audience_band(H, chips=False, cta=False) + who + earn + week + honest + tiktok + tools + checklist_band(H) + faqs + cta
    faq_ld = {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}
    return page(H, 'partner', 'Become a Bellver Card Partner: How to Share It and Earn | MTG',
                'How to share the Bellver Card and earn commissions: made for TikTok LIVE hosts and creators with a trusting audience, the $10 to $500 direct commissions, a first-week plan, honest sharing rules and a plain explanation of what partner means.',
                'images/og/og-bellver-guide.jpg', 'Become a Bellver Card partner', body, ld_extra=[faq_ld], trail=trail)
