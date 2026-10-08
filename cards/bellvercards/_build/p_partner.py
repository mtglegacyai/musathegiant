# -*- coding: utf-8 -*-
"""Become a partner: the page for people who want to share the card and earn commissions."""
from bv import *  # noqa
from p_info import phero, T


def partner(H='partner/'):
    trail = T(('Become a Partner', abs_url(H)))
    top = phero(H, trail, ['Share the card,', 'the honest way'],
                'If you already like the Bellver Card, you can share it and earn a commission when people order through your link. It suits TikTok LIVE hosts and other creators whose audiences already trust them. Here is exactly how it works, what you need first and what to expect.',
                None,
                f'<a class="btn btn-wa" href="{PARTNER_MSG}" target="_blank" rel="noopener" data-track="partner-whatsapp">{ic("wa")}Talk to MTG about partnering</a>' +
                f'<a class="btn btn-ghost" href="{L("rewards/", H)}">See the rewards plan</a>')

    who = f'''<section class="sec-tight"><div class="wrap">
 <div class="sec-head rv"><h2 class="h2">Who this is <em>for</em></h2><p class="lead">The people who do well sharing a product are the ones who use it and explain it plainly.</p></div>
 <div class="grid3">
  <div class="box rv"><div class="ico">{ic('video')}</div><h3 class="h3">TikTok LIVE hosts</h3><p>You go live regularly, your followers trust you, and you can show a product working in front of them.</p></div>
  <div class="box rv"><div class="ico">{ic('card')}</div><h3 class="h3">Cardholders who like it</h3><p>You use the card, you can show it working, and friends already ask you about it.</p></div>
  <div class="box rv" style="--d:.06s"><div class="ico">{ic('users')}</div><h3 class="h3">Network marketers</h3><p>You already build teams. This gives you a modern product with clear numbers to talk about.</p></div>
  <div class="box rv" style="--d:.12s"><div class="ico">{ic('video')}</div><h3 class="h3">Content creators</h3><p>You make videos, posts or a community, and want a crypto spending product your audience can use.</p></div>
  <div class="box rv"><div class="ico">{ic('coins')}</div><h3 class="h3">Affiliate marketers</h3><p>You send traffic and want a clear commission table and a referral link that tracks.</p></div>
  <div class="box rv" style="--d:.06s"><div class="ico">{ic('wallet')}</div><h3 class="h3">Side hustlers</h3><p>You want to add a second income stream next to a job, and you are happy to do the work of explaining it.</p></div>
  <div class="box rv" style="--d:.12s"><div class="ico">{ic('building')}</div><h3 class="h3">Community leaders</h3><p>People trust you, and a card with high limits and a wallet they control is useful to them.</p></div>
 </div>
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
  <div class="box rv"><div class="ico">{ic('gift')}</div><h3 class="h3">Monthly rewards, on top</h3><p>With your own Premium card or higher and two personal referrals who each have Premium or higher, you qualify for monthly rewards: 0.1% of completed card top-ups in your 2x2 matrix, on every level your rank unlocks. <a class="inl" href="{L('rewards/', H)}">How the matrix works</a></p></div>
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
            ('6', 'Help them get set up', 'Send them the tutorial videos and the free Starter Checklist, and stay close while they register and fund.'),
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
  <div class="box rv" style="--d:.12s"><div class="ico">{ic('wa')}</div><h3 class="h3">Personal help</h3><p>Stuck on registration, funding or your first referral? Message me and I will walk you through it.</p></div>
 </div>
</div></section>'''

    faq = [('Can I share it on TikTok LIVE?', 'Many people share products on TikTok LIVE, but you must follow TikTok\'s rules for your country. TikTok\'s advertising policy (updated June 2026) restricts crypto promotion in many markets and lists crypto debit cards as not allowed in some. Disclose that you earn a commission, never promise income and check the current rules before you go live.'),
           ('Do I need to buy a card to become a partner?', 'Yes. You need at least a Basic card before you start sharing your referral link. Bellver\'s compensation plan ranks you by the card you have personally bought, and the official steps are: request your registration link, order and load your card, then spread the word. Basic earns direct commissions only. Monthly rewards need your own card at Premium or higher plus two personal referrals who each have Premium or higher.'),
           ('Do I have to refer anyone?', 'No. The rewards program is optional. Many people just want a crypto card with high limits.'),
           ('When are commissions paid?', 'This month\'s commissions show in your dashboard. On the 15th they move to Earnings available, and you can withdraw from $100.'),
           ('Is it guaranteed income?', 'No. Commissions depend on real people ordering real cards. Read the Earnings Disclaimer before you decide.')]
    fq = ''.join(f'<details class="qa"><summary>{q}<span class="pm" aria-hidden="true"></span></summary><div class="ans"><p>{a}</p></div></details>' for q, a in faq)
    faqs = f'''<section class="sec-tight"><div class="wrap">
 <div class="sec-head rv"><h2 class="h2">Quick <em>answers</em></h2></div>
 <div class="faq rv">{fq}</div>
</div></section>'''

    cta = final_cta(H, 'Ready to <span class="hap">start?</span>', 'You need at least a Basic card before you share your link. Order yours first, then share it when you are ready.',
                    second=f'<a class="btn btn-wa" href="{PARTNER_MSG}" target="_blank" rel="noopener" data-track="partner-whatsapp">{ic("wa")}Message MTG</a>')
    body = top + audience_band(H, chips=False, cta=False) + who + earn + week + honest + tiktok + tools + checklist_band(H) + faqs + cta
    faq_ld = {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}
    return page(H, 'partner', 'Become a Bellver Card Partner: How to Share It and Earn | MTG',
                'How to share the Bellver Card and earn commissions: made for TikTok LIVE hosts and creators with a trusting audience, the $10 to $500 direct commissions, a first-week plan, honest sharing rules and help from MTG.',
                'images/og/og-bellver-guide.jpg', 'Become a Bellver Card partner', body, ld_extra=[faq_ld], trail=trail)
