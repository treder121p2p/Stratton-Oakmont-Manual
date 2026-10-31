#!/usr/bin/env python3
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')
BASE = r"C:\Users\crypt\.openclaw\workspace\belfort"
with open(os.path.join(BASE, "ru_full.json"), "r", encoding="utf-8") as f:
    T = json.load(f)

# Section 7 long paragraphs - using actual German text from HTML
with open(os.path.join(BASE, "section7_motivation.html"), "r", encoding="utf-8") as f:
    content = f.read()

import re
# Find all lang-de inner texts
for m in re.finditer(r'class="lang-de"[^>]*>(.*?)</', content, re.DOTALL):
    de_text = m.group(1).strip()
    if de_text and de_text not in T:
        print(f"MISSING s7: {de_text[:80]}...")

with open(os.path.join(BASE, "section8_phone_skills.html"), "r", encoding="utf-8") as f:
    content = f.read()
for m in re.finditer(r'class="lang-de"[^>]*>(.*?)</', content, re.DOTALL):
    de_text = m.group(1).strip()
    if de_text and de_text not in T:
        print(f"MISSING s8: {de_text[:80]}...")

with open(os.path.join(BASE, "section9_resources.html"), "r", encoding="utf-8") as f:
    content = f.read()
for m in re.finditer(r'class="lang-de"[^>]*>(.*?)</', content, re.DOTALL):
    de_text = m.group(1).strip()
    if de_text and de_text not in T:
        print(f"MISSING s9: {de_text[:80]}...")
