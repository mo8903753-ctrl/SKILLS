import fitz,sys,os
d=fitz.open(sys.argv[1]); out=sys.argv[2]
pages={58:['rokid-glasses','allpowers-monster-x','walkingpad-r1-pro','dnsys-x1','rokid-ar-lite'],
59:['feiyu-pocket3','leoch-powerstation','mokacam-moka4k','irmo-m1','inmo-go3'],
60:['hengbot-sirius','hyperdisk','3dmakerpro-whale','yashica-fx-d','petkit-purobot-ultra'],
61:['hoorii-clawstage','allpowers-monster-pro','nagualep','mokacam-alpha4k','feiyu-scorp-mini'],
62:['ortur-h20','inkjoy-frame','tecno-pocket-go','litheli-w1-pro','smartmi-p1'],
63:['ugreen-nasync',None,'code27','hoverair-x1-smart','tcl-note-a1'],
64:['neabot-nomo-q11','iflytek-aiwatch','halliday-ai-glass','iflytek-ainote-air2','hidock-p1'],
65:['makera-carvera-air','feiyu-pocket2s','looi','ropet-lopeto','creality-crscan-lizard'],
66:['mirror-fit','loona','goovis-g3-max','litheli-frozenpack','litheli-frozenpack-wild'],
67:['dreame-x30-ultra','udcap-vr-glove',None,None,'segway-cube1000'],
68:['ecovacs-deebot-x1','ecovacs-deebot-t8',None,'petsnowy-snow-plus','mokacam-alpha3'],
69:['furbulous-box',None,None,None,None],
70:['lava-genie','lalahome-realscooper','ecovacs-n8',None,'lava-me4']}
xs=[80,342,604,865,1127]
for pg,names in pages.items():
  p=d[pg-1]
  for x,n in zip(xs,names):
    if not n: continue
    r=fitz.Rect(x+5,206,x+228,206+232)
    pm=p.get_pixmap(clip=r,matrix=fitz.Matrix(400/223,400/223))
    pm.pil_save(f'{out}/cards/{n}.jpg',quality=82) if hasattr(pm,'pil_save') else pm.save(f'{out}/cards/{n}.jpg',jpg_quality=82)
res={5:'platform-partners',18:'pr-walkingpad',19:'pr-ar-treadmill',20:'pr-cnet-fox',21:'pr-tecno',22:'kol-wall',23:'kol-etaprime',24:'kol-shortcircuit-ltt',25:'kol-us-reviews',26:'kol-selfsufficientme',27:'kol-arthur-r',28:'kol-mame-jp',29:'kol-us-grid-1',30:'kol-us-grid-2',31:'kol-jp-grid',32:'kol-tw-grid',33:'celebrity',35:'ad-creative-1',36:'ad-creative-2',37:'landing-page-1',40:'sns',41:'edm',45:'offline-pepcom',47:'offline-rokid-times-square',49:'offline-pet-ny-ces',50:'offline-tokyo-isetan-feiyu-creality',51:'offline-segway-tokyo-litheli-tv',52:'offline-nojima',53:'offline-tsutaya',54:'offline-yodobashi',55:'offline-tw-ecovacs-segway',56:'offline-tw-hoverair-petsnowy',72:'brand-wall',73:'testimonials',76:'platform-kickstarter-visit',77:'platform-igg-award',78:'platform-makuake-talk',79:'platform-makuake-expo',80:'platform-makuake-award',81:'platform-flyingv-visit'}
for pg,n in res.items():
  pm=d[pg-1].get_pixmap(matrix=fitz.Matrix(1100/1440,1100/1440))
  pm.save(f'{out}/resources/{n}.jpg',jpg_quality=72)
