// GitHub Pages serves index.html with Cache-Control: max-age=600, so the
// browser can skip the network entirely for up to 10 minutes and never
// even see a fresh deploy. This service worker takes over every request
// once installed — the page document included — and always goes to the
// network, ignoring HTTP caching, so a reload is guaranteed fresh.
//
// It keeps a copy of whatever it fetches, used only if the network fails,
// so the site still opens on a bad connection.
self.addEventListener('install', function (event) {
  self.skipWaiting();
});

self.addEventListener('activate', function (event) {
  event.waitUntil(self.clients.claim());
});

self.addEventListener('fetch', function (event) {
  // Same-origin GETs only — anything on Drive or YouTube is left alone.
  const url = new URL(event.request.url);
  if (url.origin !== self.location.origin) return;
  if (event.request.method !== 'GET') return;

  // The page document is included deliberately. GitHub Pages sends
  // index.html with a 10-minute cache, so leaving navigations to the
  // browser means an edit can be invisible for ten minutes — and if the
  // page is already open in a tab, far longer. Fetching it here with
  // no-store means a reload always gets the current page.
  //
  // The cached copy is only ever used when the network fails, so the site
  // still opens on a bad connection rather than showing a browser error.
  event.respondWith(
    fetch(event.request, { cache: 'no-store' })
      .then(function (response) {
        if (response && response.ok) {
          const copy = response.clone();
          caches.open('ellen-fallback').then(function (cache) {
            cache.put(event.request, copy);
          });
        }
        return response;
      })
      .catch(function () {
        return caches.match(event.request);
      })
  );
});
