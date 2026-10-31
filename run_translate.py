import re, os, sys, json
sys.stdout.reconfigure(encoding='utf-8')
BASE = r"C:\Users\crypt\.openclaw\workspace\belfort"
with open(os.path.join(BASE, "ru_full.json"), "r", encoding="utf-8") as fh:
    T = json.load(fh)
print(f"Loaded {len(T)} translations")

def extract_text(line):
    m = re.search(r'>(.+?)(?:</\w+>\s*)$', line.rstrip())
    if m: return m.group(1).strip()
    m = re.search(r'>(.+)$', line.rstrip())
    if m: return m.group(1).strip()
    return ''

files = ["section7_motivation.html", "section8_phone_skills.html", "section9_resources.html"]
for fname in files:
    fpath = os.path.join(BASE, fname)
    with open(fpath, "r", encoding="utf-8") as fh: lines = fh.readlines()
    new_lines = []
    missing = []
    for line in lines:
        new_lines.append(line)
        if 'class="lang-de"' in line:
            inner = extract_text(line)
            if inner in T:
                ru_line = line.replace('class="lang-de"', 'class="lang-ru"', 1)
                if inner and inner in ru_line:
                    ru_line = ru_line.replace(inner, T[inner], 1)
                new_lines.append(ru_line)
            elif inner: missing.append(inner[:100])
    with open(fpath, "w", encoding="utf-8") as fh: fh.writelines(new_lines)
    print(f"{fname}: {len(new_lines)} lines, {len(missing)} missing")
    for m in missing: print(f"  MISSING: {m}")
