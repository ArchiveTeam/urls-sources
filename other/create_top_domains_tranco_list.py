import re

import requests


def main():
    response = requests.get('https://tranco-list.eu/latest_list?subdomains=true')
    assert response.status_code == 200
    url = response.url.replace('/list/', '/download/')
    assert re.match(r'^https://tranco-list\.eu/download/[^/]+/1000000$', url)
    print('Downloading latest list at', url)
    response = requests.get(url)
    assert response.status_code == 200 and len(response.text) > 1048 ** 2
    with open('86400_tranco_list_top_domains.txt', 'w') as f:
        for line in response.text.splitlines()[:200000]:
            line = line.strip()
            if len(line) == 0:
                continue
            line = line.split(',', 1)[1]
            f.write('random=RANDOM;all=1;keep_all=1;depth=1;url=http://'+line+'/\n')
            f.write('random=RANDOM;all=1;keep_all=1;depth=1;url=https://'+line+'/\n')

if __name__ == '__main__':
    main()

