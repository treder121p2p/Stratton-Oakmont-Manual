#!/usr/bin/env python3
"""Extract all lang-de text from HTML files for translation."""
import re, json, os, sys

# Force UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

BASE = r"C:\Users\crypt\.openclaw\workspace\belfort"

files = [
    "section7_motivation.html",
    "section8_phone_skills.html",
    "section9_resources.html",
]

for fname in files:
    fpath = os.path.join(BASE, fname)
    with open(fpath, "r", encoding="utf-8") as fh:
        content = fh.read()
    
    print(f"\n=== {fname} ===")
    # Find all lang-de lines and extract inner text
    for line in content.split('\n'):
        if 'class="lang-de"' in line:
            m = re.search(r'>(.+?)(?:</\w+>\s*)$', line.rstrip())
            if not m:
                m = re.search(r'>(.+)$', line.rstrip())
            if m:
                text = m.group(1).strip()
                print(f"DE: {text}")
