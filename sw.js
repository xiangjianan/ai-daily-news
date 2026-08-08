/*
 * AI 科技日报 - Service Worker
 *
 * 策略（保证「在线时永远是今天最新」）：
 *   - 文档 / 归档页 / 历史清单 JSON  → network-first（在线取最新，离线回退缓存）
 *   - 同源静态资源（CSS/图标/SVG）   → stale-while-revalidate
 *   - 跨域资源（Google 字体等）       → 透传，不缓存
 */

const CACHE = 'aidaily-v1';

/* 安装：预缓存核心外壳 */
const CORE = [
  './',
  './assets/style.css',
  './manifest.webmanifest',
  './icons/icon-192.png',
  './icons/icon-512.png',
  './icons/icon.svg'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE)
      .then((cache) => cache.addAll(CORE))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(
        keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))
      ))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  const req = event.request;
  if (req.method !== 'GET') return;

  const url = new URL(req.url);
  // 跨域请求透传，交给浏览器默认处理
  if (url.origin !== self.location.origin) return;

  const isDoc =
    req.mode === 'navigate' ||
    url.pathname.endsWith('/') ||
    url.pathname.endsWith('.html') ||
    url.pathname.endsWith('archive_manifest.json');

  if (isDoc) {
    // network-first：在线拿最新日报，失败才回退缓存
    event.respondWith(
      fetch(req, { cache: 'no-cache' })
        .then((res) => {
          const copy = res.clone();
          caches.open(CACHE).then((c) => c.put(req, copy)).catch(() => {});
          return res;
        })
        .catch(() => caches.match(req).then((r) => r || caches.match('./')))
    );
    return;
  }

  // 静态资源：stale-while-revalidate（先用缓存，后台更新）
  event.respondWith(
    (async () => {
      const cache = await caches.open(CACHE);
      const hit = await cache.match(req);
      const network = fetch(req)
        .then((res) => { cache.put(req, res.clone()); return res; })
        .catch(() => null);
      return hit || await network;
    })()
  );
});
