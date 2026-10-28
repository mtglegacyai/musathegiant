# -*- coding: utf-8 -*-
"""bellveraffiliates.com/own-domain/: put your Bellver affiliate website on your own domain (GitHub Pages + GoDaddy DNS).
Built only for bellveraffiliates.com (MTG, 24 Oct 2026): a link MTG sends to any client who wants their copy on their own domain.
Video first, then the written guide, click by click. Not linked from the menu and kept out of search results (noindex)."""
from urllib.parse import quote
from bv import *  # noqa
from p_info import phero, T

H0 = 'own-domain/'
VIDEO = 'videos/guides/own-domain-github-godaddy.mp4'
THUMB = 'images/own-domain-guide-thumbnail'
WA_HELP = WA + '?text=' + quote('Hi MTG, I need help putting my Bellver website on my own domain.')
IPS = ['185.199.108.153', '185.199.109.153', '185.199.110.153', '185.199.111.153']


def k(s):
    """a value the reader types or copies exactly"""
    return f'<code class="cp">{s}</code>'


def own_domain(H=H0):
    trail = T(('Own Domain Guide', abs_url(H)))
    art = f'''<div class="player mx-video mx-herovid mfit" id="p-own-domain" role="button" tabindex="0" aria-label="Play: Put your Bellver website on your own domain" data-src="{L(VIDEO, H)}" data-title="Put your Bellver website on your own domain">
  <img src="{L(THUMB + '-640.webp', H)}" srcset="{L(THUMB + '-640.webp', H)} 640w, {L(THUMB + '.webp', H)} 1280w" sizes="(max-width:860px) 100vw, 560px" alt="Put your Bellver website on your own domain: step-by-step video thumbnail" width="1280" height="720" fetchpriority="high">
  <span class="pbtn">{ic('play')}</span><span class="plabel">5:09</span>
 </div><p class="mx-vcap">{ic('play-c')}Watch the step-by-step video first (5 minutes)</p>'''
    btns = (f'<a class="btn btn-go" href="#guide">{ic("book")}Read the step-by-step guide</a>'
            f'<a class="btn btn-ghost" href="{WA_HELP}" target="_blank" rel="noopener">{ic("wa")}Ask MTG on WhatsApp</a>' + tg_btn('Ask MTG on Telegram'))
    top = phero(H, trail, ['Your Bellver website,', 'on your own domain'],
                'Host your Bellver affiliate website free on GitHub and connect your GoDaddy domain to it. No name server changes, about 30 minutes. Watch the video first, then follow the written guide below, click by click.',
                art, btns)

    facts = [('30', 'minutes of your time'), ('$0', 'GitHub hosting'), ('0', 'name server changes'), ('6', 'simple parts')]
    strip = '<section class="sec-tight"><div class="wrap"><div class="od-facts rv">' + ''.join(
        f'<div class="od-fact"><b>{a}</b><span>{b}</span></div>' for a, b in facts) + '</div></div></section>'

    need = [('The zip file', 'Your website files, sent to you by MTG'), ('A free GitHub account', 'Part 1 shows you how to create one'),
            ('Your GoDaddy login', 'The account where you bought your domain'), ('A laptop or desktop', 'Chrome or Edge works best for uploading')]
    before = '<div class="box od-need"><h3 class="h3">Before you start</h3><ul>' + ''.join(f'<li><b>{a}.</b> {b}</li>' for a, b in need) + \
             f'<li>In every step, replace {k("YOUR-USERNAME")} with your GitHub username and {k("yourdomain.com")} with your own domain.</li></ul></div>'

    rec = ''.join(f'<tr><td>A</td><td>{k("@")}</td><td>{k(ip)}</td></tr>' for ip in IPS) + f'<tr><td>CNAME</td><td>{k("www")}</td><td>{k("YOUR-USERNAME.github.io")}</td></tr>'
    table = f'''<div class="tbl-wrap"><table class="tbl od-tbl"><thead><tr><th>Type</th><th>Name</th><th>Value</th></tr></thead><tbody>{rec}</tbody></table></div>'''

    S = [
     ('Create your GitHub account and repository', 'First a free GitHub account, then a repository: a folder on GitHub that holds your website.', f'''<p class="od-mini">Create your free account</p><ol>
<li>Go to <a class="inl" href="https://github.com" target="_blank" rel="noopener">github.com</a> and click <b>Sign up</b>.</li>
<li>Enter your <b>Email</b>, create a <b>Password</b> and choose a <b>Username</b>. Write your username down: you need it in later steps.</li>
<li>Choose your <b>Country/Region</b>, then click <b>Create account</b>.</li>
<li>GitHub may ask you to solve a quick puzzle, then emails you a code. Enter the code, then sign in.</li></ol>
<p class="od-mini">Create your repository</p><ol>
<li>Click the <b>+</b> at the top right, then <b>New repository</b>.</li>
<li>Your username is already in the <b>Owner</b> box. Leave it as it is.</li>
<li>In the <b>Repository name</b> box, type your username followed by {k(".github.io")}. If your username is mtgtribe, type {k("mtgtribe.github.io")}.</li>
<li>Choose <b>Public</b>. Free GitHub accounts can only publish websites from public repositories.</li>
<li>Turn on <b>Add README</b>, then click <b>Create repository</b>.</li></ol>''',
      'Why username.github.io and not just your domain name: this name puts your website at the top level, so it works and you can test it before your domain is connected.'),
     ('Upload your website files', 'Drag the contents of the folder, never the folder itself.', f'''<ol>
<li>On your computer, unzip the file from MTG. You get a folder with {k("index.html")} and folders such as assets, images, docs and prices.</li>
<li>Open that folder so you can see index.html and the other folders inside it.</li>
<li>On GitHub, open your new repository and click <b>Add file</b>, then <b>Upload files</b>.</li>
<li>Select <b>everything inside</b> the folder (Ctrl+A on Windows, Cmd+A on Mac) and drag it onto the GitHub page.</li>
<li>Wait until every file has finished uploading, then click <b>Commit changes</b>.</li></ol>''',
      'Check: your repository now lists index.html next to folders like assets, images and prices. One folder holding everything? Delete the repository (Settings, bottom of the page) and start again, dragging the contents only.'),
     ('Switch on GitHub Pages and test', 'Your website goes live on a free github.io address first.', f'''<ol>
<li>In your repository, click <b>Settings</b>, then <b>Pages</b> in the menu on the left.</li>
<li>Under <b>Build and deployment</b>, set <b>Source</b> to <b>Deploy from a branch</b>.</li>
<li>Under <b>Branch</b>, choose <b>main</b> and <b>/ (root)</b>, then click <b>Save</b>.</li>
<li>Wait 2 to 10 minutes, then open {k("https://YOUR-USERNAME.github.io")}.</li></ol>''',
      'Check: you see your Bellver website with your name, your photo and your WhatsApp button, and Order your card opens Bellver with your own referral link. Do not continue until this works.'),
     ('Add your domain on GitHub first', 'GitHub asks you to do this before you touch GoDaddy.', f'''<ol>
<li>Stay on <b>Settings</b>, <b>Pages</b>.</li>
<li>Under <b>Custom domain</b>, type {k("yourdomain.com")} (no www, no https) and click <b>Save</b>.</li></ol>''',
      'A "DNS check unsuccessful" warning is normal at this point. It clears after the next part.'),
     ('Point your GoDaddy domain to GitHub', 'DNS (Domain Name System) is your domain\'s address book. You only edit records: your name servers stay as they are.', f'''<p>When you finish, your DNS records must match this table:</p>{table}<ol>
<li>Sign in to GoDaddy and open your <b>Domain Portfolio</b>.</li>
<li>Click your domain, then open the <b>DNS</b> tab.</li>
<li>Along the way GoDaddy may show offers or adverts. You do not need them: click <b>Skip</b>, <b>Skip for now</b> or <b>No thanks</b> to carry on to the DNS page.</li>
<li>Find the <b>A</b> record named <b>@</b> (it often says Parked). Click <b>Edit</b>, change the <b>Value</b> to {k(IPS[0])} and click <b>Save</b>.</li>
<li>Click <b>Add New Record</b>: Type <b>A</b>, Name <b>@</b>, Value {k(IPS[1])}, then <b>Save</b>. Repeat for {k(IPS[2])} and {k(IPS[3])}.</li>
<li>Find the <b>CNAME</b> record named <b>www</b>. Click <b>Edit</b>, set the <b>Value</b> to {k("YOUR-USERNAME.github.io")} and click <b>Save</b>. No www record? Add one with those values.</li>
<li>Check your list. <b>Keep</b> the four GitHub A records you just added and the www CNAME. If you see any <b>other</b> A record named <b>@</b> with a different address (for example "WebsiteBuilder Site"), delete that extra one only.</li>
<li>Some records, such as the <b>NS</b> (name server) records, cannot be edited or deleted. That is normal: leave them as they are.</li>
<li>Switch off <b>Forwarding</b> if it is on.</li></ol>''',
      'GoDaddy may ask you to verify your identity when you save (Domain Protection). Complete it and continue. Leave your email records (MX and TXT) as they are.'),
     ('Wait, then switch on HTTPS', 'The padlock in the address bar.', f'''<ol>
<li>Wait. Changes usually show within an hour, but can take up to 24 hours (GoDaddy says up to 48 hours worldwide).</li>
<li>Go back to GitHub, <b>Settings</b>, <b>Pages</b>, and <b>refresh the page</b>. The page does not update by itself, so it may still show the old warning until you refresh.</li>
<li>When the DNS check turns green and says <b>DNS check successful</b>, your domain is connected.</li>
<li>Still showing the warning? Wait a little and refresh again, or type your domain in <b>Custom domain</b> again and click <b>Save</b>.</li>
<li>Tick <b>Enforce HTTPS</b>. Greyed out? GitHub is still preparing your certificate. Come back later.</li>
<li>Open {k("https://yourdomain.com")} and {k("https://www.yourdomain.com")}. Both should show your Bellver website with the padlock.</li>
<li>Tap <b>Order your card</b> once more and confirm your own referral link opens.</li></ol>''',
      'Done: your Bellver affiliate website now lives on your own domain.'),
    ]
    steps = ''.join(f'''<article class="gstep rv" id="step-{i+1}">{ped(str(i + 1), "num")}<div><p class="od-part">Part {i + 1}</p><h3 class="h3 od-h">{t}</h3><p class="od-sub">{sub}</p>{b}<p class="od-check">{ic('check')}<span>{chk}</span></p></div></article>''' for i, (t, sub, b, chk) in enumerate(S))

    trouble = [('"There isn\'t a GitHub Pages site here"', 'Wait 10 minutes. Check the repository name is exactly YOUR-USERNAME.github.io and Pages is set to main and / (root).'),
               ('The page shows, but with no colours or images', 'The files went inside a folder. index.html must be at the top level (Part 2).'),
               ('Your domain still shows a GoDaddy parked page', 'Check for an extra A record named @ that is not one of the four GitHub addresses, delete it, then wait up to 24 hours.'),
               ('yourdomain.com works but www does not', 'The www CNAME value must be YOUR-USERNAME.github.io, with no https and no repository name.'),
               ('GitHub still says DNS check unsuccessful', 'Refresh the GitHub Pages settings page. Still not green? Wait a little, or retype your domain in Custom domain and click Save. Enforce HTTPS stays greyed out until the check is green.'),
               ('Your domain stopped working after an update', 'The CNAME file was deleted. Retype your domain under Settings, Pages, Custom domain, and click Save.')]
    trows = ''.join(f'<div class="od-tr"><p class="od-tr-q">{a}</p><p class="od-tr-a">{b}</p></div>' for a, b in trouble)

    guide = f'''<section class="sec" id="guide"><div class="wrap">
 <p class="kicker">The written guide</p>
 <h2 class="h2">Follow it <span class="hap">click by click</span></h2>
 <p class="lead od-lead">Keep this page open next to GitHub and GoDaddy. Do one part at a time and tick off each check before you move on.</p>
 <div class="split guide-split">
  <div class="guide">{steps}</div>
  <aside class="rv od-side">{before}
   <div class="box od-ips"><h3 class="h3">Copy these exactly</h3><p>Four A records, Name {k("@")}</p><ul class="od-iplist">{''.join(f'<li>{k(ip)}</li>' for ip in IPS)}</ul><p>One CNAME record, Name {k("www")}</p><ul class="od-iplist"><li>{k("YOUR-USERNAME.github.io")}</li></ul></div>
  </aside>
 </div>
</div></section>
<section class="sec-tight" id="updates"><div class="wrap od-after">
 <div class="box rv"><h3 class="h3">Updating your website later</h3><p>Your website is your own copy, so it does not change when MTG updates his pages. The videos are the exception: they play from bellveraffiliates.com and stay up to date by themselves.</p><ol class="od-ol"><li>When MTG sends you a new zip, unzip it.</li><li>In your repository, click <b>Add file</b>, then <b>Upload files</b>.</li><li>Drag the contents in exactly as in Part 2. Files with the same name are replaced.</li><li>Click <b>Commit changes</b>. Your website updates within about 10 minutes.</li></ol><p class="od-warn"><b>Never delete the file named CNAME</b> in your repository. It holds your domain name.</p></div>
 <div class="rv"><h3 class="h3 od-trouble-h">If something goes wrong</h3><div class="od-trl">{trows}</div></div>
</div></section>'''

    helpb = f'''<section class="sec-tight"><div class="wrap"><div class="panel help rv">
  <div class="face"><img src="{L('/images/mtg-profile.jpg', H)}" alt="MTG, Musa The Giant" width="88" height="88" loading="lazy"></div>
  <div><h2>Stuck on a step? I'll help you.</h2><p>Send me two screenshots on {wa_or_tg()}: your GitHub Pages settings and your GoDaddy DNS records. I'll tell you exactly what to change.</p></div>
  <div class="help-btns"><a class="btn btn-wa" href="{WA_HELP}" target="_blank" rel="noopener">{ic('wa')}WhatsApp MTG</a>{tg_btn()}</div>
 </div></div></section>'''

    sig = f'''<section class="sec-tight od-sig-sec"><div class="wrap"><div class="od-sig rv">
  <p class="od-thanks">Thank you for taking massive action today. Take your time, follow each step, and once you understand it, help someone else do it too.</p>
  <p class="od-slogan">Let's Get This Crypto! 💪</p>
  <p class="od-name">MTG 👑 | Your Digital Architect</p>
  <p class="od-site">Explore the full Bellver Card guide at <a class="inl" href="{L('', H)}">bellveraffiliates.com</a></p>
 </div></div></section>'''

    body = f'<style>{CSS}</style>\n' + top + strip + guide + helpb + sig
    howto = {"@type": "HowTo", "name": "Put your Bellver affiliate website on your own domain with GitHub Pages and GoDaddy", "totalTime": "PT30M",
             "step": [{"@type": "HowToStep", "position": i + 1, "name": t, "url": abs_url(H) + f"#step-{i+1}"} for i, (t, _, _, _) in enumerate(S)]}
    return page(H, 'own-domain', 'Put Your Bellver Website on Your Own Domain (GitHub + GoDaddy) | MTG',
                'Host your Bellver affiliate website free on GitHub Pages and connect your GoDaddy domain in six simple parts. Step-by-step video and written guide by MTG.',
                'images/og/og-bellver-guide.jpg', 'Put your Bellver website on your own domain', body, ld_extra=[howto], trail=trail,
                robots='noindex,follow', dash=False)


CSS = '''
/* own-domain guide (bellveraffiliates.com only) */
.od-facts{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
.od-fact{border:1px solid rgba(52,204,136,.28);border-radius:16px;padding:18px 20px;background:linear-gradient(180deg,rgba(52,204,136,.08),rgba(52,204,136,.02))}
.od-fact b{display:block;font-family:Anton,Impact,sans-serif;font-size:2.4rem;line-height:1;color:#fcbe25;font-weight:400}
.od-fact span{display:block;margin-top:6px;color:rgba(238,245,241,.75);font-size:.95rem}
.od-lead{max-width:720px;margin-top:14px}
.od-part{margin:0 0 4px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;font-size:.78rem;color:#34cc88}
.od-h{margin:0 0 6px}
.od-sub{margin:0 0 12px;color:rgba(238,245,241,.72)}
.od-mini{margin:14px 0 6px;font-weight:800;color:#fcbe25;font-size:.95rem}
.gstep ol{margin:0;padding-left:1.25em}.gstep ol li{margin:.45em 0}
.od-check{display:flex;gap:10px;align-items:flex-start;margin:14px 0 0;padding:12px 14px;border-radius:12px;background:rgba(52,204,136,.09);border:1px solid rgba(52,204,136,.25);font-size:.95rem}
.od-check svg{flex:0 0 18px;width:18px;height:18px;margin-top:3px;color:#34cc88}
code.cp{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:.92em;padding:.12em .45em;border-radius:6px;background:rgba(252,190,37,.12);color:#ffd875;border:1px solid rgba(252,190,37,.28);white-space:nowrap;user-select:all}
.od-side{position:sticky;top:96px;display:grid;gap:16px;align-self:start}
.od-ips{border-color:rgba(252,190,37,.45)!important}
.od-iplist{list-style:none;padding:0;margin:8px 0 14px;display:grid;gap:8px}
.od-iplist code.cp{font-size:1.02rem}
.od-tbl td,.od-tbl th{vertical-align:top}
.od-after{display:grid;gap:26px}
.od-after>*{min-width:0}
.od-after .tbl-stack td{text-align:left}
.od-ol{padding-left:1.25em}.od-ol li{margin:.4em 0}
.od-warn{margin:16px 0 0;padding:12px 14px;border-radius:12px;background:rgba(252,190,37,.10);border:1px solid rgba(252,190,37,.40);color:#ffe3a1}
.od-trouble-h{margin:0 0 12px}
.od-trl{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
@media (max-width:1100px){.od-trl{grid-template-columns:repeat(2,minmax(0,1fr))}}
.od-tr{padding:16px 18px;border-radius:14px;border:1px solid rgba(255,255,255,.10);background:rgba(255,255,255,.03)}
.od-tr-q{margin:0 0 6px;font-weight:800}
.od-tr-a{margin:0;color:rgba(238,245,241,.78)}
@media (max-width:700px){.od-trl{grid-template-columns:1fr}}
.od-sig{text-align:center;max-width:760px;margin:0 auto;padding:34px 22px;border-radius:22px;border:1px solid rgba(252,190,37,.35);background:radial-gradient(120% 140% at 50% 0%,rgba(252,190,37,.10),rgba(2,12,6,0) 60%)}
.od-thanks{margin:0 0 18px;color:rgba(238,245,241,.85)}
.od-slogan{margin:0;font-family:Anton,Impact,sans-serif;font-size:clamp(2rem,5vw,3rem);color:#fcbe25;letter-spacing:.01em}
.od-name{margin:8px 0 0;font-weight:800;font-size:1.15rem}
.od-site{margin:10px 0 0;color:rgba(238,245,241,.75)}
.gstep .tbl-wrap{overflow-x:auto;margin:10px 0 16px}
@media (max-width:860px){.od-facts{grid-template-columns:repeat(2,1fr)}.od-side{position:static}code.cp{white-space:normal;word-break:break-all}
 .gstep .od-tbl{width:100%;min-width:0}.gstep .od-tbl th,.gstep .od-tbl td{padding:9px 6px;font-size:.82rem}
 .gstep .od-tbl code.cp{font-size:.72rem;white-space:nowrap;word-break:normal;padding:.1em .3em}}
'''
