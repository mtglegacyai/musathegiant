# -*- coding: utf-8 -*-
"""How it works, Prices, Rewards."""
from bv import *  # noqa
from p_home import tiers_html, payback_calc
from p_tools import rewards_tool
from ex1_video import EX1, EX1_DATE, EX1_MOMENTS, EX1_TRANSCRIPT
from mx_video import MXV
from ex2_video import EX2, EX2_DATE, EX2_MOMENTS, EX2_TRANSCRIPT


def phero(H, trail, lines, lead, art=None, btns=None):
    ln = ''.join(f'<span class="ln"><span style="--l:{i}">{t}</span></span>' for i, t in enumerate(lines))
    b = f'<div class="btn-row">{btns}</div>' if btns else ''
    left = f'{crumbs_html(trail, H)}<h1 class="display">{ln}</h1><p class="lead">{lead}</p>{b}'
    if art:
        return f'<section class="phero"><div class="wrap phero-grid"><div>{left}</div><div class="phero-art">{art}</div></div></section>'
    return f'<section class="phero"><div class="wrap">{left}</div></section>'


def T(*extra):
    return root_trail() + list(extra)


# ------------------------------------------------------------------ HOW IT WORKS
def how(H='how-it-works/'):
    trail = T(('How It Works', abs_url(H)))
    vimg = EX1[6]
    art = f'''<div class="player mx-video mx-herovid mfit" id="p-money-explained" role="button" tabindex="0" aria-label="Play: {EX1[1]}" data-src="{L(EX1[5], H)}" data-title="{EX1[1]}">
  <img src="{L(vimg + '-640.webp', H)}" srcset="{L(vimg + '-640.webp', H)} 640w, {L(vimg + '.webp', H)} 1280w" sizes="(max-width:860px) 100vw, 560px" alt="Where your money really sits: explainer video thumbnail" width="1280" height="720" fetchpriority="high">
  <span class="pbtn">{ic('play')}</span><span class="plabel">{EX1[3]}</span>
 </div><p class="mx-vcap">{ic('play-c')}Watch it explained in under 5 minutes</p>'''
    top = phero(H, trail, ['How the', 'card works'], 'One card with your own wallet behind it. Press play to see where your money sits, who holds the key and how it reaches your card. The short version is below.', art,
                order_btn('Order your card') + dl_btn('slides', H, 'Presentation (PDF)'))

    em = ''.join(f'<li><b>{t}</b> {m}</li>' for t, m in EX1_MOMENTS)
    et = ''.join(f'<p>{p}</p>' for p in EX1_TRANSCRIPT)
    vdet = f'''<section class="sec-tight" style="padding-top:0"><div class="wrap"><div class="vsum-d">
 <details class="qa more"><summary>Key moments in the video<span class="pm" aria-hidden="true"></span></summary><div class="ans prose"><ul>{em}</ul></div></details>
 <details class="qa more"><summary>Read the transcript<span class="pm" aria-hidden="true"></span></summary><div class="ans prose">{et}</div></details>
</div></div></section>'''

    card = f'''<section class="sec-tight"><div class="wrap">
 <div class="sec-head rv"><h2 class="h2">The <em>card</em></h2><p class="lead">A US dollar card account you fund with crypto and spend like any other card.</p></div>
 <div class="grid3">
  <div class="box rv">{ped(ic('globe'), 'rv', cls="ped-sm")}<h3 class="h3">Pay worldwide</h3><p>Pay in shops and online in any local currency. The card account itself is kept in US dollars.</p></div>
  <div class="box rv" style="--d:.06s">{ped(ic('card'), 'rv', cls="ped-sm")}<h3 class="h3">Physical or virtual</h3><p>The physical card is a Visa and the virtual card is a Mastercard. The physical card also works for cash at ATMs. The virtual card is ready as soon as you order.</p></div>
  <div class="box rv" style="--d:.12s">{ped(ic('phone'), 'rv', cls="ped-sm")}<h3 class="h3">Phone, ring or card</h3><p>Add it to Apple Pay or Google Pay, or connect an NFC ring or wristband for tap-to-pay.</p></div>
 </div>
</div></section>'''

    wallet = f'''<section class="sec" id="wallet"><div class="wrap split">
 <div class="rv">
  <span class="badge green">{ic('lock')}Non-custodial wallet</span>
  <h2 class="h2" style="margin-top:16px">Your wallet. <em>Your key.</em></h2>
  <ul class="checks" style="margin-top:16px">
   <li><b>Your Dynamic Wallet is yours.</b> Created when you register, on Fireblocks. Bellver says it cannot freeze or access your funds.</li>
   <li><b>Only you hold the private key.</b> Export it any time.</li>
   <li><b>Move to the card only what you plan to spend.</b> The rest stays under your key.</li>
   <li><b>Lock it twice:</b> a transaction password, plus two-factor login or a passkey.</li>
  </ul>
  <div class="note">{ic('alert')}<span><b>No bank to call</b> if you lose your private key. Write it down, keep it offline, never share it.</span></div>
 </div>
 <figure class="media rv" style="--d:.1s;margin:0;background:#fff"><img src="{L('images/bellver-fireblocks-wallet-funding-flow.webp', H)}" alt="Four-step funding flow: send USDT or USDC from any wallet, via BNB chain, into your personal Fireblocks wallet, then transfer to your Bellver Visa card" width="1600" height="724" loading="lazy"></figure>
</div></section>'''

    fund = f'''<section class="sec-tight" id="funding"><div class="wrap">
 <div class="sec-head rv"><h2 class="h2">Ways to <em>fund</em> it</h2><p class="lead">Card balances run on two stablecoins. Here is every way to get money in, from best to most expensive.</p></div>
 <div class="grid3">
  <div class="box rv">{ped(ic('coins'), 'rv', cls="ped-sm")}<h3 class="h3">Best: USDT or USDC</h3><p>Send from any wallet or exchange. BNB Smart Chain is the recommended network. Tron and Ethereum work too.</p><div class="chips"><span class="chip hi"><i></i>USDT</span><span class="chip hi"><i></i>USDC</span><span class="chip">BNB Smart Chain</span><span class="chip">Tron</span><span class="chip">Ethereum</span></div></div>
  <div class="box rv" style="--d:.06s">{ped(ic('swap'), 'rv', cls="ped-sm")}<h3 class="h3">Other crypto</h3><p>Bitcoin, Ethereum, BNB, Solana and other major coins can be deposited, then swapped to USDT or USDC in your wallet before you top up.</p><div class="chips"><span class="chip">BTC</span><span class="chip">ETH</span><span class="chip">BNB</span><span class="chip">SOL</span></div></div>
  <div class="box rv" style="--d:.12s">{ped(ic('card'), 'rv', cls="ped-sm")}<h3 class="h3">No crypto yet?</h3><p>Use Buy crypto in the dashboard to pay by credit card. In Europe you can also pay by SEPA bank transfer or PayPal.</p><div class="chips"><span class="chip">Credit card</span><span class="chip">SEPA</span><span class="chip">PayPal</span></div></div>
 </div>
 {exch_note('margin-top:18px')}
 <div class="note g rv" style="margin-top:14px">{ic('info')}<span><b>Keep a little for network fees.</b> Sending tokens needs a small gas fee in the network's own coin: BNB on BNB Smart Chain, TRX on Tron. About $10 to $20 worth is plenty to start.</span></div>
</div></section>'''

    pv = f'''<section class="sec" id="physical-or-virtual"><div class="wrap">
 <div class="sec-head rv"><h2 class="h2">Physical <em>or</em> virtual?</h2><p class="lead">Both carry the same limits and the same rewards. The difference is how fast you get it and where you can use it. <a class="inl" href="{L('explainers/#which-card-explained', H)}">Watch it explained</a></p></div>
 <div class="tbl-wrap rv"><table class="tbl">
  <thead><tr><th scope="col"></th><th scope="col">Virtual card</th><th scope="col">Physical card</th></tr></thead>
  <tbody>
   <tr><td><b>Ready to use</b></td><td>As soon as it is issued</td><td>After delivery. Bellver's terms allow up to four weeks; early users reported about five days</td></tr>
   <tr><td><b>Shipping fee</b></td><td>None</td><td>$85 Europe, $149 rest of world</td></tr>
   <tr><td><b>What you must give when ordering</b></td><td>No delivery details needed</td><td>A complete, accurate shipping address and a valid mobile number from the delivery country. The courier uses the number, and Bellver says it is not stored. If either is missing or wrong, the card cannot be delivered</td></tr>
   <tr><td><b>Apple Pay and Google Pay</b></td><td>Yes</td><td>Yes</td></tr>
   <tr><td><b>Best for</b></td><td>Starting today, phone and NFC ring payments</td><td>Cash withdrawals and places that ask for a plastic card</td></tr>
   <tr><td><b>Online payments</b></td><td>Yes</td><td>Yes</td></tr>
   <tr><td><b>Cash at ATMs</b></td><td>No</td><td>Yes, 2% fee</td></tr>
  </tbody>
 </table></div>
 <p class="muted small rv" style="margin-top:12px">The physical card is a Visa and the virtual card is a Mastercard.</p>
</div></section>'''

    se = f'''<section class="sec-tight" id="special-edition"><div class="wrap"><div class="panel se rv">
 <div class="art" data-tilt="img" data-max="10"><img src="{L('images/bellver-card-special-edition-700.webp', H)}" srcset="{L('images/bellver-card-special-edition-700.webp', H)} 700w, {L('images/bellver-card-special-edition.webp', H)} 1400w" sizes="(max-width:860px) 90vw, 520px" alt="Bellver Card Special Edition" width="1400" height="831" loading="lazy"></div>
 <div>
  <h2 class="h2">Regular or <em>Special</em> Edition</h2>
  <p class="lead" style="margin-top:14px">Every level comes as a Regular card. Choose the Special Edition when you buy and it is $370 on top. In Bellver's words, you get even more security and privacy, as a physical or virtual card. Already own a regular card? Upgrading it to the Special Edition costs $470.</p>
  <ul class="checks"><li>Available on Basic, Premium, Business and Gold</li><li>Higher commissions when people you refer choose it: $150, $300 or $500</li><li>Bellver has said it may not be offered forever</li></ul>
  <a class="btn btn-ghost" href="{WA_MSG}" target="_blank" rel="noopener">{ic('wa')}Ask MTG what it includes</a>
 </div>
</div></div></section>'''

    who = f'''<section class="sec" id="who"><div class="wrap">
 <div class="split">
  <div class="rv">
   <h2 class="h2">Who is <em>behind</em> it</h2>
   <ul class="checks" style="margin-top:16px">
    <li><b>Bellver Markets Ltd, St Julian's, Malta:</b> runs the program and the rewards. It describes itself as the marketing company and does not hold your money.</li>
    <li><b>The card is registered in Singapore.</b> At the launch webinar Bellver said the card provider is licensed by the Monetary Authority of Singapore and the wallets run on Fireblocks.</li>
    <li><b>Version 1.0 launched in September 2026,</b> with improvements still rolling out. <a class="inl" href="{L('videos/#webinar', H)}">Watch the launch webinar</a></li>
   </ul>
  </div>
  <div class="box rv" style="--d:.1s">
   {ped(ic('users'), 'rv', cls="ped-sm")}
   <h3 class="h3">Who the card suits</h3>
   <ul>
    <li>Anyone who wants a crypto card with high limits</li>
    <li>People who pay or travel internationally</li>
    <li>Crypto holders who want to spend their stablecoins anywhere</li>
    <li>TikTok LIVE hosts, influencers and sales people with an audience</li>
    <li>Companies (cards can carry your company logo on request)</li>
   </ul>
  </div>
 </div>
</div></section>'''

    body = top + vdet + card + wallet + fund + pv + se + who + checklist_band(H) + help_band(H)
    vld_ex1 = {"@type": "VideoObject", "name": EX1[1], "description": EX1[7], "thumbnailUrl": abs_url(EX1[6] + ".jpg"), "inLanguage": "en", "url": abs_url(H),
               "contentUrl": abs_url(EX1[5]), "uploadDate": EX1_DATE, "duration": EX1[8], "transcript": ' '.join(EX1_TRANSCRIPT),
               "author": {"@type": "Person", "name": "MTG", "jobTitle": "Your Digital Architect", "url": "https://www.musathegiant.com/"},
               "keywords": "Bellver wallet, Bellver Dynamic Wallet, non-custodial wallet, private key, Fireblocks, USDT, USDC, BNB Smart Chain, Bellver top-up fee, is Bellver safe, who is behind Bellver"}
    howto = {"@type": "HowTo", "name": "How to fund and use the Bellver Card", "step": [
        {"@type": "HowToStep", "position": 1, "name": "Send USDT or USDC", "text": "Send USDT or USDC from any external wallet or exchange, ideally on BNB Smart Chain, plus a little BNB or TRX for gas."},
        {"@type": "HowToStep", "position": 2, "name": "Receive it in your Fireblocks wallet", "text": "Funds arrive in your own non-custodial Fireblocks dynamic wallet, protected by your private key."},
        {"@type": "HowToStep", "position": 3, "name": "Top up your card", "text": "Transfer the amount you need from your wallet to your Bellver card in one click."},
        {"@type": "HowToStep", "position": 4, "name": "Pay worldwide", "text": "Pay in shops, online, with Apple Pay or Google Pay, or withdraw cash at ATMs with the physical card."}]}
    return page(H, 'how', 'How the Bellver Card Works: Wallet, Funding and Security | MTG',
                'How the Bellver Card works: your own Fireblocks non-custodial wallet, funding with USDT or USDC, physical vs virtual cards, the Special Edition and who is behind it.',
                'images/og/og-bellver-how-it-works.jpg', 'How the Bellver Card works', body, ld_extra=[howto, vld_ex1], trail=trail)


# ------------------------------------------------------------------ PRICES
def prices(H='prices/'):
    art3 = f'''<div class="player mx-video mx-herovid pb-low mfit" id="p-which-card" role="button" tabindex="0" aria-label="Play: {EX2[1]}" data-src="{L(EX2[5], H)}?v=2" data-title="{EX2[1]}" data-more="{L('explainers/#which-card-explained', H)}">
  <img src="{L(EX2[6] + '-640.webp', H)}" srcset="{L(EX2[6] + '-640.webp', H)} 640w, {L(EX2[6] + '.webp', H)} 1280w" sizes="(max-width:860px) 100vw, 560px" alt="Which card is right for you: explainer video thumbnail" width="1280" height="720" fetchpriority="high">
  <span class="pbtn">{ic('play')}</span><span class="plabel">{EX2[3]}</span>
 </div><p class="mx-vcap">{ic('play-c')}Not sure which level? Watch it explained in under 5 minutes</p>'''
    trail = T(('Prices & Limits', abs_url(H)))
    top = phero(H, trail, ['Prices,', 'fees & limits'], 'One-time card price, clear limits, published fees. Everything below comes from Bellver\'s official price list and compensation plan, version 08/2026.', art3,
                order_btn('Order your card') + dl_btn('price', H, 'Price list (PDF)'))

    levels = f'''<section class="sec-tight"><div class="wrap">{tiers_html(H)}</div></section>'''

    rows = [('basic', 'Basic', '$99', '$1,000', '$500', '$10', 'n/a', 'None (direct commissions only)'),
            ('prem', 'Premium', '$270', '$10,000', '$5,000', '$100', '$150', 'Up to level 12'),
            ('biz', 'Business', '$490', '$50,000', '$10,000', '$200', '$300', 'Up to level 15'),
            ('gold', 'Gold', '$990', '$250,000', '$20,000', '$400', '$500', 'Up to level 20')]
    tr = ''.join(f'<tr class="{c}"><td><span class="dot"></span><b>{n}</b></td><td class="num">{p}</td><td class="num">{d}</td><td class="num">{t}</td><td class="num">{cm}</td><td class="num">{se}</td><td>{rw}</td></tr>' for c, n, p, d, t, cm, se, rw in rows)
    compare = f'''<section class="sec-tight" id="compare"><div class="wrap">
 <div class="sec-head rv"><h2 class="h2">Compare the <em>four</em> levels</h2><p class="lead">Physical and virtual cards cost the same. Commission columns show what you earn when someone you refer orders that level.</p></div>
 <div class="tbl-wrap rv"><table class="tbl">
  <thead><tr><th scope="col">Level</th><th scope="col" class="num">Card price</th><th scope="col" class="num">Daily limit</th><th scope="col" class="num">Per transaction</th><th scope="col" class="num">Your commission</th><th scope="col" class="num">With Special Edition</th><th scope="col">Monthly rewards depth</th></tr></thead>
  <tbody>{tr}</tbody>
 </table></div>
</div></section>'''

    fees = f'''<section class="sec" id="fees"><div class="wrap">
 <div class="split">
  <div class="rv">
   <h2 class="h2">Fees, <em>in plain numbers</em></h2>
   <p class="lead" style="margin-top:16px">No hidden extras. These are the fees on Bellver's official price list.</p>
   <p class="muted">Bellver is open that these fees are higher than a typical bank card. The top-up fee is what funds the commissions and monthly rewards, which is why this card can earn for you and an ordinary one cannot.</p>
   <div class="note g" style="margin-top:20px">{ic('shield')}<span><b>Why 3.9%?</b> The top-up fee can sound high next to a bank card, and it is what helps keep Bellver sustainable. A company has to pay for its team, offices, payment partners, security and support, and a profitable company is one that stays around for the long run. That is what you want from the company that holds your card.</span></div>
   <div class="note g" style="margin-top:20px">{ic('info')}<span><b>Example:</b> load $100 onto your card and $103.90 leaves your wallet, because the 3.9% fee is added on top. Pay $50 at a shop and the 1.75% transaction fee is about $0.88.</span></div>
  </div>
  <div class="grid2 rv" style="--d:.1s;align-content:start">
   <div class="box">{ped(ic('wallet'), '', cls="ped-sm")}<p class="muted small" style="margin:0">Card top-up (deposit)</p><p style="font:400 2.6rem/1.1 var(--display);color:#fff;margin:4px 0 0">3.9%</p><p class="muted small" style="margin:4px 0 0">Added on top of the amount you load</p></div>
   <div class="box">{ped(ic('card'), '', cls="ped-sm")}<p class="muted small" style="margin:0">Per transaction</p><p style="font:400 2.6rem/1.1 var(--display);color:#fff;margin:4px 0 0">1.75%</p></div>
   <div class="box">{ped(ic('coins'), '', cls="ped-sm")}<p class="muted small" style="margin:0">ATM withdrawal</p><p style="font:400 2.6rem/1.1 var(--display);color:#fff;margin:4px 0 0">2%</p></div>
   <div class="box">{ped(ic('calendar'), '', cls="ped-sm")}<p class="muted small" style="margin:0">Monthly or annual fee</p><p style="font:400 2.6rem/1.1 var(--display);color:#fff;margin:4px 0 0">None listed</p></div>
  </div>
 </div>
</div></section>'''

    addons = f'''<section class="sec-tight" id="add-ons"><div class="wrap">
 <div class="sec-head rv"><h2 class="h2">Add-ons and <em>shipping</em></h2></div>
 <div class="grid3">
  <div class="box rv">{ped(ic('star'), 'rv', cls="ped-sm")}<h3 class="h3">Special Edition, +$370</h3><p>Bellver's privacy-first version of any level, physical or virtual. Upgrading a regular card you already own costs $470. <a class="inl" href="{L('how-it-works/#special-edition', H)}">What it is</a></p></div>
  <div class="box rv" style="--d:.06s">{ped(ic('tag'), 'rv', cls="ped-sm")}<h3 class="h3">Your name on the card, +$49</h3><p>Optional. Have your name printed on your card.</p></div>
  <div class="box rv" style="--d:.12s">{ped(ic('pin'), 'rv', cls="ped-sm")}<h3 class="h3">Shipping, physical only</h3><p>$85 to Europe, $149 to the rest of the world. Virtual cards have no shipping fee.</p></div>
 </div>
</div></section>'''

    upgrade = f'''<section class="sec" id="upgrades"><div class="wrap split">
 <div class="rv">
  <h2 class="h2">Upgrade, <em>pay the difference</em></h2>
  <ul class="checks" style="margin-top:16px">
   <li><b>Pay only the difference.</b> Basic to Business costs $391.</li>
   <li><b>Same card,</b> no new order and no new shipping.</li>
   <li><b>Special Edition later costs $470</b> ($370 if chosen when you buy).</li>
   <li><b>Rewards are not back-dated.</b></li>
  </ul>
 </div>
 <div class="box warn rv" style="--d:.1s">
  {ped(ic('help'), 'warn')}
  <h3 class="h3">Which level should you choose?</h3>
  <ul>
   <li><b>Basic, $99:</b> just the card.</li>
   <li><b>Premium, $270:</b> the minimum for monthly rewards.</li>
   <li><b>Business, $490:</b> the most popular choice.</li>
   <li><b>Gold, $990:</b> the highest limits and deepest rewards.</li>
  </ul>
  <p style="margin:12px 0 0"><a class="tlink" href="{L('explainers/#which-card-explained', H)}">{ic('play-c')}Watch it explained {ic('arrow')}</a></p>
 </div>
</div></section>'''

    calc = f'''<section class="sec-tight" id="payback"><div class="wrap split">
 <div class="rv"><h2 class="h2">Let referrals <em>cover</em> your card</h2><p class="lead" style="margin-top:16px">Each person who orders through your link pays you a one-time commission. Run your own numbers.</p><p class="muted">Example from Bellver: buy Business for $490, refer three people who also choose Business ($200 each) and your card has paid for itself with $110 to spare.</p></div>
 {payback_calc(H)}
</div></section>'''

    body = top + levels + compare + fees + addons + upgrade + calc + checklist_band(H) + help_band(H)
    offers = [{"@type": "Offer", "name": f"Bellver Card {n}", "price": str(p), "priceCurrency": "USD", "availability": "https://schema.org/InStock", "url": REF}
              for n, p in [('Basic', 99), ('Premium', 270), ('Business', 490), ('Gold', 990)]]
    product = {"@type": "Product", "name": "Bellver Card", "brand": {"@type": "Brand", "name": "Bellver"}, "image": abs_url('images/bellver-card-black-visa.webp'),
               "description": "Crypto-funded card (Visa physical, Mastercard virtual) in four levels with daily limits from $1,000 to $250,000.", "offers": offers}
    vld_ex2 = {"@type": "VideoObject", "name": EX2[1], "description": EX2[7], "thumbnailUrl": abs_url(EX2[6] + ".jpg"), "inLanguage": "en", "url": abs_url(H),
               "contentUrl": abs_url(EX2[5]), "uploadDate": EX2_DATE, "duration": EX2[8], "transcript": ' '.join(EX2_TRANSCRIPT),
               "author": {"@type": "Person", "name": "MTG", "jobTitle": "Your Digital Architect", "url": "https://www.musathegiant.com/"},
               "keywords": "which Bellver card, Bellver Basic Premium Business Gold, Bellver card limits, Bellver physical or virtual card, Bellver Special Edition, Bellver upgrade"}
    return page(H, 'prices', 'Bellver Card Prices, Fees and Limits (2026) | MTG',
                'Bellver Card prices: Basic $99, Premium $270, Business $490, Gold $990. Daily limits up to $250,000, fees of 3.9% top-up, 1.75% per transaction, 2% ATM, plus add-ons and upgrades.',
                'images/og/og-bellver-prices.jpg', 'Bellver Card prices and limits', body, ld_extra=[product, vld_ex2], trail=trail)


# ------------------------------------------------------------------ REWARDS
def rewards(H='rewards/'):
    trail = T(('Rewards Program', abs_url(H)))
    art = f'''<div class="player" role="button" tabindex="0" aria-label="Play the 27-minute Bellver Card presentation" data-yt="{YT_27}" data-title="Bellver Card explained in 27 minutes" data-more="{L('videos/#explained', H)}">
     <img src="{L('images/bellver-card-explained-27-minutes-thumbnail-640.webp', H)}" srcset="{L('images/bellver-card-explained-27-minutes-thumbnail-640.webp', H)} 640w, {L('images/bellver-card-explained-27-minutes-thumbnail.webp', H)} 1280w" sizes="(max-width:860px) 100vw, 520px" alt="Beach celebration in front of a Bellver Card sign with the slogan Let's make it happen" width="1280" height="720" fetchpriority="high">
     <span class="pbtn">{ic('play')}</span><span class="plabel">27 min</span>
    </div>'''
    top = phero(H, trail, ['The rewards', 'program'], 'Optional, and simple at its core: recommend the card to two people. Below are the full rules, so you know how to qualify, how you are paid and how to stay qualified.', art,
                order_btn('Order and get your link') + f'<a class="btn btn-ghost" href="{L("matrix/", H)}"><span class="play">{ic("play")}</span>Watch the matrix explained</a>' + dl_btn('plan', H, 'Compensation plan (PDF)'))

    ways = f'''<section class="sec-tight"><div class="wrap">
 <div class="sec-head rv"><h2 class="h2">Two ways <em>to earn</em></h2></div>
 <div class="grid2">
  <div class="box rv">{ped(ic('gift'), 'rv', cls="ped-sm")}<h3 class="h3">Direct commissions, one-time</h3><p>For every card ordered through your link you earn a one-time commission based on the level they choose. Paid in USDT once their payment completes, within seven business days at the latest.</p><p>If they upgrade later, you earn an extra 50% of the commission for the level they move up to.</p>
   <div class="comm" style="margin-bottom:0">
    <div style="--m1:var(--basic-1);--m2:var(--basic-2)"><span>Basic</span><b>$10</b></div>
    <div style="--m1:var(--prem-1);--m2:var(--prem-2)"><span>Premium</span><b>$100</b><small>SE $150</small></div>
    <div style="--m1:var(--biz-1);--m2:var(--biz-2)"><span>Business</span><b>$200</b><small>SE $300</small></div>
    <div style="--m1:var(--gold-1);--m2:var(--gold-2)"><span>Gold</span><b>$400</b><small>SE $500</small></div>
   </div></div>
  <div class="box rv" style="--d:.08s">{ped(ic('coins'), 'rv', cls="ped-sm")}<h3 class="h3">Monthly rewards, recurring</h3><p>You receive 0.1% of every completed card top-up made by cardholders in your 2x2 matrix, on every level you are qualified for. Rewards are paid in USDT and settled monthly.</p><p>Because the matrix fills from the top, people placed under you can come from your upline as well as from you.</p>
   <div class="note g" style="margin-top:16px">{ic('info')}<span>Rewards are based on top-ups (money loaded onto cards), not on card purchases.</span></div></div>
 </div>
</div></section>'''

    matrix = f'''<section class="sec"><div class="wrap split">
 <div class="rv"><div class="player mx-video mx-herovid mfit" id="p-rewards-matrix" role="button" tabindex="0" aria-label="Play: {MXV[1]}" data-src="{L(MXV[5], H)}" data-title="{MXV[1]}" data-more="{L('explainers/#matrix-explained', H)}">
  <img src="{L(MXV[6] + '-640.webp', H)}" srcset="{L(MXV[6] + '-640.webp', H)} 640w, {L(MXV[6] + '.webp', H)} 1280w" sizes="(max-width:860px) 100vw, 560px" alt="The 2x2 matrix made simple: explainer video thumbnail" width="1280" height="720" loading="lazy">
  <span class="pbtn">{ic('play')}</span><span class="plabel">{MXV[3]}</span>
 </div><p class="mx-vcap">{ic('play-c')}Watch it explained in under 9 minutes</p></div>
 <div class="rv" style="--d:.1s">
  <h2 class="h2">How the <em>2x2 matrix</em> fills</h2>
  <ul class="checks">
   <li><b>Two places under everyone,</b> filled top to bottom, left to right. Extra referrals spill over.</li>
   <li><b>Only cardholders take a place.</b> Registering alone does not.</li>
   <li><b>Get your own card first.</b> Direct commissions never need one, but monthly rewards do: your place starts when your card appears.</li>
  </ul>
  <div class="btn-row"><a class="btn btn-go" href="{L('matrix/', H)}">{ic('tree')}Learn the matrix step by step</a></div>
 </div>
</div></section>'''

    lv_id = 'zEYKhn6ek1M'
    launch = f'''<section class="sec-tight" id="launch-video"><div class="wrap split">
 <div class="player rv" id="p-launch" role="button" tabindex="0" aria-label="Play: BellverCard Official Launch Presentation" data-yt="{lv_id}" data-title="BellverCard Official Launch Presentation" style="background:linear-gradient(135deg,#0b2a1f,#14452f)">
  <img src="https://i.ytimg.com/vi/{lv_id}/maxresdefault.jpg" alt="BellverCard Official Launch Presentation, video thumbnail" width="1280" height="720" loading="lazy" referrerpolicy="no-referrer" onerror="this.style.display='none'">
  <span class="pbtn">{ic('play')}</span><span class="plabel">28 min</span></div>
 <div class="rv" style="--d:.1s">
  <h2 class="h2">Watch the <em>official launch</em> presentation</h2>
  <p>The full 28 minute walkthrough of the matrix, spillover, stars and levels, with the commission structure and the product roadmap. Presentation videos are also available in 14 languages.</p>
  <ul class="checks">
   <li>How the 2x2 matrix fills and where spillover goes</li>
   <li>How stars unlock deeper reward levels</li>
   <li>Direct commissions by card level</li>
   <li>The roadmap for the card</li>
  </ul>
  <p class="fine" style="opacity:.75;font-size:.9em">This presentation was recorded before Bellver's October 2026 update, so some of its figures (the 4.95% top-up fee, the $390 Special Edition and a Premium rank step) are out of date. <a class="inl" href="{L('learn/#good-to-know', H)}">See the current figures</a>. Any earnings mentioned in a video are examples, not promises. Read the <a href="{L('/earnings-disclaimer.html', H)}">Earnings Disclaimer</a>.</p>
 </div>
</div></section>'''

    R = [('basic', 'Rank 1: Member', '', 'Everyone starts here', '0', ['Every new participant begins as a Member', 'Direct commissions on cards your referrals order: yes', 'Next step: your first star']),
         ('prem', 'Rank 2: 1 Star', '★', 'Premium card or higher', '12', ['You hold a Premium card yourself', 'You directly refer two new participants who each buy a Premium card', 'Reward depth shown is from the 08/2026 plan']),
         ('biz', 'Rank 3: 2 Stars', '★★', 'Business card', '15', ['Two personal referrals who each hold 1 Star', 'Rewards to level 15']),
         ('gold', 'Rank 4: 3 Stars', '★★★', 'Gold card', '18', ['Two personal referrals who each hold 2 Stars', 'Rewards to level 18']),
         ('gold', 'Rank 5: 4 Stars', '★★★★', 'Gold card', '19', ['Two personal referrals who each hold 3 Stars', 'Plus 20 personal referrals with Premium', 'Rewards to level 19']),
         ('gold', 'Rank 6: 5 Stars', '★★★★★', 'Gold card', '20', ['Two personal referrals who each hold 4 Stars', 'Plus 20 personal referrals with Business', 'Rewards to level 20'])]
    rk = ''.join(f'''<div class="rank {c} rv" style="--d:{(i%3)*0.06:.2f}s"><div class="top"><div><h3>{t}</h3><span class="card-lv">{cl}</span></div><span class="lv">{lv}<small>LEVELS</small></span></div><div class="stars" aria-label="{s.count('★')} stars">{s or '&nbsp;'}</div><ul>{''.join(f'<li>{x}</li>' for x in li)}</ul></div>''' for i, (c, t, s, cl, lv, li) in enumerate(R))
    ranks = f'''<section class="sec-tight" id="ranks"><div class="wrap">
 <div class="sec-head rv"><h2 class="h2">Ranks and <em>reward levels</em></h2><p class="lead">Your card level sets your ceiling. Your referrals' ranks unlock the levels underneath it.</p></div>
 <div class="note g rv" style="margin-bottom:22px">{ic('info')}<span><b>Your first star:</b> everyone starts as a Member. Your first star comes from your own Premium card plus two new participants you refer directly, who each buy a Premium card. Bellver has not yet republished its compensation plan, so the reward depths below come from the 08/2026 version. Check your dashboard for the current numbers.</span></div>
 <div class="ranks">{rk}</div>
</div></section>'''

    rules = f'''<section class="sec" id="rules"><div class="wrap">
 <div class="sec-head rv"><h2 class="h2">Staying <em>qualified</em></h2><p class="lead">The terms that decide whether you are paid each month. Read these before anything else.</p></div>
 <div class="grid2">
  <div class="box rv">{ped(ic('calendar'), 'rv', cls="ped-sm")}<h3 class="h3">Load $100 a month. It stays yours.</h3><p>To receive rewards for a month, you must load at least $100 onto your own card that month. This is <b>not a subscription fee</b>. It is your own money, loaded onto your own card, and it is yours to spend however you like. Miss it and that month's rewards are forfeited in full.</p><p class="muted small" style="margin-top:12px">The only cost is the 3.9% top-up fee. <b>Why?</b> A profitable company is one that lasts. The fee helps Bellver cover its running costs, such as its team, offices and payment partners, so the card is still here for the long term.</p></div>
  <div class="box warn rv" style="--d:.06s">{ped(ic('alert'), 'warn')}<h3 class="h3">Three misses and the position is gone</h3><p>Miss the $100 minimum three months in a row and you permanently lose your position in the matrix. Rewards built up until then are forfeited and roll up to the next qualified position. You cannot requalify for the old position.</p></div>
  <div class="box rv">{ped(ic('coins'), 'rv', cls="ped-sm")}<h3 class="h3">How and when you are paid</h3><p>Commissions and rewards are paid in USDT. Rewards settle monthly and payday is the 15th. Top-ups made in the final seven business days before settlement count toward the following month. The minimum withdrawal is $100.</p></div>
  <div class="box rv" style="--d:.06s">{ped(ic('info'), 'rv', cls="ped-sm")}<h3 class="h3">The fine print</h3><p>Basic cards earn direct commissions only. Rewards are not paid back-dated after an upgrade. Bellver Markets can change the plan with one month's notice, and payments made within four weeks count as on time.</p><p class="muted small" style="margin-top:12px">Participation in the Reward Program is entirely voluntary, and using a card never depends on referring anyone. Large-scale campaigns or public social media advertising need Bellver's prior approval, and false or misleading statements or income promises may result in suspension.</p></div>
 </div>
</div></section>'''

    est = f'''<section class="sec-tight" id="estimate"><div class="wrap">
 <div class="sec-head rv"><h2 class="h2">Do the math <em>honestly</em></h2><p class="lead">Rewards are 0.1% of what cardholders in your paid levels load each month. So 1,000 cardholders topping up $300 each pays you $300 a month. Try your own numbers.</p></div>
 <div class="split">
  {rewards_tool(H)}
  <div class="box warn rv" style="--d:.08s">
   {ped(ic('alert'), 'warn')}
   <h3 class="h3">What Bellver's big examples assume</h3>
   <p>The official slides show $2,457, $19,660 and $157,286 a month. Each assumes every place in the matrix is filled and every cardholder loads $300 a month.</p>
   <div class="tbl-wrap" style="margin-top:14px"><table class="tbl tbl-stack" style="min-width:0">
    <thead><tr><th>Levels full</th><th class="num">Cardholders needed</th><th class="num">Example a month</th></tr></thead>
    <tbody><tr><td>12 (1 Star)</td><td class="num">8,190</td><td class="num">$2,457</td></tr><tr><td>15 (Business, 2 Stars)</td><td class="num">65,534</td><td class="num">$19,660</td></tr><tr><td>18 (Gold, 3 Stars)</td><td class="num">524,286</td><td class="num">$157,286</td></tr></tbody>
   </table></div>
   <p style="margin-top:14px">Bellver itself calls these examples, not a guarantee of income. Use them to understand the model, not to plan your budget.</p>
  </div>
 </div>
</div></section>'''

    body = top + ways + audience_band(H) + matrix + launch + ranks + rules + est + help_band(H, "Want to build this properly?", "I'm MTG. Message me and I'll show you how I share the card without pressure, and help your first two referrals get set up.")
    return page(H, 'rewards', 'Bellver Card Rewards Program and 2x2 Matrix Explained | MTG',
                'The Bellver Card rewards program in plain words: direct commissions from $10 to $500, 0.1% monthly rewards per level in a 2x2 matrix, star ranks, the $100 monthly rule and honest math.',
                'images/og/og-bellver-rewards.jpg', 'Bellver Card rewards program and 2x2 matrix', body, trail=trail)
