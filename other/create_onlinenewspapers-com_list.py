import multiprocessing
import re
import time
import traceback
import typing
import urllib.parse

import requests


INITIAL_URL = 'https://onlinenewspapers.com/sitemap/sitemapkey.shtml'
INITIAL_URL_DOMAIN = INITIAL_URL.split('/')[2]

def get_urls(url: str) -> typing.List[str]:
    while True:
        print('Getting URL', url)
        try:
            response = requests.get(url, timeout=10)
            assert response.status_code in (200, 404)
            break
        except Exception:
            traceback.print_exc()
            time.sleep(2)
    domain = url.split('/')[2]
    return [
        urllib.parse.urljoin(url, s).split('#')[0]
        for s in re.findall('<li><a[^>]*? href="([^"]+)"', response.text)
    ]

def main():
    done = set()
    todo = {INITIAL_URL}
    sites = set()
    while len(todo) > 0:
        new = set()
        with multiprocessing.Pool(30) as p:
            for results in p.map(get_urls, todo):
                for result in results:
                    if result.split('/')[2] == INITIAL_URL_DOMAIN:
                        new.add(result)
                    else:
                        sites.add(result)
        done |= todo
        todo = new - done
    with open('900_onlinenewspapers-com.txt', 'w') as f:
        for site in sites:
            f.write('random=RANDOM;all=1;keep_all=1;depth=1;url={}\n'.format(site))

if __name__ == '__main__':
    main()

