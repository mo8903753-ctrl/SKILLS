import os, cv2, numpy as np, json
T=os.environ.get("KS_SEQ_THUMBS","./work/thumbs/sequence")
fs=sorted(f for f in os.listdir(T) if f.endswith(".jpg") and not f.startswith("._") and "_1" not in f)
orb=cv2.ORB_create(2500)
def feats(f):
    im=cv2.imdecode(np.fromfile(os.path.join(T,f),dtype=np.uint8),cv2.IMREAD_GRAYSCALE)
    im=cv2.createCLAHE(3.0,(8,8)).apply(im)
    return im.shape, orb.detectAndCompute(im,None)
bf=cv2.BFMatcher(cv2.NORM_HAMMING,crossCheck=True)
prev=None; groups=[]; cur=[]
for f in fs:
    shp,(kp,des)=feats(f)
    same=False
    if prev is not None and des is not None and prev[2] is not None:
        m=bf.match(prev[2],des)
        if len(m)>=25:
            a=np.float32([prev[1][x.queryIdx].pt for x in m]); b=np.float32([kp[x.trainIdx].pt for x in m])
            H,mask=cv2.findHomography(a,b,cv2.RANSAC,3.0)
            if H is not None and mask.sum()>=20:
                h,w=shp; c=np.float32([[0,0],[w,0],[w,h],[0,h]]).reshape(-1,1,2)
                d=np.abs(cv2.perspectiveTransform(c,H)-c).max()
                same = d<6 and prev[0]==shp
    if same: cur.append(f[:-4])
    else:
        if len(cur)>=3: groups.append(cur)
        cur=[f[:-4]]
    prev=(shp,kp,des)
if len(cur)>=3: groups.append(cur)
for g in groups: print(len(g), g[0], "→", g[-1])
json.dump(groups,open(os.path.join(os.environ.get("KS_SHEETS","./work/sheets"),"locked_groups.json"),"w"))
