# -*- coding: utf-8 -*-
"""The two-page Bellver Card quick guide (PDF) for the Downloads page (MTG, 27 Oct 2026).
One copy per person: MTG's (docs/bellver-card-quick-guide-by-mtg.pdf) and one per team member
(docs/quick-guide/bellver-card-quick-guide-<slug>.pdf) with that member's own name, order link, WhatsApp and site.
A member's copy never mentions MTG or his links.

   python3 quickguide.py          -> (re)makes every copy whose details or wording changed
   python3 quickguide.py --force  -> remakes them all
build.py calls ensure() before building, so a new team member gets their copy automatically.
Figures: Bellver's price list and compensation plan (08/2026) with the October 2026 update (3.9% top-up fee
taken from the amount loaded, Special Edition $370). Check prices/ and rewards/ when Bellver changes anything."""
import base64, hashlib, io, json, os, sys, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.abspath(os.path.join(HERE, '..'))           # musathegiant/cards/bellvercards
STAMPS = os.path.join(HERE, '.quickguide-stamps.json')
MTG_PDF = 'docs/bellver-card-quick-guide-by-mtg.pdf'
MTG_PREVIEW = 'images/bellver-card-quick-guide-preview'   # .webp, page 1, for the Downloads page
CHECKED = '27 Oct 2026'


def member_pdf(slug):
    return f'docs/quick-guide/bellver-card-quick-guide-{slug}.pdf'


def member_preview(slug):
    return f'images/quick-guide/bellver-card-quick-guide-{slug}-preview'


def people():
    """Everyone who gets a copy: MTG first, then each team member in team.json."""
    sys.path.insert(0, HERE)
    with open(os.path.join(HERE, 'team.json'), encoding='utf-8') as f:
        team = json.load(f)['members']
    out = [{'key': 'mtg', 'mtg': True, 'name': 'MTG', 'by': 'Independent guide by MTG 👑 | Your Digital Architect',
            'ref': 'https://app.bellvercards.com?ref=mtg', 'site': 'https://bellveraffiliates.com/', 'wa': '+27 72 171 4626',
            'wa_url': 'https://wa.me/27721714626', 'pdf': MTG_PDF, 'preview': MTG_PREVIEW}]
    for m in team:
        digits = ''.join(c for c in (m.get('whatsapp') or '') if c.isdigit())
        out.append({'key': m['slug'], 'mtg': False, 'name': m['name'], 'first': m.get('short') or m['name'].split()[0],
                    'by': 'Independent guide shared by ' + m['name'], 'ref': m['ref'],
                    'site': 'https://bellveraffiliates.com/' + m['slug'] + '/',
                    'wa': ('+' + digits) if digits else '', 'wa_url': ('https://wa.me/' + digits) if digits else '',
                    'telegram': m.get('telegram', ''), 'group': m.get('telegram_group') or m.get('whatsapp_group', ''),
                    'pdf': member_pdf(m['slug']), 'preview': member_preview(m['slug']), 'tagline': m.get('tagline', '')})
    return out


def _font(name):
    with open(os.path.join(HERE, 'qg_fonts', name), 'rb') as f:
        return 'data:font/woff2;base64,' + base64.b64encode(f.read()).decode()


def _img(rel, mime='image/webp'):
    with open(os.path.join(SRC, rel), 'rb') as f:
        return f'data:{mime};base64,' + base64.b64encode(f.read()).decode()


def _qr(url):
    import qrcode
    q = qrcode.QRCode(border=1, box_size=10, error_correction=qrcode.constants.ERROR_CORRECT_M)
    q.add_data(url); q.make(fit=True)
    im = q.make_image(fill_color='#020c06', back_color='white'); b = io.BytesIO(); im.save(b, 'PNG')
    return 'data:image/png;base64,' + base64.b64encode(b.getvalue()).decode()


def _short(url):
    return url.replace('https://', '').rstrip('/')


CSS = '''
@font-face{font-family:Anton;src:url(%(anton)s) format("woff2")}
@font-face{font-family:Manrope;font-weight:500;src:url(%(m5)s) format("woff2")}
@font-face{font-family:Manrope;font-weight:600;src:url(%(m6)s) format("woff2")}
@font-face{font-family:Manrope;font-weight:700;src:url(%(m7)s) format("woff2")}
@font-face{font-family:Manrope;font-weight:800;src:url(%(m8)s) format("woff2")}
@page{size:A4;margin:0}
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:#020c06}
body{font-family:Manrope,"Noto Color Emoji",sans-serif;color:#eef5f1;font-size:9.6pt;line-height:1.42;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.pg{width:210mm;height:297mm;padding:13mm 13mm 10mm;position:relative;overflow:hidden;page-break-after:always;
 background:radial-gradient(120mm 90mm at 92%% -8%%,rgba(52,204,136,.22),transparent 70%%),radial-gradient(110mm 80mm at -10%% 105%%,rgba(252,190,37,.10),transparent 70%%),#020c06;display:flex;flex-direction:column;gap:4.2mm}
.pg:last-child{page-break-after:auto}
.top{display:flex;align-items:center;gap:5mm}
.top img{height:12mm}
.top .t{border-left:1px solid rgba(150,255,200,.2);padding-left:5mm}
.top h1{font-family:Anton,sans-serif;font-weight:400;font-size:25pt;letter-spacing:.3px;line-height:1.02;color:#fff}
.top h1 em{font-style:normal;color:#34cc88}
.top p{color:#c3d2ca;font-size:8.6pt;font-weight:600;margin-top:1mm}
.box{border:1px solid rgba(150,255,200,.16);border-radius:4mm;background:linear-gradient(170deg,rgba(16,34,26,.92),rgba(6,16,10,.92));padding:4.2mm 5mm}
.box h2{font-family:Anton,sans-serif;font-weight:400;font-size:13.5pt;letter-spacing:.3px;color:#fcbe25;margin-bottom:2.2mm;line-height:1.1}
.box h2 small{font-family:Manrope;font-size:8pt;color:#8ea39a;font-weight:700;letter-spacing:0;margin-left:2mm}
.box p+p{margin-top:1.6mm}
b,strong{color:#fff;font-weight:800}
.g{color:#34cc88}.y{color:#fcbe25}.m{color:#8ea39a}
ul.ck{list-style:none;display:grid;gap:1.5mm}
ul.ck li{padding-left:5mm;position:relative}
ul.ck li:before{content:"";position:absolute;left:0;top:1.6mm;width:2.2mm;height:2.2mm;border-radius:50%%;background:#34cc88;box-shadow:0 0 0 .7mm rgba(52,204,136,.22)}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:4mm}
table{width:100%%;border-collapse:collapse;font-size:9pt}
th{text-align:left;color:#8ea39a;font-weight:700;font-size:7.6pt;text-transform:uppercase;letter-spacing:.5px;padding:0 2mm 1.6mm}
td{padding:2mm;border-top:1px solid rgba(150,255,200,.1);vertical-align:middle}
td.n{font-weight:800;color:#fff;white-space:nowrap}
.mini{display:inline-block;width:9mm;height:5.8mm;border-radius:1.1mm;vertical-align:middle;margin-right:2mm;position:relative;box-shadow:0 1mm 2mm rgba(0,0,0,.4)}
.mini:after{content:"";position:absolute;left:1.2mm;top:2mm;width:2mm;height:1.5mm;border-radius:.4mm;background:rgba(255,230,160,.85)}
.b1{background:linear-gradient(135deg,#1fb5b5,#0b6f73)}.b2{background:linear-gradient(135deg,#e5833a,#8f3a12)}.b3{background:linear-gradient(135deg,#d9dee3,#6c747c)}.b4{background:linear-gradient(135deg,#f6c453,#a8670d)}
.tag{display:inline-block;font-size:6.6pt;font-weight:800;color:#020c06;background:#fcbe25;border-radius:1mm;padding:.3mm 1.3mm;margin-left:1.5mm;vertical-align:1px;text-transform:uppercase;letter-spacing:.3px}
.fees{display:grid;grid-template-columns:repeat(4,1fr);gap:2.4mm}
.fee{border:1px solid rgba(150,255,200,.1);border-radius:2.4mm;padding:2.4mm 2.8mm;background:rgba(2,12,6,.5)}
.fee .v{font-family:Anton,sans-serif;font-size:15pt;color:#fff;line-height:1.05;display:block}
.fee .l{display:block;font-size:7.8pt;color:#c3d2ca;font-weight:600;margin-top:.6mm;line-height:1.3}
.vp{display:grid;grid-template-columns:1fr 1fr;gap:3mm}
.vp>div{border:1px solid rgba(150,255,200,.1);border-radius:2.6mm;padding:2.8mm 3.2mm;background:rgba(2,12,6,.5)}
.vp h3{font-size:10pt;font-weight:800;color:#fff;margin-bottom:1.4mm}
.tip{border-left:1.2mm solid #fcbe25;padding:2.2mm 3.4mm;background:rgba(252,190,37,.08);border-radius:0 2mm 2mm 0;margin-top:2.6mm}
ol.steps{list-style:none;display:grid;grid-template-columns:1fr 1fr;gap:2.2mm 4mm;counter-reset:s}
ol.steps li{counter-increment:s;position:relative;padding-left:8.2mm;min-height:6mm}
ol.steps li:before{content:counter(s);position:absolute;left:0;top:-.2mm;width:6mm;height:6mm;border-radius:50%%;background:#34b070;color:#020c06;font-weight:800;font-size:8.6pt;display:flex;align-items:center;justify-content:center}
.comm{display:grid;grid-template-columns:repeat(4,1fr);gap:2.4mm;margin:1.4mm 0 2.4mm}
.comm div{text-align:center;border:1px solid rgba(150,255,200,.1);border-radius:2.4mm;padding:2mm 1mm;background:rgba(2,12,6,.5)}
.comm .v{font-family:Anton,sans-serif;font-size:15pt;color:#34cc88;display:block;line-height:1.05}
.comm small{display:block;font-size:7.4pt;color:#c3d2ca;font-weight:700}
.links{display:grid;grid-template-columns:1fr auto;gap:5mm;align-items:center}
.links dl{display:grid;grid-template-columns:auto 1fr;gap:1.4mm 3.5mm}
.links dt{color:#8ea39a;font-weight:700;font-size:8.4pt}
.links dd{font-weight:800;color:#fff;word-break:break-all}
.qr{width:31mm;text-align:center}
.qr img{width:31mm;height:31mm;border-radius:2mm;display:block;background:#fff;padding:1.2mm}
.qr small{display:block;font-size:7pt;color:#8ea39a;font-weight:700;margin-top:1.2mm}
.disc{font-size:7.3pt;color:#8ea39a;line-height:1.45}
.disc b{color:#c3d2ca}
.foot{margin-top:auto;display:flex;justify-content:space-between;align-items:flex-end;font-size:7.4pt;color:#5f7268;gap:6mm}
.sig{text-align:right;line-height:1.35}
.sig .s1{color:#fcbe25;font-weight:800;font-size:9.6pt;display:block}
.sig .s2{color:#eef5f1;font-weight:800;font-size:9pt;display:block}
.p2{gap:3.2mm}
.p2 .box{padding:3.4mm 4.6mm}
.p2 .box h2{margin-bottom:1.6mm}
.p2 ul.ck{gap:1.1mm}
.p2 .qr,.p2 .qr img{width:27mm}
.p2 .qr img{height:27mm}
'''


def html(p):
    css = CSS % {'anton': _font('anton-latin-400-normal.woff2'), 'm5': _font('manrope-latin-500-normal.woff2'),
                 'm6': _font('manrope-latin-600-normal.woff2'), 'm7': _font('manrope-latin-700-normal.woff2'), 'm8': _font('manrope-latin-800-normal.woff2')}
    logo = _img('images/bellver-cards-logo-white-360.webp')
    who = 'MTG' if p['mtg'] else p['first']
    site = _short(p['site'])
    if p['mtg']:
        sig = '<div class="sig"><span class="s1">Let\'s Get This Crypto! 💪</span><span class="s2">MTG 👑 | Your Digital Architect</span><span>bellveraffiliates.com</span></div>'
    else:
        sig = f'<div class="sig"><span class="s1">{p.get('tagline') or 'The Card That Can Pay Your Bills'}</span><span class="s2">Shared by {p["name"]}</span><span>{site}</span></div>'
    contact = []
    if p['wa']:
        contact.append(('WhatsApp ' + who, p['wa']))
    if not p['mtg'] and p.get('telegram'):
        contact.append(('Telegram', _short(p['telegram'])))
    contact_rows = ''.join(f'<dt>{a}</dt><dd>{b}</dd>' for a, b in contact)
    ask = f'Questions? Message {who}' + (' on WhatsApp' if p['wa'] else (' on Telegram' if p.get('telegram') else '')) + '. Stuck on a step? Watch the matching tutorial video first, then ask.'
    commission_note = ('MTG earns a commission' if p['mtg'] else f'{p["name"]} earns a commission')

    page1 = f'''<section class="pg">
 <div class="top"><img src="{logo}" alt="Bellver Card"><div class="t"><h1>Bellver Card <em>quick guide</em></h1><p>{p['by']} · {site}</p></div></div>
 <div class="box"><h2>What it is</h2>
  <ul class="ck">
   <li><b>A crypto-funded payment card.</b> Load it with USDT or USDC and pay in shops, online and at ATMs. Physical Visa or virtual Mastercard, with Apple Pay and Google Pay.</li>
   <li><b>Your own wallet behind it.</b> A non-custodial Web3 wallet secured by Fireblocks. You hold the private key, so only you control the money in it.</li>
   <li><b>Fund it on BNB Smart Chain or Tron.</b> Send USDT or USDC (BEP-20 on BNB Smart Chain is the easy choice), plus a little BNB for network fees.</li>
  </ul></div>
 <div class="box"><h2>The four cards <small>one-time price, no monthly fee listed</small></h2>
  <table><thead><tr><th>Level</th><th>Price</th><th>Daily limit</th><th>Per payment</th><th>Monthly rewards</th></tr></thead><tbody>
   <tr><td class="n"><span class="mini b1"></span>Basic</td><td class="n">$99</td><td>$1,000</td><td>$500</td><td class="m">Not included</td></tr>
   <tr><td class="n"><span class="mini b2"></span>Premium</td><td class="n">$270</td><td>$10,000</td><td>$5,000</td><td>Up to 12 levels</td></tr>
   <tr><td class="n"><span class="mini b3"></span>Business<span class="tag">Most popular</span></td><td class="n">$490</td><td>$50,000</td><td>$10,000</td><td>Up to 15 levels</td></tr>
   <tr><td class="n"><span class="mini b4"></span>Gold</td><td class="n">$990</td><td>$250,000</td><td>$20,000</td><td>Up to 20 levels</td></tr>
  </tbody></table>
  <p class="m" style="margin-top:1.6mm;font-size:8pt">Physical and virtual cards cost the same. Upgrade any time and pay only the difference.</p></div>
 <div class="box"><h2>Fees in plain numbers</h2>
  <div class="fees">
   <div class="fee"><span class="v">3.9%</span><span class="l">Top-up fee, taken from what you load. Load $100 and <b>$96.10</b> reaches your card.</span></div>
   <div class="fee"><span class="v">1.75%</span><span class="l">Per payment. Pay $50 and the fee is about $0.88.</span></div>
   <div class="fee"><span class="v">2%</span><span class="l">ATM withdrawal (physical card).</span></div>
   <div class="fee"><span class="v">$85</span><span class="l">Shipping a physical card to Europe. $149 to the rest of the world.</span></div>
  </div>
  <p class="m" style="margin-top:2mm;font-size:8pt">Add-ons: Special Edition +$370 when you buy ($470 to upgrade later), your name printed on the card +$49. The minimum top-up is $10.</p></div>
 <div class="box"><h2>Virtual or physical?</h2>
  <div class="vp">
   <div><h3>Virtual Mastercard</h3><ul class="ck"><li>Issued in minutes, ready to use</li><li>Online, Apple Pay and Google Pay</li><li>No shipping fee, no waiting</li></ul></div>
   <div><h3>Physical Visa</h3><ul class="ck"><li>Tap in shops and use ATMs</li><li>Shipping $85 (Europe) or $149</li><li>Bellver says up to 4 weeks: allow 4 to 6</li></ul></div>
  </div>
  <p class="tip"><b>Smart start:</b> order the virtual card first and start paying today. A physical card makes most sense on Business or Gold, where the shipping cost is small next to the card. For delivery, give a complete address and a mobile number from the delivery country.</p></div>
 <div class="foot"><span>Prices and fees: Bellver's official price list (08/2026) with the October 2026 update. Checked {CHECKED}. Bellver can change them.</span><span>1 of 2</span></div>
</section>'''

    page2 = f'''<section class="pg p2">
 <div class="box"><h2>Order your card in 7 steps</h2>
  <ol class="steps">
   <li><b>Register</b> with {who}'s link (below), so {who} can see your sign-up and help you.</li>
   <li><b>Secure your account.</b> Two-factor login, a transaction password, and your private key written down offline.</li>
   <li><b>Fund your wallet.</b> About $10 of BNB for network fees, then USDT for your card price <b>plus $10</b> (the card's opening balance).</li>
   <li><b>Order your card</b> in My Cards: level, virtual or physical, and any add-ons. Pay from your wallet.</li>
   <li><b>Load it and pay.</b> Move money from your wallet to your card, then add it to Apple Pay or Google Pay.</li>
   <li><b>Share your link,</b> only if you want to. It is optional.</li>
   <li><b>Get paid.</b> Earnings become available on the 15th. The minimum withdrawal is $100.</li>
  </ol></div>
 <div class="box"><h2>The rewards plan <small>optional</small></h2>
  <p><b>Direct commissions, one time.</b> For every card ordered through your link, paid in USDT. You do not need a card of your own to earn these.</p>
  <div class="comm"><div><span class="v">$10</span><small>Basic</small></div><div><span class="v">$100</span><small>Premium (SE $150)</small></div><div><span class="v">$200</span><small>Business (SE $300)</small></div><div><span class="v">$400</span><small>Gold (SE $500)</small></div></div>
  <ul class="ck">
   <li><b>Monthly rewards:</b> 0.1% of every completed top-up by cardholders in your 2x2 matrix, on the levels you qualify for. Needs your own Premium card or higher.</li>
   <li><b>Your first star:</b> hold a Premium card and directly refer two new people who each buy Premium.</li>
   <li><b>The $100 rule:</b> load at least $100 onto your own card each month to receive that month's rewards. It is your own money to spend, not a fee. Miss three months in a row and the matrix position is lost.</li>
  </ul></div>
 <div class="cols">
  <div class="box"><h2>Stay safe</h2>
   <ul class="ck">
    <li>Never share your private key or passwords. No real support person asks for them.</li>
    <li>Bellver never emails login links. Type app.bellvercards.com yourself.</li>
    <li>Sending crypto? Check the network, and send a small test amount first.</li>
       </ul></div>
  <div class="box"><h2>Watch it done</h2>
   <ul class="ck">
    <li><b>6 tutorials:</b> register, secure, back up your key, fund and order, your dashboard, top up.</li>
    <li><b>5 explainers:</b> where your money sits, which card, the 2x2 matrix, your first week, 10 reasons.</li>
    <li>Free on the guide, and on its Downloads page.</li>
   </ul></div>
 </div>
 <div class="box links"><div><h2>Your links</h2>
  <dl><dt>Order your card</dt><dd>{_short(p['ref'])}</dd><dt>The full guide</dt><dd>{site}</dd>{contact_rows}</dl>
  <p class="m" style="margin-top:2mm;font-size:8pt">{ask}</p></div>
  <div class="qr"><img src="{_qr(p['site'])}" alt="QR code to the guide"><small>Scan for the full guide</small></div></div>
 <p class="disc"><b>Independent guide.</b> This is not an official Bellver document. Bellver Card is a product of Bellver Markets Ltd. The order link carries {who}'s referral code, so if you order through it, {commission_note} at no extra cost to you. Commissions and rewards depend on real card activity and Bellver's rules, and are never guaranteed. Nothing here is financial, tax or legal advice. Crypto carries real risk. Check the current figures in your Bellver dashboard before you decide.</p>
 <div class="foot"><span>2 of 2</span>{sig}</div>
</section>'''
    return f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Bellver Card quick guide</title><style>{css}</style></head><body>{page1}{page2}</body></html>'


def _stamp(p):
    with open(os.path.abspath(__file__), 'rb') as f:
        code = f.read()
    return hashlib.md5(code + json.dumps(p, sort_keys=True).encode()).hexdigest()


def make(todo):
    """Render each person's guide to PDF with the pre-installed Chromium, plus MTG's page-1 preview image."""
    from playwright.sync_api import sync_playwright
    from PIL import Image
    with sync_playwright() as pw:
        br = pw.chromium.launch(); pg = br.new_page(viewport={'width': 794, 'height': 1123}, device_scale_factor=2)
        for p in todo:
            pg.set_content(html(p), wait_until='load'); pg.wait_for_timeout(300)
            over = pg.evaluate('[...document.querySelectorAll(".pg")].map(e=>{var f=e.querySelector(".foot").getBoundingClientRect(),b=e.getBoundingClientRect();return Math.round(b.bottom-f.bottom)})')
            if min(over) < 8:
                raise SystemExit(f'quick guide for {p["key"]}: a page is too full (space under the footer: {over} px)')
            out = os.path.join(SRC, p['pdf']); os.makedirs(os.path.dirname(out), exist_ok=True)
            pg.pdf(path=out, format='A4', print_background=True, margin={'top': '0', 'right': '0', 'bottom': '0', 'left': '0'})
            if p['preview']:
                png = pg.locator('.pg').first.screenshot()
                im = Image.open(io.BytesIO(png)).convert('RGB')
                base = os.path.join(SRC, p['preview']); os.makedirs(os.path.dirname(base), exist_ok=True)
                im.resize((800, int(800 * im.height / im.width)), Image.LANCZOS).save(base + '.webp', 'WEBP', quality=84, method=6)
            print('quick guide', p['pdf'], os.path.getsize(out) // 1024, 'KB')
        br.close()


def ensure(force=False):
    try:
        stamps = json.load(open(STAMPS))
    except Exception:
        stamps = {}
    todo = [p for p in people() if force or stamps.get(p['key']) != _stamp(p) or not os.path.exists(os.path.join(SRC, p['pdf']))]
    if todo:
        make(todo)
        for p in todo:
            stamps[p['key']] = _stamp(p)
        json.dump(stamps, open(STAMPS, 'w'), indent=1)


def preview_for(partner):
    return member_preview(partner['slug']) if partner else MTG_PREVIEW


def pdf_for(partner):
    """The quick guide path (relative to the guide) for MTG (partner=None) or a team member."""
    return member_pdf(partner['slug']) if partner else MTG_PDF


if __name__ == '__main__':
    ensure('--force' in sys.argv)
