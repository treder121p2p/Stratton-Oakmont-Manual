#!/usr/bin/env python3
import sys

files = [
    r'C:\Users\crypt\.openclaw\workspace\belfort\section6_special_handling.html',
    r'C:\Users\crypt\.openclaw\workspace\belfort\section8_phone_skills.html',
    r'C:\Users\crypt\.openclaw\workspace\belfort\section9_resources.html',
]

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for i, line in enumerate(lines, 1):
        for ch in line:
            cp = ord(ch)
            if cp < 128:
                continue
            # Cyrillic
            if 0x0400 <= cp <= 0x04FF:
                continue
            # Latin Extended
            if 0x00C0 <= cp <= 0x024F:
                continue
            # German specific
            if ch in '\u00e4\u00f6\u00fc\u00c4\u00d6\u00dc\u00df\u00e9\u00e8\u00ea\u00eb\u00ef\u00ee\u00f4\u00f9\u00fb\u00ff\u00e0\u00e2\u00e6\u00e7\u0153':
                continue
            # Quotes and dashes
            if ch in '\u00ab\u00bb\u2013\u2014\u201c\u201d\u2018\u2019':
                continue
            # Copyright
            if ch == '\u00a9':
                continue
            try:
                print(f'{filepath.split(chr(92))[-1]}:{i}: U+{cp:04X} [{ch}] context: ...{line[max(0,line.index(ch)-15):line.index(ch)+15].strip()}...')
            except UnicodeEncodeError:
                print(f'{filepath.split(chr(92))[-1]}:{i}: U+{cp:04X} [?cannot print?]')
    print(f'Checked: {filepath.split(chr(92))[-1]}')
