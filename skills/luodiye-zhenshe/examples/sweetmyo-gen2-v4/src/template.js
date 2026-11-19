/**
 * Sweetmyo Gen2 — v4 "Signal" redesign templates.
 * Light-lab editorial language taken from the brand film (paper #F6F5F2, ink, volt, serif italics).
 * part="all" | "a" | "b" | "c" | "d" (Wix split mode). Form slots: 0 = hero, 1 = mid, 2 = final.
 */
export function buildPartHTML(part, A) {
  var KS = '<img class="sw-ks" src="' + A('brand/ks-wordmark.png') + '" alt="Kickstarter" width="1200" height="183">';

  function words(text, cls) {
    return text.split(' ').map(function (w) {
      return '<span class="' + (cls || 'sw-w') + '">' + w + '</span>';
    }).join(' ');
  }

  var nav = [
    '<header class="sw-nav" data-nav>',
    '  <a class="sw-nav-brand" href="#sw-hero" aria-label="Sweetmyo">',
    '    <img class="sw-wm-dark" src="' + A('brand/sweetmyo-wordmark.svg') + '" alt="Sweetmyo" width="161" height="32">',
    '    <img class="sw-wm-light" src="' + A('brand/sweetmyo-wordmark-white.svg') + '" alt="" width="161" height="32" aria-hidden="true">',
    '  </a>',
    '  <p class="sw-nav-mid"><span class="sw-dot" aria-hidden="true"></span>Live Dec. 08 on ' + KS + '</p>',
    '  <a class="sw-nav-cta" href="#sw-final">Reserve 50% OFF</a>',
    '  <span class="sw-nav-bar" aria-hidden="true"><i data-nav-bar></i></span>',
    '</header>'
  ].join('\n');

  /* ── 01 HERO — full-screen real video; scroll shrinks it into the capsule inside the headline.
        Title lives in the sticky layer; sub/offer/FORM live in a normal-flow layer so the Wix form scrolls with the page. ── */
  var hero = [
    '<section id="sw-hero" class="sw-hero" data-theme="light" data-scene="hero">',
    '  <div class="sw-hero-stage">',
    '    <div class="sw-hero-sticky">',
    '      <img class="sw-hero-glow" src="' + A('v4/glow-volt.png') + '" alt="" width="900" height="900" aria-hidden="true">',
    '      <div class="sw-capsule" data-capsule>',
    '        <video class="sw-cap-vid" autoplay muted loop playsinline preload="auto" poster="' + A('hero/hero-montage-poster.webp') + '">',
    '          <source src="' + A('hero/hero-workout-montage.mp4') + '" type="video/mp4">',
    '        </video>',
    '        <div class="sw-hero-scrim" data-hero-scrim aria-hidden="true"></div>',
    '      </div>',
    '      <p class="sw-hero-echo" aria-hidden="true" data-hero-echo>',
    '        <span class="sw-ht-row sw-ht-a">Work Out <em>Smarter.</em></span>',
    '        <span class="sw-ht-row sw-ht-b"><span class="sw-cap-slot" data-cap-slot></span>Not <em>Longer.</em></span>',
    '      </p>',
    '    </div>',
    '  </div>',
    '  <div class="sw-hero-copy">',
    '    <h1 class="sw-hero-title">Work Out <em>Smarter.</em><br>Not <em>Longer.</em></h1>',
    '    <div class="sw-hero-foot">',
    '      <div class="sw-hero-left">',
    '        <p class="sw-hero-sub">Precision AI-muscle stimulation engineered for total-body activation in 20 minutes.</p>',
    '        <p class="sw-hero-offer">Launching on ' + KS + ' <span>Sign up to lock in up to <b>50% OFF</b></span></p>',
    '        <div class="wix-form-placeholder" data-wix-slot="0" data-slot-name="hero"></div>',
    '        <p class="sw-fda"><span class="sw-dot" aria-hidden="true"></span>FDA Class I-Registered</p>',
    '      </div>',
    '      <ul class="sw-hero-specs">',
    '        <li><b data-count="16">16</b><span>Electrodes</span></li>',
    '        <li><b><span data-count="2">2</span> kHz</b><span>Smooth sine wave</span></li>',
    '        <li><b><span data-count="6">6</span>-axis</b><span>Motion sensing</span></li>',
    '        <li><b data-count="7">7</b><span>Independent channels</span></li>',
    '      </ul>',
    '    </div>',
    '  </div>',
    '</section>'
  ].join('\n');

  /* ── 02 THE COUCH — paper curtain question → capsule opens → 500 kcal ── */
  var couch = [
    '<section id="sw-couch" class="sw-couch" data-theme="light" data-scene="couch">',
    '  <div class="sw-sticky">',
    '    <div class="sw-q">',
    '      <p class="sw-q-text">' + words('What if your workout happened while you were') + ' <em>' + words('simply sitting down?') + '</em></p>',
    '    </div>',
    '    <div class="sw-couch-media" data-couch-media>',
    '      <video class="sw-auto-vid" muted loop playsinline preload="metadata" poster="' + A('gallery/poster-couch.webp') + '">',
    '        <source src="' + A('gallery/vid-couch.mp4') + '" type="video/mp4">',
    '      </video>',
    '      <div class="sw-couch-shade"></div>',
    '    </div>',
    '    <div class="sw-burn" data-burn>',
    '      <p class="sw-burn-num"><span data-burn-count>0</span><em>kcal</em></p>',
    '      <div class="sw-burn-copy">',
    '        <h2 class="sw-h2">Burn Up to 500 kcal <em>on the Couch.</em></h2>',
    '        <p>Get the calorie burn of an intense workout—while simply resting. Your muscles work. Your body uses energy.</p>',
    '        <small>Up to 500 kcal per hour at high full-body intensity. Individual results vary.</small>',
    '      </div>',
    '    </div>',
    '  </div>',
    '</section>'
  ].join('\n');

  /* ── 03 THE WAVE — 20 Hz sting morphs into a 2 kHz sine on a live canvas ── */
  var wave = [
    '<section id="sw-wave" class="sw-wave" data-theme="dark" data-scene="wave">',
    '  <div class="sw-sticky">',
    '    <canvas class="sw-wave-canvas" data-wave-canvas aria-hidden="true"></canvas>',
    '    <p class="sw-label sw-wave-label">Deep Muscle Activation</p>',
    '    <div class="sw-wave-states">',
    '      <div class="sw-wave-state is-a" data-wave-a>',
    '        <h2 class="sw-h2">Ordinary EMS <em>stings.</em></h2>',
    '        <p>Low-frequency pulses get stuck at the skin. In clinical testing, 90% of people felt burning at 20 Hz<sup>1</sup>—so you turn it down, and it stops working.</p>',
    '      </div>',
    '      <div class="sw-wave-state is-b" data-wave-b>',
    '        <h2 class="sw-h2">Gen 2 goes <em>deeper.</em></h2>',
    '        <p>A smooth 2 kHz sine wave passes through the skin to deep motor nerves<sup>2</sup>. Comfortable enough to turn up high—so 80% of your major muscle groups actually work.</p>',
    '      </div>',
    '    </div>',
    '    <p class="sw-hz"><span data-hz>20</span><em>Hz</em></p>',
    '    <ul class="sw-wave-specs">',
    '      <li><b>2 kHz</b><span>Sine wave</span></li>',
    '      <li><b>0.1–25 s</b><span>Adjustable ramp</span></li>',
    '      <li><b data-count="16">16</b><span>Electrodes</span></li>',
    '    </ul>',
    '    <p class="sw-foot-note"><sup>1</sup> Baek et al., Ann Rehabil Med, 2014. <sup>2</sup> Ward, Phys Ther, 2009.</p>',
    '  </div>',
    '</section>'
  ].join('\n');

  /* ── 04 ZONES — scroll scrubs the lime body; zones light up one by one ── */
  var zoneList = [
    ['Thighs', 0], ['Glutes', 0], ['Core', 1], ['Lower back', 1], ['Arms', 2], ['Chest', 3], ['Upper back', 3]
  ].map(function (z, i) {
    return '<li data-zone-step="' + z[1] + '"><span>' + z[0] + '</span></li>';
  }).join('');

  var zones = [
    '<section id="sw-zones" class="sw-zones" data-theme="paper" data-scene="zones">',
    '  <div class="sw-sticky">',
    '    <div class="sw-zones-copy">',
    '      <h2 class="sw-h2">One 20-Min Session. <em>Every Muscle Fired Up.</em></h2>',
    '      <p>Seven independent channels and 16 electrodes cover your chest, back, core, lower back, glutes, thighs and arms—over 70% of your skeletal muscle, working at once.</p>',
    '      <div class="sw-zones-stats">',
    '        <p><b data-count="7">7</b><span>Channels</span></p>',
    '        <p><b data-count="16">16</b><span>Electrodes</span></p>',
    '        <p><b>&gt;<span data-count="70">70</span>%</b><span>Skeletal muscle</span></p>',
    '      </div>',
    '    </div>',
    '    <div class="sw-zones-body">',
    '      <video data-zones-vid muted playsinline preload="auto" poster="' + A('v4/zones-body.webp') + '">',
    '        <source src="' + A('v4/zones-body.mp4') + '" type="video/mp4">',
    '      </video>',
    '    </div>',
    '    <div class="sw-zones-side">',
    '      <ol class="sw-zone-list">' + zoneList + '</ol>',
    '      <p class="sw-zones-tune">Too intense in one spot? Dial any zone from <b>0 to 130%</b> in the app.</p>',
    '    </div>',
    '  </div>',
    '</section>'
  ].join('\n');

  /* ── 05 MOTION — accordion of real training clips, auto-advancing on clip end ── */
  var motionItems = [
    { k: 'Squat', t: 'Squat Sync', d: 'Peaks lower-body power right at the bottom of every rep.', v: 'motion/vid-squat.mp4', p: 'motion/poster-squat.webp', hz: 0.9 },
    { k: 'Run', t: 'Stride Cadence', d: 'Locks pulse timing to your real-time running stride.', v: 'motion/vid-running.mp4', p: 'motion/poster-running.webp', hz: 2.6 },
    { k: 'Ride', t: 'Cycling Power', d: 'Matches continuous leg drive through climbs and sprints.', v: 'motion/vid-riding.mp4', p: 'motion/poster-riding.webp', hz: 1.6 }
  ];
  var motionHtml = motionItems.map(function (m, i) {
    return [
      '<article class="sw-acc' + (i === 0 ? ' is-on' : '') + '" data-acc="' + i + '" data-hz="' + m.hz + '">',
      '  <video muted playsinline preload="metadata" poster="' + A(m.p) + '"><source src="' + A(m.v) + '" type="video/mp4"></video>',
      '  <span class="sw-acc-k">' + m.k + '</span>',
      '  <div class="sw-acc-cap"><h3>' + m.t + '</h3><p>' + m.d + '</p></div>',
      '  <span class="sw-acc-time"><i></i></span>',
      '</article>'
    ].join('\n');
  }).join('\n');

  var motion = [
    '<section id="sw-motion" class="sw-motion" data-theme="dark">',
    '  <div class="sw-wrap sw-motion-head">',
    '    <p class="sw-label">Motion-Adaptive Sync</p>',
    '    <h2 class="sw-h2">It Adapts to How You Move. <em>In Real Time.</em></h2>',
    '    <p class="sw-lead">A six-axis sensor reads your pace and the depth of every squat, and recognizes whether you’re running, riding or lifting. Sweetmyo AI adjusts stimulation in real time to match the movement rather than running on a fixed pattern.</p>',
    '  </div>',
    '  <div class="sw-wrap sw-accs" data-accs>' + motionHtml + '</div>',
    '  <div class="sw-wrap sw-pulse-row"><canvas class="sw-pulse" data-pulse aria-hidden="true"></canvas><p class="sw-label" data-pulse-label>Pulse synced · Squat</p></div>',
    '</section>'
  ].join('\n');

  /* ── 06 MID BANNER (slot 1) ── */
  var mid = [
    '<section id="sw-mid" class="sw-mid" data-theme="dark" data-scene="mid">',
    '  <div class="sw-mid-media" data-mid-media>',
    '    <img src="' + A('banners/mid-vip-banner.webp') + '" alt="Athlete training in the Sweetmyo Gen2 suit" width="2400" height="1150" decoding="async">',
    '  </div>',
    '  <div class="sw-wrap sw-mid-copy">',
    '    <h2 class="sw-mid-title"><em>Don’t Miss Out.</em><span>Over 50% OFF for Early Backers.</span></h2>',
    '    <p>Join the VIP list for Super Early Bird access and launch-day pricing.</p>',
    '    <div class="wix-form-placeholder" data-wix-slot="1" data-slot-name="mid"></div>',
    '  </div>',
    '</section>'
  ].join('\n');

  /* ── 07 SCAN — lime chapter, the scan line reveals the copy ── */
  var scan = [
    '<section id="sw-scan" class="sw-scan" data-theme="volt" data-scene="scan">',
    '  <div class="sw-sticky">',
    '    <video class="sw-scan-vid sw-auto-vid" muted loop playsinline preload="metadata" poster="' + A('v4/scan-glass.webp') + '">',
    '      <source src="' + A('v4/scan-glass.mp4') + '" type="video/mp4">',
    '    </video>',
    '    <div class="sw-scan-copy" data-scan-copy>',
    '      <h2 class="sw-h2">Scan Your Body. <em>See Your True Progress.</em></h2>',
    '      <p>The scale can stall while fat drops and muscle grows. A BIA chip in the hub reads you through the same 16 electrodes on your chest, back, core, glutes, thighs and arms—not just your feet.</p>',
    '      <ul class="sw-scan-facts">',
    '        <li><b>5 · 50 · 250 kHz</b><span>Multi-frequency BIA</span></li>',
    '        <li><b>Body fat · Muscle mass · BMR</b><span>Estimated, tracked over time</span></li>',
    '        <li><b>Apple Watch</b><span>Live heart rate · Syncs to Apple Health &amp; Google Health</span></li>',
    '      </ul>',
    '    </div>',
    '    <span class="sw-scan-line" data-scan-line aria-hidden="true"></span>',
    '  </div>',
    '</section>'
  ].join('\n');

  /* ── 08 APP — 3D ring of the real app screens, turned by scroll ── */
  var appData = [
    ['Mode Selection', 'From gentle wave massage to deep muscle lock, pick your ideal feel.', 'v4/app-mode.webp'],
    ['Zone Control', 'Tune muscle zones to your exact comfort level, backed by live intensity feedback.', 'v4/app-zone.webp'],
    ['Session Summary', 'See exactly how your muscles responded right after your 20-minute session.', 'v4/app-summary.webp'],
    ['Progress Trends', 'Track your weekly routine and let your training history guide your next level.', 'v4/app-trends.webp']
  ];
  var ring = appData.map(function (a, i) {
    return '<figure class="sw-ring-card" data-ring="' + i + '"><img src="' + A(a[2]) + '" alt="Sweetmyo app — ' + a[0] + '" width="620" height="1344" decoding="async"></figure>';
  }).join('');
  var appCaps = appData.map(function (a, i) {
    return '<li class="' + (i === 0 ? 'is-on' : '') + '" data-ring-cap="' + i + '"><b>' + a[0] + '</b><span>' + a[1] + '</span></li>';
  }).join('');

  var app = [
    '<section id="sw-app" class="sw-app" data-theme="paper" data-scene="app">',
    '  <div class="sw-sticky">',
    '    <div class="sw-app-copy">',
    '      <h2 class="sw-h2">Training, <em>Generated for You.</em></h2>',
    '      <p>Sweetmyo AI brings together your body data, current state, goals and training history to generate a training mode that’s entirely your own. Each day, the AI Coach checks in and adjusts your load to match.</p>',
    '      <p class="sw-app-tag">Plan it. Track it. All in the APP.</p>',
    '      <ol class="sw-ring-caps">' + appCaps + '</ol>',
    '    </div>',
    '    <div class="sw-ring-stage"><div class="sw-ring" data-ring-el>' + ring + '</div></div>',
    '  </div>',
    '</section>'
  ].join('\n');

  /* ── 09 EVERYDAY — horizontal track + safety marquee ── */
  var easyData = [
    { n: '30', u: 's', h: 'On in 30 seconds.', p: 'Top + shorts, two pieces. Dry-wear electrodes—no soaking, no gel pads.', m: '<img src="' + A('v4/fit-two-piece.webp') + '" alt="Sweetmyo Gen2 two-piece top and shorts" width="1080" height="1350" decoding="async">' },
    { n: '1', u: 'snap', h: 'One snap. Locked in.', p: 'The hub clicks onto your thigh magnetically, then a mechanical lock holds it through squats, burpees and runs.', m: '<video class="sw-auto-vid" muted loop playsinline preload="metadata" poster="' + A('v4/hub-lock.webp') + '"><source src="' + A('v4/hub-lock.mp4') + '" type="video/mp4"></video>' },
    { n: '300', u: '+', h: 'Machine washes.', p: 'Pop off the hub, toss the suit in the wash, air dry. No consumables to rebuy.', m: '<img src="' + A('layers/layer-1-fabric.webp') + '" alt="Breathable hex compression fabric macro" width="1600" height="900" decoding="async">' },
    { n: '120', u: 'min', h: 'Per charge.', p: '4800 mAh. 0–80% in about an hour from any USB-C PD/QC charger.', m: '<img src="' + A('v4/hub-float.webp') + '" alt="Sweetmyo Smart Hub" width="1400" height="788" decoding="async">' }
  ];
  var easyHtml = easyData.map(function (e) {
    return [
      '<article class="sw-easy-card">',
      '  <div class="sw-easy-media">' + e.m + '</div>',
      '  <div class="sw-easy-txt">',
      '    <p class="sw-easy-num"><b data-count="' + e.n + '">' + e.n + '</b><em>' + e.u + '</em></p>',
      '    <h3>' + e.h + '</h3>',
      '    <p>' + e.p + '</p>',
      '  </div>',
      '</article>'
    ].join('\n');
  }).join('\n');

  var safety = ['300+ Machine Washes', 'Isolated Channels', 'Skin-Contact Detection', 'Hardware Kill Switch', 'Circuit Protection', 'Type-C Protection'];
  var safetyRun = safety.map(function (s) { return '<span>' + s + '</span>'; }).join('<i aria-hidden="true">—</i>');

  var easy = [
    '<section id="sw-easy" class="sw-easy" data-theme="dark" data-scene="easy">',
    '  <div class="sw-sticky">',
    '    <div class="sw-easy-head">',
    '      <h2 class="sw-h2">Train longer. <em>Charge less.</em></h2>',
    '      <p class="sw-easy-count"><span data-easy-idx>01</span> / 04</p>',
    '    </div>',
    '    <div class="sw-easy-track" data-easy-track>' + easyHtml + '</div>',
    '  </div>',
    '</section>',
    '<section class="sw-safety" data-theme="dark" aria-label="Built to Protect You at Every Layer">',
    '  <p class="sw-safety-title">Built to Protect You <em>at Every Layer.</em></p>',
    '  <div class="sw-marquee" data-marquee><div class="sw-marquee-in">' + safetyRun + '<i aria-hidden="true">—</i>' + safetyRun + '<i aria-hidden="true">—</i></div></div>',
    '</section>'
  ].join('\n');

  /* ── 10 FINAL (slot 2) + footer ── */
  var final = [
    '<section id="sw-final" class="sw-final" data-theme="dark" data-scene="final">',
    '  <img class="sw-final-glow" data-final-glow src="' + A('v4/glow-volt.png') + '" alt="" width="900" height="900" aria-hidden="true">',
    '  <div class="sw-wrap sw-final-in">',
    '    <p class="sw-label">Launching Dec. 08 on ' + KS + '</p>',
    '    <h2 class="sw-final-title">Don’t Miss the <em>Kickstarter Launch.</em></h2>',
    '    <div class="sw-cd" aria-label="Countdown to launch">',
    '      <p><b data-cd="d">00</b><span>Days</span></p><i>:</i>',
    '      <p><b data-cd="h">00</b><span>Hours</span></p><i>:</i>',
    '      <p><b data-cd="m">00</b><span>Minutes</span></p><i>:</i>',
    '      <p><b data-cd="s">00</b><span>Seconds</span></p>',
    '    </div>',
    '    <p class="sw-final-offer">Pay $20 Deposit, Lock In <b>50% OFF</b></p>',
    '    <div class="wix-form-placeholder" data-wix-slot="2" data-slot-name="end"></div>',
    '    <p class="sw-final-note">Get notified the moment we go live. The $20 deposit is fully refundable after the campaign ends—even if you don’t buy.</p>',
    '    <ol class="sw-steps">',
    '      <li><b>Today</b><span>Pay $20 to lock in up to 50% OFF, plus priority shipping and 6 bonus months of App Premium.</span></li>',
    '      <li><b>Dec. 08</b><span>Your launch link arrives by email. Claim 50% OFF in the first 72 hours—first 100 backers get a free Sweetmyo tote.</span></li>',
    '      <li><b>After launch</b><span>Priority delivery. Free shipping &amp; taxes covered. Deposit refunded within 10 business days.</span></li>',
    '    </ol>',
    '  </div>',
    '  <div class="sw-final-mark" data-final-mark aria-hidden="true"><img src="' + A('brand/sweetmyo-wordmark-white.svg') + '" alt="" width="161" height="32"></div>',
    '</section>',
    '<footer class="sw-foot" data-theme="dark">',
    '  <div class="sw-wrap sw-foot-in">',
    '    <div class="sw-certs">',
    '      <img src="' + A('brand/cert-fcc.svg') + '" alt="FCC" width="46" height="22">',
    '      <img src="' + A('brand/cert-ce.svg') + '" alt="CE" width="34" height="22">',
    '      <img src="' + A('brand/cert-rohs.svg') + '" alt="RoHS" width="52" height="22">',
    '      <img src="' + A('brand/cert-emc.svg') + '" alt="EMC Tested" width="52" height="22">',
    '      <img src="' + A('brand/cert-safety.svg') + '" alt="Electrical Safety Tested" width="58" height="22">',
    '    </div>',
    '    <p>Please use the same email for your deposit and Kickstarter pledge. All timelines are estimates.</p>',
    '    <p>© 2026 Sweetmyo. All rights reserved.</p>',
    '  </div>',
    '</footer>'
  ].join('\n');

  if (part === 'a') return nav + hero + couch + wave + zones + motion;
  if (part === 'b') return mid;
  if (part === 'c') return scan + app + easy;
  if (part === 'd') return final;
  return nav + hero + couch + wave + zones + motion + mid + scan + app + easy + final;
}
