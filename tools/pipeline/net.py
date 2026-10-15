import hashlib, os, time, urllib.parse, urllib.request
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.cache')
os.makedirs(CACHE, exist_ok=True)
UA = {'User-Agent': 'Mozilla/5.0 (doz data pipeline)'}

def fetch(url, data=None, min_size=0, wait=0.4, refresh=False):
    """GET (or POST when data is a dict) with an on-disk cache. Responses shorter than min_size are retried and not cached."""
    key = hashlib.sha1((url + repr(data)).encode()).hexdigest()
    p = os.path.join(CACHE, key)
    if not refresh and os.path.exists(p):
        return open(p, encoding='utf-8').read()
    body = urllib.parse.urlencode(data).encode() if data else None
    t = ''
    for i in range(4):
        try:
            t = urllib.request.urlopen(urllib.request.Request(url, data=body, headers=UA), timeout=60).read().decode('utf-8', 'replace')
            if len(t) >= min_size: break
        except Exception:
            pass
        time.sleep(2 + 2 * i)
    if len(t) >= min_size and t:
        open(p, 'w', encoding='utf-8').write(t)
    time.sleep(wait)
    return t
