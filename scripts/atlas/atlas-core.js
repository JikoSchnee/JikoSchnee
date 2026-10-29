/* AtlasCore — isolated two-layer Atlas sphere with a fixed upper-right light. */
window.AtlasCore = {
  mount({ hero = document.querySelector('[data-atlas-core], .atlas-hero'), canvas = document.querySelector('[data-atlas-canvas], #atlas-canvas'), readAudio = () => ({}), capturePhase = null } = {}) {
    if (!hero || !canvas || !window.THREE) return;
    try {
      const capturing = Number.isFinite(capturePhase);
      const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true, preserveDrawingBuffer: capturing, powerPreference: 'high-performance' });
      renderer.setPixelRatio(Math.min(devicePixelRatio || 1, 2)); renderer.outputColorSpace = THREE.SRGBColorSpace; renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.25;
      const scene = new THREE.Scene(), camera = new THREE.PerspectiveCamera(34, 1, .1, 100), core = new THREE.Group(); camera.position.set(0, .12, 6.7); scene.add(core);
      const light = new THREE.Vector3(.28, .52, .81).normalize(), vertex = `varying vec3 o,w,v;void main(){vec4 p=modelMatrix*vec4(position,1.);o=position;w=p.xyz;v=normalize(cameraPosition-p.xyz);gl_Position=projectionMatrix*viewMatrix*p;}`;
      const inner = `uniform float t;uniform float audioEnergy;uniform vec3 l;varying vec3 o,w,v;float h(vec3 p){return fract(sin(dot(p,vec3(127.1,311.7,74.7)))*43758.5453123);}float n(vec3 p){vec3 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);return mix(mix(mix(h(i),h(i+vec3(1,0,0)),f.x),mix(h(i+vec3(0,1,0)),h(i+vec3(1,1,0)),f.x),f.y),mix(mix(h(i+vec3(0,0,1)),h(i+vec3(1,0,1)),f.x),mix(h(i+vec3(0,1,1)),h(i+vec3(1,1,1)),f.x),f.y),f.z);}float f(vec3 p){float r=0.,a=.52;for(int i=0;i<5;i++){r+=n(p)*a;p=p*2.03+7.1;a*=.5;}return r;}void main(){vec3 q=normalize(cross(dFdx(w),dFdy(w)));if(dot(q,v)<0.)q*=-1.;vec3 p=normalize(o)*5.3;float a=f(p),b=f(p*2.4),e=smoothstep(.43,.82,a+b*.3+sin(t*.16+b*6.28318)*.025),d=max(0.,dot(q,l)),m=pow(smoothstep(.46,.92,d),2.6),r=m*(.38+e*.62),z=pow(d,3.);vec3 c=mix(mix(vec3(.008,.009,.012),vec3(.038,.027,.032),pow(d,.8)),vec3(.42,.002,.005),r);c+=vec3(1.,.018,.011)*m*(.2+e*.48)*(.42+z*1.45);c+=vec3(.75,.018,.009)*m*audioEnergy;gl_FragColor=vec4(c,1.);}`;
      const outer = `uniform float audioEnergy;uniform vec3 l;varying vec3 w,v;void main(){vec3 q=normalize(cross(dFdx(w),dFdy(w)));if(dot(q,v)<0.)q*=-1.;float d=max(0.,dot(q,l)),r=smoothstep(.46,.92,d),m=pow(r,2.6),f=pow(r,1.15),s=pow(d,68.)*m,b=pow(d,7.)*m,x=smoothstep(.9817,.9925,d),rim=pow(1.-max(0.,dot(q,normalize(v))),3.5);vec3 c=mix(vec3(.012,.014,.018),vec3(.05,.054,.062),pow(d,.72));c+=vec3(.46,.42,.4)*f*(.12+d*.55)+vec3(1.,.94,.9)*s*3.2+vec3(.58,.035,.038)*b+vec3(.16,.17,.19)*pow(d,2.)*.38*(1.-m)+vec3(.07,.01,.014)*rim*.22;c=mix(c,vec3(1.65,1.48,1.3),x);c+=vec3(.28,.008,.006)*m*audioEnergy;gl_FragColor=vec4(c,mix(clamp(mix(.82,.05,m)+s*.16,.16,.88),.80,x));}`;
      const geo = new THREE.IcosahedronGeometry(1, innerWidth < 720 ? 3 : 4), im = new THREE.ShaderMaterial({ uniforms: { audioEnergy: { value: 0 }, t: { value: 0 }, l: { value: light } }, vertexShader: vertex, fragmentShader: inner, extensions: { derivatives: true } }), om = new THREE.ShaderMaterial({ uniforms: { audioEnergy: { value: 0 }, l: { value: light } }, vertexShader: vertex, fragmentShader: outer, extensions: { derivatives: true }, transparent: true, depthWrite: false });
      const redContour = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ color: 0xa90b11, transparent: true, opacity: .30, side: THREE.BackSide, depthWrite: false }));
      const whiteContour = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ color: 0xfff5e8, transparent: true, opacity: .92, side: THREE.BackSide, depthWrite: false }));
      const a = new THREE.Mesh(geo, im), b = new THREE.Mesh(geo, om); redContour.scale.setScalar(1.945); whiteContour.scale.setScalar(1.918); a.scale.setScalar(1.84); b.scale.setScalar(1.9); redContour.renderOrder = -2; whiteContour.renderOrder = -1; b.renderOrder = 1; core.add(redContour, whiteContour, a, b);
      let frame = 0, destroyed = false;
      const motion = window.matchMedia('(prefers-reduced-motion: reduce)');
      const resize = () => {
        const { width, height } = hero.getBoundingClientRect();
        if (!width || !height) return;
        camera.aspect = width / height;
        camera.updateProjectionMatrix();
        renderer.setSize(width, height, false);
      };
      const amplitude = { inner: .08, outer: .10 };
      const bounded = value => Math.max(0, Math.min(1, Number(value) || 0));
      const render = time => {
        frame = 0;
        if (destroyed || (!capturing && (document.hidden || motion.matches))) return;
        const t = time * .001;
        const signal = readAudio(time) || {};
        const shellScale = 1 + bounded(signal.outerBass) * amplitude.outer;
        // Keep the fast inner pulse inside the slower shell even at debug limits.
        a.scale.setScalar(Math.min(1.84 * (1 + bounded(signal.innerBass) * amplitude.inner), 1.9 * shellScale - .023));
        b.scale.setScalar(1.9 * shellScale);
        redContour.scale.setScalar(1.945 * shellScale);
        whiteContour.scale.setScalar(1.918 * shellScale);
        im.uniforms.audioEnergy.value = bounded(signal.innerEnergy);
        om.uniforms.audioEnergy.value = bounded(signal.outerEnergy);
        im.uniforms.t.value = capturing ? 0 : t;
        camera.lookAt(0, 0, 0);
        core.rotation.y = capturing ? -capturePhase * Math.PI * 2 : -t * .035;
        core.rotation.x = capturing ? 0 : Math.sin(t * .12) * .018;
        renderer.render(scene, camera);
        if (!capturing) frame = requestAnimationFrame(render);
      };
      const syncMotion = () => {
        if (frame) cancelAnimationFrame(frame);
        frame = 0;
        hero.classList.toggle('is-webgl', !motion.matches);
        if (capturing) render(0);
        else if (!destroyed && !document.hidden && !motion.matches) frame = requestAnimationFrame(render);
      };
      addEventListener('resize', resize, { passive: true });
      document.addEventListener('visibilitychange', syncMotion);
      motion.addEventListener('change', syncMotion);
      const observer = new ResizeObserver(resize);
      observer.observe(hero);
      resize();
      syncMotion();
      return {
        setAmplitude({ inner = amplitude.inner, outer = amplitude.outer } = {}) {
          amplitude.inner = Math.max(0, Math.min(1, Number(inner) || 0));
          amplitude.outer = Math.max(0, Math.min(1, Number(outer) || 0));
        },
        destroy() {
          if (destroyed) return;
          destroyed = true;
          cancelAnimationFrame(frame);
          observer.disconnect();
          removeEventListener('resize', resize);
          document.removeEventListener('visibilitychange', syncMotion);
          motion.removeEventListener('change', syncMotion);
          geo.dispose();
          [im, om, redContour.material, whiteContour.material].forEach(material => material.dispose());
          renderer.dispose();
          hero.classList.remove('is-webgl');
        }
      };
    } catch (error) { console.warn('Atlas WebGL fallback enabled.', error); }
  }
};
