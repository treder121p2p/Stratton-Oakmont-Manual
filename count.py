import re
for f in ['section7_motivation.html','section8_phone_skills.html','section9_resources.html']:
    c = open(f, encoding="utf-8").read().count('class="lang-de"')
    print(f"{f}: {c} lang-de elements")
