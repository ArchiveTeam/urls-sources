import hashlib
import os


def main():
    for filename in os.listdir('.'):
        if not filename.endswith('.txt'):
            continue
        interval = filename.split('_', 1)[0]
        if not interval.isdigit():
            continue
        print('sorting', filename)
        with open(filename, 'r') as f:
            lines = sorted({s.strip() for s in f})
        with open(filename, 'w') as f:
            f.write('\n'.join(sorted(
                lines,
                key=lambda s: (hashlib.sha256(bytes(s.split('#')[-1], 'utf8')).hexdigest(), s)
            )))

if __name__ == '__main__':
    main()

