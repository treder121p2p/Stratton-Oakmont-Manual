#!/usr/bin/env python3
"""Добавляет lang-ru в section1 — оставшиеся 9 элементов"""
import re, os

FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "section1_self_improvement.html")

with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

# Ищем lang-de без lang-ru и добавляем переводы
# Используем ключевые фрагменты для поиска
PAIRS = [
    ("Strengthen Selbstdisziplin:</strong> Erfolg ist in der Entwicklung starrer Charakter",
     "Укрепляйте самодисциплину:</strong> Успех коренится в развитии сильного характера — дисциплины тела и разума, а также управления деньгами и временем."),
    ("Jede Aussage, die dir nicht logisch erscheint",
     "Любое утверждение, которое по какой-то причине кажется вам нелогичным, следует изучить подробнее, прежде чем просто принять или отвергнуть."),
    ("Inspirere Teamarbeit.</strong> Du kannst ein Team",
     "Вдохновляйте командную работу.</strong> Вы можете создать команду, пробудив в других энтузиазм работать над вашей целью."),
    ("Lerne aus Schwierigkeiten-und lerne aus Niederlagen.</strong> Niemand gewinnt",
     "Учитесь на трудностях — и учитесь на поражениях.</strong> Никто не побеждает всё время. Но тот, кто в итоге добьётся успеха — это тот, кто использует поражение как возможность пересмотреть план."),
    ("Fürchtet euch nicht vor Niederlagen.</strong> Alles Neue beinhaltet",
     "Не бойтесь поражений.</strong> Всё новое сопряжено с риском провала. Но как бы выглядела ваша жизнь, если бы страх перед неудачей взял полный контроль над вашими действиями?"),
]

lines = content.split('\n')
new_lines = []
added = 0

for i, line in enumerate(lines):
    new_lines.append(line)
    if 'class="lang-de"' not in line:
        continue
    # Проверяем接下来 3 строки
    has_ru = False
    for j in range(i+1, min(i+4, len(lines))):
        if 'class="lang-ru"' in lines[j]:
            has_ru = True
            break
    if has_ru:
        continue
    
    # Ищем совпадение по ключевому фрагменту
    for search, replacement in PAIRS:
        if search in line:
            ru_line = line.replace('class="lang-de"', 'class="lang-ru"')
            # Заменяем немецкий текст на русский
            ru_line = re.sub(r'>[^<]*</', f'>{replacement}</', ru_line, count=1)
            new_lines.append(ru_line)
            added += 1
            break

with open(FILE, 'w', encoding='utf-8') as f:
    f.write('\n'.join(new_lines))

en_count = content.count('class="lang-en"')
ru_count = content.count('class="lang-ru"') + added
print(f"section1: added {added} lang-ru, total en={en_count} ru={ru_count}")
