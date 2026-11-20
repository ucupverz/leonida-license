from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
W = H = 1024
F = "C:/Windows/Fonts/"
def font(n, s): return ImageFont.truetype(F + n, s)
AR="arial.ttf"; AB="arialbd.ttf"; CB="consolab.ttf"; CO="consola.ttf"
img = Image.new("RGB", (W, H), "#1a0b2e"); d = ImageDraw.Draw(img)
stops=[(0,(43,16,85)),(0.42,(214,36,159)),(0.72,(255,140,66)),(1.0,(255,209,102))]
def grad(t):
    for i in range(len(stops)-1):
        t0,c0=stops[i]; t1,c1=stops[i+1]
        if t0<=t<=t1:
            f=(t-t0)/(t1-t0); return tuple(int(c0[k]+(c1[k]-c0[k])*f) for k in range(3))
    return stops[-1][1]
for y in range(H): d.line([(0,y),(W,y)], fill=grad(y/H))
sun=Image.new("RGBA",(W,H),(0,0,0,0)); ImageDraw.Draw(sun).ellipse([W/2-140,330,W/2+140,610],fill=(255,236,179,220))
sun=sun.filter(ImageFilter.GaussianBlur(3)); img.paste(sun,(0,0),sun); d=ImageDraw.Draw(img)
def ctext(y,s,fnt,fill,stroke=0,sc=None):
    bb=d.textbbox((0,0),s,font=fnt); w=bb[2]-bb[0]
    d.text(((W-w)/2-bb[0],y),s,font=fnt,fill=fill,stroke_width=stroke,stroke_fill=sc)
ctext(48,"13 YEARS. ONE LICENSE.",font(AB,60),"#ffffff",3,"#2b1055")
cx0,cy0,cx1,cy1=64,158,960,902
sh=Image.new("RGBA",(W,H),(0,0,0,0)); ImageDraw.Draw(sh).rounded_rectangle([cx0+10,cy0+14,cx1+10,cy1+14],30,fill=(0,0,0,120))
sh=sh.filter(ImageFilter.GaussianBlur(11)); img.paste(sh,(0,0),sh); d=ImageDraw.Draw(img)
d.rounded_rectangle([cx0,cy0,cx1,cy1],30,fill="#f7f3e9",outline="#1a1a1a",width=5)
d.rounded_rectangle([cx0,cy0,cx1,cy0+98],30,fill="#d6249f"); d.rectangle([cx0,cy0+52,cx1,cy0+98],fill="#d6249f")
ctext(cy0+16,"STATE OF LEONIDA",font(AB,42),"#ffffff")
ctext(cy0+62,"D R I V E R   L I C E N S E",font(AB,22),"#ffe3f3")
px0,py0,px1,py1=cx0+34,cy0+130,cx0+300,cy0+452
d.rectangle([px0,py0,px1,py1],fill="#dfe6ee",outline="#1a1a1a",width=4)
g=Image.open("assets/mark-1024.png").convert("RGBA")
g.thumbnail((px1-px0-22,py1-py0-22),Image.LANCZOS)
img.paste(g,(px0+(px1-px0-g.width)//2,py0+(py1-py0-g.height)//2),g); d=ImageDraw.Draw(img)
d.text((px0+4,py1+8),"LICENSEE PHOTO",font=font(CO,19),fill="#666")
d.text((px0+4,py1+32),"VICE CITY · LEONIDA",font=font(CO,18),fill="#666")
fx=cx0+336
def field(x,y,label,value,vf,vfill="#1a1a1a"):
    d.text((x,y),label,font=font(CO,20),fill="#8a8a8a"); d.text((x,y+24),value,font=vf,fill=vfill)
field(fx,cy0+128,"NAME","EVERY GTA FAN",font(AB,34))
field(fx,cy0+214,"DOB","09 / 17 / 2013",font(CB,28))
field(fx+252,cy0+214,"CLASS","VI",font(AB,34),"#d6249f")
field(fx,cy0+296,"ISSUED","11 / 19 / 2026",font(CB,28))
field(fx+252,cy0+296,"EXPIRES","NEVER",font(AB,30),"#c0392b")
field(fx,cy0+380,"RESTRICTIONS","13 YEARS OF PATIENCE",font(AB,27))
stamp=Image.new("RGBA",(470,168),(0,0,0,0)); st=ImageDraw.Draw(stamp)
st.rounded_rectangle([6,6,464,162],14,fill=(247,243,233,255),outline=(214,36,159,255),width=7)
st.text((30,26),"PAID IN FULL",font=font(AB,40),fill=(214,36,159,255))
st.text((30,80),"my AI agent earned it on",font=font(AR,26),fill=(150,20,110,255))
st.text((30,114),"make.fun",font=font(AB,34),fill=(214,36,159,255))
stamp=stamp.rotate(-9,expand=True,resample=Image.BICUBIC)
img.paste(stamp,(cx1-512,cy1-306),stamp); d=ImageDraw.Draw(img)
d.text((cx0+40,cy1-70),"LEONIDA DMV  ·  GTA VI  ·  EST. 2013",font=font(CO,21),fill="#555")
d.text((cx0+40,cy1-44),"make.fun",font=font(AB,26),fill="#d6249f")
img.save("meme.png"); print("saved meme.png",img.size)
