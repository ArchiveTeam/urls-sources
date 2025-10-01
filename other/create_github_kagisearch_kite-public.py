import requests


def main():
    response = requests.get(
        'https://github.com/kagisearch/kite-public/raw/refs/heads/main/kite_feeds.json',
        timeout=10
    )
    assert response.status_code == 200
    with open('900_github_kagisearch_kite-public.txt', 'w') as f:
        for feed_url in [url for d in response.json().values() for url in d['feeds']]:
            f.write('random=RANDOM;all=1;keep_all=1;deep_extract=1;depth=1;url={}\n'.format(feed_url))

if __name__ == '__main__':
    main()

