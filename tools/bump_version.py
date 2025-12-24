#!/usr/bin/env python3
import re
import sys

VERSION_FILE = 'include/version.h'

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(data)

def bump_minor_version(content):
    m = re.search(r'#define\s+BUILD_VERSION\s+"v(\d+)\.(\d+)\.(\d+)"', content)
    if not m:
        print('BUILD_VERSION pattern not found', file=sys.stderr)
        return None, content
    major, minor, patch = map(int, m.groups())
    minor += 1
    patch = 0
    new = f'v{major}.{minor}.{patch}'
    content = re.sub(r'(#define\s+BUILD_VERSION\s+)"v\d+\.\d+\.\d+"', r"\1\"" + new + '\"', content, count=1)
    # update WEB_VERSION as well if present
    if re.search(r'#define\s+WEB_VERSION\s+"v\d+\.\d+\.\d+"', content):
        content = re.sub(r'(#define\s+WEB_VERSION\s+)"v\d+\.\d+\.\d+"', r"\1\"" + new + '\"', content, count=1)
    return new, content

def main():
    try:
        s = read_file(VERSION_FILE)
    except FileNotFoundError:
        print('Version file not found: ' + VERSION_FILE, file=sys.stderr)
        sys.exit(2)

    new, out = bump_minor_version(s)
    if new is None:
        sys.exit(1)

    if out != s:
        write_file(VERSION_FILE, out)
        print(new)
        sys.exit(0)
    else:
        print('No change')
        sys.exit(0)

if __name__ == '__main__':
    main()
