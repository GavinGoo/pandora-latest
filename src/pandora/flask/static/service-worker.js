const Pandora_Cache_Name = "PandoraWeb_Cache_250112";

self.addEventListener("fetch", (event) => {
    const url = new URL(event.request.url);
    if (url.protocol !== 'http:' && url.protocol !== 'https:') {
        event.respondWith(fetch(event.request));
        return;
    }
    if (url.pathname.endsWith('service-worker.js')) {
        event.respondWith(fetch(event.request));
        return;
    }
    event.respondWith(
        caches.match(event.request).then((response) => {
            if (response) {
                return response;
            }
            if (/\.(css|js|woff|woff2|png|jpg)$/.test(event.request.url)) {
                return caches.open(Pandora_Cache_Name).then((cache) => {
                    return fetch(event.request).then((networkResponse) => {
                        cache.put(event.request, networkResponse.clone());
                        return networkResponse;
                    });
                });
            }
            return fetch(event.request);
        })
    );
});

self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.map(cacheName => {
                    if (cacheName !== Pandora_Cache_Name) {
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
});

self.addEventListener('install', (event) => {
    event.waitUntil(self.skipWaiting());
});