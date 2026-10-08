# Generates the 1200x630 social preview images (run once after changing titles)
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
HERE=os.path.dirname(os.path.abspath(__file__)); IMG=os.path.join(HERE,'..','images')
FA='/tmp/fontsrc/fontsource-anton-5.3.0/package/files/anton-latin-400-normal.woff2'
FM='/tmp/fontsrc/manrope/package/files/manrope-latin-{}-normal.woff2'
W,H=1200,630
def base():
    im=Image.new('RGB',(W,H),(2,12,6)); g=Image.new('RGB',(W,H),(0,0,0)); d=ImageDraw.Draw(g)
    d.ellipse((560,-260,1500,520),fill=(30,110,70)); d.ellipse((-300,300,500,900),fill=(14,60,38))
    g=g.filter(ImageFilter.GaussianBlur(140)); im=Image.blend(im,g,.55)
    return im
logo=Image.open(os.path.join(IMG,'bellver-cards-logo-white.webp')).convert('RGBA')
card=Image.open(os.path.join(IMG,'bellver-card-black-visa.webp')).convert('RGBA')
se=Image.open(os.path.join(IMG,'bellver-card-special-edition.webp')).convert('RGBA')
def shadowed(im,blur=26,off=(0,24),alpha=170):
    pad=80; sh=Image.new('RGBA',(im.width+pad*2,im.height+pad*2),(0,0,0,0))
    a=im.split()[3].point(lambda v:v*alpha//255); blk=Image.new('RGBA',im.size,(0,0,0,255)); blk.putalpha(a)
    sh.alpha_composite(blk,(pad+off[0],pad+off[1])); sh=sh.filter(ImageFilter.GaussianBlur(blur)); sh.alpha_composite(im,(pad,pad)); return sh
def make(name,l1,l2,sub,art='card',green=2):
    im=base().convert('RGBA'); d=ImageDraw.Draw(im)
    lg=logo.resize((250,round(250*logo.height/logo.width)),Image.LANCZOS); im.alpha_composite(lg,(64,54))
    fm=ImageFont.truetype(FM.format(700),24); d.text((64+262,82),'by Affiliate MTG',font=fm,fill=(195,210,202))
    if art=='both':
        s=se.resize((470,round(470*se.height/se.width)),Image.LANCZOS).rotate(9,expand=True,resample=Image.BICUBIC); im.alpha_composite(shadowed(s),(640,10))
    c=card.resize((560,round(560*card.height/card.width)),Image.LANCZOS)
    im.alpha_composite(shadowed(c),(600,190))
    size=104
    for t in (l1,l2):
        while ImageFont.truetype(FA,size).getlength(t)>540: size-=4
    fa=ImageFont.truetype(FA,size); y=190
    for i,t in enumerate((l1,l2)):
        col=(52,204,136) if i+1==green else (255,255,255)
        d.text((64,y),t,font=fa,fill=col); y+=int(size*1.02)
    fs=ImageFont.truetype(FM.format(600),27)
    words=sub.split(); line=''; ys=y+18
    for w in words:
        if fs.getlength(line+" "+w)>520 and line: d.text((64,ys),line,font=fs,fill=(195,210,202)); ys+=38; line=w
        else: line=(line+' '+w).strip()
    d.text((64,ys),line,font=fs,fill=(195,210,202))
    d.rounded_rectangle((64,H-74,64+12,H-62),3,fill=(252,190,37))
    d.text((86,H-82),'musathegiant.com/cards/bellvercards',font=ImageFont.truetype(FM.format(700),22),fill=(142,163,154))
    im.convert('RGB').save(os.path.join(IMG,'og',name),'JPEG',quality=86,optimize=True,progressive=True); print(name)
make('og-bellver-cards.jpg','THE CARD THAT','CAN PAY YOUR BILLS','Crypto-funded card, physical Visa or virtual Mastercard. Limits up to $250,000 a day. From $99.','both')
make('og-bellver-how-it-works.jpg','HOW THE','CARD WORKS','Your own Fireblocks wallet, funding with USDT or USDC, physical or virtual.')
make('og-bellver-prices.jpg','PRICES, FEES','AND LIMITS','Basic $99, Premium $270, Business $490, Gold $990. Every fee in plain numbers.')
make('og-bellver-rewards.jpg','THE REWARDS','PROGRAM','Commissions, the 2x2 matrix, star ranks and the rules to stay qualified.','both')
make('og-bellver-get-started.jpg','ORDER YOUR CARD','STEP BY STEP','Register, secure, fund, order, pay. Seven short steps.')
make('og-bellver-videos.jpg','PRESENTATION','VIDEOS','The 3-minute overview, the 27-minute presentation and the launch webinar.')
make('og-bellver-tutorials.jpg','TUTORIAL','VIDEOS','Short step-by-step videos: register, fund, order, pay and withdraw.')
make('og-bellver-guide.jpg','YOUR BELLVER','CARD GUIDE','Everything about the card in one place: prices, wallet, rewards, videos.','both')
make('og-bellver-faq.jpg','QUESTIONS,','ANSWERED','Fees, limits, wallet security, rewards and payouts, in plain words.')
make('og-bellver-downloads.jpg','OFFICIAL','DOCUMENTS','Price list, compensation plan and presentation slides as PDFs.','both')
