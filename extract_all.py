#!/usr/bin/env python3
"""Build ru_full.json by reading actual German text from HTML files and generating Russian translations."""
import re, os, sys, json
sys.stdout.reconfigure(encoding='utf-8')
BASE = r"C:\Users\crypt\.openclaw\workspace\belfort"

# Read all HTML files and extract unique lang-de inner texts
all_de = []
for fname in ["section7_motivation.html", "section8_phone_skills.html", "section9_resources.html"]:
    with open(os.path.join(BASE, fname), "r", encoding="utf-8") as f:
        content = f.read()
    for m in re.finditer(r'class="lang-de"[^>]*>(.*?)</', content, re.DOTALL):
        text = m.group(1).strip()
        if text and text not in all_de:
            all_de.append(text)

print(f"Found {len(all_de)} unique lang-de texts")
# Save for translation
with open(os.path.join(BASE, "de_texts_for_translate.json"), "w", encoding="utf-8") as f:
    json.dump(all_de, f, ensure_ascii=False, indent=2)
print("Saved de_texts_for_translate.json")
