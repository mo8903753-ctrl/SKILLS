import os, cv2, numpy as np
from PIL import Image, ImageOps
Image.MAX_IMAGE_PIXELS=None
RAW=os.environ.get("KS_RAW","./raw").rstrip("/")+"/"          # original photos (read-only)
TMP=os.environ.get("KS_TMP","./work/tmp").rstrip("/")+"/"    # scratch files
OUT=os.environ.get("KS_OUT","./site/assets").rstrip("/")+"/"  # processed web assets
D={"S":"9-22静物产品/09-220%s.jpg","B":"基地拍摄jpg/9.200%s.jpg","R":"键盘图已修/DSC0%s"}
def path(key):
    k,n=key[0],key[1:]
    if k=="R":
        base=RAW+"键盘图已修/DSC03"+n
        for suf in ("-修图.png","-修.png"):
            if os.path.exists(base+suf): return base+suf
        raise FileNotFoundError(key)
    return RAW+D[k]%n
def load(key,maxw=None):
    """BGR float32 0..1"""
    p=path(key); im=Image.open(p)
    if maxw and im.format=="JPEG": im.draft("RGB",(maxw*2,maxw*2))
    im=ImageOps.exif_transpose(im).convert("RGB")
    if maxw and im.width>maxw: im=im.resize((maxw,round(im.height*maxw/im.width)),Image.LANCZOS)
    return np.asarray(im)[:,:,::-1].astype(np.float32)/255
def rd(p): return cv2.imdecode(np.fromfile(p,dtype=np.uint8),1).astype(np.float32)/255
def crop(a,x0,y0,x1,y1):
    h,w=a.shape[:2]; return a[round(y0*h):round(y1*h),round(x0*w):round(x1*w)]
def cover(a,W,H,cx=.5,cy=.5):
    h,w=a.shape[:2]; s=max(W/w,H/h); nw,nh=round(w*s),round(h*s)
    a=cv2.resize(a,(nw,nh),interpolation=cv2.INTER_AREA if s<1 else cv2.INTER_LANCZOS4)
    x=round((nw-W)*cx); y=round((nh-H)*cy); return a[y:y+H,x:x+W]
def fitw(a,W):
    h,w=a.shape[:2]; return cv2.resize(a,(W,round(h*W/w)),interpolation=cv2.INTER_AREA)
def luma(a): return a[:,:,0]*.114+a[:,:,1]*.587+a[:,:,2]*.299
def grade(a,black=0.0,white=1.0,gamma=1.0,sat=1.0,contrast=0.0,tint=None):
    a=np.clip((a-black)/(white-black),0,1)
    if gamma!=1: a=a**gamma
    if contrast: # s-curve
        a=a+contrast*(a-0.5)*(1-np.abs(2*a-1))*1.0
        a=np.clip(a,0,1)
    if sat!=1:
        l=luma(a)[:,:,None]; a=np.clip(l+(a-l)*sat,0,1)
    if tint is not None:
        a=np.clip(a*np.array(tint,dtype=np.float32)[None,None,:],0,1)
    return a
def vignette(a,strength=.6,power=2.2,cx=.5,cy=.5,rx=.75,ry=.75):
    h,w=a.shape[:2]; y,x=np.mgrid[0:h,0:w].astype(np.float32)
    d=np.sqrt(((x/w-cx)/rx)**2+((y/h-cy)/ry)**2); v=1-strength*np.clip(d,0,1.6)**power
    return a*np.clip(v,0,1)[:,:,None]
def grain(a,amt=.018,seed=7):
    rng=np.random.default_rng(seed); n=rng.normal(0,amt,a.shape[:2]).astype(np.float32)
    return np.clip(a+n[:,:,None],0,1)
def save(a,name,q=82,alpha=None):
    os.makedirs(os.path.dirname(OUT+name),exist_ok=True)
    rgb=(np.clip(a,0,1)[:,:,::-1]*255+.5).astype(np.uint8)
    if alpha is not None:
        im=Image.fromarray(np.dstack([rgb,(np.clip(alpha,0,1)*255+.5).astype(np.uint8)]),"RGBA")
    else: im=Image.fromarray(rgb,"RGB")
    im.save(OUT+name,"WEBP",quality=q,method=6)
    print("  →",name,im.size,"%dKB"%(os.path.getsize(OUT+name)//1024),flush=True)
def sift_align(ref,img,w=None):
    def prep(b):
        m=(b.min(axis=2)*255).astype(np.uint8); return cv2.createCLAHE(2.0,(8,8)).apply(m)
    s=cv2.SIFT_create(7000); kr,dr=s.detectAndCompute(prep(ref),None); k,d=s.detectAndCompute(prep(img),None)
    mm=cv2.FlannBasedMatcher(dict(algorithm=1,trees=5),dict(checks=64)).knnMatch(d,dr,k=2)
    g=[a for a,b in mm if a.distance<0.72*b.distance]
    H,mask=cv2.findHomography(np.float32([k[x.queryIdx].pt for x in g]),np.float32([kr[x.trainIdx].pt for x in g]),cv2.RANSAC,4.0)
    return cv2.warpPerspective(img,H,(ref.shape[1],ref.shape[0]),flags=cv2.INTER_LANCZOS4), int(mask.sum())
