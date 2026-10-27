# -*- coding: utf-8 -*-
"""Downloads (downloads/): the quick guide PDF, a ready share message, every video as an MP4 and the official PDFs,
in one place (MTG, 27 Oct 2026, modelled on his ALTRUVA downloads page). Team copies get their own quick guide,
their own share link and their own video; MTG's ad (which shows his number) stays on his pages only."""
import os, urllib.parse
from bv import *  # noqa
import bv
from p_info import phero, T
from p_watch import REG, SEC, KEY, FUND, DASH, TOPUP, EX1, EX2, MXV, EX3, EX4, DOCS
import quickguide

SRC = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

# (video tuple, short title for the list)
TUT_ROWS = [(REG, 'Register your account'), (SEC, 'Log in and secure it'), (KEY, 'Back up your private key'),
            (FUND, 'Fund your wallet and order'), (DASH, 'Your dashboard, explained'), (TOPUP, 'Top up your card')]
EXP_ROWS = [(EX1, 'Where your money sits'), (EX2, 'Which card is right for me'), (MXV, 'The 2x2 matrix, made simple'),
            (EX3, 'Your first week as a partner'), (EX4, '10 reasons, and what comes next')]
OVERVIEW = ('overview', 'Bellver Card in 3 minutes', '', '3:31', 'mp4', MP4_3MIN, 'images/bellver-card-3-minute-video-thumbnail')
MTG_AD = ('ad', 'My Bellver Card ad', '', '0:36', 'mp4', 'videos/mtg-bellver-card-ad.mp4', 'images/mtg-bellver-card-ad-thumbnail')


def _mb(rel, team_file=None):
    f = team_file or os.path.join(SRC, rel)
    return f'{os.path.getsize(f) / 1048576:.0f} MB' if os.path.exists(f) else ''


def _row(n, title, dur, size, href, thumb, H, sub=None):
    meta = ', '.join(x for x in (dur, size) if x)
    return f'''<li class="dlrow"><span class="dlth"><img src="{thumb}" alt="" width="640" height="360" loading="lazy"><span class="dln">{n}</span></span>
 <span class="dlt"><b>{title}</b><small>{sub + ", " if sub else ""}{meta}</small></span>
 <a class="btn btn-ghost btn-sm dlbtn" href="{href}" download aria-label="Download {title} (MP4, {meta})">{ic('download')}<span>MP4</span></a></li>'''


def _group(h, rows):
    return f'<div class="dlgrp rv"><h3 class="h3">{h}</h3><ul class="dllist">{rows}</ul></div>'


def downloads(H='downloads/'):
    P = bv.PARTNER
    first = (P.get('short') or P['name'].split()[0]) if P else 'MTG'
    trail = T(('Downloads', abs_url(H)))
    pdf = L(quickguide.pdf_for(P), H)
    prev = L(quickguide.preview_for(P) + '.webp', H)
    pdf_kb = os.path.getsize(os.path.join(SRC, quickguide.pdf_for(P))) / 1048576
    share_url = (bv.SITE + bv.BASE) if P else BVA_SITE + '/'

    top = phero(H, trail, ['Download', 'and share'],
                'Save the videos and the quick guide to your phone, and share them with the people you are introducing to the card. Free, and every video comes exactly as it plays on this guide.', None,
                f'<a class="btn btn-go" href="{pdf}" download>{ic("download")}Download the quick guide</a><a class="btn btn-ghost" href="#videos">{ic("video")}Jump to the videos</a>')

    guide = f'''<section class="sec-tight" style="padding-top:0" id="quick-guide"><div class="wrap"><div class="panel qgpanel rv">
  <a class="qgthumb" href="{pdf}" target="_blank" rel="noopener" aria-label="Open the quick guide PDF"><img src="{prev}" alt="Bellver Card quick guide, page 1" width="800" height="1131" loading="lazy"><span class="ext">PDF</span></a>
  <div class="qgtx">
   <span class="badge green">New, 2 pages</span>
   <h2 class="h2">Bellver Card <em>quick guide</em></h2>
   <p>The four cards and their limits, every fee, virtual or physical, the seven ordering steps, the rewards plan, safety habits{" and " + first + "'s links" if P else " and my links"}, on two pages. Keep it on your phone, or send it to someone before they decide.</p>
   <ul class="qgpts"><li>{ic('check')}Prices and fees checked {quickguide.CHECKED}</li><li>{ic('check')}Includes the 3.9% top-up fee update</li><li>{ic('check')}A QR code back to this guide</li></ul>
   <div class="btn-row"><a class="btn btn-go btn-sm" href="{pdf}" download>{ic('download')}Download the PDF</a><a class="btn btn-ghost btn-sm" href="{pdf}" target="_blank" rel="noopener">{ic('eye')}Open it</a></div>
   <p class="fine">PDF, 2 pages, {pdf_kb:.1f} MB.</p>
  </div>
 </div></div></section>'''

    msg = (f"I've been learning about the Bellver Card with this free guide. Short videos and plain-English pages show how the card works, "
           f"what it costs and how to order it safely, before you decide anything: {share_url}")
    wa_share = 'https://wa.me/?text=' + urllib.parse.quote(msg, safe='')
    share = f'''<section class="sec-tight" id="share"><div class="wrap">
 <div class="sec-head rv"><span class="kicker"><i>{ic('users')}</i>Share kit</span><h2 class="h2">We learn best when we <em>teach others</em></h2></div>
 <div class="panel sharepanel rv">
  <p class="muted">A ready message for WhatsApp. It points to this free guide, so people learn before they decide.</p>
  <textarea class="sharebox" id="share-msg" rows="4" readonly aria-label="Share message">{msg}</textarea>
  <div class="btn-row"><button type="button" class="btn btn-gold btn-sm" data-copybox="share-msg">{ic('check')}<span>Copy the message</span></button><a class="btn btn-wa btn-sm" href="{wa_share}" target="_blank" rel="noopener">{ic('wa')}Share on WhatsApp</a></div>
  <p class="fine">Sharing the card is optional. Keep it honest: no income promises, and say that you earn a commission if you do.</p>
 </div></div></section>'''

    def thumb(v):
        return L(v[6] + '-640.webp', H)
    tut = ''.join(_row(i + 1, t, v[3], _mb(v[5]), L(v[5], H), thumb(v), H) for i, (v, t) in enumerate(TUT_ROWS))
    exp = ''.join(_row(i + 1, t, v[3], _mb(v[5]), L(v[5], H), thumb(v), H) for i, (v, t) in enumerate(EXP_ROWS))
    more = _row(1, OVERVIEW[1], OVERVIEW[3], _mb(OVERVIEW[5]), L(OVERVIEW[5], H), thumb(OVERVIEW), H, sub="Bellver's official overview")
    if not P:
        more += _row(2, MTG_AD[1], MTG_AD[3], _mb(MTG_AD[5]), L(MTG_AD[5], H), thumb(MTG_AD), H, sub='By MTG')
    elif P.get('hero_video'):
        hv = P['hero_video']; tf = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'team_media', P['slug'], hv['file'])
        more += _row(2, f"{first}'s Bellver Card video", hv['duration'], _mb(None, tf), bv.BASE + hv['file'], bv.BASE + hv['poster'] + '.webp', H, sub=f"By {first}")
    count = len(TUT_ROWS) + len(EXP_ROWS) + more.count('class="dlrow"')
    videos = f'''<section class="sec-tight" id="videos"><div class="wrap">
 <div class="sec-head rv"><span class="kicker"><i>{ic('video')}</i>{count} videos</span><h2 class="h2">Every video, <em>ready to save</em></h2>
  <p class="lead">Tap MP4 to save a video. On an iPhone, open it, tap the share button, then Save Video.</p></div>
 <div class="dlgrid">{_group('Tutorials', tut)}{_group('Explainers', exp)}{_group('More videos', more)}</div>
 <p class="fine rv">Sharing a video? Please share it exactly as it is, with its notes and disclaimers kept in.</p>
</div></section>'''

    drows = ''
    for i, (k, img, t, d, m) in enumerate(DOCS):
        href = L(DOCS_PDF[k], H)
        drows += f'''<li class="dlrow doc-row"><span class="dlth pdf"><img src="{L(img, H)}" alt="" width="800" height="600" loading="lazy"><span class="ext">PDF</span></span>
 <span class="dlt"><b>{t}</b><small>{m}</small></span><a class="btn btn-ghost btn-sm dlbtn" href="{href}" download aria-label="Download the {t.lower()} (PDF, {m})">{ic('download')}<span>PDF</span></a></li>'''
    docs = f'''<section class="sec-tight" id="documents"><div class="wrap">
 <div class="sec-head rv"><span class="kicker"><i>{ic('book')}</i>Documents</span><h2 class="h2">Bellver's <em>official PDFs</em></h2>
  <p class="lead">Version 08/2026, straight from Bellver, plus a plain-words 2x2 matrix guide. Some figures have changed since: the quick guide above has the current ones.</p></div>
 <ul class="dllist dldocs rv">{drows}</ul>
 <p class="rv" style="margin-top:16px"><a class="tlink" href="{L('docs/', H)}">See every document with a preview {ic('arrow')}</a></p>
</div></section>'''

    body = top + guide + share + videos + docs + help_band(H, 'Need something else?', "Tell me which video or guide you'd like next, or message me on WhatsApp if a download doesn't work on your phone.")
    ld = [{"@type": "DigitalDocument", "name": "Bellver Card quick guide", "encodingFormat": "application/pdf", "url": abs_url(quickguide.pdf_for(P))}]
    return page(H, 'downloads', 'Bellver Card Downloads: Videos, Quick Guide PDF and Share Kit | MTG',
                f'Download every Bellver Card video as an MP4, the two-page Bellver Card quick guide PDF and a ready-made WhatsApp share message. Free.',
                'images/og/og-bellver-download-kit.jpg', 'Bellver Card downloads: videos, quick guide PDF and share kit', body, ld_extra=ld, trail=trail)
