#!/usr/bin/env python3
"""Добавляет lang-ru переводы в section8_phone_skills.html"""
import re, os

FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "section8_phone_skills.html")

TRANS = {
    "Stratton Oakmont Schulungshandbuch für Vertrieb": "Stratton Oakmont. Руководство по продажам",
    "Telefonkompetenzen": "Навыки телефонных продаж",
    "← Zurück zu Motivation und Denkweise": "← Назад к мотивации и мышлению",
    "Weiter: Ressourcen →": "Далее: Ресурсы →",
    "Voice Training": "Тренировка голоса",
    "Developing Your Telephone Persona": "Развитие вашего телефонального образа",
    "Your voice is your most powerful tool when selling over the phone. Unlike face-to-face sales, clients cannot see your expressions or body language - they can only hear you. How you sound directly impacts your success rate.": "Голос — ваш самый мощный инструмент при телефонных продажах. В отличие от очных продаж, клиенты не видят ваших эмоций и языка тела — они только слышат вас. Звучание вашего голоса напрямую влияет на ваш успех.",
    "Voice Exercises": "Упражнения для голоса",
    "Daily Voice Warm-up Routine": "Ежедневная разминка голоса",
    "Take 5 deep breaths, filling your diaphragm completely.": "Сделайте 5 глубоких вдохов, полностью наполняя диафрагму.",
    "Hum at different pitches for 30 seconds.": "Мурлыкайте на разных тонах в течение 30 секунд.",
    'Practice articulation with "My money makes money" repeated 10 times with increasing speed.': 'Практикуйте артикуляцию: «Мои деньги делают деньги» — повторите 10 раз, постепенно ускоряясь.',
    "Read a paragraph from the Wall Street Journal aloud, focusing on clarity and appropriate pacing.": "Прочитайте вслух абзац из Wall Street Journal, сосредоточившись на чёткости и правильном темпе.",
    "Practice your opening pitch in three different tones: enthusiastic, authoritative, and conversational.": "Попрактикуйте вашу начальную речь в трёх тонах: воодушевляющем, авторитетном и разговорном.",
    "Phone Rules": "Правила телефонных звонков",
    "Essential Guidelines for Phone Success": "Основные принципы успешных телефонных разговоров",
    "Phone Sales Tips": "Советы по телефонным продажам",
    "12 Common Phone Errors to Avoid": "12 распространённых ошибок при телефонных звонках",
    "NUR FÜR SCHULUNGSZWECKE": "ТОЛЬКО ДЛЯ ЦЕЛЕЙ ОБУЧЕНИЯ",
    "Stratton Oakmont, Inc. &copy; 1995": "Stratton Oakmont, Inc. &copy; 1995",
}

with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Добавить кнопку RU
if 'data-lang="ru"' not in content:
    content = content.replace(
        "onclick=\"switchLanguage('de')\">DE</button>",
        "onclick=\"switchLanguage('de')\">DE</button>\n        <button class=\"language-btn\" data-lang=\"ru\" onclick=\"switchLanguage('ru')\">RU</button>"
    )

# 2. Добавить lang-ru
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
print(f"section8: added {added} lang-ru, total en={en_count} ru={ru_count}")
