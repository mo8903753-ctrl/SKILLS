// 3D stage: Lucy AI Studio model on a white page. Driven entirely by a state object.
import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';

const DRIVE_PULL = 0.13;      // metres a drive slides out
const ACCENT = 0x2b50e0;

export function createStage(canvas, { onProgress, mobile, labels }) {
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true, powerPreference: 'high-performance' });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, mobile ? 1.6 : 2));
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.3;
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.setClearColor(0xffffff, 0);

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(30, 1, 0.01, 10);

  const pmrem = new THREE.PMREMGenerator(renderer);
  const room = new RoomEnvironment();
  scene.environment = pmrem.fromScene(room, 0.03).texture;
  scene.environmentIntensity = 1.5;
  room.dispose(); pmrem.dispose();

  // soft contact shadow on the white "floor"
  const floor = new THREE.Mesh(new THREE.PlaneGeometry(4, 4), new THREE.ShadowMaterial({ color: 0x0b1440, opacity: 0.13 }));
  floor.rotation.x = -Math.PI / 2; floor.position.y = -0.0004; floor.receiveShadow = true;
  scene.add(floor);
  // faint blue ground glow under the machine
  const glowTex = (() => {
    const c = document.createElement('canvas'); c.width = c.height = 256;
    const g = c.getContext('2d'); const gr = g.createRadialGradient(128, 128, 0, 128, 128, 128);
    gr.addColorStop(0, 'rgba(43,80,224,0.22)'); gr.addColorStop(1, 'rgba(43,80,224,0)');
    g.fillStyle = gr; g.fillRect(0, 0, 256, 256); return new THREE.CanvasTexture(c);
  })();
  const glow = new THREE.Mesh(new THREE.PlaneGeometry(0.62, 0.62), new THREE.MeshBasicMaterial({ map: glowTex, transparent: true, depthWrite: false }));
  glow.rotation.x = -Math.PI / 2; glow.position.y = 0.0002; scene.add(glow);

  const key = new THREE.DirectionalLight(0xf2f5ff, 2.6);
  key.position.set(-0.35, 0.6, 0.42); key.castShadow = true;
  key.shadow.mapSize.set(mobile ? 1024 : 2048, mobile ? 1024 : 2048);
  Object.assign(key.shadow.camera, { left: -0.4, right: 0.4, top: 0.4, bottom: -0.4, near: 0.05, far: 1.6 });
  key.shadow.bias = -0.0001; key.shadow.normalBias = 0.0008; key.shadow.radius = 6;
  scene.add(key);
  const rim = new THREE.DirectionalLight(0x8fa8ff, 2.4); rim.position.set(0.4, 0.35, -0.4); scene.add(rim);
  const fill = new THREE.DirectionalLight(0xffffff, 0.9); fill.position.set(0.45, 0.2, 0.5); scene.add(fill);
  scene.add(new THREE.HemisphereLight(0xffffff, 0xdfe3ea, 0.75));


  // ---------- 3D ribbon that wraps around the machine (passes in front of and behind it) ----------
  const RIB_N = 720;
  const ribCanvas = document.createElement('canvas'); ribCanvas.width = 2048; ribCanvas.height = 96;
  function drawRibbonTex() {
    const g = ribCanvas.getContext('2d');
    g.fillStyle = '#2B50E0'; g.fillRect(0, 0, 2048, 96);
    g.fillStyle = 'rgba(255,255,255,.25)'; g.fillRect(0, 6, 2048, 2); g.fillRect(0, 88, 2048, 2);
    g.fillStyle = '#FFFFFF'; g.textBaseline = 'middle';
    const words = ['LUCY AI STUDIO', '✦', 'AGENT WORKSTATION', '✦', '128GB', '✦', '5 × SATA BAYS', '✦', 'MAKUAKE 2027', '✦'];
    let x = 30;
    for (const w of words) { g.font = w === '✦' ? '400 40px "IBM Plex Mono", monospace' : '800 54px Archivo, sans-serif'; g.fillText(w, x, 50); x += g.measureText(w).width + 34; }
    ribTex.needsUpdate = true;
  }
  const ribTex = new THREE.CanvasTexture(ribCanvas);
  ribTex.colorSpace = THREE.SRGBColorSpace; ribTex.wrapS = THREE.RepeatWrapping; ribTex.anisotropy = 8;
  drawRibbonTex();
  const ribbon = (() => {
    const pos = [], nor = [], uv = [], idx = [];
    const up = new THREE.Vector3(0, 1, 0), P = new THREE.Vector3(), Q = new THREE.Vector3(), T = new THREE.Vector3(), Wd = new THREE.Vector3(), Nn = new THREE.Vector3();
    const at = (t, out) => { const a = t * 2.15 * Math.PI * 2 + 0.9, r = 0.205 + 0.018 * Math.sin(t * 9.0); return out.set(Math.cos(a) * r, 0.006 + t * 0.215 + 0.01 * Math.sin(t * 14), Math.sin(a) * r * 0.92); };
    let len = 0; const w = 0.03;
    for (let i = 0; i < RIB_N; i++) {
      const t = i / (RIB_N - 1);
      at(t, P); at(Math.min(1, t + 0.001), Q); T.subVectors(Q, P).normalize();
      if (i) len += P.distanceTo(at((i - 1) / (RIB_N - 1), Q));
      Wd.copy(up).addScaledVector(T, -up.dot(T)).normalize(); Nn.crossVectors(T, Wd).normalize();
      pos.push(P.x + Wd.x * w / 2, P.y + Wd.y * w / 2, P.z + Wd.z * w / 2, P.x - Wd.x * w / 2, P.y - Wd.y * w / 2, P.z - Wd.z * w / 2);
      nor.push(Nn.x, Nn.y, Nn.z, Nn.x, Nn.y, Nn.z);
      const u = -len / 0.62; uv.push(u, 1, u, 0);
      if (i < RIB_N - 1) { const k = i * 2; idx.push(k, k + 1, k + 2, k + 1, k + 3, k + 2); }
    }
    const geo = new THREE.BufferGeometry();
    geo.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
    geo.setAttribute('normal', new THREE.Float32BufferAttribute(nor, 3));
    geo.setAttribute('uv', new THREE.Float32BufferAttribute(uv, 2));
    geo.setIndex(idx);
    const m = new THREE.Mesh(geo, new THREE.MeshStandardMaterial({ map: ribTex, side: THREE.DoubleSide, roughness: 0.45, metalness: 0.05, emissive: 0x2b50e0, emissiveIntensity: 0.18 }));
    m.castShadow = true; m.visible = false; m.frustumCulled = false;
    scene.add(m); return m;
  })();
  document.fonts?.ready.then(drawRibbonTex);

  const api = { ready: null, model: null, drives: [], driveBase: [], cover: null, coverBase: null };
  const tmpV = new THREE.Vector3(), tmpBox = new THREE.Box3();
  const raycaster = new THREE.Raycaster();
  const pickables = [];
  let modelMeshes = [];
  let handleMats = [], ledMat = null;
  let W = 1, H = 1;

  function resize() {
    W = window.innerWidth; H = window.innerHeight;
    renderer.setSize(W, H, false);
    camera.aspect = W / H;
    camera.updateProjectionMatrix();
  }
  resize();

  // ---------- drive top labels (chapter names printed on each HDD) ----------
  function makeLabelTexture(i) {
    const L = labels[i];
    const c = document.createElement('canvas'); c.width = 1024; c.height = 1000;
    const g = c.getContext('2d');
    g.fillStyle = '#F6F7F9'; g.fillRect(0, 0, 1024, 1000);
    g.fillStyle = '#2B50E0'; g.fillRect(0, 0, 1024, 30);
    g.fillStyle = '#2B50E0'; g.font = '600 54px "IBM Plex Mono", monospace';
    g.fillText(`DRIVE 0${i + 1} / 05`, 70, 150);
    g.fillStyle = '#111318'; g.font = '900 300px "Noto Serif SC", serif';
    g.fillText(L.zh, 56, 500);
    g.fillStyle = '#2B50E0'; g.font = '800 130px "Archivo", sans-serif';
    g.fillText(L.en, 66, 690);
    g.fillStyle = '#6B717C'; g.font = '500 40px "IBM Plex Mono", monospace';
    g.fillText(L.ch.split(' · ')[0], 70, 820); if (L.ch.includes(' · ')) g.fillText(L.ch.split(' · ')[1], 70, 880);
    g.strokeStyle = 'rgba(17,19,24,.15)'; g.lineWidth = 3; g.strokeRect(40, 70, 944, 890);
    const t = new THREE.CanvasTexture(c);
    t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8;
    return t;
  }

  api.ready = new Promise((resolve, reject) => {
    new GLTFLoader().load('assets/model/lucy.glb', async gltf => {
      const model = gltf.scene; api.model = model;
      model.traverse(o => {
        if (!o.isMesh) return;
        o.castShadow = true; o.receiveShadow = true; modelMeshes.push(o);
      });
      scene.add(model);
      api.cover = model.getObjectByName('Front_Cover');
      api.coverBase = api.cover.position.clone();
      for (let i = 0; i < 5; i++) {
        const d = model.getObjectByName(`HDD_0${i + 1}`);
        api.drives.push(d); api.driveBase.push(d.position.z);
        d.traverse(o => { if (o.isMesh) { o.userData.drive = i; pickables.push(o); } });
        const handle = model.getObjectByName(`HDD_0${i + 1}_Pull_Handle`);
        if (handle) { handle.material = handle.material.clone(); handleMats.push(handle.material); }
        const txt = model.getObjectByName(`HDD_0${i + 1}_Side_Text`);
        if (txt) txt.visible = false;
      }
      const led = model.getObjectByName('Front_Status_LED');
      if (led) { led.material = led.material.clone(); ledMat = led.material; ledMat.emissive = new THREE.Color(ACCENT); }
      // print chapter labels once fonts are ready
      try { await document.fonts.ready; await Promise.all(['900 40px "Noto Serif SC"', '800 40px Archivo', '600 20px "IBM Plex Mono"'].map(f => document.fonts.load(f, labels.map(l => l.zh + l.en).join('')))); } catch (e) {}
      model.updateMatrixWorld(true);
      api.drives.forEach((d, i) => {
        // labels live on each drive's left (-X) side face: readable once the drive is pulled out
        const lab = model.getObjectByName(`HDD_0${i + 1}_Side_Label`);
        if (!lab) return;
        tmpBox.setFromObject(lab);
        const size = tmpBox.getSize(new THREE.Vector3()), ctr = tmpBox.getCenter(new THREE.Vector3());
        const local = d.worldToLocal(ctr.clone());
        const w = size.z, h = size.y;
        const plane = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshStandardMaterial({ map: makeLabelTexture(i), roughness: .55, metalness: 0 }));
        plane.rotation.y = -Math.PI / 2;
        plane.position.set(d.worldToLocal(new THREE.Vector3(tmpBox.min.x, 0, 0)).x - 0.00035, local.y, local.z);
        plane.receiveShadow = true;
        d.add(plane);
      });
      resolve(api);
    }, e => { if (e.lengthComputable && onProgress) onProgress(e.loaded / e.total); }, reject);
  });

  // ---------- state → scene ----------
  const easeIO = t => t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
  const target = new THREE.Vector3();
  api.apply = (S, time) => {
    if (!api.model) return;
    // cover: pull forward, then slide to the right and away
    const c = S.cover;
    const pz = easeIO(Math.min(1, c / 0.5)), px = easeIO(Math.max(0, (c - 0.42) / 0.58));
    api.cover.position.set(api.coverBase.x + 0.42 * px, api.coverBase.y + 0.008 * pz - 0.03 * px, api.coverBase.z + 0.075 * pz - 0.05 * px);
    api.cover.rotation.y = 0.9 * px;
    api.cover.visible = c < 0.995;
    api.drives.forEach((d, i) => {
      const out = easeIO(Math.min(1, Math.max(0, S.drives[i])));
      d.position.z = api.driveBase[i] + DRIVE_PULL * out + 0.016 * S.hover[i];
      if (handleMats[i]) handleMats[i].color.set(S.drives[i] > 0.5 || S.hover[i] > 0.5 ? ACCENT : 0x1c1f26);
    });
    api.model.rotation.y = S.spin || 0;
    const ra = Math.max(0, Math.min(1, S.ribA || 0)), rb = Math.max(0, Math.min(1, S.ribB || 0));
    if (rb - ra > 0.002) {
      const a = Math.floor(ra * (RIB_N - 1)), b = Math.floor(rb * (RIB_N - 1));
      ribbon.geometry.setDrawRange(a * 6, Math.max(0, b - a) * 6); ribbon.visible = true;
      ribbon.rotation.y = -(S.spin || 0) * 0.25 + 0.4;
      ribTex.offset.x = time * 0.06;
    } else ribbon.visible = false;
    if (ledMat) ledMat.emissiveIntensity = 1.4 + Math.sin(time * 2.4) * 0.9;

    const az = S.az, el = S.el, dist = S.dist;
    target.set(S.tx || 0, S.ty, S.tz || 0);
    camera.position.set(target.x + dist * Math.sin(az) * Math.cos(el), target.y + dist * Math.sin(el), target.z + dist * Math.cos(az) * Math.cos(el));
    camera.lookAt(target);
    camera.setViewOffset(W, H, -S.sx * W, -S.sy * H, W, H);
    camera.updateMatrixWorld();
  };

  api.render = () => renderer.render(scene, camera);
  api.resize = resize;

  // world point → screen px
  api.project = v => {
    tmpV.copy(v).project(camera);
    return { x: (tmpV.x * .5 + .5) * W, y: (-tmpV.y * .5 + .5) * H, z: tmpV.z };
  };
  api.nodeWorld = (name, off = [0, 0, 0]) => {
    const o = api.model?.getObjectByName(name); if (!o) return null;
    tmpBox.setFromObject(o);
    return tmpBox.getCenter(new THREE.Vector3()).add(new THREE.Vector3(...off));
  };
  // anchor at the right-front corner of a drive plate
  api.driveAnchor = (i, side = 1) => {
    const p = api.model?.getObjectByName(`HDD_0${i + 1}_Front_Plate`); if (!p) return null;
    tmpBox.setFromObject(p);
    return new THREE.Vector3(side > 0 ? tmpBox.max.x : tmpBox.min.x, (tmpBox.min.y + tmpBox.max.y) / 2, tmpBox.max.z);
  };
  // screen rect of a drive's front plate (sleeve origin)
  api.driveRect = i => {
    const p = api.model?.getObjectByName(`HDD_0${i + 1}_Front_Plate`); if (!p) return null;
    tmpBox.setFromObject(p);
    let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9;
    for (let k = 0; k < 8; k++) {
      tmpV.set(k & 1 ? tmpBox.max.x : tmpBox.min.x, k & 2 ? tmpBox.max.y : tmpBox.min.y, k & 4 ? tmpBox.max.z : tmpBox.min.z).project(camera);
      const x = (tmpV.x * .5 + .5) * W, y = (-tmpV.y * .5 + .5) * H;
      x0 = Math.min(x0, x); x1 = Math.max(x1, x); y0 = Math.min(y0, y); y1 = Math.max(y1, y);
    }
    return { x: x0, y: y0, w: x1 - x0, h: y1 - y0 };
  };
  // top-centre / bottom-centre of a drive's front plate (drives stand side by side along X)
  api.driveEdge = (i, top = true) => {
    const p = api.model?.getObjectByName(`HDD_0${i + 1}_Front_Plate`); if (!p) return null;
    tmpBox.setFromObject(p);
    return new THREE.Vector3((tmpBox.min.x + tmpBox.max.x) / 2, top ? tmpBox.max.y : tmpBox.min.y, tmpBox.max.z);
  };
  api.driveY = i => api.drives[i] ? api.drives[i].position.y : 0.023 + 0.027 * i;

  const ndc = new THREE.Vector2();
  api.pick = (x, y, drivesOnly) => {
    if (!api.model) return null;
    ndc.set(x / W * 2 - 1, -(y / H) * 2 + 1);
    raycaster.setFromCamera(ndc, camera);
    const hits = raycaster.intersectObjects(drivesOnly ? pickables : modelMeshes, false);
    const h = hits.find(h => h.object.visible);
    if (!h) return null;
    return { drive: h.object.userData.drive ?? -1 };
  };
  return api;
}
