import os
import re
import time
import traceback

import requests

ENDPOINT = 'https://qlever.dev/api/wikidata'
PREFIX = 'random=RANDOM;all=1;keep_all=1;depth=1;url='
PREFIX_FEED = 'random=RANDOM;all=1;keep_all=1;depth=1;deep_extract=1;url='

QUERY_TEMPLATE = '''
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX ps: <http://www.wikidata.org/prop/statement/>
PREFIX wikibase: <http://wikiba.se/ontology#>
SELECT DISTINCT ?website WHERE {{
  {{
    ?item p:{p} ?statement0 .
    ?statement0 (ps:{p}{instance_of}/(wdt:P279*)) wd:{q} .
    ?statement0 wikibase:rank ?rank .
    FILTER(?rank != wikibase:DeprecatedRank)
  }}
  ?item wdt:P856 ?website .
}}
'''
P_TERMS = [
    'P31',
    'P452',
    'P3912',
    'P361',
    'P749',
    'P101',
    'P127',
    'P137',
    'P1454',
    'P366',
    'P1269',
    'P2650',
    'P460'
]


def main(directory: str = '.'):
    for filename in os.listdir(directory):
        if not filename.endswith('.wikidata'):
            continue
        print('processing', filename)
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r') as f:
            wikidata_q = f.read().strip()
        sites = set()
        for wikidata_p in P_TERMS:
            print(wikidata_p)
            query = QUERY_TEMPLATE.format(
                q=wikidata_q,
                p=wikidata_p,
                instance_of='' if wikidata_p == 'P31' else '/(wdt:P31?)'
            )
            while True:
                try:
                    response = requests.get(
                        ENDPOINT,
                        params={
                            'query': query,
                            'format': 'json'
                        },
                        headers={
                            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:158.0) Gecko/20100101 Firefox/158.0'
                        },
                        timeout=1000
                    )
                    assert response.status_code == 200
                    data = {
                        s['website']['value']
                        for s in response.json()['results']['bindings']
                    }
                    break
                except KeyboardInterrupt:
                    raise
                except Exception as e:
                    traceback.print_exc()
                    print('retrying')
                    time.sleep(60)
            print(len(data))
            for site in data:
                result = re.search(r'^(https?://[^/\?#]+)', site, flags=re.I)
                if not result:
                    continue
                if site == result.group(1):
                    site += '/'
                sites.add(PREFIX + site)
                sites.add(PREFIX + result.group(1) + '/')
            print('total', len(sites))
        target_file = filepath + '.txt'
        print('final total', len(sites))
        with open(target_file, 'w') as f:
            f.write('\n'.join(sorted(sites)))

if __name__ == '__main__':
    main()

