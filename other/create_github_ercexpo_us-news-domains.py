import csv
import io

import requests


CSV_URL = 'https://github.com/ercexpo/us-news-domains/raw/refs/heads/main/us-news-domains-v2.0.0.csv'

def main():
    response = requests.get(CSV_URL, timeout=10)
    items = {
        'random=RANDOM;all=1;keep_all=1;depth=1;url=http://'+row[0]+'/'
        for row in csv.reader(io.StringIO(response.text))
    }
    with open('900_github_ercexpo_us-news-domains.txt', 'w') as f:
        f.write('\n'.join(items))

if __name__ == '__main__':
    main()

