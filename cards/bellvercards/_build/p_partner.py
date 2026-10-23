# -*- coding: utf-8 -*-
"""Become a partner: the page for people who want to share the card and earn commissions."""
from bv import *  # noqa
from p_info import phero, T
from ex3_video import EX3, EX3_DATE, EX3_TRANSCRIPT


def partner(H='partner/'):
    trail = T(('Become a Partner', abs_url(H)))
    art = f'''<div class="player mx-video mx-herovid mfit pb-mid" id="p-first-week" role="button" tabindex="0" aria-label="Play: {EX3[1]}" data-src="{L(EX3[5], H)}" data-title="{EX3[1]}" data-more="{L('explainers/#first-week-explained', H)}">
  <img src="{L(EX3[6] + '-640.webp', H)}" srcset="{L(EX3[6] + '-640.webp', H)} 640w, {L(EX3[6] + '.webp', H)} 1280w" sizes="(max-width:860px) 100vw, 560px" alt="Your first week as a partner: explainer video thumbnail" width="1280" height="720" fetchpriority="high">
  <span class="pbtn">{ic('play')}</span><span class="plabel">{EX3[3]}</span>
 </div><p class="mx-vcap">{ic('play-c')}New partner? Watch your first week explained in under 5 minutes</p>'''
    top = phero(H, trail, ['Share the card,', 'the honest way'],
                'You become a Bellver affiliate partner when you share the card through your referral link. There is nothing to apply for and nobody to sign up with: your referral link is your partnership. Bellver pays a referral commission on your personal referrals whether or not you own a card yourself. It suits TikTok LIVE hosts and other creators whose audiences already trust them.',
                art,
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
 <div class="box warn rv" style="margin-top:22px">{ped(ic('alert'), 'warn')}<h3 class="h3">Who it is not for</h3><p>Anyone looking for guaranteed or effortless income. Commissions depend on real people ordering real cards, and nothing is promised. If that is what you want to hear, this is not the right fit.</p></div>
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
  <div class="box rv">{ped(ic('gift'), '')}<h3 class="h3">Monthly rewards, on top</h3><p>Everyone starts as a Member. Hold a Premium card or higher and directly refer two new participants who each buy Premium or higher, and you earn your first star and qualify for monthly rewards: 0.1% of completed card top-ups in your 2x2 matrix, on every level your rank unlocks. <a class="inl" href="{L('matrix/', H)}">How the 2x2 matrix works, with a video</a></p></div>
  <div class="box rv" style="--d:.06s">{ped(ic('lock'), '')}<h3 class="h3">The rule that decides payment</h3><p>To receive monthly rewards you load at least $100 a month onto your own card. Miss it three months in a row and you lose your matrix position for good. <a class="inl" href="{L('matrix/#step7', H)}">See the $100 rule</a></p></div>
  <div class="box rv" style="--d:.12s">{ped(ic('info'), '')}<h3 class="h3">Your own card is optional</h3><p>Bellver pays a referral commission on personal referrals in all cases, whether or not you bought a Visa or Mastercard yourself. Buying a card is not a requirement. A card of your own is needed for monthly rewards, and you get your matrix position when it appears. Someone you refer who buys before you still earns you the commission, but is not placed in your matrix.</p></div>
 </div>
 <p class="fine rv" style="margin-top:16px">Results vary and are never guaranteed. Read the <a class="inl" href="{L('/earnings-disclaimer.html', H)}">Earnings Disclaimer</a> and the <a class="inl" href="{L('/risk-disclaimer.html', H)}">Risk Disclaimer</a>.</p>
</div></section>'''

    days = [('1', 'Register and secure', 'Authenticator app on, private key written on paper. <a class="inl" href="%s">Setup guide</a>' % L('get-started/', H)),
            ('2', 'Fund and order your card (optional)', 'Not needed for commissions. Go virtual to pay the same day.'),
            ('3', 'Use it for real', 'Pay for something and load your $100 for the month.'),
            ('4', 'Learn the numbers', 'Watch the explainer videos, read Prices and Rewards.'),
            ('5', 'Pick your first two people', 'Two people who would value the card. Show them, do not push.'),
            ('6', 'Help them get set up', 'Tutorial videos and the Starter Checklist. Physical card: full address and a local mobile number.'),
            ('7', 'Check your dashboard', 'Registrations, orders and commissions. Learn from what worked.')]
    wk = ''.join(f'<div class="day rv"><b class="d"><small>DAY</small>{n}</b><div><h3>{t}</h3><p>{p}</p></div></div>' for n, t, p in days)
    week = f'''<section class="sec-tight"><div class="wrap">
 <div class="sec-head rv"><h2 class="h2">Your <em>first week</em></h2><p class="lead">One small step a day, at your own speed. <a class="inl" href="{L('explainers/#first-week-explained', H)}">Watch it explained</a></p></div>
 <div class="wk">{wk}</div>
</div></section>'''

    tiktok = f'''<section class="sec-tight" id="tiktok"><div class="wrap">
 <div class="sec-head rv"><h2 class="h2">Going live on <em>TikTok</em></h2><p class="lead">Live selling works because people trust the host. Keep that trust, and keep your account safe, by following these rules.</p></div>
 <div class="dd">
  <div class="box do rv">{ped(ic('check'), 'do')}<h3 class="h3">Do</h3><ul class="checks"><li>Say on screen and out loud that you earn a commission if people order through your link.</li><li>Use TikTok's branded content disclosure where it applies to your account and country.</li><li>Show the card working: a real payment, the app, the limits and the fees.</li><li>Pin a short note that points viewers to this guide for prices, fees and rules.</li><li>Read TikTok's current rules for your country before every campaign.</li></ul></div>
  <div class="box dont rv" style="--d:.08s">{ped(ic('alert'), 'dont')}<h3 class="h3">Do not</h3><ul class="checks"><li>Promise or hint at income, or say "passive", "risk free" or "guaranteed".</li><li>Show your private key, your full balance or any login screen.</li><li>Ask viewers to send you money or crypto for any reason.</li><li>Lead with recruiting. Lead with the card and what it does.</li><li>Pressure anyone with countdowns, "last chance" or "limited spots".</li><li>Run a large-scale campaign or public social media advertising without Bellver's prior approval.</li></ul></div>
 </div>
 <div class="box warn rv" style="margin-top:22px">{ped(ic('info'), 'warn')}<h3 class="h3">Check TikTok's rules for your country</h3><p>TikTok's advertising policy (updated June 2026) restricts cryptocurrency promotion in many markets, lists crypto debit cards as not allowed in some, and restricts multi-level marketing. Organic live content and paid ads follow different rules, and the rules change, so read the current policy for your country. This is general information, not legal advice.</p></div>
</div></section>'''

    brules = f'''<section class="sec-tight" id="bellver-rules"><div class="wrap">
 <div class="sec-head rv"><h2 class="h2">Bellver's rules for <em>promoting</em> the card</h2><p class="lead">Three points from Bellver that every partner should know before sharing a single link.</p></div>
 <div class="grid3">
  <div class="box warn rv">{ped(ic('alert'), 'warn')}<h3 class="h3">Big campaigns need approval</h3><p>Any large-scale promotional campaign or public advertising on social media requires Bellver's prior approval. Ask first, then publish.</p></div>
  <div class="box warn rv" style="--d:.06s">{ped(ic('lock'), 'warn')}<h3 class="h3">Be accurate, or risk suspension</h3><p>False or misleading statements, or promises of income, may result in suspension. Stick to the facts on this site and the official documents.</p></div>
  <div class="box rv" style="--d:.12s">{ped(ic('check'), '')}<h3 class="h3">Referring is always optional</h3><p>Using a card is never dependent on or tied to referring new cardholders. Customers who do not refer anyone are just as welcome, and the Reward Program is entirely voluntary.</p></div>
 </div>
</div></section>'''

    honest = f'''<section class="sec-tight"><div class="wrap">
 <div class="sec-head rv"><h2 class="h2">How to share it <em>honestly</em></h2><p class="lead">Trust is what makes people order. <a class="inl" href="{L('explainers/#first-week-explained', H)}">Watch it explained</a></p></div>
 <div class="dd">
  <div class="box do rv">{ped(ic('check'), 'do')}<h3 class="h3">Do</h3><ul class="checks"><li>Say plainly that you earn a commission.</li><li>Show the card working, how you really use it.</li><li>Give real numbers: prices, fees, limits, the $100 rule.</li><li>Remind people that nobody can recover a lost private key.</li></ul></div>
  <div class="box dont rv" style="--d:.08s">{ped(ic('alert'), 'dont')}<h3 class="h3">Do not</h3><ul class="checks"><li>Promise income, or say "passive", "risk free" or "guaranteed".</li><li>Quote the biggest examples as if they are typical.</li><li>Pressure anyone to buy now or miss out.</li><li>Say Bellver is a bank, that money is insured, or that you work for Bellver.</li></ul></div>
 </div>
</div></section>'''

    tools = f'''<section class="sec-tight"><div class="wrap">
 <div class="sec-head rv"><h2 class="h2">What you get <em>from me</em></h2><p class="lead">Everything on this guide is yours to point people to.</p></div>
 <div class="grid3">
  <div class="box rv">{ped(ic('video'), '')}<h3 class="h3">Videos</h3><p>The 3-minute overview, the 27-minute presentation and the launch webinar, plus short tutorials. <a class="inl" href="{L('videos/', H)}">Presentation videos</a></p></div>
  <div class="box rv" style="--d:.06s">{ped(ic('book'), '')}<h3 class="h3">Starter Checklist</h3><p>A free two-page checklist for new cardholders. Message me on WhatsApp and I will send it.</p><div class="btn-row" style="margin-top:12px"><a class="btn btn-ghost btn-sm" data-track="checklist" href="{CHECKLIST_MSG}" target="_blank" rel="noopener">Get the checklist</a></div></div>
  <div class="box rv" style="--d:.12s">{ped(ic('wa'), '')}<h3 class="h3">Questions? Ask me</h3><p>You do not need my permission to partner. If you get stuck on registration, funding or your first referral, you are welcome to message me.</p><div class="btn-row" style="margin-top:12px"><a class="btn btn-ghost btn-sm" data-track="partner-whatsapp" href="{PARTNER_MSG}" target="_blank" rel="noopener">Ask MTG a question</a></div></div>
 </div>
</div></section>'''

    faq = [('Can I share it on TikTok LIVE?', 'Many people share products on TikTok LIVE, but you must follow TikTok\'s rules for your country. TikTok\'s advertising policy (updated June 2026) restricts crypto promotion in many markets and lists crypto debit cards as not allowed in some. Disclose that you earn a commission, never promise income and check the current rules before you go live.'),
           ('Do I need to talk to MTG or apply to become a partner?', 'No. Partner simply means you are an affiliate of Bellver Cards. Once you share the card with people through your referral link, you are an affiliate partner. There is no application and no approval from MTG. You are welcome to message MTG with questions, but you never have to.'),
           ('Do I need to buy a card to become a partner?', 'No. Bellver pays a referral commission for personal referrals in all cases, whether or not you have purchased a Visa or Mastercard yourself. Purchasing a card is not a requirement. A card of your own is needed for monthly rewards: your own Premium card or higher plus two new personal referrals who each buy Premium or higher, which earns your first star.'),
           ('Can I run ads or a big social media campaign?', 'Only with Bellver\'s approval. Any large-scale promotional campaign or public advertising on social media requires Bellver\'s prior approval. False or misleading statements, or promises of income, may result in suspension.'),
           ('Do I have to refer anyone?', 'No. Using a card is never dependent on or tied to referring new cardholders, and customers who do not refer anyone are just as welcome. Participation in the Reward Program is entirely voluntary.'),
           ('When are commissions paid?', 'This month\'s commissions show in your dashboard. On the 15th they move to Earnings available, and you can withdraw from $100.'),
           ('Is it guaranteed income?', 'No. Commissions depend on real people ordering real cards. Read the Earnings Disclaimer before you decide.')]
    fq = ''.join(f'<details class="qa"><summary>{q}<span class="pm" aria-hidden="true"></span></summary><div class="ans"><p>{a}</p></div></details>' for q, a in faq)
    faqs = f'''<section class="sec-tight"><div class="wrap">
 <div class="sec-head rv"><h2 class="h2">Quick <em>answers</em></h2></div>
 <div class="faq rv">{fq}</div>
</div></section>'''

    cta = final_cta(H, 'Ready to <span class="hap">start?</span>', 'You do not need a card of your own to earn commissions. Order one to use it and qualify for monthly rewards, or share your link when you are ready.',
                    second=f'<a class="btn btn-ghost" href="{L("rewards/", H)}">See the rewards plan</a>')
    mean = f'''<section class="sec-tight"><div class="wrap">
 <div class="sec-head rv"><h2 class="h2">What "partner" <em>means</em></h2><p class="lead">No forms, no approval, no call with me.</p></div>
 <div class="grid3">
  <div class="box rv">{ped(ic('card'), '')}<h3 class="h3">1. Use the card, if you want to</h3><p>Buying a card is not a requirement. Owning one lets you show real use and is needed for monthly rewards.</p></div>
  <div class="box rv" style="--d:.06s">{ped(ic('users'), '')}<h3 class="h3">2. Share it</h3><p>Share your referral link with people who would value the card.</p></div>
  <div class="box rv" style="--d:.12s">{ped(ic('check'), '')}<h3 class="h3">3. You are a partner</h3><p>You are now an affiliate partner of Bellver Cards. Commissions follow the plan.</p></div>
 </div>
</div></section>'''
    body = top + mean + reasons_band(H, 'compact', title='What people <em>say yes</em> to: 10 reasons', lead='When you share Bellver Card, these are the reasons people give for joining. More than 1,000 cards were sold in the testing phase alone (as reported at launch). Explain each reason honestly, and let people decide for themselves.') + audience_band(H, chips=False, cta=False) + who + earn + week + brules + honest + cbp_section(H) + tiktok + tools + checklist_band(H) + faqs + cta
    vld_ex3 = {"@type": "VideoObject", "name": EX3[1], "description": EX3[7], "thumbnailUrl": abs_url(EX3[6] + ".jpg"), "inLanguage": "en", "url": abs_url(H),
               "contentUrl": abs_url(EX3[5]), "uploadDate": EX3_DATE, "duration": EX3[8], "transcript": ' '.join(EX3_TRANSCRIPT),
               "author": {"@type": "Person", "name": "MTG", "jobTitle": "Your Digital Architect", "url": "https://www.musathegiant.com/"},
               "keywords": "Bellver partner, Bellver affiliate, Bellver referral link, Bellver commission, Bellver first week plan, how to share Bellver Card"}
    faq_ld = {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}
    return page(H, 'partner', 'Become a Bellver Card Partner: How to Share It and Earn | MTG',
                'How to share the Bellver Card and earn commissions: made for TikTok LIVE hosts and creators with a trusting audience, the $10 to $500 direct commissions, a first-week plan, honest sharing rules and a plain explanation of what partner means.',
                'images/og/og-bellver-partner.jpg', 'Become a Bellver Card partner', body, ld_extra=[faq_ld, vld_ex3], trail=trail)
