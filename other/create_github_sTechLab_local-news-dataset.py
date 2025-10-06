import csv
import io

import requests


CSV_URL = 'https://raw.githubusercontent.com/sTechLab/local-news-dataset/refs/heads/main/local_news_outlets_dataset.csv'

def main():
    response = requests.get(CSV_URL, timeout=10)
    items = {
        'random=RANDOM;all=1;keep_all=1;depth=1;url=http://'+row[2]+'/'
        for row in csv.reader(io.StringIO(response.text))
        if '.' in row[2]
    }
    with open('900_github_sTechLab_local-news-dataset.txt', 'w') as f:
        f.write('\n'.join(items))

if __name__ == '__main__':
    main()

