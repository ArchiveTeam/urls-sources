import typing

import requests


def get_url(d: typing.Union[None, str]) -> typing.Union[None, str]:
    if not d or (not d.startswith('http://') and not d.startswith('https://')):
        return None
    if d.count('/') == 2:
        d += '/'
    return d


def get_urls() -> typing.List[str]:
    response = requests.get('https://brave-today-cdn.brave.com/sources.global.json', timeout=10)
    assert response.status_code == 200
    result = []
    for d in response.json():
        site_url = get_url(d.get('site_url'))
        if site_url:
            result.append('random=RANDOM;all=1;keep_all=1;depth=1;url='+site_url)
        feed_url = get_url(d.get('feed_url'))
        if feed_url:
            result.append('random=RANDOM;all=1;keep_all=1;deep_extract=1;depth=1;url='+feed_url)
    return result


def main():
    with open('900_brave.txt', 'w') as f:
        f.write('\n'.join(get_urls()))

if __name__ == '__main__':
    main()

