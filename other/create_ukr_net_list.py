import gzip
import multiprocessing.dummy
import re

import requests


def worker(url: str):
    print('getting', url)
    while True:
        try:
            response = requests.get(url, timeout=2)
            break
        except:
            continue
    if (match := re.search('<div class="im-tl"><a href="(https?://[^"/]+/?)', response.text)):
        return match.group(1)
    return 'https://www.ukr.net/'


def main():
    response = requests.get('https://www.ukr.net/sitemap/partners.xml.gz')
    data = str(gzip.decompress(response.content), 'utf8')
    with multiprocessing.dummy.Pool(20) as p:
        results = list(p.imap_unordered(
            worker, 
            re.findall(r'<loc>\s*(https?://[^\s<]+)\s*</loc>', data)
        ))
    print(len(results))
    results = {'random=RANDOM;all=1;keep_all=1;depth=1;url='+s for s in results}
    print(len(results))
    with open('600_ukr_net_sites.txt', 'w') as f:
        f.write('\n'.join(sorted(results)))

if __name__ == '__main__':
    main()
        
