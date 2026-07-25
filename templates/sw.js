// EduManage Service Worker — অফলাইন-ফার্স্ট কৌশল
// লোকাল সার্ভার (127.0.0.1:8000) সবসময় Primary।
// এই SW শুধু static assets ক্যাশ করে।

const CACHE_NAME = 'edumanage-offline-v3';
const SYNC_CACHE = 'edumanage-sync-v1';

// প্রি-ক্যাশ করার URL গুলো
const URLS_TO_CACHE = [
  '/',
  '/login/',
  '/dashboard/admin/',
  '/dashboard/teacher/',
  '/dashboard/student/',
  '/admin-panel/students/',
  '/admin-panel/admissions/',
  '/admin-panel/employees/',
  '/admin-panel/classes/',
  '/admin-panel/subjects/',
  '/finance/fees/',
  '/finance/accounts/',
  '/operations/attendance/',
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

// ──────────────────────────────────────────────
//  Install — সব রিসোর্স প্রি-ক্যাশ করা
// ──────────────────────────────────────────────
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('[EduManage SW] ক্যাশ খুলছে...');
      // addAll ব্যর্থ হলেও SW ইনস্টল হবে
      return Promise.allSettled(
        URLS_TO_CACHE.map(url => cache.add(url).catch(e => console.warn(`Cache miss: ${url}`)))
      );
    })
  );
  self.skipWaiting();
});

// ──────────────────────────────────────────────
//  Activate — পুরনো ক্যাশ সাফ করা
// ──────────────────────────────────────────────
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames
          .filter(name => name !== CACHE_NAME && name !== SYNC_CACHE)
          .map(name => {
            console.log(`[EduManage SW] পুরনো ক্যাশ মুছছে: ${name}`);
            return caches.delete(name);
          })
      );
    })
  );
  self.clients.claim();
});

// ──────────────────────────────────────────────
//  Fetch — অফলাইন-ফার্স্ট কৌশল
//  লোকালহোস্ট: Network First (সবসময় তাজা ডেটা)
//  Static assets: Cache First (দ্রুত লোড)
// ──────────────────────────────────────────────
self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;

  const url = new URL(event.request.url);

  // সিঙ্ক API — SW বাইপাস করে সরাসরি নেটওয়ার্কে
  if (url.pathname.startsWith('/api/sync/')) {
    return;
  }

  // Static files — Cache First
  if (url.pathname.startsWith('/static/') || url.pathname.startsWith('/media/')) {
    event.respondWith(
      caches.match(event.request).then((cached) => {
        if (cached) return cached;
        return fetch(event.request).then((response) => {
          if (response && response.status === 200) {
            const clone = response.clone();
            caches.open(CACHE_NAME).then(c => c.put(event.request, clone));
          }
          return response;
        });
      })
    );
    return;
  }

  // Django পেজ — Network First, Cache ফলব্যাক
  event.respondWith(
    fetch(event.request)
      .then((networkResponse) => {
        if (networkResponse && networkResponse.status === 200 && networkResponse.type === 'basic') {
          const responseToCache = networkResponse.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, responseToCache);
          });
        }
        return networkResponse;
      })
      .catch(() => {
        // নেটওয়ার্ক ব্যর্থ — ক্যাশ থেকে সার্ভ করা
        return caches.match(event.request).then(cached => {
          if (cached) return cached;
          // ক্যাশেও নেই — রুট পেজ দেওয়া
          return caches.match('/');
        });
      })
  );
});
