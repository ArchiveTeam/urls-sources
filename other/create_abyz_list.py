import multiprocessing.dummy
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import requests

DONE = set()


def check_protocol(url: str):
    if True:
        return url
    if url in DONE:
        return None
    DONE.add(url)
    tries = 0
    while tries < 1:
        try:
            response = requests.get(url, verify=False, timeout=2)
            break
        except Exception as e:
            if 'Failed to establish a new connection' in str(e):
                return None
            print(str(e))
            tries += 1
            print('retrying', tries, url)
    else:
        return url
    print(url, response.url)
    return response.url


def extract_urls(url: str):
    DONE.add(url)
    while True:
        try:
            print('checking', url)
            response = requests.get(url, timeout=5)
            break
        except Exception as e:
            print(str(e))
            continue
    base = re.search('^(https?://[^/]+/)', url).group(1)
    for page in re.findall(r'<a href="([^"]+\.htm)">', response.text):
        page = base + page
        if page not in DONE:
            yield from extract_urls(page)
    with multiprocessing.dummy.Pool(100) as p:
        for site in p.imap_unordered(
            check_protocol,
            re.findall('<a href="(https?://[^"]+)">[^<]+</a><br>', response.text)
        ):
            if site is None:
                continue
            if site.count('/') == 2:
                site += '/'
            elif site.count('/') > 3:
                yield re.search('^(https?://[^/]+/)', site).group(1)
            yield site


def main():
    urls = {'random=RANDOM;all=1;keep_all=1;depth=1;url='+s for s in extract_urls('http://www.abyznewslinks.com/')}
    print('found', len(urls), 'urls')
    with open('3600_abyz.txt', 'w') as f:
        f.write('\n'.join(list(urls)))

if __name__ == '__main__':
    main()

