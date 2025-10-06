import gzip
import json

import requests


DATA_URL = 'https://github.com/wm-newslab/3DLNews/raw/refs/heads/main/resources/usa_2016_2024_pu5e.json.gz'

def main():
    response = requests.get(DATA_URL, timeout=10)
    data = json.loads(gzip.decompress(response.content))
    items = set()
    for _, types in data.items():
        for _, l in types.items():
            for item in l:
                website = item.get('website')
                if website and len(website) > 0:
                    items.add('random=RANDOM;all=1;keep_all=1;depth=1;url='+website)
                rss = item.get('rss', [])
                for feed_url in rss:
                    items.add('random=RANDOM;all=1;keep_all=1;deep_extract=1;depth=1;url='+feed_url)
    with open('900_github_wm-newslab_3DLNews.txt', 'w') as f:
        f.write('\n'.join(items))

if __name__ == '__main__':
    main()

