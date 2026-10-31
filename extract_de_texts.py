#!/usr/bin/env python3
"""Extract all lang-de texts and generate a translations mapping file."""
import re, os, json, sys
sys.stdout.reconfigure(encoding='utf-8')
BASE = r"C:\Users\crypt\.openclaw\workspace\belfort"

# Read all three HTML files and extract unique lang-de inner texts
all_de_texts = set()
for fname in ["section7_motivation.html", "section8_phone_skills.html", "section9_resources.html"]:
    with open(os.path.join(BASE, fname), "r", encoding="utf-8") as f:
        content = f.read()
    for m in re.finditer(r'class="lang-de"[^>]*>(.*?)</', content, re.DOTALL):
        text = m.group(1).strip()
        if text:
            all_de_texts.add(text)

print(f"Found {len(all_de_texts)} unique lang-de texts")
# Save them for reference
with open(os.path.join(BASE, "de_texts.json"), "w", encoding="utf-8") as f:
    json.dump(sorted(list(all_de_texts)), f, ensure_ascii=False, indent=2)
print("Saved to de_texts.json")
