# -*- coding: utf-8 -*-
from bv import *  # noqa


def tiers_html(here, compact=True):
    T = [
     ('basic', 'Basic', 99, '$1,000', '$500', 'Not included', False),
     ('prem', 'Premium', 270, '$10,000', '$5,000', 'Up to 12 levels', False),
     ('biz', 'Business', 490, '$50,000', '$10,000', 'Up to 15 levels', True),
     ('gold', 'Gold', 990, '$250,000', '$20,000', 'Up to 20 levels', False),
    ]
    out = []
    for i, (cls, name, price, day, tx, rew, pop) in enumerate(T):
        flag = '<span class="flag">Most popular</span>' if pop else ''
        rew_html = f'<b class="no">{rew}</b>' if cls == 'basic' else f'<b>{rew}</b>'
        out.append(f'''<article class="tier {cls}{' pop' if pop else ''} rv" style="--d:{i*0.08:.2f}s">
  <div class="tier-in">{flag}
   <div class="slab"><h3 class="name">{name}</h3><p class="price">${price}<small>one-time</small></p></div>
   <div class="rows">
    <div class="row"><span>Daily limit</span><b>{day}</b></div>
    <div class="row"><span>Per payment</span><b>{tx}</b></div>
    <div class="row"><span>Monthly rewards</span>{rew_html}</div>
   </div>
   <a class="btn {'btn-go' if pop else 'btn-ghost'}" href="{REF}" target="_blank" rel="sponsored noopener">Choose {name}</a>
  </div>
 </article>''')
    return '<div class="tiers">' + ''.join(out) + '</div>'


def payback_calc(here):
    opts = ''.join(f'<option value="{v}"{" selected" if v==sel else ""}>{n} (${p})</option>' for v, n, p, sel in [('basic','Basic',99,'business'),('premium','Premium',270,'business'),('business','Business',490,'business'),('gold','Gold',990,'business')])
    opts2 = ''.join(f'<option value="{v}"{" selected" if v=="business" else ""}>{n} (${c} each)</option>' for v, n, c in [('basic','Basic',10),('premium','Premium',100),('business','Business',200),('gold','Gold',400)])
    return f'''<div class="panel calc rv" data-calc="payback">
  <h3 class="h3">Can your card pay for itself?</h3>
  <p class="muted small">Pick your card, then count the people who order through your link.</p>
  <div class="fields">
   <div class="field"><label for="pc-mine">Your card</label><select id="pc-mine" name="mine">{opts}</select></div>
   <div class="field"><label for="pc-theirs">Their card</label><select id="pc-theirs" name="theirs">{opts2}</select></div>
   <div class="field"><label id="pc-n">People you refer</label><div class="stepper" role="group" aria-labelledby="pc-n"><button type="button" data-step="-1" aria-label="One fewer">−</button><output aria-live="polite">2</output><button type="button" data-step="1" aria-label="One more">+</button></div></div>
   <div class="field" style="align-self:end"><label class="toggle"><input type="checkbox" name="se"><span class="sw" aria-hidden="true"></span>They add the Special Edition</label></div>
  </div>
  <div class="result">
   <div><span>Commissions earned</span><b data-o="earned">$400</b></div>
   <div><span>Your card costs</span><b data-o="price">$490</b></div>
   <div class="warn"><span>Still to cover</span><b data-o="left">$90</b></div>
  </div>
  <div class="meter" aria-hidden="true"><i></i></div>
  <p class="fine"><span data-o="hint"></span> One-time direct commissions from Bellver's compensation plan (version 08/2026). Monthly rewards come on top once you qualify. Shipping for a physical card is extra.</p>
 </div>'''


def build(here=''):
    H = here
    hero = f'''<section class="hero">
 <div class="wrap">
  <div class="hero-grid">
   <div>
    <span class="kicker"><i>{ic('check')}</i>Physical Visa or instant virtual card</span>
    <h1 class="display"><span class="ln"><span style="--l:0">The card<span class="tri" aria-hidden="true"></span></span></span><span class="ln"><span style="--l:1">that can <span class="pay">pay</span></span></span><span class="ln"><span style="--l:2">your bills</span></span></h1>
    <p class="lead">Fund it with crypto. Spend in any currency, anywhere in the world. And when the people you recommend load their cards, you earn a share every month.</p>
    <div class="btn-row">
     {order_btn('Order your card')}
     <a class="btn btn-ghost" href="#watch" data-play="#v3"><span class="play">{ic('play')}</span>Watch the 3-minute video</a>
    </div>
   </div>
   <div class="stage" data-tilt=".c-main" data-max="16" aria-hidden="true">
    <div class="glow"></div><div class="ring"></div><div class="ring"></div>
    <div class="card3d c-back"><img src="{L('images/bellver-card-special-edition-700.webp', H)}" alt="" width="700" height="416"></div>
    <div class="card3d c-main"><div class="float"><img src="{L('images/bellver-card-black-visa.webp', H)}" alt="" width="1087" height="654" fetchpriority="high"><span class="sweep"></span><span class="glare"></span></div></div>
    <div class="tagpill t1"><span class="dot"></span><span>Daily limit up to <b>$250,000</b></span></div>
    <div class="tagpill t2"><span class="dot"></span><span>From <b>$99</b> one-time</span></div>
   </div>
  </div>
  <div class="facts rv" data-hero-end>
   <div class="fact"><span class="ic">{ic('bolt')}</span><div><b>Up to $20,000</b><span>per payment, worldwide</span></div></div>
   <div class="fact"><span class="ic">{ic('key')}</span><div><b>Your own key</b><span>Fireblocks wallet only you control</span></div></div>
   <div class="fact"><span class="ic">{ic('phone')}</span><div><b>Apple Pay & Google Pay</b><span>or tap with an NFC ring</span></div></div>
   <div class="fact"><span class="ic">{ic('gift')}</span><div><b>Two referrals</b><span>to join the rewards program</span></div></div>
  </div>
 </div>
</section>'''

    videos = f'''<section class="sec" id="watch">
 <div class="wrap">
  <div class="sec-head rv"><h2 class="h2">See it <em>before</em> you order</h2><p class="lead">Short on time? The 3-minute overview gives you the big picture. Ready for every detail? The 27-minute presentation covers it all.</p></div>
  <div class="vgrid">
   <div class="vcard rv">
    <div class="vmeta"><span class="dur">3<small>MIN</small></span><div><h3>Quick overview</h3><p>What the card is and why it is different</p></div></div>
    <div class="player" id="v3" role="button" tabindex="0" aria-label="Play the 3-minute Bellver Card video" data-src="{L(MP4_3MIN, H)}" data-title="Bellver Card in 3 minutes">
     <img src="{L('images/bellver-card-3-minute-video-thumbnail-640.webp', H)}" srcset="{L('images/bellver-card-3-minute-video-thumbnail-640.webp', H)} 640w, {L('images/bellver-card-3-minute-video-thumbnail.webp', H)} 1280w" sizes="(max-width:860px) 100vw, 560px" alt="Man holding a black Bellver Card under the headline The card that can pay your bills" width="1280" height="720" loading="lazy">
     <span class="pbtn">{ic('play')}</span><span class="plabel">3:31</span>
    </div>
   </div>
   <div class="vcard rv" style="--d:.1s">
    <div class="vmeta"><span class="dur">27<small>MIN</small></span><div><h3>Full presentation</h3><p>Card, wallet, prices and rewards, explained</p></div></div>
    <div class="player" role="button" tabindex="0" aria-label="Play the 27-minute Bellver Card presentation" data-yt="{YT_27}" data-title="Bellver Card explained in 27 minutes" data-more="{L('videos/#explained', H)}">
     <img src="{L('images/bellver-card-explained-27-minutes-thumbnail-640.webp', H)}" srcset="{L('images/bellver-card-explained-27-minutes-thumbnail-640.webp', H)} 640w, {L('images/bellver-card-explained-27-minutes-thumbnail.webp', H)} 1280w" sizes="(max-width:860px) 100vw, 560px" alt="Beach celebration in front of a Bellver Card sign with the slogan Let's make it happen" width="1280" height="720" loading="lazy">
     <span class="pbtn">{ic('play')}</span><span class="plabel">27 min</span>
    </div>
   </div>
  </div>
  <p class="vnote rv" style="margin-top:14px">Videos are Bellver's official presentations. Parts of the voice-over and graphics were created with AI. <a class="inl" href="{L('videos/#explained', H)}">Read the 27-minute summary</a></p>
 </div>
</section>'''

    feats = f'''<section class="sec" style="padding-top:0">
 <div class="wrap">
  <div class="sec-head rv"><h2 class="h2">Not the card <em>already</em> in your wallet</h2><p class="lead">Most cards give you a little cashback or points. This one is built around four things you rarely find together.</p></div>
  <div class="feat-grid">
   <div class="feat rv">{ic('bolt','ico')}<span class="big" data-count="250000" data-pre="$">$250,000</span><h3 class="h3">Limits that keep up with you</h3><p>Spend up to $250,000 a day and $20,000 per payment on Gold. Even Basic gives you $1,000 a day, in any local currency.</p></div>
   <div class="feat rv" style="--d:.08s">{ic('key','ico')}<span class="big">Your keys</span><h3 class="h3">Your money stays in your wallet</h3><p>Funds sit in your own Fireblocks non-custodial wallet, protected by your private key. You move only what you need onto the card, in one click.</p></div>
   <div class="feat rv">{ic('phone','ico')}<span class="big y">Today</span><h3 class="h3">A virtual card you can use now</h3><p>No shipping and no waiting. Add it to Apple Pay or Google Pay, or link an NFC ring and pay with a tap of your finger.</p></div>
   <div class="feat rv" style="--d:.08s">{ic('users','ico')}<span class="big" data-count="2" data-suf=" referrals">2 referrals</span><h3 class="h3">A card that can earn</h3><p>Recommend it to two people and you join the rewards program: a share of what cardholders in your team load onto their cards, paid monthly.</p></div>
  </div>
 </div>
</section>'''

    flow = f'''<section class="sec" style="padding-top:0">
 <div class="wrap">
  <div class="sec-head center rv"><h2 class="h2">From crypto to checkout in <em>four</em> steps</h2><p class="lead">Your money never sits on the card waiting. It stays in your wallet until the moment you need it.</p></div>
  <div class="flow rv"><span class="track" aria-hidden="true"></span>
   <div class="step"><div class="n">{ic('coins')}</div><h3>Send USDT or USDC</h3><p>From any wallet or exchange. BNB Smart Chain is fast and low-cost.</p></div>
   <div class="step"><div class="n">{ic('wallet')}</div><h3>It lands in your wallet</h3><p>Your own Fireblocks wallet. Only you hold the private key.</p></div>
   <div class="step"><div class="n">{ic('swap')}</div><h3>Top up your card</h3><p>Move the exact amount you need. It arrives in seconds.</p></div>
   <div class="step"><div class="n">{ic('globe')}</div><h3>Pay anywhere</h3><p>In shops, online and at ATMs, in any local currency.</p></div>
  </div>
  <p class="rv" style="text-align:center;margin-top:34px"><a class="tlink" href="{L('how-it-works/', H)}">How funding and security work {ic('arrow')}</a></p>
 </div>
</section>'''

    tiers = f'''<section class="sec" id="levels" style="padding-top:0">
 <div class="wrap">
  <div class="sec-head center rv"><h2 class="h2">Pick your level. <em>Upgrade</em> any time.</h2><p class="lead">Same card, four levels. What changes is how much you can spend, and how deep your monthly rewards go.</p></div>
  {tiers_html(H)}
  <div class="tier-note rv">
   <span>{ic('check')}Upgrade later and pay only the difference</span>
   <span>{ic('check')}Virtual card: no shipping fee</span>
   <span>{ic('check')}Physical card shipping: $85 Europe, $149 worldwide</span>
   <span><a class="inl" href="{L(DOCS_PDF['price'], H)}" download>{ic('download')}Download the official price list</a></span>
  </div>
  <p class="rv" style="text-align:center;margin-top:22px"><a class="tlink" href="{L('prices/', H)}">See every price, fee and add-on {ic('arrow')}</a></p>
 </div>
</section>'''

    virtual = f'''<section class="sec" style="padding-top:0">
 <div class="wrap split">
  <div class="media-duo rv">
   <figure class="media" style="margin:0"><img src="{L('images/bellver-virtual-card-apple-pay-google-pay.webp', H)}" alt="Paying contactless with a Bellver Visa card on a smartphone" width="1000" height="566" loading="lazy"></figure>
   <figure class="media" style="margin:0"><img src="{L('images/bellver-card-nfc-ring-contactless-payment.webp', H)}" alt="Paying at a card terminal with an NFC ring linked to a Bellver card" width="1000" height="715" loading="lazy"></figure>
  </div>
  <div class="rv" style="--d:.1s">
   <h2 class="h2">Skip the post. <em>Go virtual.</em></h2>
   <p class="lead" style="margin-top:16px">New to crypto cards? The virtual card is the easiest way to learn how one works, and you can be paying the same day.</p>
   <ul class="checks">
    <li><b>Ready when you order.</b> No courier, no waiting weeks.</li>
    <li><b>No shipping fee.</b> Keep the $85 to $149 a physical card costs to send.</li>
    <li><b>Pay with your phone.</b> Works with Apple Pay and Google Pay.</li>
    <li><b>Or with a ring.</b> Link an NFC ring or wristband and pay with a tap.</li>
    <li><b>Fund it with crypto,</b> spend it in any currency, worldwide.</li>
   </ul>
   {order_btn('Order a virtual card')}
  </div>
 </div>
</section>'''

    rewards = f'''<section class="sec" style="padding-top:0">
 <div class="wrap split">
  <div class="rv">
   <span class="badge gold">{ic('star')}Optional rewards program</span>
   <h2 class="h2" style="margin-top:16px">Two referrals. <em>Paid</em> every month.</h2>
   <p class="lead" style="margin-top:16px">Instead of paying for advertising, Bellver shares its card fees with cardholders who spread the word. Refer two people who order a card and you qualify for monthly rewards from cardholders across your 2x2 matrix, including people placed under you by others.</p>
   <div class="comm">
    <div style="--m1:var(--basic-1);--m2:var(--basic-2)"><span>Basic</span><b>$10</b><small>per referral</small></div>
    <div style="--m1:var(--prem-1);--m2:var(--prem-2)"><span>Premium</span><b>$100</b><small>$150 Special Edition</small></div>
    <div style="--m1:var(--biz-1);--m2:var(--biz-2)"><span>Business</span><b>$200</b><small>$300 Special Edition</small></div>
    <div style="--m1:var(--gold-1);--m2:var(--gold-2)"><span>Gold</span><b>$400</b><small>$500 Special Edition</small></div>
   </div>
   <div class="btn-row"><a class="btn btn-ghost" href="{L('rewards/', H)}">How rewards work</a>{order_btn('Order and get your link')}</div>
   <p class="fine">To receive monthly rewards you load at least $100 a month onto your own card. That is not a subscription fee, it is your own money to spend. Basic cardholders earn direct commissions only. Earnings are not guaranteed.</p>
  </div>
  {payback_calc(H)}
 </div>
</section>'''

    se = f'''<section class="sec-tight" style="padding-top:0">
 <div class="wrap"><div class="panel se rv">
  <div class="art" data-tilt="img" data-max="10"><img src="{L('images/bellver-card-special-edition-700.webp', H)}" srcset="{L('images/bellver-card-special-edition-700.webp', H)} 700w, {L('images/bellver-card-special-edition.webp', H)} 1400w" sizes="(max-width:860px) 90vw, 520px" alt="Bellver Card Special Edition, black Visa Business card with red stripes" width="1400" height="831" loading="lazy"></div>
  <div>
   <span class="badge red">Add-on to any level, +$390</span>
   <h2 class="h2" style="margin-top:16px">The <em>Special</em> Edition</h2>
   <p class="lead" style="margin-top:14px">Bellver's option for people who put privacy and security first, available as a physical or virtual card. It also lifts the commissions your referrals earn you.</p>
   <p class="muted">Bellver has said this option may not stay available forever. Ask me what it includes before you decide.</p>
   <div class="btn-row" style="margin-top:22px"><a class="btn btn-ghost" href="{WA_MSG}" target="_blank" rel="noopener">{ic('wa')}Ask MTG about it</a><a class="tlink" href="{L('how-it-works/#special-edition', H)}">Regular vs Special Edition {ic('arrow')}</a></div>
  </div>
 </div></div>
</section>'''

    steps = f'''<section class="sec" style="padding-top:clamp(40px,6vw,70px)">
 <div class="wrap">
  <div class="sec-head center rv"><h2 class="h2">Three steps to <em>your card</em></h2></div>
  <div class="steps3">
   <div class="s3 rv"><span class="no">1</span><h3 class="h3">Register with MTG's link</h3><p>Create your free account. Your dashboard and your own wallet are set up straight away.</p></div>
   <div class="s3 rv" style="--d:.08s"><span class="no">2</span><h3 class="h3">Fund your wallet and order</h3><p>Send USDT or USDC, choose your level and pay from your wallet.</p></div>
   <div class="s3 rv" style="--d:.16s"><span class="no">3</span><h3 class="h3">Pay, then share</h3><p>Use it every day. Share your own link whenever you are ready.</p></div>
  </div>
  <div class="btn-row rv" style="justify-content:center;margin-top:34px">{order_btn('Start step one')}<a class="btn btn-ghost" href="{L('get-started/', H)}">Read the full setup guide</a></div>
 </div>
</section>'''

    faqs = [
     ('How much does the Bellver Card cost?', f'A one-time $99 for Basic, $270 for Premium, $490 for Business or $990 for Gold. Physical cards add shipping ($85 Europe, $149 rest of world). Using the card has published fees: 4.95% when you top up, 1.75% per transaction and 2% at ATMs. The top-up fee helps keep Bellver profitable and around for the long term. <a class="inl" href="{L("prices/", H)}">Full price list</a>'),
     ('Do I need crypto to get one?', 'It helps, but no. Card balances run on USDT or USDC, and sending those from any wallet is the cheapest route. You can also buy crypto with a credit card inside the dashboard, and in Europe pay by bank transfer or PayPal.'),
     ('Who controls my money?', 'You do. Deposits go into your own non-custodial Fireblocks wallet protected by your private key. Bellver cannot freeze or access it. The flip side: keep your key safe, because nobody can recover it for you.'),
     ('Do I have to refer anyone?', 'No. The rewards program is optional. Many people simply want a crypto card with high limits. If you do share it, two referrals are enough to qualify.'),
    ]
    faq_html = ''.join(f'<details class="qa"><summary>{q}<span class="pm" aria-hidden="true"></span></summary><div class="ans"><p>{a}</p></div></details>' for q, a in faqs)
    faq = f'''<section class="sec" style="padding-top:0">
 <div class="wrap faq-cols">
  <div class="sticky rv"><h2 class="h2">Quick <em>answers</em></h2><p class="lead" style="margin-top:14px">The questions people ask me most. Every other one is answered on the FAQ page.</p><p style="margin-top:20px"><a class="tlink" href="{L('faq/', H)}">All questions and the glossary {ic('arrow')}</a></p></div>
  <div class="faq rv" style="--d:.08s">{faq_html}</div>
 </div>
</section>'''

    learn = f'''<section class="sec-tight" style="padding-top:0"><div class="wrap"><div class="panel learnband rv">
  <div><h2 class="h2">Want the <em>full picture?</em></h2><p class="lead" style="margin-top:12px">Wallet and security, every price and fee, the rewards rules, a step-by-step setup guide, tutorial videos and the official PDFs. All in one place.</p></div>
  <div class="btn-row"><a class="btn btn-go" href="{L('learn/', H)}">{ic('book')}Learn more</a>{dl_btn('price', H, 'Price list (PDF)')}</div>
 </div></div></section>'''
    body = hero + videos + feats + flow + tiers + virtual + rewards + se + learn + steps + help_band(H) + faq + final_cta(H, second=f'<a class="btn btn-ghost" href="{L("learn/", H)}">Learn more</a>')

    product = {"@type": "Product", "@id": abs_url('') + "#product", "name": "Bellver Card", "description": "Crypto-funded Visa debit card, physical or virtual, with a US dollar account, a non-custodial Fireblocks wallet and an optional rewards program.",
               "brand": {"@type": "Brand", "name": "Bellver"}, "image": [abs_url('images/bellver-card-black-visa.webp'), abs_url('images/bellver-card-special-edition.webp')],
               "offers": {"@type": "AggregateOffer", "priceCurrency": "USD", "lowPrice": "99", "highPrice": "990", "offerCount": "4", "availability": "https://schema.org/InStock", "url": REF}}
    v3 = {"@type": "VideoObject", "name": "Bellver Card in 3 minutes", "description": "A quick overview of the Bellver Card: limits, privacy, physical and virtual cards, and the rewards program.",
          "thumbnailUrl": abs_url('images/bellver-card-3-minute-video-thumbnail.webp'), "uploadDate": "2026-10-06", "duration": "PT3M31S", "contentUrl": abs_url(MP4_3MIN), "embedUrl": abs_url('') + "#watch", "inLanguage": "en"}
    v27 = {"@type": "VideoObject", "name": "Bellver Card explained in 27 minutes", "description": "Bellver's complete video presentation of the card, the Fireblocks wallet, prices and the rewards program.",
           "thumbnailUrl": abs_url('images/bellver-card-explained-27-minutes-thumbnail.webp'), "embedUrl": f"https://www.youtube.com/embed/{YT_27}", "url": abs_url('videos/') + '#explained', "inLanguage": "en"}
    return page(H, 'home',
                'Bellver Card: The Crypto Visa Card That Can Pay Your Bills | MTG',
                'Order the Bellver Card from $99. A crypto-funded Visa card with limits up to $250,000 a day, your own private-key wallet and monthly rewards when your referrals use their cards.',
                'images/og/og-bellver-cards.jpg', 'Bellver Card, the card that can pay your bills', body,
                ld_extra=[product, v3, v27], preload='images/bellver-card-black-visa.webp', dash=False)
