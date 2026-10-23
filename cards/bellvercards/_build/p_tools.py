# -*- coding: utf-8 -*-
"""Calculators: one shared Rewards tool and one Payback tool, used on their own pages and inside other pages.
Maths (Bellver compensation plan 08/2026, October 2026 update):
  rewards a month = cardholders in your paid levels x average top-up x 0.1%
  seats in your paid levels = 2^(levels+1) - 2   (12 levels = 8,190)
  payback = referrals x commission per referral, compared with your card price."""
from bv import *  # noqa

RANKS = [(12, '1 Star', 'Premium card'), (15, '2 Stars', 'Business card'), (18, '3 Stars', 'Gold card'), (19, '4 Stars', 'Gold card'), (20, '5 Stars', 'Gold card')]
PRICE = [('basic', 'Basic', 99), ('premium', 'Premium', 270), ('business', 'Business', 490), ('gold', 'Gold', 990)]
COM = {'basic': (10, 10), 'premium': (100, 150), 'business': (200, 300), 'gold': (400, 500)}


def seats(lv):
    return 2 ** (lv + 1) - 2


def spin(fid, name, label, val, mn, mx, step, unit='', presets=None, slider=True, smax=None):
    """Number box with - and + keys, an optional slider and quick picks, all kept in sync by bellver.js."""
    pre = ''
    if presets:
        pre = '<div class="tchips" role="group" aria-label="Quick picks">' + ''.join(
            f'<button type="button" data-set="{v}">{lab}</button>' for v, lab in presets) + '</div>'
    sl = (f'<input class="range" type="range" tabindex="-1" aria-hidden="true" data-for="{fid}" min="{mn}" max="{smax or mx}" step="{step}" value="{val}">' if slider else '')
    u = f'<span class="tunit" aria-hidden="true">{unit}</span>' if unit else ''
    return f'''<div class="tfield">
   <label for="{fid}">{label}</label>
   <div class="tspin"><button type="button" class="tkey" data-d="-1" aria-label="Less">&minus;</button>{u}<input id="{fid}" name="{name}" type="number" inputmode="numeric" min="{mn}" max="{mx}" step="{step}" value="{val}"><button type="button" class="tkey" data-d="1" aria-label="More">+</button></div>
   {sl}{pre}
  </div>'''


def rewards_tool(H, full=False):
    opts = ''.join(f'<option value="{lv}"{" selected" if lv == 12 else ""}>{r}: {lv} levels ({seats(lv):,} seats)</option>' for lv, r, c in RANKS)
    ex = ''.join(f'<button type="button" class="tex" data-ex="{lv}"><b>{seats(lv):,}</b><small>{lv} levels full</small></button>' for lv in (12, 15, 18))
    link = '' if full else f'<a class="tlink tool-open" href="{L("rewards-calculator/", H)}">Open the full calculator {ic("arrow")}</a>'
    return f'''<div class="tool rv" data-calc="rewards" data-def="12,1000,300">
 <div class="tool-top"><span class="tool-led" aria-hidden="true"></span><h3>Monthly rewards calculator</h3><button type="button" class="tool-reset" data-reset>{ic('swap')}Reset</button></div>
 <div class="tool-in">
  <div class="tfield tspan"><label for="rw-lv">Your rank (how many levels you are paid on)</label><select id="rw-lv" name="lv">{opts}</select></div>
  {spin('rw-n', 'n', 'Cardholders in your paid levels', 1000, 0, 524286, 1, presets=[(14, '14'), (100, '100'), (500, '500'), (1000, '1,000'), (8190, '8,190')], smax=20000)}
  {spin('rw-a', 'a', 'Average top-up each, per month', 300, 0, 100000, 10, unit='$', presets=[(100, '$100'), (300, '$300'), (500, '$500')], smax=1000)}
 </div>
 <div class="tool-screen" aria-live="polite">
  <div class="ts-row"><span>Loaded a month</span><b data-o="vol">$300,000</b></div>
  <div class="ts-row ts-main"><span>Your rewards a month</span><b data-o="rew">$300</b></div>
  <div class="ts-row"><span>Over a year</span><b data-o="yr">$3,600</b></div>
  <div class="ts-fill"><span>Seats filled in your paid levels</span><div class="meter"><i data-o="bar"></i></div><b data-o="pct">12.2%</b></div>
 </div>
 <p class="tool-how"><span class="badge-ill">Illustration, not a promise</span><span data-o="how">1,000 cardholders × $300 = $300,000 loaded. 0.1% of that = $300 a month.</span></p>
 <div class="tool-ex"><p>Try Bellver's own examples (everyone loads $300):</p><div>{ex}</div></div>
 <p class="fine">You are only paid for a month if you load at least $100 onto your own card that month. Real results depend on how many cardholders are actually placed in your levels and how much they load. Nothing is guaranteed. 4 and 5 Stars: Bellver has not republished these depths since its October 2026 update.</p>
 {link}
</div>'''


def payback_tool(H, full=False):
    mine = ''.join(f'<option value="{k}"{" selected" if k == "business" else ""}>{n}, ${p}</option>' for k, n, p in PRICE)
    theirs = ''.join(f'<option value="{k}"{" selected" if k == "business" else ""}>{n}, ${COM[k][0]} each</option>' for k, n, p in PRICE)
    link = '' if full else f'<a class="tlink tool-open" href="{L("payback-calculator/", H)}">Open the full calculator {ic("arrow")}</a>'
    return f'''<div class="tool rv" data-calc="payback" data-def="business,business,3,0">
 <div class="tool-top"><span class="tool-led" aria-hidden="true"></span><h3>Can your card pay for itself?</h3><button type="button" class="tool-reset" data-reset>{ic('swap')}Reset</button></div>
 <div class="tool-in">
  <div class="tfield"><label for="pb-mine">Your card</label><select id="pb-mine" name="mine">{mine}</select></div>
  <div class="tfield"><label for="pb-theirs">The card they order</label><select id="pb-theirs" name="theirs">{theirs}</select></div>
  {spin('pb-n', 'n', 'People who order through your link', 3, 0, 50, 1, presets=[(1, '1'), (2, '2'), (3, '3'), (5, '5'), (10, '10')], slider=False)}
  <div class="tfield tse"><label class="toggle"><input type="checkbox" name="se"><span class="sw" aria-hidden="true"></span>They add the Special Edition</label></div>
 </div>
 <div class="tool-screen" aria-live="polite">
  <div class="ts-row"><span>Commissions earned</span><b data-o="earned">$600</b></div>
  <div class="ts-row"><span>Your card costs</span><b data-o="price">$490</b></div>
  <div class="ts-row ts-main" data-o="leftbox"><span data-o="leftlab">Covered, plus</span><b data-o="left">$110</b></div>
  <div class="ts-fill"><span>Card covered</span><div class="meter"><i data-o="bar"></i></div><b data-o="pct">100%</b></div>
 </div>
 <p class="tool-how"><span class="badge-ill">One-time commissions</span><span data-o="how">3 × $200 = $600 earned. $600 minus your $490 card = $110 to spare.</span></p>
 <p class="fine">Direct commissions from Bellver's compensation plan (version 08/2026). They are paid once per card ordered through your link, and you do not need a card of your own to earn them. Monthly rewards come on top once you qualify. Shipping for a physical card is extra.</p>
 {link}
</div>'''


def rewards_page(H='rewards-calculator/'):
    from p_info import phero, T
    trail = T(('Rewards Calculator', abs_url(H)))
    top = phero(H, trail, ['Rewards', 'calculator'], 'See the 0.1% at work with your own numbers: pick your rank, how many cardholders sit in your paid levels and how much they load. A learning tool, not a promise.')
    tool = f'<section class="sec-tight tool-sec" style="padding-top:0"><div class="wrap tool-wrap">{rewards_tool(H, True)}</div></section>'
    info = f'''<section class="sec-tight" id="how-it-works"><div class="wrap">
 <div class="grid3">
  <div class="box rv">{ped(ic('coins'), '')}<h3 class="h3">How it is worked out</h3><p>Every time a cardholder in your paid levels tops up their card, you receive 0.1% of that top-up. So $1,000 loaded pays you $1. The calculator multiplies cardholders by their average top-up, then takes 0.1%.</p></div>
  <div class="box rv" style="--d:.06s">{ped(ic('tree'), '')}<h3 class="h3">Where the cardholders come from</h3><p>Your rank decides how many levels you are paid on. Seats fill top to bottom, left to right, and spillover from above can land under you. <a class="inl" href="{L('matrix/', H)}">See the 2x2 matrix</a></p></div>
  <div class="box warn rv" style="--d:.12s">{ped(ic('alert'), 'warn')}<h3 class="h3">To be paid each month</h3><p>Hold a Premium card or higher, reach your rank, and load at least $100 onto your own card that month. Early on, direct commissions are usually the bigger money. <a class="inl" href="{L('payback-calculator/', H)}">Try the Payback Calculator</a></p></div>
 </div>
</div></section>'''
    body = top + tool + info + help_band(H, 'Want help with your numbers?', "I'm MTG. Message me on WhatsApp and I'll walk you through how the rewards work, without the hype.")
    app = {"@type": "WebApplication", "name": "Bellver Card monthly rewards calculator", "url": abs_url(H), "applicationCategory": "FinanceApplication", "operatingSystem": "Any", "isAccessibleForFree": True,
           "description": "Estimate Bellver Card monthly matrix rewards: 0.1% of the top-ups made by cardholders in your paid levels. Illustration only."}
    return page(H, 'rcalc', 'Bellver Card Rewards Calculator: Estimate Your 0.1% Monthly Rewards | MTG',
                'Free Bellver Card rewards calculator: choose your rank, cardholders in your paid levels and their average top-up to see how the 0.1% monthly reward works. Illustration only, not a promise.',
                'images/og/og-bellver-rewards-calculator.jpg', 'Bellver Card rewards calculator', body, ld_extra=[app], trail=trail)


def payback_page(H='payback-calculator/'):
    from p_info import phero, T
    trail = T(('Payback Calculator', abs_url(H)))
    top = phero(H, trail, ['Payback', 'calculator'], 'Can your referrals cover the price of your card? Pick your card, the card your referrals order and how many people order through your link.')
    tool = f'<section class="sec-tight tool-sec" style="padding-top:0"><div class="wrap tool-wrap">{payback_tool(H, True)}</div></section>'
    rows = ''.join(f'<tr><td><b>{n}</b></td><td class="num">${p}</td><td class="num">${COM[k][0]}</td><td class="num">{"$" + str(COM[k][1]) if k != "basic" else "n/a"}</td></tr>' for k, n, p in PRICE)
    info = f'''<section class="sec-tight" id="commissions"><div class="wrap split">
 <div class="rv"><h2 class="h2">The commission <em>table</em></h2><p class="lead" style="margin-top:14px">A one-time commission for every card ordered through your link. Bellver's own example: buy Business for $490, refer three people who also choose Business and your card has paid for itself with $110 to spare.</p><p style="margin-top:16px"><a class="tlink" href="{L('rewards-calculator/', H)}">Then try the Rewards Calculator {ic('arrow')}</a></p></div>
 <div class="tbl-wrap rv"><table class="tbl tbl-stack" style="min-width:0"><thead><tr><th>Level</th><th class="num">Card price</th><th class="num">You earn</th><th class="num">With Special Edition</th></tr></thead><tbody>{rows}</tbody></table></div>
</div></section>'''
    body = top + tool + info + cbp_band(H, 'Want your referrals to come faster?') + help_band(H, 'Not sure which card to choose?', "I'm MTG. Message me on WhatsApp and I'll help you pick the level that fits you.")
    app = {"@type": "WebApplication", "name": "Bellver Card payback calculator", "url": abs_url(H), "applicationCategory": "FinanceApplication", "operatingSystem": "Any", "isAccessibleForFree": True,
           "description": "Check how many referrals cover the price of your Bellver Card using the one-time direct commissions."}
    return page(H, 'pcalc', 'Bellver Card Payback Calculator: Can Referrals Cover Your Card? | MTG',
                'Free Bellver Card payback calculator: pick your card, your referrals\' card and how many people order through your link to see when your card pays for itself.',
                'images/og/og-bellver-payback.jpg', 'Bellver Card payback calculator', body, ld_extra=[app], trail=trail)
