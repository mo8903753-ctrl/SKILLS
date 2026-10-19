import os, cv2, numpy as np, sys
T=os.environ.get("KS_SEQ_THUMBS","./work/thumbs/sequence")
def load(n):
    im=cv2.imdecode(np.fromfile(os.path.join(T,"09-220%03d.jpg"%n),dtype=np.uint8),cv2.IMREAD_GRAYSCALE)
    im=cv2.resize(im,(600,400)); im=cv2.GaussianBlur(im,(0,0),2)
    gx=cv2.Sobel(im,cv2.CV_32F,1,0); gy=cv2.Sobel(im,cv2.CV_32F,0,1); g=cv2.magnitude(gx,gy)
    return cv2.normalize(np.log1p(g),None,0,1,cv2.NORM_MINMAX)
for a,b in [(114,134),(135,153),(165,187),(188,231),(849,871),(633,667),(79,85),(64,74),(864,871),(729,731),(738,741),(747,751)]:
    out=[]; prev=load(a)
    for n in range(a+1,b+1):
        if not os.path.exists(os.path.join(T,"09-220%03d.jpg"%n)): continue
        cur=load(n); M=np.eye(2,3,dtype=np.float32)
        try:
            cc,M=cv2.findTransformECC(prev,cur,M,cv2.MOTION_EUCLIDEAN,(cv2.TERM_CRITERIA_EPS|cv2.TERM_CRITERIA_COUNT,80,1e-5),None,5)
            d=np.hypot(M[0,2],M[1,2]); rot=np.degrees(np.arctan2(M[1,0],M[0,0]))
            out.append("%d:%.0f/%.1f°/%.2f"%(n,d,rot,cc))
        except cv2.error: out.append("%d:FAIL"%n)
        prev=cur
    print(a,"-",b,"| shift px@600 / rot / corr\n ", "  ".join(out))
