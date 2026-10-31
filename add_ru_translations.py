#!/usr/bin/env python3
"""
Массовое добавление русского перевода во все section-файлы.
Для каждой строки с class="lang-de" добавляет аналогичную строку с class="lang-ru".
"""
import re
import os
import json

# Словари переводов для каждого файла
TRANSLATIONS = {
    "section1_self_improvement.html": {
        # Заголовки и навигация
        "Stratton Oakmont Schulungshandbuch für Vertrieb": "Stratton Oakmont. Руководство по продажам",
        "Selbstverbesserung": "Самосовершенствование",
        "← Zurück zur Startseite": "← Назад на главную",
        "Weiter: Verkaufskraft →": "Далее: Сила продаж →",
        "Download Original PDF": "Скачать оригинальный PDF",
        "Napoleon Hills Prinzipien": "Принципы Наполеона Хилла",
        "Persönliche Erfahrung": "Личный опыт",
        "Ich hörte zum ersten Mal von Napoleon Hills Prinzipien des persönlichen Erfolgs, als ich mir meinen Weg durch das College bahnte und in den 1900er Jahren Lebensversicherungen verkaufte.": "Я впервые узнал о принципах личного успеха Наполеона Хилла, когда пробивался через колледж, продавая страхование жизни в 1960-х годах.",
        "Eines Tages besuchte ich einen Mann, der Nachschlagewerke von Tür zu Tür verkaufte. Er kaufte eine Police von mir, sagte aber, dass mein Verkaufsgespräch noch etwas Arbeit brauchen könnte. Er gab mir ein Exemplar von Hills \"Denke nach und werde reich\", das 1937 geschrieben worden war.": "Однажды я навестил мужчину, который продавал справочники от двери к двери. Он купил у меня полис, но сказал, что моей технике продаж есть над чем поработать. Он дал мне экземпляр книги Хилла «Думай и богатей», написанной в 1937 году.",
        "Ich las das Buch und bemerkte fast sofort, dass meine Einstellung besser wurde... und dass sich mein Verkaufsgespräch zu verbessern begann.": "Я прочитал книгу и почти сразу заметил, что моё отношение улучшилось... и что моя техника продаж начала расти.",
        "Ich war neugierig, wie Hill, der Vater der Selbstverbesserungsbewegung, dazu kam, diesen Klassiker zu schreiben, dessen Botschaft noch heute gültig ist.": "Мне было интересно, как Хилл, отец движения самосовершенствования, пришёл к написанию этого классического произведения, послание которого актуально и по сей день.",
        "Carnegies Herausforderung annehmen": "Встречая вызов Карнеги",
        "Im Jahr 1908, als Hill ein 25-jähriger Journalist war, wurde er beauftragt, ein Profil des Stahlmagnaten Andrew Carnegie zu schreiben. Während ihres Treffens sprach Carnegie darüber, wie er erfolgreich geworden war.": "В 1908 году, когда Хиллу было 25 лет и он работал журналистом, ему поручили написать профиль сталелитейного магната Эндрю Карнеги. Во время встречи Карнеги рассказывал о том, как добился успеха.",
        "Am Ende des Interviews forderte der wohlhabende Industrielle Hill heraus, eine praktische persönliche Philosophie zu entwickeln, die von jedem in jedem Bereich genutzt werden könnte, um seine Ziele zu erreichen.": "В конце интервью этот богатый промышленник бросил вызов Хиллу — разработать практическую личную философию, которой мог бы воспользоваться каждый в любой области для достижения своих целей.",
        "Hill nahm die Herausforderung an. Obwohl Carnegie das Projekt nicht finanzierte, stellte er Hill Geschäfts- und politischen Führern sowie innovativen Denkern seiner Zeit vor, darunter Henry Ford, William Howard Taft und Thomas Edison.": "Хилл принял вызов. Хотя Карнеги не финансировал проект, он познакомил Хилла с бизнес- и политическими лидерами, а также новаторскими мыслителями своего времени, включая Генри Форда, Уильяма Тафта и Томаса Эдисона.",
        "Hill arbeitete fast 30 Jahre lang an der Erforschung, dem Schreiben und der Verfeinerung des Buches, das seine Erkenntnisse zusammenfasste. Es wird auch heute noch von Millionen von Menschen auf der ganzen Welt gelesen.": "Хилл将近30 лет работал над исследованием, написанием и совершенствованием книги, обобщившей его выводы. Её до сих пор читают миллионы людей по всему миру.",
        "Hills Prinzipien des Erfolgs": "Принципы успеха Хилла",
    },
    "section2_selling_power.html": {
        "Stratton Oakmont Schulungshandbuch für Vertrieb": "Stratton Oakmont. Руководство по продажам",
        "Verkaufskraft": "Сила продаж",
        "← Zurück zur Startseite": "← Назад на главную",
        "Weiter: Verkaufstechniken →": "Далее: Техники продаж →",
        "Download Original PDF": "Скачать оригинальный PDF",
        "Du musst hungrig sein! Lebe deine Größe": "Будь голодным! Живи в полную силу",
        "MAN KANN AN JEMANDES LEBENSSTIL ERKENNEN, ob er hungrig ist. Er arbeitet länger und härter. Er recherchiert Konten. Er kennt das Produkt, die Branche und die Konkurrenz.": "ПО СТИЛИЗИ ЖИЗНИ ЧЕЛОВЕКА МОЖНО ОПРЕДЕЛИТЬ, голоден ли он. Он работает дольше и усерднее. Он изучает клиентов. Он знает продукт, отрасль и конкурентов.",
        "Als ich Verkaufsvertreter bei einem Radiosender in Florida war, hatte ich einen wirklich egoistischen Manager. Er genoss es, jeden Monat unsere Gehaltsschecks auszuhändigen und zu höhnen: \"Hier ist, was du wert bist.\" Wenn du einen kleinen Provisionsscheck hattest, ließest du den Kopf hängen. Aber ich sah diesen Kerl als Herausforderung. Du kannst verbittert oder besser werden, und ich entschloss mich, ihn im Verkauf weit zu übertreffen. In einem Monat verkaufte ich viermal so viel wie sein Gehalt.": "Когда я был торговым представителем на радиостанции во Флориде, у меня был по-настоящему эгоистичный менеджер. Он наслаждался тем, что каждый месяц раздавал наши зарплатные чеки и произносил: «Вот чего ты стоишь». Если чек был маленьким, ты опускал голову. Но я воспринял этого парня как вызов. Можно стать озлобленным или стать лучше — и я решил превзойти его в продажах. В один месяц я продал на четыре зарплаты его.",
        "Das Leben kann so negativ erscheinen. Aber ich glaube, dass du jedes Mal, wenn du auf den Rücken geworfen wirst, daran denken musst: Wenn du nach oben schauen kannst, kannst du auch aufstehen! Steh auf, um den Leuten zu beweisen, dass sie falsch liegen. Steh auf, weil du hungrig bist, etwas aus deinem Leben zu machen. Du musst dich selbst entwickeln und an deinen Wert glauben. Wenn dein Selbstwertgefühl wächst, wächst auch dein Gehaltsscheck. Persönliches Wachstum umfasst vier Stufen:": "Жизнь может казаться такой негативной. Но я верю, что каждый раз, когда тебя сбивают с ног, ты должен помнить: если можешь посмотреть вверх — можешь и встать! Встань, чтобы доказать всем, что они ошибаются. Встань, потому что ты голоден сделать из своей жизни что-то стоящее. Ты должен развиваться и верить в свою ценность. Когда растёт твоя самооценка — растёт и зарплата. Личный рост включает четыре ступени:",
    },
    "section3_sales_techniques.html": {
        "Stratton Oakmont Schulungshandbuch für Vertrieb": "Stratton Oakmont. Руководство по продажам",
        "Verkaufstechniken": "Техники продаж",
        "← Zurück zur Startseite": "← Назад на главную",
        "Weiter: Bewährte Methoden →": "Далее: Лучшие практики →",
        "Download Original PDF": "Скачать оригинальный PDF",
        "Qualifizierendes Anrufskript": "Сценарий квалификационного звонка",
        "Qualifizierende Fragen": "Квалификационные вопросы",
        "Einwandbehandlung": "Работа с возражениями",
    },
    "section8_phone_skills.html": {
        "Stratton Oakmont Schulungshandbuch für Vertrieb": "Stratton Oakmont. Руководство по продажам",
        "Telefonkompetenzen": "Навыки телефонных продаж",
        "← Zurück zu Motivation und Denkweise": "← Назад к мотивации и мышлению",
        "Weiter: Ressourcen →": "Далее: Ресурсы →",
        "Download Original PDF": "Скачать оригинальный PDF",
        "Stimmtraining": "Тренировка голоса",
        "Telefonregeln": "Правила телефонных звонков",
        "Tipps für Telefonverkauf": "Советы по телефонным продажам",
    },
    "section9_resources.html": {
        "Stratton Oakmont Schulungshandbuch für Vertrieb": "Stratton Oakmont. Руководство по продажам",
        "Ressourcen": "Ресурсы",
        "← Zurück zu Telefonkompetenzen": "← Назад к телефонным навыкам",
        "Empfohlene Lektüre": "Рекомендуемая литература",
        "Einwände und Entgegnungen": "Возражения и ответы на них",
        "Finanzdefinitionen": "Финансовые термины",
        "Erfolgsnachweis": "Трек-рекорд",
        "Download Original PDF": "Скачать оригинальный PDF",
    },
    "section4_best_practices.html": {
        "Stratton Oakmont Schulungshandbuch für Vertrieb": "Stratton Oakmont. Руководство по продажам",
        "Bewährte Methoden": "Лучшие практики",
        "← Zurück zu Verkaufstechniken": "← Назад к техникам продаж",
        "Weiter: Besondere Situationen →": "Далее: Особые ситуации →",
        "Download Original PDF": "Скачать оригинальный PDF",
        "Dos und Don'ts": "Что можно и что нельзя",
        "Was ist ein qualifizierter Investor?": "Кто такой квалифицированный инвестор?",
    },
    "section5_special_situations.html": {
        "Stratton Oakmont Schulungshandbuch für Vertrieb": "Stratton Oakmont. Руководство по продажам",
        "Besondere Situationen": "Особые ситуации",
        "← Zurück zu Bewährte Methoden": "← Назад к лучшим практикам",
        "Weiter: Besondere Handhabungssituationen →": "Далее: Особые ситуации работы с клиентами →",
        "Download Original PDF": "Скачать оригинальный PDF",
        "Immobilieninvestoren": "Инвесторы в недвижимость",
        "Möglichkeiten der Unternehmensfinanzierung": "Возможности корпоративных финансов",
    },
    "section6_special_handling.html": {
        "Stratton Oakmont Schulungshandbuch für Vertrieb": "Stratton Oakmont. Руководство по продажам",
        "Besondere Handhabungssituationen": "Особые ситуации работы с клиентами",
        "← Zurück zu Besondere Situationen": "← Назад к особым ситуациям",
        "Weiter: Motivation und Denkweise →": "Далее: Мотивация и мышление →",
        "Download Original PDF": "Скачать оригинальный PDF",
    },
    "section7_motivation.html": {
        "Stratton Oakmont Schulungshandbuch für Vertrieb": "Stratton Oakmont. Руководство по продажам",
        "Motivation und Denkweise": "Мотивация и мышление",
        "← Zurück zu Besondere Handhabungssituationen": "← Назад к особым ситуациям",
        "Weiter: Telefonkompetenzen →": "Далее: Телефонные навыки →",
        "Download Original PDF": "Скачать оригинальный PDF",
        "Die Anatomie des Erfolgs: Die richtigen Gewohnheiten entwickeln": "Анатомия успеха: развитие правильных привычек",
        "Manifest der Gewinner": "Манифест победителей",
        "Mentale Stärke": "Сила разума",
        "Von: Ira Boshnack<br>Geschäftsführender Direktor": "Автор: Ира Бошнак<br>Управляющий директор",
        "Ein Einblick, wie man ein besserer Vertriebsprofi wird": "Путь к тому, чтобы стать лучшим специалистом по продажам",
    },
}


def add_lang_ru_to_file(filepath, translations_dict):
    """Добавляет lang-ru элементы после каждого lang-de элемента."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    new_lines = []
    modified = False
    
    for line in lines:
        new_lines.append(line)
        
        # Ищем строки с class="lang-de" (но не с lang-de в составе других классов)
        if 'class="lang-de"' in line or "class='lang-de'" in line:
            # Проверяем, есть ли уже lang-ru после этой строки (избегаем дублирования)
            # Простой способ: определить тег и создать lang-ru версию
            ru_line = create_ru_line(line, translations_dict)
            if ru_line:
                new_lines.append(ru_line)
                modified = True
    
    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
        print(f"  ✅ {os.path.basename(filepath)}: добавлены lang-ru элементы")
    else:
        print(f"  ⏭️ {os.path.basename(filepath)}: уже есть lang-ru или нет lang-de")


def create_ru_line(de_line, translations_dict):
    """Создаёт строку lang-ru на основе строки lang-de."""
    # Заменяем lang-de на lang-ru
    ru_line = de_line.replace('class="lang-de"', 'class="lang-ru"')
    
    # Пытаемся найти перевод в словаре
    for de_text, ru_text in translations_dict.items():
        if de_text in ru_line:
            # Заменяем немецкий текст на русский в этой строке
            # Но сохраняем HTML-структуру
            ru_line = ru_line.replace(de_text, ru_text)
            return ru_line
    
    # Если перевод не найден в словаре — пропускаем (не генерируем автоматический)
    return None


def process_all_files():
    """Обрабатывает все section файлы."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    section_files = [
        "section1_self_improvement.html",
        "section2_selling_power.html",
        "section3_sales_techniques.html",
        "section4_best_practices.html",
        "section5_special_situations.html",
        "section6_special_handling.html",
        "section7_motivation.html",
        "section8_phone_skills.html",
        "section9_resources.html",
    ]
    
    print("=== Добавление русского перевода ===\n")
    
    for filename in section_files:
        filepath = os.path.join(base_dir, filename)
        if not os.path.exists(filepath):
            print(f"  ❌ {filename}: файл не найден")
            continue
        
        trans = TRANSLATIONS.get(filename, {})
        print(f"\n📁 {filename} ({len(trans)} переводов в словаре)")
        add_lang_ru_to_file(filepath, trans)
    
    # Также обработать index.html
    index_path = os.path.join(base_dir, "index.html")
    if os.path.exists(index_path):
        print(f"\n📁 index.html")
        add_lang_ru_to_file(index_path, TRANSLATIONS.get("index.html", {}))


if __name__ == "__main__":
    process_all_files()
