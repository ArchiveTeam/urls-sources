import json
import re
import time
import traceback
import typing

import requests


def get_url(url: str) -> str:
    while True:
        print('Getting', url)
        try:
            response = requests.get(
                url,
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:136.0) Gecko/20100101 Firefox/136.0'},
                timeout=10
            )
            assert response.status_code == 200
            return response.text
        except Exception:
            traceback.print_exc()
            time.sleep(1)


def extract_urls(url: str) -> typing.Set[str]:
    response = get_url(url)
    items = set()
    for s in re.findall('(https?://[^,"\s]+)', response):
        if 'web.archive.org' not in s:
            items.add('random=RANDOM;all=1;keep_all=1;depth=1;url='+s)
    return items


def main():
    response = get_url('https://github.com/GSA/govt-urls')
    for s in re.findall(r'data\-target="react\-partial\.embeddedData">(\{".+?\})<', response):
        data = json.loads(s)
        if 'props' in data and 'initialPayload' in data['props']:
            break
    items = set()
    for d in data['props']['initialPayload']['tree']['items']:
        path = d['path']
        if path.split('_', 1)[0].isnumeric() and path.rsplit('.', 1)[1] == 'csv':
            new_items = extract_urls('https://github.com/GSA/govt-urls/raw/refs/heads/main/'+path)
            print(path, len(new_items))
            items |= new_items
    with open('43200_github_GSA_govt-urls.txt', 'w') as f:
        f.write('\n'.join(items))

if __name__ == '__main__':
    main()

