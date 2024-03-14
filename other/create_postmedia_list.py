import re
import typing

import requests


def get_urls() -> typing.List[str]:
    response = requests.get('https://www.postmedia.com/brands/')
    assert response.status_code == 200
    result = []
    for url in re.findall(r'<a\s+class="brands--region--link"\s+href="([^"]+)"', response.text):
        if url.count('/') == 2:
            url += '/'
        result.append('random=RANDOM;all=1;keep_all=1;depth=1;url='+url)
    return result


def main():
    with open('3600_postmedia_com.txt', 'w') as f:
        f.write('\n'.join(get_urls()))

if __name__ == '__main__':
    main()

