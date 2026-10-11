# -*- coding: utf-8 -*-
"""Renders the 2x2 Matrix Explained extras with Chromium (Playwright):
   docs/bellver-2x2-matrix-explained-by-mtg.pdf   (6-page plain-words guide)
   images/bellver-2x2-matrix-one-picture.png      (1080x1350 share picture) + -640.webp
   images/og/og-bellver-matrix.jpg                (1200x630 social preview)
Run: python3 mx_assets.py   (needs the Anton and Manrope woff2 files in /tmp/fontsrc)"""
import os, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image
from playwright.sync_api import sync_playwright
import p_matrix as M

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..'))
FA = 'file:///tmp/fontsrc/fontsource-anton-5.3.0/package/files/anton-latin-400-normal.woff2'
FM = 'file:///tmp/fontsrc/manrope/package/files/manrope-latin-{}-normal.woff2'
LOGO = 'file://' + os.path.join(ROOT, 'images', 'bellver-cards-logo-white.webp')
MTG = 'file://' + os.path.abspath(os.path.join(ROOT, '..', '..', 'images', 'mtg-profile.jpg'))
URL = 'musathegiant.com/cards/bellvercards/matrix'
FONTS = f"""@font-face{{font-family:Anton;src:url({FA})}}""" + ''.join(f"@font-face{{font-family:Manrope;font-weight:{w};src:url({FM.format(w)})}}" for w in (400, 700, 800))

TREE_CSS = """
.mx-tree{width:100%;height:auto;overflow:visible}
.mx-tree text{text-anchor:middle;font:800 13px Manrope;pointer-events:none}
.mx-tree .rowlab{text-anchor:start;font:800 11px Manrope;letter-spacing:.1em}
.mx-tree .drop{fill:none;stroke:#2f7fe0;stroke-width:2.5;stroke-dasharray:7 6}
.mx-tree .tag{text-anchor:start;font-size:13px}
"""
LIGHT = TREE_CSS + """
.mx-tree .ln line{stroke:#b9d3c4;stroke-width:2}
.mx-tree .rowlab{fill:#7c9187}
.mx-tree .you circle{fill:#0d3a24;stroke:#1d8a55;stroke-width:3}.mx-tree .you text{fill:#fff;font-size:12px}
.mx-tree .up circle{fill:#dbe9fb;stroke:#2f7fe0;stroke-width:3}.mx-tree .up text{fill:#173a63;font-size:11px}
.mx-tree .seat circle{fill:#e8f4ed;stroke:#1d8a55;stroke-width:2}.mx-tree .seat text{fill:#0d3a24}
.mx-tree .seat.spill circle{fill:#2f7fe0;stroke:#173a63}.mx-tree .seat.spill text{fill:#fff}
.mx-spill .seat:not(.full):not(.spill) circle{fill:#fff;stroke-dasharray:4 4;stroke:#9db8a9}
.mx-tree .tag{fill:#2f7fe0}
.mx-tree .mine circle{fill:#fcbe25;stroke:#a8670d}
"""
DARK = TREE_CSS + """
.mx-tree .ln line{stroke:rgba(150,255,200,.3);stroke-width:2}
.mx-tree .rowlab{fill:#6f857a}
.mx-tree .you circle{fill:#0d3a24;stroke:#34cc88;stroke-width:3}.mx-tree .you text{fill:#fff;font-size:12px}
.mx-tree .seat circle{fill:#1a5c3c;stroke:#34cc88;stroke-width:2}.mx-tree .seat text{fill:#fff}
"""


def numbered(depth=3):
    return M.tree_svg(depth, 480, numbered=True)


# ---------------------------------------------------------------- PDF
def pdf_html():
    rk_at = {12: '1 Star', 15: '2 Stars', 18: '3 Stars', 19: '4 Stars', 20: '5 Stars'}
    def lvt(a, b):
        r = ''.join(f'<tr class="{"hit" if lv in rk_at else ""}"><td>Level {lv}{(" <small>" + rk_at[lv] + "</small>") if lv in rk_at else ""}</td><td>{M.seats(lv):,}</td><td>{M.upto(lv):,}</td></tr>' for lv in range(a, b + 1))
        return f'<table class="lt"><thead><tr><th>Level</th><th>Seats</th><th>Total so far</th></tr></thead><tbody>{r}</tbody></table>'
    lvrows = f'<div class="two" style="gap:5mm">{lvt(1, 10)}{lvt(11, 20)}</div>'
    ex = ''.join(f'<tr><td>{t}</td><td>{n:,}</td><td>${n * 300:,}</td><td><b>{M.money(n * 300 * .001)}</b></td></tr>' for n, t in [(2, 'Level 1 full'), (14, 'Levels 1 to 3 full'), (126, 'Levels 1 to 6 full'), (8190, 'Levels 1 to 12 full'), (65534, 'Levels 1 to 15 full')])
    rk = ''.join(f'<tr><td><b>{n}</b> <span class="st">{"★" * s}</span></td><td>{c}</td><td>{"<br>".join(needs)}</td><td class="c"><b>{lv}</b></td></tr>' for _, n, s, c, needs, lv in M.RANKS)
    myths = [('It is a binary plan, paid on the weaker side.', 'No weaker leg. You earn on everyone in your paid levels, left and right.'),
             ('I have to recruit lots of people.', 'Two direct referrals unlock your first star.'),
             ('Signing up takes a seat.', 'Only cardholders take seats.'),
             ('A Basic card earns monthly rewards.', 'Basic earns direct commissions only.'),
             ('I can choose where people sit.', 'The system uses the next free seat.'),
             ('The $100 a month is a fee.', 'It is your own money on your own card.'),
             ('Upgrading later pays what I missed.', 'Rewards are not back-dated.'),
             ('The big numbers are guaranteed.', 'Rewards depend on real top-ups.')]
    my = ''.join(f'<tr><td>✗ {m}</td><td>✓ {f}</td></tr>' for m, f in myths)
    gl = [('Matrix', 'The tree of seats under you.'), ('Level', 'One row of seats. Level 1 is right under you.'), ('Seat', 'A place in the matrix. One cardholder per seat.'),
          ('Upline', 'The people above you.'), ('Direct referral', 'Someone who joined through your own link.'), ('Spillover', 'People placed under you that someone above you referred.'),
          ('Top-up', 'Money loaded onto a card. Rewards are paid on these.'), ('Qualified', 'You loaded $100 onto your own card this month.'),
          ('Star (rank)', 'Decides how many levels you are paid on.'), ('Direct commission', 'One-time payment when someone you refer buys a card.'),
          ('Monthly reward', '0.1% per level on top-ups in your paid levels.'), ('Payday', 'The 15th of each month, in USDT.')]
    gd = ''.join(f'<div><b>{t}</b><span>{d}</span></div>' for t, d in gl)
    foot = lambda n: f'<div class="ft"><span>The Bellver 2x2 Matrix, Explained Simply · by Affiliate MTG 👑</span><span>{n} / 7</span></div>'
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>{FONTS}
@page{{size:A4;margin:0}}
*{{box-sizing:border-box}}
body{{margin:0;font:400 10.4pt/1.45 Manrope;color:#11211a;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.pg{{position:relative;width:210mm;height:297mm;padding:14mm 15mm 20mm;overflow:hidden;page-break-after:always;background:#fff}}
.pg:last-child{{page-break-after:auto}}
h1,h2{{font-family:Anton;font-weight:400;text-transform:uppercase;letter-spacing:.01em;margin:0;color:#0b2418;line-height:1}}
h2{{font-size:23pt;margin:0 0 2.5mm}} h2 em,h1 em{{font-style:normal;color:#1d8a55}}
h3{{font-size:11.5pt;margin:4mm 0 1.5mm;color:#0b2418}}
.step{{display:inline-block;padding:1mm 3mm;border-radius:99px;background:#fff4d6;color:#8a5a00;font-weight:800;font-size:8pt;letter-spacing:.1em;text-transform:uppercase;margin-bottom:2mm}}
p{{margin:0 0 2mm}} .lead{{font-size:11pt;color:#2d4438}}
ul{{margin:0 0 3mm;padding-left:5mm}} li{{margin:0 0 1.2mm}}
table{{width:100%;border-collapse:collapse;font-size:9pt;margin:2mm 0 3mm}}
.lt td small{{color:#a8670d;font-weight:800;margin-left:1.5mm}}
th{{text-align:left;background:#0b2418;color:#fff;font-weight:800;padding:1.6mm 3mm}}
td{{padding:1.3mm 3mm;border-bottom:1px solid #dce9e1;vertical-align:top}}
tr.hit td{{background:#fff7df;font-weight:800}}
td.c{{text-align:center;font-size:13pt}}
.st{{color:#d99a0b}}
.box{{border:1.5px solid #cfe3d7;border-radius:4mm;padding:4mm 5mm;margin:3mm 0;background:#f5faf7}}
.warn{{border-color:#f3d37a;background:#fffaeb}}
.two{{display:grid;grid-template-columns:1fr 1fr;gap:6mm;align-items:start}}
.fig{{border:1.5px solid #dce9e1;border-radius:4mm;padding:3mm 4mm;background:#fbfdfc}}
.cap{{font-size:8.6pt;color:#5b7166;text-align:center;margin-top:1mm}}
.ft{{position:absolute;left:16mm;right:16mm;bottom:9mm;display:flex;justify-content:space-between;font-size:8pt;color:#7c9187;border-top:1px solid #e3ede7;padding-top:2mm}}
.five{{display:grid;grid-template-columns:repeat(5,1fr);gap:2.5mm;margin:3mm 0}}
.five div{{border-radius:3mm;padding:3mm;background:#0b2418;color:#cfe3d7;font-size:8.6pt;line-height:1.4}}
.five b{{display:block;font-family:Anton;font-weight:400;font-size:17pt;color:#34cc88;line-height:1}}
.five strong{{display:block;color:#fff;font-size:9.4pt;margin:1.5mm 0 1mm}}
.flow{{display:grid;grid-template-columns:1fr auto 1fr auto 1.3fr;gap:3mm;align-items:center;margin:3mm 0}}
.flow div{{border-radius:3mm;border:1.5px solid #cfe3d7;padding:3mm;text-align:center;font-size:8.6pt;color:#5b7166}}
.flow b{{display:block;font-family:Anton;font-weight:400;font-size:20pt;color:#0b2418;line-height:1.1}}
.flow .y b{{color:#c98a00}} .flow .g b{{color:#1d8a55}} .flow i{{font-style:normal;font-size:16pt;color:#1d8a55}}
.months{{display:grid;grid-template-columns:repeat(7,1fr);gap:1.5mm;margin:2mm 0 3mm}}
.months div{{border-radius:2.5mm;padding:2mm 1mm;text-align:center;font-size:7.6pt;border:1.5px solid #cfe3d7}}
.months b{{display:block;font-size:13pt}} .months .ok b{{color:#1d8a55}} .months .ms{{border-color:#f3d37a;background:#fffaeb}} .months .ms b{{color:#c98a00}}
.months .gn{{border-color:#e5484d;background:#fdeeee}} .months .gn b{{color:#c42e33}}
.pay{{display:grid;grid-template-columns:repeat(4,1fr);gap:2mm}}
.pay div{{border-radius:3mm;background:#f0f7f3;padding:3mm;font-size:8.6pt}} .pay b{{display:block;font-size:9.6pt;color:#0b2418}}
.gl{{display:grid;grid-template-columns:1fr 1fr;gap:1.6mm 6mm;font-size:9pt}} .gl b{{display:block;color:#1d8a55}}
.cover{{background:radial-gradient(120% 80% at 80% 0%,#1e6e46,transparent 60%),linear-gradient(170deg,#06150d,#020c06);color:#dfeee6;padding:20mm 18mm}}
.cover h1{{color:#fff;font-size:54pt;line-height:.95;margin-top:16mm}} .cover h1 em{{color:#34cc88}}
.cover .lead{{color:#c3d2ca;font-size:13.5pt;max-width:150mm;margin-top:6mm}}
.cover .fig{{background:rgba(255,255,255,.03);border-color:rgba(150,255,200,.18);margin-top:10mm;padding:6mm 10mm}}
.cover .by{{position:absolute;left:18mm;right:18mm;bottom:16mm;display:flex;align-items:center;gap:5mm;font-size:10pt;color:#a9bdb3}}
.cover .by img{{width:16mm;height:16mm;border-radius:50%;border:2px solid #34cc88;object-fit:cover}}
.cover .by b{{display:block;color:#fff;font-size:12pt}}
.cover .logo{{width:55mm}}
.chk{{display:grid;grid-template-columns:repeat(3,1fr);gap:3mm;margin-top:3mm}}
.chk div{{border-radius:3mm;border:1.5px solid #cfe3d7;padding:3mm;font-size:9pt}} .chk b{{display:block;color:#0b2418}}
.yel{{color:#c98a00}}
.whyfig svg{{height:62mm;width:auto;margin:0 auto;display:block}}
.why{{display:grid;grid-template-columns:1fr 1fr;gap:4mm;margin-top:4mm}}
.why div{{position:relative;border:1.5px solid #cfe3d7;border-radius:4mm;padding:4mm 5mm 4mm 15mm;background:#f5faf7;font-size:9.6pt}}
.why b{{position:absolute;left:4mm;top:3.5mm;font-family:Anton;font-weight:400;font-size:20pt;color:#1d8a55}}
.why strong{{display:block;font-size:11pt;color:#0b2418;margin-bottom:1mm}}
{LIGHT}
.cover .mx-tree .ln line{{stroke:rgba(150,255,200,.3)}} .cover .mx-tree .seat circle{{fill:#1a5c3c;stroke:#34cc88}} .cover .mx-tree .seat text{{fill:#fff}} .cover .mx-tree .rowlab{{fill:#7c9187}}
</style></head><body>

<section class="pg cover">
 <img class="logo" src="{LOGO}" alt="">
 <h1>The 2x2 matrix<br><em>made simple</em></h1>
 <p class="lead">The Bellver Card rewards plan in plain words. Seven short steps, clear pictures and honest numbers. Read it once and you can explain it to anyone.</p>
 <div class="fig">{numbered(3)}</div>
 <div class="by"><img src="{MTG}" alt=""><div><b>MTG 👑 | Your Digital Architect</b>Independent Bellver affiliate guide · {URL}<br>Based on Bellver's compensation plan (version 08/2026) and the October 2026 update.</div></div>
</section>

<section class="pg">
 <h2>The 30-second <em>version</em></h2>
 <div class="five">
  <div><b>1</b><strong>Two seats under everyone</strong>That is what 2x2 means.</div>
  <div><b>2</b><strong>Reading order</strong>Seats fill top to bottom, left to right. No gaps.</div>
  <div><b>3</b><strong>Every row doubles</strong>2, 4, 8, 16. Twelve rows hold 8,190 people.</div>
  <div><b>4</b><strong>You earn 0.1% per level</strong>On every top-up in the rows you qualify for.</div>
  <div><b>5</b><strong>Load $100 a month</strong>Onto your own card. It stays your money.</div>
 </div>
 <div class="two" style="margin-top:6mm">
  <div><span class="step">Step 1 of 7</span><h2 style="font-size:20pt">Two seats <em>under everyone</em></h2>
   <ul><li><b>"2x2" means two by two.</b> Every person has two seats directly under them.</li><li><b>The row right under you is Level 1.</b> The row under that is Level 2.</li><li><b>Your first two referrals</b> usually sit in your Level 1 seats.</li><li><b>Only cardholders take a seat.</b> Registering alone does not.</li></ul></div>
  <div class="fig">{M.tree_svg(1, 480, labels={1: 'A', 2: 'B'})}<p class="cap">You, with seat A on the left and seat B on the right.</p></div>
 </div>
 <span class="step" style="margin-top:4mm">Step 2 of 7</span><h2 style="font-size:20pt">Seats fill in <em>reading order</em></h2>
 <div class="two">
  <div class="fig">{numbered(3)}<p class="cap">The numbers show the order seats are filled.</p></div>
  <div><ul><li><b>Top row first, left to right,</b> then the next row. Like reading a page.</li><li><b>No gaps, ever.</b> The system always uses the next free seat. Nobody can pick a seat or skip the line.</li><li><b>Your 3rd, 4th or 10th referral</b> goes to the next free seat further down. Nobody you bring is wasted.</li><li><b>You still get your commission</b> for everyone you refer, wherever they are placed.</li></ul></div>
 </div>
 {foot(2)}
</section>

<section class="pg">
 <span class="step">Step 3 of 7</span><h2>Spillover: <em>help from above</em></h2>
 <div class="two">
  <div><ul><li><b>Spillover means people under you that you did not refer.</b></li><li><b>They come from your upline</b> (the people above you) who refer more than two. Their extras flow down into the next free seats, and some land under you.</li><li><b>Their top-ups count for your rewards</b> when they sit in a level you qualify for.</li><li><b>No direct commission for you</b> on spillover. That goes to whoever referred them.</li></ul>
  <div class="box"><b>Not a binary plan.</b> There is no "weaker leg". You earn on everyone in your paid levels, left and right.</div></div>
  <div class="fig">{M.spill_svg()}<p class="cap">Your upline already has two people (you and B). Their third referral takes the first free seat on the next row: under you.</p></div>
 </div>
 <span class="step" style="margin-top:3mm">Step 4 of 7</span><h2>Every level <em>doubles</em></h2>
 <p class="lead">Like a family tree turned upside down: 2 parents, 4 grandparents, 8 great-grandparents.</p>
 {lvrows}
 {foot(3)}
</section>

<section class="pg">
 <span class="step">Step 5 of 7</span><h2>How you earn: <em>0.1%</em></h2>
 <p class="lead">For every <b>$1,000</b> loaded onto cards in your paid levels, you get <b>$1</b>. Every month, as long as they keep loading and you stay qualified.</p>
 <div class="flow"><div>A cardholder in your matrix loads<b>$300</b></div><i>→</i><div class="y">0.1% of that goes to you<b>$0.30</b></div><i>→</i><div class="g">Multiply by everyone in your paid levels<b>x 8,190</b>= $2,457 a month (Bellver's 1 Star example)</div></div>
 <h3>The same 0.1% at different sizes (everyone loads $300 a month)</h3>
 <table><thead><tr><th>Your matrix</th><th>Cardholders</th><th>Loaded a month</th><th>You get a month</th></tr></thead><tbody>{ex}</tbody></table>
 <div class="box warn"><b>Honest takeaway.</b> Early on, direct commissions are the bigger part. Monthly rewards grow with the size of your matrix. Bellver's big examples assume every seat is full and every cardholder loads $300 every month. Bellver itself calls them examples, not a guarantee of income.</div>
 <h3>Two ways you are paid</h3>
 <table><thead><tr><th></th><th>Direct commission</th><th>Monthly reward</th></tr></thead><tbody>
  <tr><td><b>For</b></td><td>Each card bought through your link</td><td>Every top-up in your paid levels</td></tr>
  <tr><td><b>How much</b></td><td>$10 Basic, $100 Premium, $200 Business, $400 Gold. Special Edition: $150, $300, $500</td><td>0.1% per level</td></tr>
  <tr><td><b>How often</b></td><td>Once, plus 50% extra if they upgrade</td><td>Every month</td></tr>
  <tr><td><b>Who counts</b></td><td>Only people you refer</td><td>Everyone in your paid levels, spillover too</td></tr>
  <tr><td><b>Needs your own card?</b></td><td>No</td><td>Yes: Premium or higher, plus $100 a month</td></tr></tbody></table>
 <p style="font-size:9pt;color:#5b7166">Rewards are paid on top-ups (money loaded onto cards), not on card purchases. Bellver's videos say "spending"; the official plan says top-ups.</p>
 {foot(4)}
</section>

<section class="pg">
 <span class="step">Step 6 of 7</span><h2>Stars decide <em>how deep</em> you are paid</h2>
 <p class="lead">Think of a lift in a tall building. Your card decides how high the lift can go. Your stars decide which floors you have unlocked.</p>
 <table><thead><tr><th>Rank</th><th>Your own card</th><th>What you need</th><th>Levels paid</th></tr></thead><tbody>{rk}</tbody></table>
 <p style="font-size:9pt;color:#5b7166"><b>October 2026 update:</b> everyone now starts as a Member and the old "Premium" step is gone. Bellver has not republished its plan yet, so the level depths come from version 08/2026. Check your dashboard for the current numbers. A Basic card earns direct commissions only. Upgrading later does not pay back rewards you missed.</p>
 <span class="step" style="margin-top:2mm">Step 7 of 7</span><h2>Stay paid: <em>the $100 rule</em></h2>
 <div class="months"><div class="ok">Month 1<b>✓</b>Paid</div><div class="ok">Month 2<b>✓</b>Paid</div><div class="ms">Month 3<b>!</b>Missed: lost</div><div class="ok">Month 4<b>✓</b>Paid again</div><div class="ms">Month 5<b>!</b>Lost</div><div class="ms">Month 6<b>!</b>Lost</div><div class="gn">Month 7<b>✗</b>3rd miss in a row: seat gone</div></div>
 <ul><li><b>It is not a fee.</b> The $100 is your own money on your own card. The only cost is the 3.9% top-up fee, which keeps Bellver running long term.</li><li><b>Miss one month:</b> you lose that month's rewards in full.</li><li><b>Miss three in a row:</b> your seat is gone for good, and you cannot get it back.</li><li><b>Get your own card first.</b> Your seat starts when your card is bought. If someone you refer buys before you, they are not placed in your matrix.</li></ul>
 <h3>When the money arrives</h3>
 <div class="pay"><div><b>During the month</b>Cardholders in your levels load their cards.</div><div><b>Month end</b>Top-ups in the last 7 business days roll into next month.</div><div><b>The 15th</b>Payday. Rewards arrive in USDT.</div><div><b>Your choice</b>Fund your card, or withdraw once you have $100 or more.</div></div>
 {foot(5)}
</section>

<section class="pg">
 <h2>Why a <em>2x2 matrix?</em></h2>
 <p class="lead">Why would Bellver pay people like you and me? Six honest reasons.</p>
 <div class="why">
  <div><b>1</b><strong>A marketing strategy</strong>Instead of paying for billboards, TV and social media ads, Bellver rewards the people who use the card and share it. Word of mouth, from people you already trust.</div>
  <div><b>2</b><strong>Paid from the top-up fee</strong>Every top-up carries a 3.9% fee. Part of it is shared with the matrix, so monthly rewards come from real people using a real card.</div>
  <div><b>3</b><strong>Rewards the builders</strong>People who share the card and help others earn monthly income, again and again, for as long as they stay qualified and keep their seat.</div>
  <div><b>4</b><strong>Built to last</strong>A company that earns from everyday card use can pay its staff, its partners and its rewards, month after month. That is sustainability.</div>
  <div><b>5</b><strong>Teamwork</strong>Thanks to spillover, the people above you help fill your matrix, and you help the people below you. Nobody builds alone.</div>
  <div><b>6</b><strong>Simple to share</strong>You only need two. Two is easy to explain, easy to copy and easy to teach.</div>
 </div>
 <div class="box warn" style="margin-top:6mm"><b>Remember:</b> the $100 you load every month is not a subscription. It is your own money, on your own card, for your own life. The 3.9% top-up fee is the only cost, and it is what keeps the card and the rewards going.</div>
 <div class="fig whyfig" style="margin-top:6mm">{M.spill_svg()}<p class="cap">Teamwork in one picture: your upline's extra referral lands in the first free seat under you.</p></div>
 {foot(6)}
</section>

<section class="pg">
 <h2>Myths vs <em>facts</em></h2>
 <table><thead><tr><th>Myth</th><th>Fact</th></tr></thead><tbody>{my}</tbody></table>
 <h2 style="font-size:20pt;margin-top:4mm">The words, <em>in plain English</em></h2>
 <div class="gl">{gd}</div>
 <h2 style="font-size:20pt;margin-top:6mm">Your <em>next step</em></h2>
 <div class="chk"><div><b>1. Order your card</b>app.bellvercards.com?ref=mtg<br><span class="yel">Premium or higher for rewards</span></div><div><b>2. Play with the matrix</b>{URL}</div><div><b>3. Questions? Ask MTG</b>WhatsApp: wa.me/27721714626</div></div>
 <p style="margin-top:6mm;font-size:8.2pt;color:#5b7166">Bellver Card is a product of Bellver Markets Ltd. This guide is made independently by MTG, a Bellver affiliate, and is not an official Bellver document. MTG may earn a commission if you order through his link, at no extra cost to you. Facts come from Bellver's compensation plan (version 08/2026), presentation, videos and the October 2026 update, and can change: Bellver can amend the plan with one month's notice. Rewards depend on real card activity and are never guaranteed. Nothing here is financial, tax or legal advice. Always do your own research.</p>
 <p style="font-size:10pt;margin-top:4mm"><b>Let's Get This Crypto! 💰 Crypto-Regards, MTG 👑</b></p>
 {foot(7)}
</section>
</body></html>'''


# ---------------------------------------------------------------- share picture 1080x1350
def share_html():
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>{FONTS}
*{{box-sizing:border-box}} body{{margin:0}}
.c{{width:1080px;height:1350px;padding:64px 70px;background:radial-gradient(900px 600px at 85% -5%,rgba(52,204,136,.28),transparent 60%),linear-gradient(170deg,#07170e,#020c06);color:#dfeee6;font-family:Manrope;position:relative;overflow:hidden}}
.top{{display:flex;justify-content:space-between;align-items:center}} .top img{{width:230px}} .top span{{font-weight:800;color:#a9bdb3;font-size:22px}}
h1{{font:400 92px/0.95 Anton;text-transform:uppercase;color:#fff;margin:34px 0 0}} h1 em{{font-style:normal;color:#34cc88}}
.sub{{font-size:28px;color:#c3d2ca;margin:16px 0 0}}
.fig svg{{height:350px;width:auto;margin:0 auto}}
.fig{{margin:24px 0 22px;padding:18px 30px 8px;border:1px solid rgba(150,255,200,.18);border-radius:30px;background:rgba(255,255,255,.025)}}
.pts{{display:grid;grid-template-columns:1fr 1fr;gap:16px}}
.pts div{{display:flex;gap:16px;align-items:flex-start;padding:14px 18px;border-radius:20px;background:rgba(12,26,18,.85);border:1px solid rgba(150,255,200,.12)}}
.pts b{{font:400 46px/1 Anton;color:#34cc88;min-width:34px}} .pts p{{margin:0;font-size:22px;line-height:1.35}} .pts strong{{color:#fff;display:block;font-size:24px}}
.pts .w{{grid-column:1/-1;border-color:rgba(252,190,37,.45);background:rgba(252,190,37,.07)}} .pts .w b{{color:#fcbe25}}
.ft{{position:absolute;left:70px;right:70px;bottom:46px;display:flex;justify-content:space-between;align-items:flex-end;font-size:20px;color:#8ea39a}}
.ft strong{{display:block;color:#fff;font-size:24px}} .ft .y{{color:#fcbe25;font-weight:800}}
{DARK}
</style></head><body><div class="c">
 <div class="top"><img src="{LOGO}" alt=""><span>by Affiliate MTG 👑</span></div>
 <h1>The 2x2 matrix<br><em>in one picture</em></h1>
 <p class="sub">How Bellver Card monthly rewards work, in plain words.</p>
 <div class="fig">{numbered(3)}</div>
 <div class="pts">
  <div><b>1</b><p><strong>Two seats under everyone</strong>That is what 2x2 means.</p></div>
  <div><b>2</b><p><strong>Seats fill in reading order</strong>Top to bottom, left to right.</p></div>
  <div><b>3</b><p><strong>Every row doubles</strong>2, 4, 8... 12 rows = 8,190 seats.</p></div>
  <div><b>4</b><p><strong>0.1% of every top-up</strong>$1 for every $1,000 loaded in your paid levels.</p></div>
  <div class="w"><b>5</b><p><strong>Load $100 a month onto your own card to stay paid</strong>It stays your money. Miss 3 months in a row and the seat is gone.</p></div>
 </div>
 <div class="ft"><div><strong>Learn it step by step:</strong>{URL}</div><div class="y">Rewards depend on real card<br>activity. Not guaranteed.</div></div>
</div></body></html>'''


# ---------------------------------------------------------------- OG 1200x630
def og_html():
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>{FONTS}
*{{box-sizing:border-box}} body{{margin:0}}
.c{{width:1200px;height:630px;padding:54px 64px;background:radial-gradient(760px 520px at 88% 0%,rgba(52,204,136,.28),transparent 62%),linear-gradient(170deg,#06150d,#020c06);font-family:Manrope;position:relative;overflow:hidden;display:grid;grid-template-columns:560px 1fr;gap:30px}}
.l img{{width:250px}} .l small{{display:inline-block;margin-left:12px;color:#c3d2ca;font-weight:700;font-size:24px;vertical-align:14px}}
h1{{font:400 92px/1 Anton;text-transform:uppercase;color:#fff;margin:44px 0 0}} h1 em{{font-style:normal;color:#34cc88}}
p{{color:#c3d2ca;font-size:27px;font-weight:600;line-height:1.4;margin:18px 0 0}}
.u{{position:absolute;left:64px;bottom:44px;color:#8ea39a;font-weight:700;font-size:22px}} .u i{{display:inline-block;width:12px;height:12px;border-radius:3px;background:#fcbe25;margin-right:10px}}
.r{{align-self:center;padding:20px 10px 4px;border-radius:28px;border:1px solid rgba(150,255,200,.2);background:rgba(255,255,255,.03)}}
{DARK}
</style></head><body><div class="c">
 <div class="l"><img src="{LOGO}" alt=""><small>by Affiliate MTG</small><h1>The 2x2 matrix<br><em>made simple</em></h1><p>Seats, spillover, levels, the 0.1% and the $100 rule, in plain words.</p></div>
 <div class="r">{numbered(3)}</div>
 <div class="u"><i></i>{URL}</div>
</div></body></html>'''


def main():
    tmp = tempfile.mkdtemp()
    out_pdf = os.path.join(ROOT, M.GUIDE_PDF)
    out_png = os.path.join(ROOT, M.SHARE_IMG)
    out_og = os.path.join(ROOT, 'images', 'og', 'og-bellver-matrix.jpg')
    with sync_playwright() as p:
        b = p.chromium.launch()
        def page_for(html, w, h):
            f = os.path.join(tmp, f'{w}x{h}.html'); open(f, 'w', encoding='utf-8').write(html)
            pg = b.new_page(viewport={'width': w, 'height': h}); pg.goto('file://' + f); pg.wait_for_timeout(900); return pg
        pg = page_for(pdf_html(), 794, 1123)
        pg.pdf(path=out_pdf, format='A4', print_background=True, prefer_css_page_size=True); pg.close()
        pg = page_for(share_html(), 1080, 1350); pg.screenshot(path=out_png); pg.close()
        pg = page_for(og_html(), 1200, 630); tmp_og = os.path.join(tmp, 'og.png'); pg.screenshot(path=tmp_og); pg.close()
        b.close()
    im = Image.open(out_png).convert('RGB'); im.save(out_png, optimize=True)
    im.resize((640, 800), Image.LANCZOS).save(out_png.replace('.png', '-640.webp'), 'WEBP', quality=86)
    Image.open(tmp_og).convert('RGB').save(out_og, 'JPEG', quality=88, optimize=True, progressive=True)
    for f in (out_pdf, out_png, out_og):
        print(os.path.relpath(f, ROOT), os.path.getsize(f) // 1024, 'KB')


if __name__ == '__main__':
    main()
