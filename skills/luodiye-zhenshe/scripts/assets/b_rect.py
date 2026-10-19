import sys; sys.path.insert(0,".")
from lib import *
from rembg import remove, new_session
sess=new_session("isnet-general-use")
def quad(key):
    a=load(key,1600); rgb=(a[:,:,::-1]*255).astype(np.uint8)
    m=np.asarray(remove(Image.fromarray(rgb),session=sess,only_mask=True))
    b=(m>128).astype(np.uint8); b=cv2.morphologyEx(b,cv2.MORPH_OPEN,np.ones((9,9),np.uint8))
    cs,_=cv2.findContours(b,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE); c=max(cs,key=cv2.contourArea)
    hull=cv2.convexHull(c); peri=cv2.arcLength(hull,True); q=None
    for e in np.linspace(.005,.08,40):
        ap=cv2.approxPolyDP(hull,e*peri,True)
        if len(ap)==4: q=ap.reshape(4,2).astype(np.float32); break
    if q is None: q=cv2.boxPoints(cv2.minAreaRect(c)).astype(np.float32); print(key,"fallback box")
    # refine each side by fitting a line to hull points near that side
    pts=c.reshape(-1,2).astype(np.float32); ctr=q.mean(0)
    ang=np.arctan2(q[:,1]-ctr[1],q[:,0]-ctr[0]); q=q[np.argsort(ang)]      # clockwise from top-left-ish
    lines=[]
    for i in range(4):
        p0,p1=q[i],q[(i+1)%4]; d=p1-p0; L=np.linalg.norm(d); d/=L; n=np.array([-d[1],d[0]])
        t=(pts-p0)@d; dist=np.abs((pts-p0)@n); sel=pts[(t>L*.12)&(t<L*.88)&(dist<L*.03+6)]
        if len(sel)>20:
            vx,vy,x0,y0=cv2.fitLine(sel,cv2.DIST_HUBER,0,.01,.01).ravel(); lines.append((np.array([x0,y0]),np.array([vx,vy])))
        else: lines.append((p0,d))
    def inter(l1,l2):
        (p,r),(q_,s)=l1,l2; A=np.array([r,-s]).T; t=np.linalg.solve(A,q_-p); return p+t[0]*r
    q2=np.float32([inter(lines[i-1],lines[i]) for i in range(4)])
    return q2/1600.0, a.shape[1]/a.shape[0]
def order(q):
    # tl,tr,br,bl with long side horizontal
    s=q.sum(1); d=q[:,0]-q[:,1]
    return np.float32([q[s.argmin()],q[d.argmax()],q[s.argmax()],q[d.argmin()]])
def rectify(key,name,OW=3000,aspect=None,inset=.006,radius=.045,rot180=False,q=86,g=None):
    qn,_=quad(key); a=load(key,5200); h,w=a.shape[:2]; qp=order(qn*np.float32([w,w]))
    wt=np.linalg.norm(qp[1]-qp[0]); wb=np.linalg.norm(qp[2]-qp[3]); hl=np.linalg.norm(qp[3]-qp[0]); hr=np.linalg.norm(qp[2]-qp[1])
    asp=((wt+wb)/2)/((hl+hr)/2); print(key,"aspect %.3f"%asp,"sides",round(wt),round(wb),round(hl),round(hr))
    if aspect: asp=aspect
    OH=round(OW/asp); M=cv2.getPerspectiveTransform(qp,np.float32([[0,0],[OW,0],[OW,OH],[0,OH]]))
    out=cv2.warpPerspective(a,M,(OW,OH),flags=cv2.INTER_AREA)
    if rot180: out=out[::-1,::-1]
    i=round(OW*inset); out=out[i:OH-i,i:OW-i]; OH,OW=out.shape[:2]
    al=np.zeros((OH*2,OW*2),np.uint8); r=round(OH*radius*2); cv2.rectangle(al,(r,0),(OW*2-r,OH*2),255,-1); cv2.rectangle(al,(0,r),(OW*2,OH*2-r),255,-1)
    for cx,cy in [(r,r),(OW*2-r,r),(r,OH*2-r),(OW*2-r,OH*2-r)]: cv2.circle(al,(cx,cy),r,255,-1)
    al=cv2.resize(al,(OW,OH),interpolation=cv2.INTER_AREA).astype(np.float32)/255
    if g: out=grade(out,**g)
    save(out,name,q=q,alpha=al); return asp
if __name__=="__main__":
    jobs=sys.argv[1:]
    A=2.60
    if not jobs or "tops" in jobs:
        rectify("S068","obj/top-silver-rgb.webp",aspect=A,g=dict(black=.02,contrast=.2))
        rectify("S082","obj/top-black-rgb.webp",aspect=A,g=dict(black=.02,contrast=.2))
        rectify("S865","obj/top-silver-off.webp",aspect=A,g=dict(black=.02,contrast=.15))
    if not jobs or "plates" in jobs:
        rectify("S246","obj/plate-lumen.webp",aspect=A)
        rectify("S236","obj/plate-aurum.webp",aspect=A,g=dict(black=.0,white=.8,contrast=.15))
        rectify("S112","obj/plate-aurea.webp",aspect=A,g=dict(black=.0,white=.85,contrast=.15))
