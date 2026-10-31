#!/usr/bin/env python3
"""Добавляет lang-ru переводы в section1_self_improvement.html"""
import re, os

FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "section1_self_improvement.html")

TRANS = {
    "Stratton Oakmont Schulungshandbuch für Vertrieb": "Stratton Oakmont. Руководство по продажам",
    "Selbstverbesserung": "Самосовершенствование",
    "Napoleon Hills Prinzipien": "Принципы Наполеона Хилла",
    "Persönliche Erfahrung": "Личный опыт",
    "Carnegies Herausforderung annehmen": "Встречая вызов Карнеги",
    "Hills Prinzipien des Erfolgs": "Принципы успеха Хилла",
    "Carl Mays Strategie zum Gewinnen": "Стратегия побед Карла Мэя",
    "Entwickle Zielstrebigkeit.": "Развивайте целеустремлённость.",
    "Gründe eine \"Mastermind-Allianz\"": "Создайте «майндмайнд-альянс»",
    "Entwickle eine positive mental attitude.": "Развивайте позитивное мышление.",
    "Stärke Selbstdisziplin:": "Укрепляйте самодисциплину:",
    "Denke genau.": "Думайте точно.",
    "Inspiriere Teamarbeit.": "Вдохновляйте командную работу.",
    "Lerne aus Schwierigkeiten—und lerne aus Niederlagen.": "Учитесь на трудностях — и учитесь на поражениях.",
    "Akzeptiere dich und deinen Wert.": "Прими себя и свою ценность.",
    "Entwickle und halte eine positive Einstellung.": "Развивайте и поддерживайте позитивное отношение.",
    "Sei kreativ.": "Будьте креативны.",
    "Furchtet euch nicht vor Niederlagen.": "Не бойтесь поражений.",
    "Lebe nach positiven Werten.": "Живите по позитивным ценностям.",
    "Setze Ziele.": "Ставьте цели.",
    "Visualisiere deinen Weg zum Erfolg.": "Визуализируйте свой путь к успеху.",
    "Arbeite hart an der Zusammenarbeit mit anderen.": "Усердно работайте над сотрудничеством с другими.",
    "Tu es jetzt.": "Сделайте это сейчас.",
    "NUR FÜR SCHULUNGSZWECKE": "ТОЛЬКО ДЛЯ ЦЕЛЕЙ ОБУЧЕНИЯ",
    "Stratton Oakmont, Inc. &copy; 1995": "Stratton Oakmont, Inc. &copy; 1995",
    "← Zurück zur Startseite": "← Назад на главную",
    "Weiter: Verkaufskraft →": "Далее: Сила продаж →",
    "Download Original PDF": "Скачать оригинальный PDF",
}

with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Кнопка RU
if 'data-lang="ru"' not in content:
    content = content.replace(
        "onclick=\"switchLanguage('de')\">DE</button>",
        "onclick=\"switchLanguage('de')\">DE</button>\n        <button class=\"language-btn\" data-lang=\"ru\" onclick=\"switchLanguage('ru')\">RU</button>"
    )

# 2. lang-ru
lines = content.split('\n')
new_lines = []
added = 0

for i, line in enumerate(lines):
    new_lines.append(line)
    if 'class="lang-de"' not in line:
        continue
    has_ru = False
    for j in range(i+1, min(i+4, len(lines))):
        if 'class="lang-ru"' in lines[j]:
            has_ru = True
            break
    if has_ru:
        continue
    
    text_match = re.search(r'>(.*?)</', line)
    if not text_match:
        continue
    de_text = text_match.group(1)
    
    ru_text = None
    for key, val in TRANS.items():
        if key == de_text or key in de_text or de_text in key:
            ru_text = val
            break
    
    if ru_text:
        ru_line = line.replace('class="lang-de"', 'class="lang-ru"')
        ru_line = re.sub(r'>(.*?)<', f'>{ru_text}<', ru_line, count=1)
        new_lines.append(ru_line)
        added += 1

with open(FILE, 'w', encoding='utf-8') as f:
    f.write('\n'.join(new_lines))

en_count = content.count('class="lang-en"')
ru_count = content.count('class="lang-ru"') + added
print(f"section1: added {added} lang-ru, total en={en_count} ru={ru_count}")
