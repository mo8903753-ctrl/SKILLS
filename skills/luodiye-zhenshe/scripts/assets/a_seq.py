from lib import *
names={190:"blue",193:"violet",196:"white",199:"wave",202:"red",208:"amber",211:"green",214:"cyan",230:"prism"}
fr={n:rd(TMP+"A_%03d.jpg"%n) for n in names}
h,w=fr[190].shape[:2]
# keyboard mask: union of brightness, convex hull, feather
u=np.max([luma(f) for f in fr.values()],axis=0)
u[:, int(w*.80):]*= (np.linspace(1,0,w-int(w*.80))[None,:]**2)   # kill wooden desk on the right
u[:int(h*.10),:]=0
m=(cv2.GaussianBlur(u,(0,0),9)>0.16).astype(np.uint8)
m=cv2.morphologyEx(m,cv2.MORPH_OPEN,np.ones((25,25),np.uint8))
cs,_=cv2.findContours(m,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE); c=max(cs,key=cv2.contourArea)
hull=cv2.convexHull(c); mask=np.zeros((h,w),np.float32); cv2.fillConvexPoly(mask,hull,1.0)
x,y,bw,bh=cv2.boundingRect(hull); print("bbox",x,y,bw,bh,"of",w,h)
core=cv2.GaussianBlur(cv2.dilate(mask,np.ones((61,61),np.uint8)),(0,0),28)
halo=cv2.GaussianBlur(cv2.dilate(mask,np.ones((301,301),np.uint8)),(0,0),160)
np.save(TMP+"A_bbox.npy",np.array([x,y,bw,bh]))
cx,cy=x+bw/2,y+bh/2; CW=int(bw*1.34); CH=int(CW*10/16)
x0=int(np.clip(cx-CW/2,0,w-CW)); y0=int(np.clip(cy-CH*.52,0,h-CH)); print("crop",x0,y0,CW,CH)
for n,nm in names.items():
    a=fr[n]
    bg=grade(a,black=.035,sat=.55)*0.55          # surroundings: darker, less saturated (keeps real spill)
    k=core[:,:,None]; out=a*k+bg*(1-k)
    out=out*(0.10+0.90*np.clip(halo*1.25,0,1))[:,:,None]   # fall to black away from the keyboard
    out=grade(out,black=.012,contrast=.25)
    out=out[y0:y0+CH,x0:x0+CW]
    out=cv2.resize(out,(2400,1500),interpolation=cv2.INTER_AREA)
    save(grain(out,.012),"seq/a-%s.webp"%nm,q=80)
    save(cv2.resize(out,(1200,750),interpolation=cv2.INTER_AREA),"seq/a-%s@m.webp"%nm,q=76)
