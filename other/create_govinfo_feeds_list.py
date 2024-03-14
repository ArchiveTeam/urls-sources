import re
import urllib.parse

import requests

URL = 'https://www.govinfo.gov/feeds'
PREFIX = 'random=RANDOM;all=1;deep_extract=1;url='


def main():
    response = requests.get(URL, timeout=10)
    assert response.status_code == 200
    with open('3600_govinfo.txt', 'w') as f:
        f.write('\n'.join(
            PREFIX + urllib.parse.urljoin(URL, newurl)
            for newurl in re.findall(r'"([^"]+\.xml)"', response.text)
        ))

if __name__ == '__main__':
    main()
    
