#!/usr/bin/env python3
"""Add lang-ru elements after lang-de elements in HTML files."""
import json
import re
import os

def merge_translations():
    merged = {}
    for fname in ['tr1.json', 'tr2.json', 'tr3.json', 'tr4.json']:
        with open(fname, 'r', encoding='utf-8') as f:
            merged.update(json.load(f))
    print(f"Merged {len(merged)} translations")
    return merged

def process_file(filepath, tr):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    result = []
    
    for line in lines:
        result.append(line)
        if 'lang-de' not in line:
            continue
        ru = make_ru_line(line, tr)
        if ru:
            result.append(ru)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(result))
    print(f"OK: {filepath}")

def make_ru_line(line, tr):
    """Create a lang-ru version of a lang-de line."""
    # Find element with class="lang-de"
    m = re.search(r'(<(\w+)(\s[^>]*?)class="lang-de"([^>]*?)>)(.*)', line)
    if not m:
        return None
    
    open_tag_full = m.group(1)
    tag_name = m.group(2)
    rest = m.group(5)
    
    # Find matching closing tag by counting depth
    depth = 1
    pos = 0
    close_pos = -1
    while pos < len(rest) and depth > 0:
        tag_m = re.search(r'<(/?)(\w+)([^>]*)>', rest[pos:])
        if not tag_m:
            break
        is_close = tag_m.group(1) == '/'
        tag = tag_m.group(2)
        if is_close:
            if tag == tag_name:
                depth -= 1
                if depth == 0:
                    close_pos = pos + tag_m.start()
        else:
            attrs = tag_m.group(3)
            if not attrs.rstrip().endswith('/'):
                depth += 1
        pos += tag_m.end()
    
    if close_pos == -1:
        return None
    
    inner = rest[:close_pos]
    close_tag_str = rest[close_pos:]
    
    # Clean inner for lookup
    clean = re.sub(r'<[^>]+>', '', inner).strip()
    
    if clean not in tr:
        return None
    
    ru_text = tr[clean]
    
    # Build the line with lang-ru
    leading = len(line) - len(line.lstrip())
    sp = line[:leading]
    ru_open = open_tag_full.replace('lang-de', 'lang-ru', 1)
    
    return f'{sp}{ru_open}{ru_text}{close_tag_str}'

if __name__ == '__main__':
    tr = merge_translations()
    files = [
        'section1_self_improvement.html',
        'section2_selling_power.html',
        'section3_sales_techniques.html'
    ]
    for fp in files:
        if os.path.exists(fp):
            process_file(fp, tr)
        else:
            print(f"SKIP: {fp}")
