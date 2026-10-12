/* Read the full Steps without leaving the anniversary page. */
(() => {
  'use strict';
  const dialog = document.querySelector('#aa-twelve-steps');
  const trigger = document.querySelector('.steps-open');
  const close = dialog?.querySelector('.aa-dialog-close');
  if (!dialog || !trigger || !close || typeof dialog.showModal !== 'function') return;
  const root = document.documentElement;
  const body = document.body;
  let scrollPosition = 0;
  let pointerStartedOutside = false;
  function openDialog(event) {
    event.preventDefault();
    if (dialog.open) return;
    scrollPosition = window.scrollY;
    dialog.showModal();
    body.style.setProperty('--dialog-scroll-top', `${-scrollPosition}px`);
    root.classList.add('steps-dialog-open');
    dialog.querySelector('.aa-dialog-content').scrollTop = 0;
    dialog.querySelector('#aa-dialog-title').focus({ preventScroll: true });
  }
  function closeDialog(event) {
    event?.preventDefault();
    if (dialog.open) dialog.close();
  }
  trigger.addEventListener('click', openDialog);
  close.addEventListener('click', closeDialog);
  dialog.addEventListener('close', () => {
    root.classList.remove('steps-dialog-open');
    body.style.removeProperty('--dialog-scroll-top');
    const previous = root.style.scrollBehavior;
    root.style.scrollBehavior = 'auto';
    window.scrollTo(0, scrollPosition);
    root.style.scrollBehavior = previous;
    trigger.focus({ preventScroll: true });
  });
  function outside(event) {
    const rect = dialog.getBoundingClientRect();
    return event.clientX < rect.left || event.clientX > rect.right ||
      event.clientY < rect.top || event.clientY > rect.bottom;
  }
  dialog.addEventListener('pointerdown', event => { pointerStartedOutside = outside(event); });
  dialog.addEventListener('click', event => {
    if (pointerStartedOutside && outside(event)) closeDialog();
    pointerStartedOutside = false;
  });
  // Native dialog handles Escape, focus containment and an inert background.
})();

/* CMA: SVG introduction and once-per-visit scroll choreography. No dependencies. */
(() => {
  'use strict';
  const root = document.documentElement;
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)');
  const main = document.querySelector('main');
  const hero = document.querySelector('.s1');
  const intro = document.querySelector('.intro-overlay');
  const logo = document.querySelector('.intro-logo');
  const skip = document.querySelector('.intro-skip');
  const animations = new Set();
  let introDone = false;
  let observer;
  let lineObserver;
  let acornObserver;
  let grassObserver;
  let growthTimer;
  let seedParkTimer;
  const wait = ms => new Promise(resolve => setTimeout(resolve, ms));
  const frame = () => new Promise(resolve => requestAnimationFrame(resolve));
  const delay = (element, ms) => element.style.setProperty('--delay', `${ms > 0 ? ms + 80 : 0}ms`);
  function visible(element) {
    element.classList.remove('waiting');
    element.classList.add('visible');
  }
  async function decode(elements) {
    const images = [...new Set(elements.flatMap(element => element.tagName === 'IMG' ? [element] : Array.from(element.querySelectorAll('img'))))];
    await Promise.race([
      Promise.allSettled(images.map(image => image.decode ? image.decode() : Promise.resolve())),
      wait(450)
    ]);
  }
  async function reveal(element) {
    if (element.dataset.revealed) return;
    element.dataset.revealed = 'true';
    await decode([element]);
    if (reduce.matches) delay(element, 0);
    visible(element);
    if (element.classList.contains('cloud')) driftCloud(element);
    if (element.classList.contains('big-five')) countFive(element);
  }
  const depthArt = Array.from(document.querySelectorAll('[data-depth]'));
  const numeral = document.querySelector('.big-five');
  async function countFive(element) {
    if (element.dataset.counted || reduce.matches) { element.textContent = '5'; return; }
    element.dataset.counted = 'true';
    element.textContent = '1';
    await wait(240);
    for (const [index, duration] of [130, 130, 160, 180].entries()) {
      await wait(duration);
      if (reduce.matches || element.dataset.cancelCount) { element.textContent = '5'; return; }
      element.textContent = String(index + 2);
    }
  }
  function updateDepth() {
    depthArt.forEach(art => {
      if (reduce.matches || window.innerWidth < 1000) { art.style.setProperty('--depth-y', '0px'); return; }
      const section = art.closest('.section');
      const rect = section.getBoundingClientRect();
      if (rect.bottom < 0 || rect.top > window.innerHeight) return;
      const progress = (window.innerHeight / 2 - rect.top - rect.height / 2) * 2 / (window.innerHeight + rect.height);
      const offset = Math.max(-1, Math.min(1, progress)) * Number(art.dataset.depth);
      art.style.setProperty('--depth-y', `${offset.toFixed(2)}px`);
    });
  }
  function driftCloud(cloud) {
    if (reduce.matches || cloud.classList.contains('cloud-drifting')) return;
    const stage = cloud.closest('.visual');
    if (!stage) return;
    // Measure before animation: both loop endpoints are outside the clipped scene.
    const enter = stage.clientWidth - cloud.offsetLeft;
    const exit = -cloud.offsetLeft - cloud.offsetWidth;
    const duration = stage.clientWidth < 1000 ? 140 : 160;
    cloud.style.setProperty('--cloud-enter', `${enter}px`);
    cloud.style.setProperty('--cloud-exit', `${exit}px`);
    cloud.style.setProperty('--cloud-duration', `${duration}s`);
    cloud.style.setProperty('--cloud-phase', `${-duration * enter / (enter - exit)}s`);
    cloud.classList.add('cloud-drifting');
  }
  // Paragraphs are independent: long text containers never trigger too early.
  document.querySelectorAll('.copy').forEach(copy => {
    let index = 0;
    copy.querySelectorAll(':scope > *, :scope > .steps > li, :scope > .first-step-cta > *').forEach(element => {
      if (element.classList.contains('steps') || element.classList.contains('first-step-cta') || element.classList.contains('wish-actions') || element.classList.contains('sr-only')) return;
      element.classList.add('motion', 'text-motion');
      if (copy.closest('.s1')) element.classList.add('hero-part');
      element.style.setProperty('--delay', `${Math.min(230, 80 + index++ * 50)}ms`);
    });
  });
  // Footer content stays visible; its rule has a viewport-edge trigger below.
  document.querySelectorAll('.support > div, .contacts > a, .thanks-mobile').forEach((element, i) => {
    element.classList.add('motion', 'text-motion');
    element.style.setProperty('--delay', `${90 + i % 4 * 40}ms`);
  });
  document.querySelector('.header-link')?.classList.add('motion', 'text-motion', 'hero-part');
  const words = Array.from(document.querySelectorAll('.life-words li'));
  words.forEach(word => word.classList.add('motion', 'letters-enabled'));
  document.querySelectorAll('.rule, .site-footer-inner').forEach(line => line.classList.add('motion', 'line-reveal'));
  // Enable the closed state only after it loads, before the viewport reveal.
  // Late or failed image loads keep the original open-door illustration.
  document.querySelectorAll('.door-stage').forEach(stage => {
    const closed = stage.querySelector('.door-closed');
    if (!closed) return;
    const enable = () => {
      if (!reduce.matches && 'IntersectionObserver' in window && closed.naturalWidth > 0 &&
          !stage.dataset.revealed && stage.getBoundingClientRect().bottom >= 0) {
        stage.classList.add('door-transition-enabled');
      }
    };
    if (closed.complete) enable();
    else closed.addEventListener('load', enable, { once: true });
  });
  const elements = Array.from(document.querySelectorAll('.motion'));
  const layered = Array.from(document.querySelectorAll('.steps-stage, .dandelion-stage, .sprout-stage, .lighthouse-stage, .rest-stage, .lion-stage'));
  const supportsLayers = window.CSS?.supports('clip-path', 'polygon(0 0, 100% 0, 100% 100%)') &&
    (window.CSS.supports('mask-image', 'url("assets/steps-mask.svg")') || window.CSS.supports('-webkit-mask-image', 'url("assets/steps-mask.svg")'));
  if (!reduce.matches && supportsLayers && 'IntersectionObserver' in window) {
    layered.forEach(stage => stage.classList.add('layers-enabled'));
  }

  function initWishes() {
    const section = document.querySelector('.s13');
    const button = document.querySelector('.wish-button');
    const text = document.querySelector('.wish-text');
    const status = document.querySelector('#wish-status');
    const art = document.querySelector('.wishes-art');
    let wishes;
    try { wishes = JSON.parse(document.querySelector('#wish-data')?.textContent || '[]'); } catch { return; }
    if (!section || !button || !text || !Array.isArray(wishes)) return;
    wishes = wishes.filter(wish => typeof wish === 'string' && wish.trim());
    if (wishes.length < 2) return;
    section.classList.add('wishes-ready');
    text.textContent = 'Нажми, чтобы получить несколько слов поддержки.';
    if (status) { text.setAttribute('aria-hidden', 'true'); status.textContent = text.textContent; }
    // A shuffled deck visits every wish once before starting the next cycle.
    let previous = -1;
    let deck = [];
    function nextWish() {
      if (!deck.length) {
        deck = wishes.map((_, index) => index);
        for (let i = deck.length - 1; i > 0; i--) {
          const j = Math.floor(Math.random() * (i + 1));
          [deck[i], deck[j]] = [deck[j], deck[i]];
        }
        if (deck[deck.length - 1] === previous) [deck[0], deck[deck.length - 1]] = [deck[deck.length - 1], deck[0]];
      }
      previous = deck.pop();
      return wishes[previous];
    }
    let used = 0;
    const seeds = Array.from(art?.querySelectorAll('.seed-layer') || []);
    function park() {
      if (reduce.matches || !art?.classList.contains('layers-enabled')) return;
      art.classList.add('seeds-parked');
    }
    function consumeSeed() {
      if (reduce.matches || !art?.classList.contains('layers-enabled') || !seeds.length) return;
      park();
      if (used >= seeds.length) {
        seeds.forEach(seed => seed.classList.remove('seed-used'));
        used = 0;
      }
      seeds[used++].classList.add('seed-used');
    }
    function showLetters(value) {
      if (reduce.matches) { text.textContent = value; return; }
      const fragment = document.createDocumentFragment();
      const step = Math.min(9, 380 / Math.max(1, value.length - 1));
      let index = 0;
      value.split(/(\s+)/u).forEach(part => {
        if (/^\s+$/u.test(part)) { fragment.appendChild(document.createTextNode(part)); index += part.length; return; }
        const word = document.createElement('span');
        word.className = 'wish-word';
        Array.from(part).forEach(char => {
          const letter = document.createElement('span');
          letter.className = 'wish-letter';
          letter.textContent = char;
          letter.style.setProperty('--letter-delay', `${(index++ * step).toFixed(1)}ms`);
          word.appendChild(letter);
        });
        fragment.appendChild(word);
      });
      text.replaceChildren(fragment);
    }
    button.addEventListener('click', () => {
      const value = nextWish();
      showLetters(value);
      if (status) status.textContent = value;
      button.textContent = 'Ещё несколько слов';
      consumeSeed();
    });
    return { park };
  }
  const wishesController = initWishes();
  const scenes = [document.querySelector('.s6 .visual'), document.querySelector('.s7 .visual'), document.querySelector('.s9 .visual'), ...layered].filter(Boolean);
  // Trigger at the objects themselves, not at the top of their tall section.
  const sceneByTrigger = new Map(scenes.map(scene => [layered.includes(scene) ? (scene.querySelector('.illustration-trigger') || scene) : scene.querySelector('.illustration-trigger, .lamp, .chair-2'), scene]));
  const sceneElements = new Set([...layered, ...scenes.flatMap(scene => Array.from(scene.querySelectorAll('.motion:not(.dot)')))]);
  async function playScene(scene) {
    if (scene.dataset.played) return;
    scene.dataset.played = 'true';
    const local = Array.from(scene.querySelectorAll('.motion:not(.dot)'));
    await decode([scene, ...local]);
    await frame();
    // Commit the separated initial poses before starting their transitions.
    if (scene.classList.contains('lion-stage')) await frame();
    if (layered.includes(scene)) {
      delay(scene, 80);
      visible(scene);
      // First reveal the surrounding illustration, then reveal steps / move seeds.
      if (!scene.classList.contains('sprout-stage')) scene.classList.add('scene-ready');
      else if (window.innerWidth >= 1000) {
        wait(980).then(() => scene.classList.add('scene-ready'));
      }
      if (scene.classList.contains('wishes-art')) {
        clearTimeout(seedParkTimer);
        seedParkTimer = setTimeout(() => wishesController?.park(), 530);
      } else if (scene.classList.contains('dandelion-stage')) scene.classList.add('seeds-flying');
    } else if (scene.closest('.s6')) {
      const hands = scene.querySelector('.hands-stage');
      const circle = scene.querySelector('.deco');
      delay(hands, 100);
      delay(circle, 100);
      visible(hands);
      visible(circle);
    } else if (scene.closest('.s7')) {
      const lamp = scene.querySelector('.lamp');
      const light = scene.querySelector('.lamp-light');
      const glow = scene.querySelector('.lamp-glow');
      delay(lamp, 80);
      delay(light, 630);
      visible(lamp);
      visible(light);
      words.forEach((word, i) => { delay(word, 1050 + i * 160); visible(word); });
      wait(3100).then(() => { if (!reduce.matches) light.classList.add('light-awake'); });
      wait(window.innerWidth < 1000 ? 2230 : 3260).then(() => glow?.classList.add('glow-on'));
    } else {
      const shape = scene.querySelector('.chairs-shape');
      delay(shape, 80);
      visible(shape);
      scene.querySelectorAll('.chair').forEach((chair, i) => {
        if (i === 4 && observer && window.innerWidth < 1000 && chair.getBoundingClientRect().top > window.innerHeight * .8) {
          // The foreground seat may be below the fold; let it appear when read.
          delay(chair, 120);
          observer.observe(chair);
        } else {
          delay(chair, 180 + i * 225);
          visible(chair);
        }
      });
    }
  }
  async function showHero() {
    const local = elements.filter(element => hero.contains(element));
    await decode(local);
    await frame();
    local.forEach(element => {
      // Hero lines below the fold must draw when reached, after the intro.
      if (lineObserver && !reduce.matches && element.classList.contains('line-reveal')) {
        lineObserver.observe(element);
        return;
      }
      // On phones the panorama can be below the fold: wait until it is in view.
      if (observer && !reduce.matches && !element.classList.contains('hero-part')) { visible(element); return; }
      if (observer && !reduce.matches && element.classList.contains('art') && element.getBoundingClientRect().top > window.innerHeight * .9) {
        observer.observe(element);
      } else {
        visible(element);
        if (element.classList.contains('cloud')) driftCloud(element);
      }
    });
  }
  function finishIntro(immediate = false) {
    if (introDone) return;
    introDone = true;
    clearTimeout(window.cmaIntroFallback);
    main.inert = false;
    root.classList.remove('intro-pending');
    if (!immediate && intro) {
      root.classList.add('intro-settling');
      intro.querySelector('.intro-paper').animate([{ opacity: 1 }, { opacity: 0 }], {
        duration: 550, easing: 'ease-out', fill: 'forwards'
      });
      wait(600).then(() => {
        root.classList.remove('intro-settling');
        intro.remove();
        animations.forEach(animation => animation.cancel());
        animations.clear();
      });
    } else {
      root.classList.remove('intro-settling');
      intro?.remove();
      animations.forEach(animation => animation.cancel());
      animations.clear();
    }
    skip?.remove();
    showHero();
  }
  async function playIntro() {
    if (!root.classList.contains('intro-pending') || reduce.matches || !logo?.animate) {
      finishIntro(true);
      return;
    }
    main.inert = true;
    window.scrollTo(0, 0);
    const rect = logo.getBoundingClientRect();
    logo.style.left = `${rect.left}px`;
    logo.style.top = `${rect.top}px`;
    logo.style.width = `${rect.width}px`;
    logo.style.transform = 'none';
    const strokes = Array.from(logo.querySelectorAll('path, polyline'));
    try {
      await frame();
      const draws = strokes.map((stroke, i) => {
        const length = Math.ceil(stroke.getTotalLength()) + 1;
        stroke.style.strokeDasharray = `${length} ${length}`;
        stroke.style.strokeDashoffset = String(length);
        stroke.style.opacity = '1';
        const animation = stroke.animate([
          { strokeDashoffset: String(length) }, { strokeDashoffset: '0' }
        ], {
          duration: i === 0 ? 1450 : 900,
          delay: i === 0 ? 100 : 600 + (i - 1) * 300,
          easing: 'cubic-bezier(.45,0,.2,1)', fill: 'forwards'
        });
        animations.add(animation);
        return animation.finished.then(() => {
          stroke.style.strokeDashoffset = '0';
          animation.cancel();
          animations.delete(animation);
        }).catch(() => {});
      });
      await Promise.all(draws);
      if (introDone) return;
      await wait(200);
      if (introDone) return;
      // Measure at docking time, including the mobile logo's actual size.
      const destination = document.querySelector('.hero-header .brand').getBoundingClientRect();
      const transform = `translate(${destination.left - rect.left}px, ${destination.top - rect.top}px) scale(${destination.width / rect.width})`;
      const docking = logo.animate([{ transform: 'none' }, { transform }], {
        duration: 1150, easing: 'cubic-bezier(.65,0,.2,1)', fill: 'forwards'
      });
      animations.add(docking);
      await docking.finished.catch(() => {});
      if (introDone) return;
      logo.style.transform = transform;
      docking.cancel();
      animations.delete(docking);
      finishIntro();
    } catch (error) {
      // A failed SVG or animation API must never block the site.
      finishIntro(true);
    }
  }
  function stopMotion() {
    observer?.disconnect();
    lineObserver?.disconnect();
    acornObserver?.disconnect();
    grassObserver?.disconnect();
    clearTimeout(growthTimer);
    clearTimeout(seedParkTimer);
    elements.forEach(element => { delay(element, 0); visible(element); });
    layered.forEach(scene => scene.classList.add('scene-ready'));
    if (numeral) { numeral.dataset.cancelCount = 'true'; numeral.textContent = '5'; }
    updateDepth();
    finishIntro(true);
  }
  if (reduce.matches) {
    stopMotion();
    return;
  }
  if ('IntersectionObserver' in window) {
    // Breeze runs only while the illustration is on screen, and resumes in place.
    const grass = document.querySelector('.rest-stage');
    if (grass && supportsLayers) {
      grassObserver = new IntersectionObserver(entries => {
        entries.forEach(entry => {
          if (entry.isIntersecting) entry.target.classList.add('grass-awake');
          else entry.target.classList.remove('grass-awake');
        });
      }, { threshold: 0, rootMargin: '0px' });
      grassObserver.observe(grass);
    }
    const acorn = document.querySelector('.acorn-trigger');
    const sprout = document.querySelector('.sprout-stage');
    if (acorn && sprout && supportsLayers) {
      acornObserver = new IntersectionObserver(entries => {
        entries.forEach(entry => {
          if (window.innerWidth >= 1000 || sprout.classList.contains('scene-ready')) return;
          clearTimeout(growthTimer);
          if (!entry.isIntersecting || entry.intersectionRatio < .99) return;
          growthTimer = setTimeout(async () => {
            const bounds = acorn.getBoundingClientRect();
            if (bounds.top < 24 || bounds.bottom > window.innerHeight - 24) return;
            await decode([sprout]);
            const current = acorn.getBoundingClientRect();
            if (current.top < 24 || current.bottom > window.innerHeight - 24) return;
            visible(sprout);
            sprout.classList.add('scene-ready');
            acornObserver.unobserve(acorn);
          }, 950);
        });
      }, { threshold: 1, rootMargin: '-24px 0px -24px 0px' });
      acornObserver.observe(acorn);
    }
    // Include the viewport edge: even the footer rule can enter at page end.
    lineObserver = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        lineObserver.unobserve(entry.target);
        reveal(entry.target);
      });
    }, { threshold: 0, rootMargin: '0px' });
    observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        observer.unobserve(entry.target);
        if (sceneByTrigger.has(entry.target)) playScene(sceneByTrigger.get(entry.target));
        else reveal(entry.target);
      });
    }, { threshold: 0, rootMargin: '0px 0px -20% 0px' });
    elements.forEach(element => {
      const rect = element.getBoundingClientRect();
      // Restored deep scroll positions keep earlier content readable.
      if (rect.bottom < 0) { visible(element); return; }
      element.classList.add('waiting');
      if (hero.contains(element)) return;
      if (element.classList.contains('line-reveal')) { lineObserver.observe(element); return; }
      if (!sceneElements.has(element)) observer.observe(element);
    });
    sceneByTrigger.forEach((scene, trigger) => {
      if (trigger.getBoundingClientRect().bottom < 0) {
        visible(scene);
        scene.classList.add('scene-ready');
        scene.querySelectorAll('.motion').forEach(visible);
      } else observer.observe(trigger);
    });
  } else {
    elements.forEach(visible);
    layered.forEach(scene => scene.classList.add('scene-ready'));
    document.querySelector('.lamp-glow')?.classList.add('glow-on');
  }
  skip?.addEventListener('click', () => finishIntro(true));
  document.querySelector('.skip')?.addEventListener('click', () => finishIntro(true));
  document.addEventListener('keydown', event => { if (event.key === 'Escape') finishIntro(true); });
  reduce.addEventListener('change', () => { if (reduce.matches) stopMotion(); });
  let depthScheduled = false;
  window.addEventListener('scroll', () => {
    if (depthScheduled || reduce.matches || window.innerWidth < 1000) return;
    depthScheduled = true;
    requestAnimationFrame(() => { updateDepth(); depthScheduled = false; });
  }, { passive: true });
  let resizeTimer;
  window.addEventListener('resize', () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => {
      updateDepth();
      const sprout = document.querySelector('.sprout-stage');
      if (window.innerWidth >= 1000 && sprout?.dataset.played) sprout.classList.add('scene-ready');
      const cloud = hero.querySelector('.cloud.cloud-drifting');
      if (!cloud) return;
      cloud.classList.remove('cloud-drifting');
      driftCloud(cloud);
    }, 180);
  });
  window.addEventListener('pagehide', () => finishIntro(true), { once: true });
  updateDepth();
  playIntro();
})();
