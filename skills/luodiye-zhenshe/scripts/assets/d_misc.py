import sys; sys.path.insert(0,".")
from lib import *
# ---- seq A re-export: padded, brighter
names={190:"blue",193:"violet",196:"white",199:"wave",202:"red",208:"amber",211:"green",214:"cyan",230:"prism"}
fr={n:rd(TMP+"A_%03d.jpg"%n) for n in names}; h,w=fr[190].shape[:2]
u=np.max([luma(f) for f in fr.values()],axis=0); u[:, int(w*.80):]*=(np.linspace(1,0,w-int(w*.80))[None,:]**2); u[:int(h*.10),:]=0
m=(cv2.GaussianBlur(u,(0,0),9)>0.16).astype(np.uint8); m=cv2.morphologyEx(m,cv2.MORPH_OPEN,np.ones((25,25),np.uint8))
cs,_=cv2.findContours(m,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE); hull=cv2.convexHull(max(cs,key=cv2.contourArea))
mask=np.zeros((h,w),np.float32); cv2.fillConvexPoly(mask,hull,1.0); x,y,bw,bh=cv2.boundingRect(hull)
core=cv2.GaussianBlur(cv2.dilate(mask,np.ones((61,61),np.uint8)),(0,0),28); halo=cv2.GaussianBlur(cv2.dilate(mask,np.ones((301,301),np.uint8)),(0,0),160)
P=500; CW=int(bw*1.42); CH=int(CW*10/16); cx,cy=x+bw/2+P,y+bh/2+P; x0=int(cx-CW/2); y0=int(cy-CH*.5)
for n,nm in names.items():
    a=fr[n]; bg=grade(a,black=.035,sat=.55)*0.5; k=core[:,:,None]; out=a*k+bg*(1-k)
    out=out*(0.06+0.94*np.clip(halo*1.25,0,1))[:,:,None]
    out=grade(out,black=.012,gamma=.86,contrast=.28,sat=1.12)
    out=cv2.copyMakeBorder(out,P,P,P,P,cv2.BORDER_CONSTANT,value=(0,0,0))[y0:y0+CH,x0:x0+CW]
    out=cv2.resize(out,(2400,1500),interpolation=cv2.INTER_AREA)
    save(grain(out,.01),"seq/a-%s.webp"%nm,q=80); save(cv2.resize(out,(1200,750),interpolation=cv2.INTER_AREA),"seq/a-%s@m.webp"%nm,q=76)
# ---- battery pair: lit (730) aligned onto off (729)
off=load("S729",3200); lit,inl=sift_align(off,load("S730",3200)); print("battery inliers",inl)
def bat(a):
    a=crop(a,.14,.10,.86,.94); a=cover(a,2400,1500,.5,.62); a=grade(a,black=.02,contrast=.2); return vignette(a,.55,2.0)
save(bat(off),"bat/off.webp"); save(bat(lit),"bat/on.webp")
# ---- gaming flipbook 640..643 (tripod locked)
for i,n in enumerate([640,641,642,643]):
    a=load("S%03d"%n,3200); a=crop(a,.0,.22,1,.78)
    h2,w2=a.shape[:2]; yy,xx=np.mgrid[0:h2,0:w2].astype(np.float32)
    # paint out the green sign (top-left) and gadget (top-right) with a soft falloff to black
    f=np.clip((yy/h2-.02)/.22,0,1); edge=np.clip(np.minimum((xx/w2)/.36,(1-xx/w2)/.30),0,1)
    k=np.clip(f+ (1-f)*np.clip(1-np.abs(xx/w2-.5)/.5*1.6+.25,0,1)*0+ (f>=1),0,1)
    a=a*np.clip(np.maximum(f**1.5, np.clip(1-np.abs(xx/w2-.52)/.20,0,1)*0),0,1)[:,:,None]
    a=cover(a,2400,1000,.5,.6); a=grade(a,black=.03,contrast=.25)
    save(a,"game/react-%d.webp"%i)
# ---- logo: white on transparent
lg=np.asarray(Image.open(RAW+"飙虬logo(1).jpg").convert("L")).astype(np.float32)/255
al=np.clip((0.86-lg)/0.7,0,1); ys,xs=np.where(al>.2); pad=20
al=al[ys.min()-pad:ys.max()+pad, xs.min()-pad:xs.max()+pad]
im=Image.fromarray(np.dstack([np.full(al.shape,255,np.uint8)]*3+[(al*255).astype(np.uint8)]),"RGBA"); im.save(OUT+"logo-white.png",optimize=True); print("logo",im.size)
