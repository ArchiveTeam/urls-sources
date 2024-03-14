import re

import requests

BASE_URL = 'https://arxiv.org'
PREFIX = 'random=RANDOM;all=1;url='


def main():
    r = requests.get(BASE_URL)
    lines = set()
    for url in re.findall('"(/list/[^/]+/new)"', r.text):
        lines.add(PREFIX+BASE_URL+url)
    with open('3600_arxiv.txt', 'w') as f:
        f.write('\n'.join(sorted(lines)))

if __name__ == '__main__':
    main()

