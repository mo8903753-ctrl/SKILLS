import os, sys, cv2, numpy as np, json
from PIL import Image
Image.MAX_IMAGE_PIXELS=None
SRC=os.environ.get("KS_SEQ_DIR","./raw/sequence").rstrip("/")+"/"   # folder holding the lighting burst
def load(n, w=3000):
    im=Image.open(SRC+"09-220%03d.jpg"%n); im.draft("RGB",(w*2,w*2)); im=im.convert("RGB")
    im=im.resize((w,int(im.height*w/im.width)),Image.LANCZOS)
    return cv2.cvtColor(np.array(im),cv2.COLOR_RGB2BGR)
def prep(bgr):
    # legends are near-white in every lighting state: use min channel so coloured light is suppressed
    m=bgr.min(axis=2)
    return cv2.createCLAHE(2.0,(8,8)).apply(m)
sift=cv2.SIFT_create(6000)
def align(ref_n, nums, outdir, tag):
    ref=load(ref_n); kr,dr=sift.detectAndCompute(prep(ref),None)
    fl=cv2.FlannBasedMatcher(dict(algorithm=1,trees=5),dict(checks=64))
    res={}
    for n in nums:
        if n==ref_n: H=np.eye(3); inl=9999; img=ref
        else:
            img=load(n); k,d=sift.detectAndCompute(prep(img),None)
            mm=fl.knnMatch(d,dr,k=2); good=[a for a,b in mm if a.distance<0.72*b.distance]
            if len(good)<12: print(n,"few matches",len(good)); continue
            src=np.float32([k[g.queryIdx].pt for g in good]); dst=np.float32([kr[g.trainIdx].pt for g in good])
            H,mask=cv2.findHomography(src,dst,cv2.RANSAC,4.0); inl=int(mask.sum()) if mask is not None else 0
        out=cv2.warpPerspective(img,H,(ref.shape[1],ref.shape[0]),flags=cv2.INTER_LANCZOS4)
        cv2.imencode(".jpg",out,[cv2.IMWRITE_JPEG_QUALITY,93])[1].tofile(os.path.join(outdir,"%s_%03d.jpg"%(tag,n)))
        res[n]=inl; print(n,"inliers",inl, flush=True)
    return res
if __name__=="__main__":
    ref=int(sys.argv[1]); nums=[int(x) for x in sys.argv[2].split(",")]; tag=sys.argv[3]
    align(ref,nums,os.environ.get("KS_TMP","./work/tmp"),tag)
