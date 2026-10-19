import sys; sys.path.insert(0,".")
from lib import *
DARK=dict(black=.03,contrast=.22)
J=[ # key, name, (W,H), (cx,cy), box(x0,y0,x1,y1) or None, grade, extra
 ("R269","pos/light.webp",(1200,1500),(.42,.5),None,dict(black=.02,contrast=.2),{}),
 ("R228","pos/feel.webp",(1200,1500),(.62,.5),None,dict(black=.02,contrast=.15),{}),
 ("R264","pos/genesis.webp",(1200,1500),(1.0,.5),None,dict(contrast=.12),{}),
 ("R208","amb/screen.webp",(2400,1800),(.5,.5),None,dict(black=.01,contrast=.12),{}),
 ("S660","fx/01.webp",(720,960),(.5,.6),None,DARK,{}),
 ("S651","fx/02.webp",(720,960),(.45,.55),None,DARK,{}),
 ("S639","fx/03.webp",(720,960),(.5,.5),None,DARK,{}),
 ("S654","fx/04.webp",(720,960),(.5,.6),(.3,.3,1,1),DARK,{}),
 ("S232","fx/05.webp",(720,960),(.5,.5),None,DARK,{}),
 ("S646","fx/06.webp",(720,960),(.55,.6),(.2,.25,1,1),DARK,{}),
 ("S106","fx/07.webp",(720,960),(.45,.5),None,DARK,{}),
 ("S648","fx/08.webp",(720,960),(.5,.6),(.1,.3,1,1),DARK,{}),
 ("R268","fx/09.webp",(720,960),(.5,.5),None,DARK,{}),
 ("S652","fx/10.webp",(720,960),(.45,.6),(0,.3,1,1),DARK,{}),
 ("S075","fx/11.webp",(720,960),(.6,.4),None,DARK,{}),
 ("S663","fx/12.webp",(720,960),(.75,.0),(.2,.0,1,.72),DARK,{}),
 ("R225","craft/corner-black.webp",(1800,1200),(.5,.5),None,dict(contrast=.1),{}),
 ("R233","craft/back-black.webp",(1800,1200),(.5,.5),None,dict(contrast=.1),{}),
 ("S055","craft/edge-silver.webp",(1200,1500),(.6,.6),None,DARK,{}),
 ("R266","craft/lightbar.webp",(1800,1200),(.5,.6),None,dict(black=.02,contrast=.15),{}),
 ("S057","craft/side-rgb.webp",(1800,1200),(.55,.5),None,DARK,{}),
 ("S108","craft/side-navy.webp",(1800,1200),(.5,.5),None,dict(black=.02,contrast=.2),{}),
 ("R262","craft/macro-lumen.webp",(1600,1067),(.5,.5),None,dict(contrast=.1),{}),
 ("S110","craft/macro-aurea.webp",(1600,1067),(.5,.5),None,dict(black=.01,white=.85,contrast=.15),{}),
 ("S241","craft/macro-aurum.webp",(1600,1067),(.5,.5),None,dict(black=.01,white=.8,contrast=.15),{}),
 ("R254","craft/aurum-stand.webp",(1800,1200),(.5,.5),None,dict(contrast=.08),{}),
 ("R241","sw/macro.webp",(1800,1350),(.5,.5),None,dict(black=.02,contrast=.15),{}),
 ("R245","sw/caps.webp",(1500,1500),(.3,.4),None,dict(contrast=.1),{}),
 ("R267","mode/wired.webp",(1800,1200),(.5,.5),None,dict(black=.02,contrast=.15),{}),
 ("B372","mode/24g.webp",(1800,1200),(.5,.5),None,dict(black=.02,contrast=.15),{}),
 ("B448","mode/bt.webp",(1800,1200),(.5,.55),None,dict(contrast=.1),{}),
 ("B403","game/hand.webp",(1800,1200),(.5,.5),None,dict(black=.02,contrast=.18),{}),
 ("B257","scene/gaming.webp",(2000,1250),(.5,.55),None,dict(black=.02,contrast=.15),{}),
 ("B098","scene/work.webp",(2000,1250),(.5,.6),None,dict(contrast=.08),{}),
 ("S051","scene/desk.webp",(2000,1250),(.5,.45),None,dict(black=.02,contrast=.18),{}),
 ("S736","scene/creative.webp",(2000,1250),(.5,.5),None,dict(black=.02,contrast=.18),{}),
 ("B389","cta/glow.webp",(2400,1200),(.5,.6),None,dict(black=.03,contrast=.2),{}),
]
only=sys.argv[1:]
for key,name,(OW,OH),(cx,cy),box,g,ex in J:
    if only and not any(o in name for o in only): continue
    a=load(key,max(OW,OH)*3)
    if box: a=crop(a,*box)
    a=cover(a,OW,OH,cx,cy); a=grade(a,**g)
    save(a,name,q=ex.get("q",80))
