import requests


def main():
    response = requests.get('https://raw.githubusercontent.com/gabefair/News-and-Culture-Websites/refs/heads/main/sites.md')
    assert response.status_code == 200
    items = set()
    for line in response.text.splitlines():
        fields = [s.strip() for s in line.split('|')]
        if fields[1] == 'id' \
            or fields[1].startswith('-'):
            continue
        for i in (2, 3):
            url = fields[i]
            if '.' not in url:
                print('No \'.\' in', url)
                continue
            if not url.startswith('https://') or not url.startswith('http://'):
                url = 'http://' + url
            items.add('random=RANDOM;all=1;keep_all=1;depth=1;url='+url)
    print(len(items))
    with open('3600_github_gabefair_News-and-Culture-Websites.txt', 'w') as f:
        f.write('\n'.join(items))

if __name__ == '__main__':
    main()

