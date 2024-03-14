import os
import re

REASON_DUPLICATE = '#REASON=DUPLICATE#'
REASON_WAYBACK = '#REASON=WAYBACK#'


def main(directory: str = '.'):
    files = []
    for filename in os.listdir(directory):
        if not filename.endswith('.txt'):
            continue
        interval = filename.split('_', 1)[0]
        if not interval.isdigit():
            continue
        interval = int(interval)
        files.append((interval, os.path.join(directory, filename)))
    seen = set()
    if os.path.isfile('ignore.txt'):
        with open('ignore.txt', 'r') as f:
            for line in f:
                print(line)
                seen.add(re.search(r'^https?://(?:www\.)?(.+?)/?$', line.strip(), re.I).group(1))
    for _, filepath in sorted(files):
        print('deduplicating', filepath)
        new = []
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if len(line) == 0:
                    continue
                if line.startswith(REASON_WAYBACK):
                    line = line[len(REASON_WAYBACK):]
                if line.startswith(REASON_DUPLICATE):
                    line = line[len(REASON_DUPLICATE):]
                if line.startswith('#'):
                    continue
                line = line.split('#', 1)[0]
                line = line.rstrip('?&')
                site = line.split('url=', 1)[1].lower()
                is_wayback = re.search(r'^https?://web\.archive\.org/web/', site, re.I)
                site = re.search(r'^https?://(?:www\.)?(.+?)/?$', site, re.I)
                if site:
                    site = site.group(1).lower()
                    if site not in seen:
                        seen.add(site)
                    else:
                        line = REASON_DUPLICATE + line
                if is_wayback and not line.startswith('#'):
                    line = REASON_WAYBACK + line
                new.append(line)
        with open(filepath, 'w') as f:
            f.write('\n'.join(new))

if __name__ == '__main__':
    main()

