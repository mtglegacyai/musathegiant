# -*- coding: utf-8 -*-
"""Team member images: profile photo and social preview images (the picture shown when a link is shared on WhatsApp).
   python3 team_assets.py SLUG PHOTO.jpg   -> photo + 11 preview images into bellvercards/SLUG/
   python3 team_assets.py SLUG             -> preview images only (no photo given: the help band shows initials)
Run once when a member joins or changes their name or photo. Fonts: see og.py."""
import os, sys
from PIL import Image, ImageOps
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import og, team
from team_shell import SLOGAN, TEAM_DIR

ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
m = team.member(sys.argv[1])
# source of truth: _build/team_media/<slug>/ (not published on musathegiant.com); copied to each site the member lives on
out = os.path.join(HERE, 'team_media', m['slug']); os.makedirs(os.path.join(out, 'og'), exist_ok=True)

if len(sys.argv) > 2:
    src = Image.open(sys.argv[2]); src = ImageOps.exif_transpose(src).convert('RGB')
    s = min(src.size); sq = src.crop(((src.width - s) // 2, (src.height - s) // 2, (src.width + s) // 2, (src.height + s) // 2))
    sq.resize((176, 176), Image.LANCZOS).save(os.path.join(out, 'photo.webp'), 'WEBP', quality=82, method=6)   # help band (88px, sharp on phones)
    sq.resize((400, 400), Image.LANCZOS).save(os.path.join(out, 'photo.jpg'), 'JPEG', quality=84, optimize=True, progressive=True)  # search engines
    print('photo', m['slug'])

pages = list(og.PAGES) + [('og-bellver-matrix.jpg', 'THE 2X2 MATRIX', 'MADE SIMPLE', 'Two seats, spillover, levels, the 0.1% and the $100 rule, in plain words.', 'both')]
for args in pages:
    foot = 'Your Bellver Card guide' if args[0] == 'og-bellver-cards.jpg' else (m.get('tagline') or SLOGAN)
    og.make(*args[:4], *(args[4:] or ['card']), by='by Affiliate ' + m['name'], url=foot, out=os.path.join(out, 'og'))

if 'mtg' in m.get('sites', ['bva']):      # this member also has pages on musathegiant.com/bellvercards/<slug>/
    import shutil
    dst = os.path.join(ROOT, 'bellvercards', m['slug'])
    shutil.copytree(out, dst, dirs_exist_ok=True)
print('team files in', out)
