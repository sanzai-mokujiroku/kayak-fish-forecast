// カヤック釣果予報 サービスワーカー：アプリの外枠をキャッシュし、電波の弱い出艇地点でも起動できるようにする。
// アプリを更新したら CACHE の番号を上げる（古いキャッシュを破棄するため）。
// ※予報データ(Open-Meteo/tide736)は別オリジンなのでキャッシュせず、常に最新をネットから取る。
const CACHE = "fish-forecast-v2";
const ASSETS = [
  "./", "./index.html", "./manifest.webmanifest", "./stations.js",
  "./icon-192.png", "./icon-512.png", "./icon-180.png",
];

self.addEventListener("install", (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(ASSETS)).then(() => self.skipWaiting()));
});
self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys().then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});
self.addEventListener("fetch", (e) => {
  if (e.request.method !== "GET") return;
  const url = new URL(e.request.url);
  // 別オリジン（予報API）はSWが介入しない＝素通しで常に最新・オフライン時は普通に失敗
  if (url.origin !== location.origin) return;

  const isShell = e.request.mode === "navigate"
    || url.pathname.endsWith("/")
    || url.pathname.endsWith("/index.html")
    || url.pathname.endsWith("/stations.js");

  if (isShell) {
    // ネットワーク優先（オンラインなら最新HTML/JS、圏外はキャッシュにフォールバック）
    e.respondWith(
      fetch(e.request)
        .then((res) => {
          if (res && res.status === 200 && res.type === "basic") {
            const cp = res.clone();
            caches.open(CACHE).then((c) => c.put(e.request, cp));
          }
          return res;
        })
        .catch(() => caches.match(e.request).then((c) => c || caches.match("./index.html")))
    );
    return;
  }
  // アイコン等はキャッシュ優先
  e.respondWith(caches.match(e.request).then((cached) => cached || fetch(e.request)));
});
