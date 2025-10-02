import json
import os
import re
import traceback

import requests

ENDPOINT = 'https://query.wikidata.org/sparql'
PREFIX = 'random=RANDOM;all=1;keep_all=1;depth=1;url='
PREFIX_FEED = 'random=RANDOM;all=1;keep_all=1;depth=1;deep_extract=1;url='

QUERY_TEMPLATE = '''
SELECT DISTINCT ?item ?website WHERE {{
  {{
    ?item p:{p} ?statement0 .
    ?statement0 (ps:{p}/(wdt:P31*)/(wdt:P279*)) wd:{q} .
  }}
  ?item wdt:P856 ?website .
}}
'''
P_TERMS = [
    'P31',
    'P452',
    'P3912',
    'P361',
    'P101',
    'P127',
    'P366',
    'P1269',
    'P2650',
    'P5869',
    'P460'
]


def main(directory: str = '.'):
    for filename in os.listdir('.'):
        if not filename.endswith('.wikidata'):
            continue
        print('processing', filename)
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r') as f:
            wikidata_q = f.read().strip()
        sites = set()
        for wikidata_p in P_TERMS:
            print(wikidata_p)
            query = QUERY_TEMPLATE.format(q=wikidata_q, p=wikidata_p)
            while True:
                try:
                    response = requests.get(
                        ENDPOINT,
                        params={
                            'query': query,
                            'format': 'csv'
                        },
                        timeout=1000
                    )
                    assert response.status_code == 200
                    data = {
                        s for s in re.findall(r'<uri>\s*(https?://.+?)\s*</uri>', response.text, flags=re.I)
                        if 'wikidata.org' not in s
                    }
                    break
                except KeyboardInterrupt:
                    raise
                except Exception as e:
                    traceback.print_exc()
                    print('retrying')
            print(len(data))
            for site in data:
                if not re.search('^https?://', site, flags=re.I):
                    continue
                if site.count('/') == 2:
                    site += '/'
                sites.add(PREFIX + site)
                sites.add(PREFIX + re.search('^(https?://+[^/]+/)', site, flags=re.I).group(1))
            print('total', len(sites))
        target_file = filepath + '.txt'
        if os.path.isfile(target_file):
            with open(target_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if len(line) == 0:
                        continue
                    if line.startswith('#'):
                        line = line.split('#', 2)[2]
                    sites.add(line)
        print('final total', len(sites))
        with open(target_file, 'w') as f:
            f.write('\n'.join(sorted(sites)))

if __name__ == '__main__':
    main()

