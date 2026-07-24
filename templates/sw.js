const CACHE_NAME = 'edumanage-offline-v2';

// Add the URLs you want to cache here (static assets and offline fallback page)
const URLS_TO_CACHE = [
  '/',
  '/login/',
  '/dashboard/admin/',
  '/admin-panel/students/',
  '/admin-panel/admissions/',
  '/admin-panel/employees/',
  '/online-admission/',
  '/static/logo.png',
  '/static/school_campus.png',
  '/static/vendor/bootstrap/css/bootstrap.min.css',
  '/static/vendor/bootstrap/js/bootstrap.bundle.min.js',
  '/static/vendor/bootstrap-icons/bootstrap-icons.css',
  '/static/vendor/bootstrap-icons/fonts/bootstrap-icons.woff2',
  '/static/vendor/chartjs/chart.umd.min.js',
  '/static/vendor/jsbarcode/JsBarcode.all.min.js',
  '/static/vendor/qrcodejs/qrcode.min.js',
  '/static/vendor/tailwindcss/tailwindcss.js'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('Opened cache');
        return cache.addAll(URLS_TO_CACHE);
      })
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
  self.clients.claim();
});

self.addEventListener('fetch', (event) => {
  // We use a Stale-While-Revalidate strategy for mostly static or offline-first content.
  // Or Network First for dynamic content. 
  // Since this is a dashboard, Network First with a fallback to cache is usually safest.
  if (event.request.method !== 'GET') return;

  event.respondWith(
    fetch(event.request)
      .then((networkResponse) => {
        // Only cache valid responses
        if (networkResponse && networkResponse.status === 200 && networkResponse.type === 'basic') {
          const responseToCache = networkResponse.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, responseToCache);
          });
        }
        return networkResponse;
      })
      .catch(() => {
        // If network fails, try cache
        return caches.match(event.request);
      })
  );
});
