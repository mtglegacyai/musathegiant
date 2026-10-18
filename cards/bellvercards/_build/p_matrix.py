# -*- coding: utf-8 -*-
"""2x2 Matrix Explained: the rewards plan taught step by step, in plain words.
Facts come from Bellver's compensation plan (version 08/2026), the presentation slides,
the official videos and the October 2026 Bellver news update."""
import json
from bv import *  # noqa
from p_info import phero, T
from p_tools import rewards_tool

GUIDE_PDF = 'docs/bellver-2x2-matrix-explained-by-mtg.pdf'
VIDEO = 'videos/bellver-2x2-matrix-explained.mp4'
SHARE_IMG = 'images/bellver-2x2-matrix-one-picture.png'
AVG = 300          # Bellver's own example: average top-up per cardholder per month
RATE = 0.001       # 0.1% per level

# rank ladder: (css, name, stars, card needed, needs, levels)
RANKS = [
    ('basic', 'Member', 0, 'Any card', ['Everyone starts here', 'Direct commissions on cards you refer'], 0),
    ('prem', '1 Star', 1, 'Premium or higher', ['Two people you refer directly', 'Each buys a Premium card or higher'], 12),
    ('biz', '2 Stars', 2, 'Business or higher', ['Two people you refer directly', 'Each has reached 1 Star'], 15),
    ('gold', '3 Stars', 3, 'Gold', ['Two people you refer directly', 'Each has reached 2 Stars'], 18),
    ('gold', '4 Stars', 4, 'Gold', ['Two direct referrals with 3 Stars', 'Plus 20 direct referrals with Premium'], 19),
    ('gold', '5 Stars', 5, 'Gold', ['Two direct referrals with 4 Stars', 'Plus 20 direct referrals with Business'], 20),
]


def seats(level):
    return 2 ** level


def upto(level):
    return 2 ** (level + 1) - 2


def money(v):
    return '${:,.0f}'.format(v) if v >= 10 else '${:,.2f}'.format(v)


# ---------------------------------------------------------------- SVG pictures
def tree_svg(depth=3, w=480, labels=None, cls='', numbered=False, you='YOU', extra=''):
    """Static matrix picture: You on top, then 2, 4, 8 seats."""
    gap = 92 if depth <= 3 else 74
    h = 50 + depth * gap + 40
    rr = [30, 24, 20, 16, 12]
    pos = {}
    lines, dots = [], []
    for lv in range(depth + 1):
        n = 2 ** lv
        for i in range(n):
            x = (i + .5) * w / n; y = 40 + lv * gap
            idx = n - 1 + i
            pos[idx] = (x, y)
            if lv:
                px, py = pos[(idx - 1) // 2]
                lines.append(f'<line x1="{px:.1f}" y1="{py:.1f}" x2="{x:.1f}" y2="{y:.1f}"/>')
    for idx, (x, y) in pos.items():
        lv = (idx + 1).bit_length() - 1; r = rr[min(lv, 4)]
        if idx == 0:
            dots.append(f'<g class="you"><circle cx="{x:.1f}" cy="{y:.1f}" r="{r}"/><text x="{x:.1f}" y="{y + 5:.1f}">{you}</text></g>')
            continue
        lab = (labels or {}).get(idx, str(idx) if numbered else '')
        t = f'<text x="{x:.1f}" y="{y + 5:.1f}">{lab}</text>' if lab else ''
        dots.append(f'<g class="seat lv{lv}"><circle cx="{x:.1f}" cy="{y:.1f}" r="{r}"/>{t}</g>')
    rows = ''.join(f'<text class="rowlab" x="-60" y="{44 + lv * gap:.1f}">LEVEL {lv}</text>' for lv in range(1, depth + 1))
    return f'<svg class="mx-tree {cls}" viewBox="-64 0 {w + 64} {h}" role="img" aria-label="Matrix picture"><g class="ln">{"".join(lines)}</g>{rows}{"".join(dots)}{extra}</svg>'


def spill_svg():
    """Upline view: the upline's third referral drops into the first free seat under you."""
    w, h = 480, 330
    up, you, oth = (240, 46), (120, 150), (360, 150)
    l2 = [(60, 262), (180, 262), (300, 262), (420, 262)]
    ln = ''.join(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}"/>' for a, b in [(up, you), (up, oth), (you, l2[0]), (you, l2[1]), (oth, l2[2]), (oth, l2[3])])
    return f'''<svg class="mx-tree mx-spill" viewBox="0 0 {w} {h}" role="img" aria-label="Spillover: the upline's third referral is placed in the first free seat under you">
 <g class="ln">{ln}</g>
 <g class="up"><circle cx="{up[0]}" cy="{up[1]}" r="30"/><text x="{up[0]}" y="{up[1] + 5}">UPLINE</text></g>
 <g class="you"><circle cx="{you[0]}" cy="{you[1]}" r="27"/><text x="{you[0]}" y="{you[1] + 5}">YOU</text></g>
 <g class="seat lv1 full"><circle cx="{oth[0]}" cy="{oth[1]}" r="27"/><text x="{oth[0]}" y="{oth[1] + 5}">B</text></g>
 <g class="seat lv2 spill"><circle cx="{l2[0][0]}" cy="{l2[0][1]}" r="24"/><text x="{l2[0][0]}" y="{l2[0][1] + 6}">+1</text></g>
 <g class="seat lv2"><circle cx="{l2[1][0]}" cy="{l2[1][1]}" r="24"/></g>
 <g class="seat lv2"><circle cx="{l2[2][0]}" cy="{l2[2][1]}" r="24"/></g>
 <g class="seat lv2"><circle cx="{l2[3][0]}" cy="{l2[3][1]}" r="24"/></g>
 <defs><marker id="mxa" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#5aa9ff"/></marker></defs>
 <path class="drop" d="M211 54 C 120 40, 28 120, 50 232" marker-end="url(#mxa)"/>
 <text class="tag" x="60" y="318">Upline's 3rd referral lands here</text>
</svg>'''


def hero_svg():
    """Animated hero: seats fill in reading order, then coins rise to you. Driven by matrix.js."""
    return tree_svg(3, 480, cls='mx-hero', you='YOU')


# ---------------------------------------------------------------- page
def matrix(H='matrix/'):
    trail = T(('Rewards Program', abs_url('rewards/')), ('2x2 Matrix Explained', abs_url(H)))
    art = f'''<div class="player mx-video mx-herovid mfit" id="p-matrix-explained" role="button" tabindex="0" aria-label="Play: the Bellver 2x2 matrix explained" data-src="{L(VIDEO, H)}" data-title="The Bellver 2x2 matrix, made simple">
  <img src="{L('images/bellver-2x2-matrix-explainer-thumbnail-640.webp', H)}" srcset="{L('images/bellver-2x2-matrix-explainer-thumbnail-640.webp', H)} 640w, {L('images/bellver-2x2-matrix-explainer-thumbnail.webp', H)} 1280w" sizes="(max-width:860px) 100vw, 560px" alt="The 2x2 matrix made simple: explainer video by MTG" width="1280" height="720" fetchpriority="high">
  <span class="pbtn">{ic('play')}</span><span class="plabel">8:46</span>
 </div><p class="mx-vcap">{ic('play-c')}Watch it explained in under 9 minutes, in my own voice</p>'''
    top = phero(H, trail, ['The 2x2 matrix', 'made simple'],
                'Press play and watch it explained in under nine minutes. Prefer to read? Seven short steps below, pictures you can play with and honest numbers. No jargon, no hype.', art,
                order_btn('Order your card') + f'<a class="btn btn-ghost" href="{L(GUIDE_PDF, H)}" download>{ic("download")}Download the PDF guide</a>')

    # 30-second version
    quick = [('users', 'Two seats under everyone', 'That is what 2x2 means. Every cardholder has two seats right under them.'),
             ('layers', 'Seats fill like reading a book', 'Top row first, left to right. Then the next row. No gaps.'),
             ('tree', 'Every row doubles', '2, then 4, then 8, then 16. Twelve rows hold 8,190 people.'),
             ('coins', 'You earn 0.1% per level', 'On every top-up made by cardholders in the rows you qualify for.'),
             ('calendar', 'Load $100 a month', 'Onto your own card. It stays your money. That keeps you paid.')]
    qc = ''.join(f'<li class="rv" style="--d:{i * .06:.2f}s"><span class="n">{i + 1}</span><span class="qi">{ic(k)}</span><b>{t}</b><p>{d}</p></li>' for i, (k, t, d) in enumerate(quick))
    s_quick = f'''<section class="sec-tight" id="quick" data-title="In 30 seconds"><div class="wrap">
 <div class="sec-head rv"><span class="badge green">{ic('bolt')}The 30-second version</span><h2 class="h2">Five things. <em>That's the whole plan.</em></h2></div>
 <ol class="mx-quick">{qc}</ol>
 <div class="mx-jump rv">{''.join(f'<a href="#step{i}"><small>Step {i}</small>{t}</a>' for i, t in enumerate(['Two seats', 'Reading order', 'Spillover', 'Doubling', 'The 0.1%', 'Stars', 'Stay paid'], 1))}</div>
</div></section>'''

    def step_head(n, title, lead=''):
        lp = f'<p class="lead">{lead}</p>' if lead else ''
        return f'<div class="sec-head rv"><span class="mx-step">Step {n} of 7</span><h2 class="h2">{title}</h2>{lp}</div>'

    # step 1
    s1 = f'''<section class="sec" id="step1" data-title="1. Two seats"><div class="wrap split">
 <div class="rv">{step_head(1, 'Two seats <em>under everyone</em>')}
  <ul class="checks mx-checks">
   <li><b>"2x2" just means two by two.</b> Every person has two seats directly under them.</li>
   <li><b>The row right under you is Level 1.</b> The row under that is Level 2, and so on.</li>
   <li><b>The first two cardholders you refer</b> usually sit in your Level 1 seats.</li>
   <li><b>Only cardholders take a seat.</b> Registering alone does not.</li>
  </ul>
 </div>
 <figure class="mx-fig rv" style="--d:.1s">{tree_svg(1, 480, labels={1: 'A', 2: 'B'})}<figcaption>You, with two seats under you: A on the left, B on the right.</figcaption></figure>
</div></section>'''

    # step 2: interactive builder
    s2 = f'''<section class="sec" id="step2" data-title="2. Reading order"><div class="wrap">
 {step_head(2, 'Seats fill in <em>reading order</em>', 'Top to bottom, left to right, like reading a page. The numbers show the order. Try it.')}
 <div class="panel mx-build rv" data-mx-build>
  <div class="mx-build-top">
   <div class="btn-row" style="opacity:1;animation:none;margin:0">
    <button class="btn btn-go btn-sm" type="button" data-act="you">{ic('users')}You refer someone</button>
    <button class="btn btn-ghost btn-sm" type="button" data-act="spill">{ic('down')}Spillover from above</button>
    <button class="btn btn-ghost btn-sm" type="button" data-act="reset">Reset</button>
   </div>
   <p class="mx-tip">{ic('info')}Tip: tap any filled seat to let <b>that person</b> refer someone.</p>
  </div>
  <div class="mx-build-svg" data-svg></div>
  <ul class="mx-legend"><li><i class="k-you"></i>You</li><li><i class="k-mine"></i>You referred them</li><li><i class="k-team"></i>Your team referred them</li><li><i class="k-spill"></i>Spillover from above</li></ul>
  <div class="mx-msg" data-msg aria-live="polite">Press <b>You refer someone</b> to start.</div>
 </div>
 <div class="grid3 mx-after">
  <div class="box rv"><div class="ico">{ic('layers')}</div><h3 class="h3">No gaps, ever</h3><p>The system always uses the next free seat. You cannot pick a seat, and nobody can skip the line.</p></div>
  <div class="box rv" style="--d:.06s"><div class="ico">{ic('users')}</div><h3 class="h3">Your 3rd, 4th, 10th referral</h3><p>Once your two seats are full, extra people you refer go to the next free seat further down. Nobody you bring is wasted.</p></div>
  <div class="box rv" style="--d:.12s"><div class="ico">{ic('gift')}</div><h3 class="h3">You still get your commission</h3><p>You always earn the direct commission for people you refer, wherever the system places them.</p></div>
 </div>
</div></section>'''

    # step 3: spillover
    s3 = f'''<section class="sec" id="step3" data-title="3. Spillover"><div class="wrap split rev">
 <div class="rv">{step_head(3, 'Spillover: <em>help from above</em>')}
  <ul class="checks mx-checks">
   <li><b>Spillover means people under you that you did not refer.</b></li>
   <li><b>They come from people above you</b> (your upline) who refer more than two. Their extras flow down into the next free seats, and some land under you.</li>
   <li><b>Their top-ups count for your rewards</b>, as long as they sit in a level you qualify for.</li>
   <li><b>No direct commission for you</b> on spillover. That goes to whoever referred them.</li>
  </ul>
  <div class="note g">{ic('info')}<span>This is why Bellver says it is <b>not a binary plan</b>. There is no "weaker leg". You earn on everyone in your paid levels, left and right.</span></div>
 </div>
 <figure class="mx-fig rv" style="--d:.1s">{spill_svg()}<figcaption>Your upline already has two people (you and B). Their third referral goes to the first free seat on the next row: under you.</figcaption></figure>
</div></section>'''

    # step 4: doubling
    rows = ''
    marks = {12: '1 Star', 15: '2 Stars', 18: '3 Stars', 19: '4 Stars', 20: '5 Stars'}
    for lv in range(1, 21):
        m = marks.get(lv)
        chip = f'<span class="mx-chip">{m}</span>' if m else ''
        rows += f'<tr class="{"hit" if m else ""}"><td><b>Level {lv}</b>{chip}</td><td class="num">{seats(lv):,}</td><td class="num">{upto(lv):,}</td></tr>'
    s4 = f'''<section class="sec" id="step4" data-title="4. Doubling"><div class="wrap">
 {step_head(4, 'Every level <em>doubles</em>', 'Like a family tree turned upside down: 2 parents, 4 grandparents, 8 great-grandparents. Each row holds twice as many seats as the row above.')}
 <div class="split mx-dbl">
  <div class="tbl-wrap rv"><table class="tbl mx-tbl"><thead><tr><th>Level</th><th class="num">Seats on this level</th><th class="num">Total, Level 1 to here</th></tr></thead><tbody>{rows}</tbody></table></div>
  <div class="rv" style="--d:.08s">
   <div class="mx-big"><b data-count="8190">8,190</b><span>seats in 12 levels. That is how deep a 1 Star rank is paid.</span></div>
   <div class="mx-big"><b data-count="65534">65,534</b><span>seats in 15 levels (2 Stars).</span></div>
   <div class="mx-big"><b data-count="524286">524,286</b><span>seats in 18 levels (3 Stars).</span></div>
   <p class="muted">Big numbers, and they take time to fill. The doubling is why everyone in the plan benefits when anyone, anywhere above or below them, shares the card.</p>
  </div>
 </div>
</div></section>'''

    # step 5: the 0.1%
    ex = [(2, 'Level 1 full'), (14, 'Levels 1 to 3 full'), (126, 'Levels 1 to 6 full'), (8190, 'Levels 1 to 12 full')]
    exr = ''.join(f'<tr><td>{t}</td><td class="num">{n:,}</td><td class="num">${n * AVG:,}</td><td class="num"><b>{money(n * AVG * RATE)}</b></td></tr>' for n, t in ex)
    s5 = f'''<section class="sec" id="step5" data-title="5. The 0.1%"><div class="wrap">
 {step_head(5, 'How you earn: <em>0.1%</em>', 'For every $1,000 loaded onto cards in your paid levels, you get $1. Every month, for as long as they keep loading and you stay qualified.')}
 <div class="mx-coin rv">
  <div class="c1"><small>A cardholder in your matrix loads</small><b>$300</b></div>
  <div class="arr">{ic('arrow')}</div>
  <div class="c2"><small>0.1% of that goes to you</small><b>$0.30</b></div>
  <div class="arr">{ic('arrow')}</div>
  <div class="c3"><small>Now multiply by everyone in your paid levels</small><b>x 8,190</b><small>= $2,457 a month (Bellver's 1 Star example)</small></div>
 </div>
 <div class="split" style="align-items:start;margin-top:clamp(28px,4vw,44px)">
  <div class="rv">
   <h3 class="h3">The same 0.1%, at different sizes</h3>
   <p class="muted small">Example: everyone loads $300 a month, Bellver's own example figure.</p>
   <div class="tbl-wrap"><table class="tbl" style="min-width:0"><thead><tr><th>Your matrix</th><th class="num">Cardholders</th><th class="num">Loaded a month</th><th class="num">You get</th></tr></thead><tbody>{exr}</tbody></table></div>
   <p class="fine">Honest takeaway: in the early days, direct commissions are the bigger part. Monthly rewards grow with the size of your matrix.</p>
  </div>
  <div class="rv" style="--d:.08s">
   <h3 class="h3">Two ways you are paid</h3>
   <div class="tbl-wrap"><table class="tbl" style="min-width:0"><thead><tr><th></th><th>Direct commission</th><th>Monthly reward</th></tr></thead><tbody>
    <tr><td><b>For</b></td><td>Each card bought through your link</td><td>Every top-up in your paid levels</td></tr>
    <tr><td><b>How much</b></td><td>$10 Basic, $100 Premium, $200 Business, $400 Gold (Special Edition: $150, $300, $500)</td><td>0.1% per level</td></tr>
    <tr><td><b>How often</b></td><td>Once, plus 50% extra if they upgrade</td><td>Every month</td></tr>
    <tr><td><b>Who counts</b></td><td>Only people you refer</td><td>Everyone in your paid levels, spillover too</td></tr>
    <tr><td><b>Needs your own card?</b></td><td>No</td><td>Yes, Premium or higher, plus $100 a month</td></tr>
   </tbody></table></div>
   <div class="note g" style="margin-top:14px">{ic('info')}<span>Rewards are paid on <b>top-ups</b> (money loaded onto cards), not on card purchases. Bellver's videos say "spending"; the official plan says top-ups.</span></div>
  </div>
 </div>
</div></section>'''

    # calculator
    opts = ''.join(f'<option value="{lv}"{" selected" if lv == 12 else ""}>{m}: Levels 1 to {lv} ({upto(lv):,} seats)</option>' for lv, m in [(12, '1 Star'), (15, '2 Stars'), (18, '3 Stars'), (19, '4 Stars'), (20, '5 Stars')])
    chips = ''.join(f'<button type="button" data-n="{n}">{n:,}</button>' for n in [14, 100, 500, 1000, 8190])
    calc = f'''<section class="sec-tight" id="calculator" data-title="Calculator"><div class="wrap">
 <div class="sec-head rv"><h2 class="h2">Try your <em>own numbers</em></h2><p class="lead">Move the numbers and watch the 0.1% at work. This is a learning tool, not a promise.</p></div>
 {rewards_tool(H)}
</div></section>'''

    # why a 2x2 matrix
    WHY = [('rocket', 'A marketing strategy', 'Instead of paying for billboards, TV and social media ads, Bellver rewards the people who use the card and share it. Word of mouth, from people you already trust.'),
           ('coins', 'Paid from the top-up fee', 'Every top-up carries a 3.9% fee. Part of it is shared with the matrix, so monthly rewards come from real people using a real card.'),
           ('calendar', 'Rewards the builders', 'People who share the card and help others earn monthly income, again and again, for as long as they stay qualified and keep their seat.'),
           ('building', 'Built to last', 'A company that earns from everyday card use can pay its staff, its partners and its rewards, month after month. That is sustainability.'),
           ('users', 'Teamwork', 'Thanks to spillover, the people above you help fill your matrix, and you help the people below you. Nobody builds alone.'),
           ('tree', 'Simple to share', 'You only need two. Two is easy to explain, easy to copy and easy to teach.')]
    wc = ''.join(f'<div class="box rv mx-why" style="--d:{(i % 3) * .06:.2f}s"><span class="mx-wn">{i + 1}</span><div class="ico">{ic(k)}</div><h3 class="h3">{t}</h3><p>{d}</p></div>' for i, (k, t, d) in enumerate(WHY))
    s_why = f'''<section class="sec" id="why" data-title="Why a 2x2 matrix?"><div class="wrap">
 <div class="sec-head rv"><span class="badge gold">{ic('help')}The big question</span><h2 class="h2">Why a <em>2x2 matrix?</em></h2><p class="lead">Why would Bellver pay people like you and me? Six honest reasons.</p></div>
 <div class="grid3">{wc}</div>
 <div class="note g rv" style="margin-top:18px">{ic('wallet')}<span><b>Remember:</b> the $100 you load every month is not a subscription. It is your own money, on your own card, for your own life. The 3.9% top-up fee is the only cost, and it is what keeps the card and the rewards going.</span></div>
</div></section>'''

    # step 6: stars
    lad = ''
    for i, (c, name, st, card, needs, lv) in enumerate(RANKS):
        stars = '★' * st if st else '&nbsp;'
        depth = f'<b>{lv}</b><small>levels paid</small>'
        w = (lv / 20) * 100 if lv else 4
        lad += f'''<div class="mx-rung {c} rv" style="--d:{i * .05:.2f}s"><div class="nm"><span class="st">{stars}</span><b>{name}</b><small>{card}</small></div><ul>{''.join(f'<li>{x}</li>' for x in needs)}</ul><div class="dp">{depth}</div><div class="db" aria-hidden="true"><i style="width:{w:.0f}%"></i></div></div>'''
    s6 = f'''<section class="sec" id="step6" data-title="6. Stars"><div class="wrap">
 {step_head(6, 'Stars decide <em>how deep</em> you are paid', 'Think of a lift in a tall building. Your card decides how high the lift can go. Your stars decide which floors you have unlocked.')}
 <div class="mx-ladder">{lad}</div>
 <div class="grid2" style="margin-top:18px">
  <div class="note g rv">{ic('star')}<span><b>The easy rule:</b> the first star needs your own Premium card plus two people you refer directly who each buy Premium or higher. After that, every new star needs <b>two direct referrals who reached the star below</b>.</span></div>
  <div class="note rv" style="--d:.06s">{ic('info')}<span><b>Good to know:</b> everyone starts as a Member. Bellver has not republished its plan yet, so the level depths shown come from version 08/2026. Check your dashboard for the current numbers.</span></div>
 </div>
 <p class="fine rv">A Basic card earns direct commissions only, never monthly rewards. Upgrading later does not pay back rewards you missed before the upgrade.</p>
</div></section>'''

    # step 7: stay paid
    mo = [('ok', 'Month 1', 'Loaded $100', 'Paid'), ('ok', 'Month 2', 'Loaded $100', 'Paid'), ('miss', 'Month 3', 'Missed', 'That month lost'),
          ('ok', 'Month 4', 'Loaded $100', 'Paid again'), ('miss', 'Month 5', 'Missed', 'Lost'), ('miss', 'Month 6', 'Missed', 'Lost'), ('gone', 'Month 7', 'Missed, 3rd in a row', 'Seat gone for good')]
    tl = ''.join(f'<li class="{c} rv" style="--d:{i * .05:.2f}s"><small>{m}</small><i>{ic("check") if c == "ok" else ic("alert")}</i><b>{a}</b><span>{r}</span></li>' for i, (c, m, a, r) in enumerate(mo))
    s7 = f'''<section class="sec" id="step7" data-title="7. The $100 rule"><div class="wrap">
 {step_head(7, 'Stay paid: <em>the $100 rule</em>', 'One condition, every month: load at least $100 onto your own card.')}
 <ol class="mx-months">{tl}</ol>
 <div class="grid3" style="margin-top:22px">
  <div class="box rv"><div class="ico">{ic('wallet')}</div><h3 class="h3">It is not a fee</h3><p>The $100 is your own money on your own card, to spend however you like. A week of groceries covers it.</p><p class="muted small">The only cost is the 3.9% top-up fee. It keeps Bellver running long term: team, offices and payment partners.</p></div>
  <div class="box rv" style="--d:.06s"><div class="ico">{ic('alert')}</div><h3 class="h3">Miss one month</h3><p>You lose that month's rewards in full. Next month, load $100 and you are paid again.</p></div>
  <div class="box warn rv" style="--d:.12s"><div class="ico">{ic('lock')}</div><h3 class="h3">Miss three in a row</h3><p>Your seat in the matrix is gone for good. Rewards built up until then move up to the next qualified person. You cannot get the old seat back.</p></div>
 </div>
 <div class="note g rv" style="margin-top:16px">{ic('star')}<span><b>Get your own card first.</b> Your matrix seat starts when your card is bought. If someone you refer buys before you do, they are not placed in your matrix. You still earn their direct commission.</span></div>
</div></section>'''

    # payday
    pay = [('calendar', 'During the month', 'Cardholders in your levels load their cards.'), ('layers', 'Month end', 'Bellver adds it all up. Top-ups in the last 7 business days roll into next month.'),
           ('coins', 'The 15th', 'Payday. Rewards arrive in USDT.'), ('card', 'Your choice', 'Use it to fund your card, or withdraw once you have $100 or more.')]
    pt = ''.join(f'<li class="rv" style="--d:{i * .06:.2f}s"><span class="ic">{ic(k)}</span><b>{t}</b><p>{d}</p></li>' for i, (k, t, d) in enumerate(pay))
    s_pay = f'''<section class="sec-tight" id="payday" data-title="Payday"><div class="wrap">
 <div class="sec-head rv"><h2 class="h2">When the <em>money arrives</em></h2></div>
 <ol class="mx-pay">{pt}</ol>
</div></section>'''

    # myths
    myths = [
        ('"It is a binary plan. I only get paid on my weaker side."', 'No. There is no weaker leg. You earn on every cardholder in your paid levels, left and right.'),
        ('"I have to recruit lots of people."', 'Two direct referrals unlock your first star. More referrals mean more commissions, and they fill seats under you, but two is the starting point.'),
        ('"Signing up takes a seat."', 'Only cardholders take seats. A sign-up without a card is not placed.'),
        ('"A Basic card earns monthly rewards."', 'No. Basic earns direct commissions only. Monthly rewards start with Premium.'),
        ('"I can choose where people sit."', 'No. The system places everyone in the next free seat, top to bottom, left to right.'),
        ('"The $100 a month is a fee."', 'No. It is your own money, loaded onto your own card, yours to spend.'),
        ('"If I upgrade later, I get paid what I missed."', 'No. Rewards are not back-dated. They count from your upgrade onwards.'),
        ('"The big numbers are guaranteed."', 'No. Rewards depend on real top-ups. Bellver\'s examples assume every seat is full and everyone loads $300 a month.'),
    ]
    mc = ''.join(f'<details class="mx-myth rv" style="--d:{(i % 2) * .06:.2f}s"><summary><span class="x">{ic("alert")}Myth</span><b>{m}</b>{ic("chevron", "chev")}</summary><p><span class="ok">{ic("check")}Fact</span>{f}</p></details>' for i, (m, f) in enumerate(myths))
    s_myth = f'''<section class="sec" id="myths" data-title="Myths vs facts"><div class="wrap">
 <div class="sec-head rv"><h2 class="h2">Myths vs <em>facts</em></h2><p class="lead">The eight things people get wrong most often. Tap each one.</p></div>
 <div class="mx-myths">{mc}</div>
</div></section>'''

    # big numbers, honestly
    big = [(12, '1 Star'), (15, '2 Stars'), (18, '3 Stars')]
    br = ''.join(f'<tr><td><b>{m}</b>, Levels 1 to {lv}</td><td class="num">{upto(lv):,}</td><td class="num">${round(upto(lv) * AVG * RATE):,}</td></tr>' for lv, m in big)
    s_big = f'''<section class="sec-tight" id="examples" data-title="Big examples"><div class="wrap split">
 <div class="rv"><h2 class="h2">Bellver's big examples, <em>honestly</em></h2><p class="lead">The slides show $2,457, $19,660 and $157,286 a month. Here is what each one needs.</p>
  <ul class="checks mx-checks"><li><b>Every seat in those levels filled</b>, with no empty places.</li><li><b>Every cardholder loading $300</b> every month.</li><li><b>You qualified all month</b>, with $100 loaded onto your own card.</li></ul>
  <p class="muted">Bellver itself says these are examples, not a guarantee of income. Use them to understand the model, not to plan your budget.</p></div>
 <div class="tbl-wrap rv" style="--d:.08s"><table class="tbl" style="min-width:0"><thead><tr><th>Rank</th><th class="num">Cardholders needed</th><th class="num">Example a month</th></tr></thead><tbody>{br}</tbody></table></div>
</div></section>'''

    # quiz
    quiz = [
        ('How many seats sit directly under each person?', ['One', 'Two', 'Ten'], 1, 'Two. That is the "2x2" in the name.'),
        ('Your two Level 1 seats are full and you refer a third person. Where do they go?', ['They are turned away', 'Into the next free seat further down', 'Into your upline\'s matrix'], 1, 'The next free seat, top to bottom, left to right. You still earn the direct commission.'),
        ('A cardholder in your paid levels loads $1,000. What do you earn?', ['$1', '$10', '$100'], 0, '0.1% of $1,000 is $1.'),
        ('What does a Basic card earn?', ['Monthly rewards only', 'Direct commissions only', 'Both'], 1, 'Basic earns direct commissions only. Monthly rewards start with Premium.'),
        ('You forget to load $100 for three months in a row. What happens?', ['Nothing', 'You pay a penalty', 'You lose your seat for good'], 2, 'The seat is lost for good, and you cannot requalify for it.'),
        ('What is spillover?', ['People placed under you that you did not refer', 'A fee', 'Unused card balance'], 0, 'People your upline referred who land in free seats under you.'),
        ('Where do the monthly rewards come from?', ['New sign-ups paying a joining fee', 'A share of the top-up fee when people load their cards', 'Your $100 monthly subscription'], 1, 'Part of the 3.9% top-up fee is shared with the matrix. Your $100 is your own money, not a subscription.'),
    ]
    qd = json.dumps([{'q': q, 'a': a, 'c': c, 'e': e} for q, a, c, e in quiz], ensure_ascii=False)
    s_quiz = f'''<section class="sec-tight" id="quiz" data-title="Quiz"><div class="wrap">
 <div class="sec-head rv center"><h2 class="h2">Check <em>yourself</em></h2><p class="lead">Seven quick questions. Get them all right and you can explain the matrix to anyone.</p></div>
 <div class="panel mx-quiz rv" data-quiz><script type="application/json">{qd}</script>
  <div class="mx-qhead"><span data-qn>Question 1 of 7</span><span class="mx-qscore" data-qs>Score 0</span></div>
  <div class="meter"><i data-qbar></i></div>
  <h3 class="h3" data-qq></h3><div class="mx-qa" data-qa></div><p class="mx-qe" data-qe aria-live="polite"></p>
  <div class="btn-row" style="opacity:1;animation:none;margin-top:8px"><button class="btn btn-go btn-sm" type="button" data-qnext hidden>Next question</button></div>
 </div>
</div></section>'''

    # glossary
    gl = [('Matrix', 'The tree of seats under you.'), ('Level', 'One row of seats. Level 1 is right under you.'), ('Seat', 'A place in the matrix. One cardholder per seat.'),
          ('Upline', 'The people above you.'), ('Direct referral', 'Someone who joined through your own link.'), ('Spillover', 'People placed under you that someone above you referred.'),
          ('Top-up', 'Money loaded onto a card. Rewards are paid on these.'), ('Qualified', 'You loaded $100 onto your own card this month, so you are paid.'),
          ('Star (rank)', 'Your step on the ladder. It decides how many levels you are paid on.'), ('Direct commission', 'A one-time payment when someone you refer buys a card.'),
          ('Monthly reward', '0.1% per level on top-ups in your paid levels.'), ('Payday', 'The 15th of each month, paid in USDT.')]
    gc = ''.join(f'<div class="rv" style="--d:{(i % 3) * .05:.2f}s"><dt>{t}</dt><dd>{d}</dd></div>' for i, (t, d) in enumerate(gl))
    s_gl = f'''<section class="sec-tight" id="words" data-title="Glossary"><div class="wrap">
 <div class="sec-head rv"><h2 class="h2">The words, <em>in plain English</em></h2></div>
 <dl class="mx-gloss">{gc}</dl>
</div></section>'''

    # downloads
    s_dl = f'''<section class="sec-tight" id="download" data-title="PDF and picture"><div class="wrap">
 <div class="panel mx-dl rv">
  <a class="mx-dl-thumb" href="{L(SHARE_IMG, H)}" target="_blank" rel="noopener"><img src="{L('images/bellver-2x2-matrix-one-picture-640.webp', H)}" alt="The Bellver 2x2 matrix in one picture: two seats, reading order, doubling levels, 0.1% rewards and the $100 rule" width="640" height="800" loading="lazy"></a>
  <div>
   <span class="badge gold">{ic('download')}Free to keep and share</span>
   <h2 class="h2" style="margin-top:14px">Take it <em>with you</em></h2>
   <p class="lead">The full guide as a PDF to read offline, plus the whole matrix in one picture, sized for WhatsApp and social media.</p>
   <div class="btn-row" style="opacity:1;animation:none">
    <a class="btn btn-go" href="{L(GUIDE_PDF, H)}" download>{ic('download')}PDF guide (7 pages)</a>
    <a class="btn btn-ghost" href="{L(SHARE_IMG, H)}" download>{ic('download')}One-picture summary</a>
   </div>
   <p class="fine">Made by MTG from Bellver's official compensation plan (version 08/2026) and the October 2026 update. Also see the <a class="inl" href="{L(DOCS_PDF['plan'], H)}" target="_blank" rel="noopener">official compensation plan (PDF)</a>.</p>
  </div>
 </div>
</div></section>'''

    body = (top + s_quick + s1 + s2 + s3 + s4 + s5 + calc + s_why + s6 + s7 + s_pay + s_myth + s_big + cbp_band(H) + s_quiz + s_gl + s_dl
            + final_cta(H, 'Ready to take <span class="hap">your seat</span>?', 'Your seat starts when your card is bought. Premium or higher puts you in line for monthly rewards.',
                        f'<a class="btn btn-ghost" href="{L("rewards/", H)}">See the full rewards rules</a>')
            + help_band(H, 'Still unsure? Ask me.', "I'm MTG. Send me a WhatsApp and I'll draw your matrix with you, seat by seat, until it clicks.")
            + f'<script src="{asset("assets/matrix.js", H)}" defer></script>')

    faq_ld = {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": m.strip('"'), "acceptedAnswer": {"@type": "Answer", "text": f}} for m, f in myths]}
    learn_ld = {"@type": "LearningResource", "name": "The Bellver Card 2x2 Matrix Explained", "learningResourceType": "Guide", "educationalLevel": "Beginner",
                "inLanguage": "en", "author": {"@id": SITE + "/#mtg"}, "teaches": "How the Bellver Card 2x2 matrix fills, spillover, levels, 0.1% rewards, star ranks and the $100 monthly rule",
                "url": abs_url(H), "hasPart": {"@type": "DigitalDocument", "name": "Bellver 2x2 Matrix Explained (PDF)", "encodingFormat": "application/pdf", "url": abs_url(GUIDE_PDF)}}
    vid_ld = {"@type": "VideoObject", "name": "The Bellver 2x2 Matrix, Made Simple", "description": "An animated explainer in MTG's own voice: two seats under everyone, reading-order filling, spillover, doubling levels, the 0.1% reward, why a 2x2 matrix, star ranks and the $100 monthly rule.",
              "thumbnailUrl": abs_url('images/bellver-2x2-matrix-explainer-thumbnail.jpg'), "contentUrl": abs_url(VIDEO), "uploadDate": "2026-10-11", "duration": "PT8M45S", "inLanguage": "en", "author": {"@id": SITE + "/#mtg"}}
    return page(H, 'matrix', 'Bellver 2x2 Matrix Explained Simply: Spillover, Levels, 0.1% Rewards | MTG',
                'The Bellver Card 2x2 matrix in plain words: two seats under everyone, reading-order filling, spillover, doubling levels, 0.1% rewards, star ranks and the $100 rule. With a playable diagram, calculator, quiz and free PDF.',
                'images/og/og-bellver-matrix.jpg', 'The Bellver 2x2 matrix explained simply', body, ld_extra=[faq_ld, learn_ld, vid_ld], trail=trail)
