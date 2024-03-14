import csv
import io
import multiprocessing
import re
import typing

import requests

REPO_URL = 'https://github.com/GSA/govt-urls/'
RAW_PREFIX = REPO_URL + 'raw/master/'


def get_actual_url(url: str, results: typing.Set[str]) -> typing.Optional[str]:
    if not url.startswith('http'):
        return None
    try:
        response = requests.get(url, timeout=10)
    except:
        return None
    if response.status_code != 200:
        return None
    url = response.url
    if url.count('/') == 2:
        url += '/'
    return {
        response.url,
        '/'.join(response.url.split('/', 3)[:3])+'/'
    }


def get_list_csv(filename: str) -> typing.List[str]:
    print('getting', filename)
    response = requests.get(RAW_PREFIX+filename)
    assert response.status_code == 200
    results = set()
    with multiprocessing.Pool(100) as p:
        for urls in p.starmap(
            get_actual_url,
            [
                (row[6], results)
                for row in csv.reader(io.StringIO(response.text), delimiter=',', quotechar='"')
            ]
        ):
            if urls is not None:
                results |= urls
    return results


def get_all_urls() -> typing.List[str]:
    response = requests.get(REPO_URL)
    assert response.status_code == 200
    results = set()
    for filename in re.findall(r'<a\s+href="[^"]+/([^"/]+\.csv)">', response.text):
        results |= get_list_csv(filename)
        print(len(results))
    return results


def main():
    urls = get_all_urls()
    with open('43200_govt_urls.txt', 'w') as f:
        f.write('\n'.join(['random=RANDOM;all=1;keep_all=1;depth=1;url='+s for s in urls]))

if __name__ == '__main__':
    main()

