// Each scene gets its own viewport state; only a rendered model replaces Iustitia.
(() => {
  document.querySelectorAll('iframe[src*="metamorfose/embed.html"]').forEach(frame => {
    const medal = frame.closest('.cover-3d');
    let intersecting = false;
    let timer;
    const state = value => {
      if (medal) medal.dataset.state = value;
      dispatchEvent(new Event('cover3dstate'));
    };
    const sendVisibility = (requestState = false) => frame.contentWindow?.postMessage({
      type: 'iconocracy:visibility',
      requestState: requestState === true,
      visible: intersecting && !document.hidden && (!medal || getComputedStyle(medal).display !== 'none')
    }, location.origin);
    const start = () => {
      clearTimeout(timer);
      state('loading');
      timer = setTimeout(() => state('error'), 20000); // CDN/module failures may never execute the scene.
      sendVisibility();
    };
    addEventListener('message', event => {
      if (event.origin !== location.origin || event.source !== frame.contentWindow) return;
      if (event.data?.type === 'iconocracy:scene') {
        if (!['ready', 'error'].includes(event.data.state)) return;
        clearTimeout(timer);
        state(event.data.state);
        sendVisibility();
      }
    });
    frame.addEventListener('load', () => sendVisibility(true));
    new IntersectionObserver(entries => {
      intersecting = entries[0].isIntersecting;
      sendVisibility();
    }).observe(frame);
    addEventListener('resize', sendVisibility);
    document.addEventListener('visibilitychange', sendVisibility);
    start();
  });
})();
