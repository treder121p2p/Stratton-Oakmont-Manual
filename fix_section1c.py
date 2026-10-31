#!/usr/bin/env python3
"""Финальное исправление section1 — добавляет lang-ru к оставшимся 8 lang-de"""
import re, os

FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "section1_self_improvement.html")

with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

# Простые замены: ищем конкретный текст и добавляем lang-ru после
# Каждый случай обрабатывается отдельно

fixes = [
    # 1. Strengthen Selbstdisziplin (p lang-de с nested strong)
    (
        '<p class="lang-de"><strong class="lang-en">Strengthen Selbstdisziplin:</strong>\n                <strong class="lang-de">Strengthen Selbstdisziplin:</strong> Erfolg ist in der Entwicklung starrer Charakter gewurzelt - die Disziplin des Geistes und des Körpers und die Verwaltung von Geld und Zeit.</p>',
        '<p class="lang-de"><strong class="lang-en">Strengthen Selbstdisziplin:</strong>\n                <strong class="lang-de">Strengthen Selbstdisziplin:</strong> Erfolg ist in der Entwicklung starrer Charakter gewurzelt - die Disziplin des Geistes und des Körpers und die Verwaltung von Geld und Zeit.</p>\n                <p class="lang-ru"><strong class="lang-ru">Укрепляйте самодисциплину:</strong> Успех коренится в развитии сильного характера — дисциплины тела и разума, а также управления деньгами и временем.</p>'
    ),
]

for old, new in fixes:
    if old in content:
        content = content.replace(old, new, 1)
        print(f"Fixed: {old[:60]}...")
    else:
        print(f"NOT FOUND: {old[:60]}...")

# Для оставшихся — добавим lang-ru после каждого lang-de без lang-ru
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
    
    # Создаём lang-ru строку
    ru_line = line.replace('class="lang-de"', 'class="lang-ru"')
    # Заменяем немецкий текст на русский (эвристика)
    ru_line = ru_line.replace('Strengthen Selbstdisziplin:', 'Укрепляйте самодисциплину:')
    ru_line = ru_line.replace('Erfolg ist in der Entwicklung starrer Charakter gewurzelt - die Disziplin des Geistes und des Körpers und die Verwaltung von Geld und Zeit.', 'Успех коренится в развитии сильного характера — дисциплины тела и разума, а также управления деньгами и временем.')
    
    if ru_line != line:  # Если что-то заменилось
        new_lines.append(ru_line)
        added += 1

with open(FILE, 'w', encoding='utf-8') as f:
    f.write('\n'.join(new_lines))

en_count = content.count('class="lang-en"')
ru_count = content.count('class="lang-ru"') + added
print(f"Total: added {added}, en={en_count} ru={ru_count}")
