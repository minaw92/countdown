// GitHub Pages serves index.html with Cache-Control: max-age=600, so the
// browser can skip the network entirely for up to 10 minutes and never
// even see a fresh deploy. This service worker takes over every request
// once installed and always goes to the network, ignoring HTTP caching,
// so repeat visits are guaranteed fresh.
self.addEventListener('install', function (event) {
  self.skipWaiting();
});

self.addEventListener('activate', function (event) {
  event.waitUntil(self.clients.claim());
});

self.addEventListener('fetch', function (event) {
  // Only handle same-origin GETs for our own files. Leave navigation
  // requests (the HTML document itself) to the browser's normal handling —
  // intercepting those here can cause the page to be parsed twice in some
  // browsers. GitHub Pages' 10-minute cache on index.html is short enough
  // that this alone is an acceptable tradeoff.
  const url = new URL(event.request.url);
  if (event.request.mode === 'navigate') return;
  if (url.origin !== self.location.origin) return;

  event.respondWith(
    fetch(event.request, { cache: 'no-store' }).catch(function () {
      return caches.match(event.request);
    })
  );
});
