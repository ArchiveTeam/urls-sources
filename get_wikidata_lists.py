import json
import os
import re

import requests

ENDPOINT = 'https://query.wikidata.org/sparql'
PREFIX = 'random=RANDOM;all=1;keep_all=1;depth=1;url='
PREFIX_FEED = 'random=RANDOM;all=1;keep_all=1;depth=1;deep_extract=1;url='

QUERY_TEMPLATE_OLD = '''
SELECT DISTINCT ?item ?website WHERE {
  {
    ?item p:P31 ?statement0 .
    ?statement0 (ps:P31/(wdt:P31*)/(wdt:P279*)) wd:{q} .
  }
  UNION
  {
    ?item p:P452 ?statement1 .
    ?statement1 (ps:P452/(wdt:P31*)/(wdt:P279*)) wd:{q} .
  }
  UNION
  {
    ?item p:P3912 ?statement1 .
    ?statement1 (ps:P3912/(wdt:P31*)/(wdt:P279*)) wd:{q} .
  }
  UNION
  {
    ?item p:P361 ?statement1 .
    ?statement1 (ps:P361/(wdt:P31*)/(wdt:P279*)) wd:{q} .
  }
  UNION
  {
    ?item p:P101 ?statement1 .
    ?statement1 (ps:P101/(wdt:P31*)/(wdt:P279*)) wd:{q} .
  }
  UNION
  {
    ?item p:P127 ?statement1 .
    ?statement1 (ps:P127/(wdt:P31*)/(wdt:P279*)) wd:{q} .
  }
  ?item wdt:P856 ?website .
}
'''
QUERY_TEMPLATE = '''
SELECT DISTINCT ?item ?website WHERE {
  {
    ?item p:{p} ?statement0 .
    ?statement0 (ps:{p}/(wdt:P31*)/(wdt:P279*)) wd:{q} .
  }
  ?item wdt:P856 ?website .
}
'''
P_TERMS = [
    'P31',
    'P452',
    'P3912',
    'P361',
    'P101',
    'P127',
    'P366',
    'P1269'
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
            query = QUERY_TEMPLATE.replace('{q}', wikidata_q).replace('{p}', wikidata_p)
            while True:
                try:
                    response = requests.get(
                        ENDPOINT,
                        params={
                            'query': query,
                            'format': 'json'
                        },
                        timeout=1000
                    )
                    assert response.status_code == 200
                    data = json.loads(response.content, strict=False)
                    break
                except KeyboardInterrupt:
                    raise
                except Exception as e:
                    print(str(e))
                    print('retrying')
            print(len(data['results']['bindings']))
            for d in data['results']['bindings']:
                if 'website' not in d:
                    continue
                site = d['website']['value']
                if not re.search('^https?://', site, flags=re.I):
                    continue
                if site.count('/') == 2:
                    site += '/'
                sites.add(PREFIX + site)
                sites.add(PREFIX + re.search('^(https?://+[^/]+/)', site, flags=re.I).group(1))
        with open(filepath+'.txt', 'w') as f:
            f.write('\n'.join(sorted(sites)))

if __name__ == '__main__':
    main()

