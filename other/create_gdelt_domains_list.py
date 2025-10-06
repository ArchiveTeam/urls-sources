import csv
import io
import typing

import requests


SOURCES = [
    'http://data.gdeltproject.org/supportingdatasets/DOMAINSBYCOUNTRY-ALLLANGUAGES.TXT',
    'http://data.gdeltproject.org/supportingdatasets/DOMAINSBYCOUNTRY-ENGLISH.TXT'
]

def get_domains(url: str) -> typing.Set[str]:
    response = requests.get(url, timeout=10)
    return {
        row[0]
        for row in csv.reader(io.StringIO(response.text), delimiter='\t')
        if '.' in row[0]
    }

def main():
    items = set()
    for url in SOURCES:
        items |= {
            'random=RANDOM;all=1;keep_all=1;depth=1;url=http://'+domain+'/'
            for domain in get_domains(url)
        }
    with open('900_gdelt_domains.txt', 'w') as f:
        f.write('\n'.join(items))

if __name__ == '__main__':
    main()

