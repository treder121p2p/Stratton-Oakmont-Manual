#!/usr/bin/env python3
"""Перевод section9_resources.html — все lang-de → lang-ru"""
import re, os

FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "section9_resources.html")

# Полный словарь DE→RU для section9
TRANS = {
    "Stratton Oakmont Schulungshandbuch für Vertrieb": "Stratton Oakmont. Руководство по продажам",
    "Ressourcen": "Ресурсы",
    "← Zurück zu Telefonkompetenzen": "← Назад к телефонным навыкам",
    "Zurück zur Startseite": "Назад на главную",
    "Empfohlene Lektüre": "Рекомендуемая литература",
    "Wesentliche Bücher für Vertriebsexzellenz": "Ключевые книги для мастерства в продажах",
    "Der grundlegende Text über Erfolgspsychologie und Vermögensbildung. Besondere Aufmerksamkeit sollte den Kapiteln über Verlangen, Glaube und Ausdauer gewidmet werden.": "Фундаментальный труд по психологии успеха и созданию богатства. Особое внимание следует уделить главам о желании, вере и настойчивости.",
    "Umfassender Leitfaden zu Verkaufstechniken mit besonderer Relevanz für unseren Kaltakquise-Ansatz und Methoden zur Einwandbehandlung.": "Комплексное руководство по техникам продаж, особенно актуальное для нашего подхода к холодным звонкам и методам работы с возражениями.",
    "Das Verständnis der sechs Prinzipien der Beeinflussung wird Ihre Fähigkeit, Interessenten zu überzeugen, dramatisch verbessern.": "Понимание шести принципов влияния драматически повысит вашу способность убеждать потенциальных клиентов.",
    "Wesentlicher Grundkurs zu Finanzmärkten und -instrumenten, den jeder Broker beherrschen sollte.": "Основы финансовых рынков и инструментов, которые должен знать каждый брокер.",
    "Klassischer Text über Marktpsychologie und wie Emotionen finanzielle Entscheidungen beeinflussen.": "Классический труд о рыночной психологии и о том, как эмоции влияют на финансовые решения.",
    "Einfache, zugängliche Finanzplanungsanleitung, die Ihnen hilft, die Denkweise von Privatanlegern zu verstehen.": "Простое и доступное руководство по финансовому планированию, помогающее понять мышление частных инвесторов.",
    "Interviews mit Top-Händlern, die wertvolle Einblicke в Marktpsychologie und Handelsstrategien liefern.": "Интервью с лучшими трейдерами, дающие ценные представления о рыночной психологии и торговых стратегиях.",
    "Praktische Techniken zur Steigerung Ihrer Effektivität in Verkaufsinteraktionen.": "Практические техники повышения эффективности в продажах.",
    "Tägliche Leseanforderungen": "Ежедневные требования к чтению",
    "Alle Broker sind verpflichtet zu lesen:": "Все брокеры обязаны читать:",
    "The Wall Street Journal (täglich)": "The Wall Street Journal (ежедневно)",
    "Investor's Business Daily (wöchentlich)": "Investor's Business Daily (еженедельно)",
    "Stratton Oakmont Forschungsberichte (wie verteilt)": "Исследовательские отчёты Stratton Oakmont (по распределению)",
    "Mindestens ein Buch aus der empfohlenen Leseliste pro Monat": "Минимум одна книга из рекомендованного списка в месяц",
    "Einwände und Erwiderungen": "Возражения и ответы на них",
    "Bibliothek häufiger Einwände": "Библиотека типичных возражений",
    "Einwand": "Возражение",
    "Hauptanliegen": "Основная причина",
    "Effektive Erwiderung": "Эффективный ответ",
    '"Ich muss darüber nachdenken."': '«Мне нужно обдумать.»',
    "Unsicherheit, Angst vor einer falschen Entscheidung": "Неуверенность, страх ошибиться",
    '"Ich muss mit meinem Ehepartner/Finanzberater sprechen."': '«Мне нужно поговорить с мужем/женой или финансовым консультантом.»',
    "Verantwortung verteilen, Bestätigung suchen": "Разделить ответственность, получить подтверждение",
    '"Der Zeitpunkt ist nicht richtig."': '«Не тот момент.»',
    "Marktunsicherheit, persönliche finanzielle Situation": "Неопределённость рынка, личная финансовая ситуация",
    '"Ich kenne Sie oder Ihre Firma nicht."': '«Я вас или вашу компанию не знаю.»',
    "Vertrauen und Glaubwürdigkeit": "Доверие и авторитет",
    '"Ich habe schon früher Geld in Aktien verloren."': '«Я уже терял деньги на акциях.»',
    "Vergangene negative Erfahrungen, Risikoaversion": "Прошлый негативный опыт, неприятие рисков",
    '"Ich habe im Moment kein Geld zum Investieren."': '«У меня сейчас нет денег для инвестиций.»',
    "Liquiditätsbedenken, Budgetprioritäten": "Проблемы ликвидности, приоритеты бюджета",
    '"Ihre Gebühren sind zu hoch."': '«Ваши комиссии слишком высоки.»',
    "Wertwahrnehmung, Kostenempfindlichkeit": "Восприятие стоимости, чувствительность к затратам",
    '"Ich bin mit meinem aktuellen Broker zufrieden."': '«Я доволен своим текущим брокером.»',
    "Loyalität, Komfort mit dem Status quo": "Лояльность,comfort с текущим положением",
    "Die Fühlen-Fühlten-Fanden Technik": "Техника «Чувствовал — чувствовали — обнаружили»",
    "Beim Umgang mit Einwänden verwenden Sie diesen dreistufigen Prozess:": "При работе с возражениями используйте этот трёхэтапный процесс:",
    "Finanzielle Definitionen": "Финансовые термины",
    "Wesentliche Terminologie": "Основные понятия",
    "Broker müssen in der Lage sein, diese Konzepte den Kunden klar zu erklären:": "Брокеры должны уметь ясно объяснять эти концепции клиентам:",
    "Börsengang (IPO)": "ИПО (Initial Public Offering)",
    "Market Maker": "Маркетмейкер",
    "Blue-Chip-Aktie": "Акция «голубых фишек»",
    "KGV (Kurs-Gewinn-Verhältnis)": "P/E (цена/прибыль)",
    "Wachstumsaktie": "Акция роста",
    "Marktkapitalisierung": "Рыночная капитализация",
    "Volatilität": "Волатильность",
    "Margin": "Маржа",
    "Liquidität": "Ликвидность",
    "Prospekt": "Проспект",
    "Diversifikation": "Диверсификация",
    "Bärenmarkt": "Медвежий рынок",
    "Bullenmarkt": "Бычий рынок",
    "Rendite": "Доходность",
    "SEC": "SEC (Комиссия по ценным бумагам)",
    "Erfolgsbilanz": "Трек-рекорд",
    "Stratton Oakmont IPO-Leistungstabellen": "Таблицы результатов IPO Stratton Oakmont",
    "Verwenden Sie diese Zahlen, wenn Sie unsere Erfolgsbilanz mit potenziellen Kunden besprechen:": "Используйте эти цифры при обсуждении нашего трек-рекорда с потенциальными клиентами:",
    "Unternehmen": "Компания",
    "Angebotspreis": "Цена предложения",
    "Schlusskurs 1. Tag": "Закрытие 1-го дня",
    "30-Tage-Kurs": "Цена через 30 дней",
    "90-Tage-Kurs": "Цена через 90 дней",
    "% Gewinn (90 Tage)": "% прибыли (90 дней)",
    "Stratton Oakmont Jahresverlauf Performance": "Динамика Stratton Oakmont за год",
    "Portfolio-Typ": "Тип портфеля",
    "YTD-Rendite": "Доходность с начала года",
    "1-Jahres-Rendite": "Годовая доходность",
    "3-Jahres-Rendite": "3-летняя доходность",
    "Branchendurchschnitt": "Среднеотраслевой показатель",
    "Wichtig:": "Важно:",
    "NUR FÜR SCHULUNGSZWECKE": "ТОЛЬКО ДЛЯ ЦЕЛЕЙ ОБУЧЕНИЯ",
    "Stratton Oakmont, Inc. &copy; 1995": "Stratton Oakmont, Inc. &copy; 1995",
    "← Zurück zu Telefonkompetenzen": "← Назад к телефонным навыкам",
}

# Длинные абзацы — переводы
LONG_TRANS = {
    "Ich verstehe das vollkommen, Herr Jones. Die meisten meiner erfolgreichen Kunden hatten zunächst das Gefühl, dass sie Zeit zum Nachdenken brauchten. Aber sie stellten fest, dass sich die Marktbedingungen so schnell änderten, dass selbst eine Verzögerung von einem Tag sie erhebliche Gewinnchancen kostete. Bei welchem spezifischen Aspekt dieser Gelegenheit sind Sie unsicher? Lassen Sie mich dieses Anliegen gleich ansprechen.": "Полностью понимаю, мистер Джонс. Большинство моих успешных клиентов поначалу хотели время на обдумывание. Но они обнаружили, что рыночные условия менялись так быстро, что даже один день задержки лишал их значительного потенциала роста. Какой конкретный аспект этой возможности вызывает у вас неуверенность? Позвольте мне прямо сейчас обратиться к этой проблеме.",
    "Das ist ein kluger Schritt, Herr Smith. Ich respektiere, dass Sie sich mit anderen beraten. Die Herausforderung besteht darin, dass diese besondere Gelegenheit möglicherweise bereits voll gezeichnet ist, bis Sie mit ihnen in Kontakt treten. Lassen Sie mich Sie fragen - wenn Ihr Berater jetzt hier wäre, welche spezifischen Fragen würde er zu dieser Investition stellen?": "Мудрый подход, мистер Смит. Я уважаю, что вы советуетесь с другими. Но проблема в том, что эта конкретная возможность может быть полностью закрыта, пока вы свяжетесь с ними. Позвольте спросить: если бы ваш консультант был здесь прямо сейчас, какие вопросы он задал бы об этой инвестиции?",
    "Ich verstehe Ihre Bedenken bezüglich des Timings, Frau Johnson. Viele Anleger warten auf den 'perfekten' Moment, aber die Marktgeschichte zeigt, dass das Timing weniger wichtig ist als die Zeit im Markt. Selbst wenn Sie zum schlechtestmöglichen Zeitpunkt vor jeder größeren Marktkorrektur in den letzten 50 Jahren mit dem Investieren begonnen hätten, wären Sie heute immer noch deutlich im Vorteil. Wann würden Sie das Timing als richtig betrachten?": "Понимаю вашу озабоченность временем, миссис Джонсон. Многие инвесторы ждут «идеального момента», но история рынка показывает, что тайминг менее важен, чем время на рынке. Даже если бы вы начали инвестировать в самый неподходящий момент перед каждым крупным рыночным корректировкой за последние 50 лет, вы всё равно были бы значительно в плюсе. Когда вы считаете момент подходящим?",
    "Berechtigter Einwand, Frau Wilson. Ich wäre auch vorsichtig. Deshalb möchte ich Ihnen den Hintergrund unserer Firma, unsere Erfolgsbilanz bei ähnlichen Investitionen zusenden und Sie mit anderen Kunden verbinden, die mit uns zusammengearbeitet haben. Unser Ruf basiert auf Ergebnissen - wie die 42%ige Rendite, die unsere Kunden im letzten Quartal bei unserem Aegis-Börsengang erzielt haben. Welche spezifischen Informationen würden Ihnen helfen, sich bei der Zusammenarbeit mit uns wohlzufühlen?": "Справедливое замечание, миссис Уилсон. Я бы тоже проявил осторожность. Поэтому я хотел бы отправить вам информацию о нашей компании, наш трек-рекорд на аналогичных инвестициях и связать вас с другими клиентами, с которыми мы работали. Наша репутация основана на результатах — таких как 42% доходность, которую наши клиенты получили на нашем IPO Aegis в прошлом квартале. Какая информация помогла бы вам почувствовать комфорт при работе с нами?",
    "Es tut mir leid, von Ihrer vorherigen Erfahrung zu hören. Viele meiner Kunden hatten ähnliche Situationen, bevor sie mit mir zusammenarbeiteten. Der Unterschied ist, dass wir uns auf aufstrebende Wachstumsunternehmen mit starken Fundamentaldaten spezialisieren, nicht auf spekulative Aktien. Und wir bieten laufende Beratung, nicht nur Kaufempfehlungen. Was ist bei Ihren früheren Investitionen schiefgelaufen?": "Мне жаль узнать о вашем прошлом опыте. Многие мои клиенты сталкивались с подобными ситуациями до начала сотрудничества со мной. Разница в том, что мы специализируемся на растущих компаниях с сильными фундаментальными показателями, а не на спекулятивных акциях. И мы предоставляем постоянное сопровождение, а не просто рекомендации по покупке. Что пошло не так с вашими прошлыми инвестициями?",
    "Ich verstehe Cashflow-Überlegungen, Herr Thomas. Viele meiner Kunden dachten zunächst, sie hätten kein verfügbares Kapital. Was wir herausfanden, war, dass sie durch Umstrukturierung einiger bestehender Investitionen, die nicht gut performten, teilnehmen konnten, ohne neues Kapital zu finden. Darf ich fragen, welche Investitionen Sie derzeit halten, die möglicherweise unterdurchschnittlich abschneiden?": "Понимаю соображения о денежном потоке, мистер Томас. Многие мои клиенты сначала думали, что у них нет свободного капитала. Выяснилось, что, реструктурировав некоторые текущие инвестиции, которые показывали низкую доходность, они смогли принять участие, не привлекая нового капитала. Можно спросить, какие инвестиции у вас сейчас, которые могли бы показывать недостаточные результаты?",
    "Ich schätze Ihren Fokus auf Kosten, Frau Garcia. Die teuerste Investition ist tatsächlich eine, die unterdurchschnittlich abschneidet. Unsere Provisionsstruktur ist so konzipiert, dass unsere Interessen mit Ihren übereinstimmen - wir sind nur erfolgreich, wenn Sie es sind. Wenn Sie die Nettorenditen nach allen Gebühren betrachten, übertreffen unsere Kunden typischerweise Standardindizes um 12-18%. Welche Rendite würden Sie angesichts unserer Gebührenstruktur als fair betrachten?": "Ценю ваше внимание к комиссиям, миссис Гарсия. Самая дорогая инвестиция — это та, которая показывает низкую доходность. Наша комиссия построена так, чтобы наши интересы совпадали с вашими — мы зарабатываем только тогда, когда зарабатываете вы. Если рассматривать чистую доходность после всех комиссий, наши клиенты обычно превосходят стандартные индексы на 12-18%. Какую доходность вы считали бы справедливой с учётом нашей комиссии?",
    "Ich respektiere Ihre Loyalität, Herr Brown. Eine gute Broker-Beziehung ist wertvoll. Viele meiner Kunden pflegen Beziehungen zu mehreren Beratern, um ihre Beratung zu diversifizieren, genau wie sie ihre Portfolios diversifizieren. Ich schlage nicht vor, Ihren aktuellen Berater zu ersetzen - nur einen kleinen Teil Ihres Portfolios zuzuweisen, um unseren Ansatz zu testen. Wie ist die Rendite Ihres aktuellen Portfolios seit Jahresbeginn?": "Уважаю вашу лояльность, мистер Браун. Хорошие отношения с брокером ценны. Мои многие клиенты поддерживают отношения с несколькими консультантами для диверсификации рекомендаций — так же, как они диверсифицируют портфели. Я не предлагаю заменить вашего текущего консультанта — лишь направить небольшую часть портфеля для тестирования нашего подхода. Какая доходность вашего текущего портфеля с начала года?",
    "Erinnern Sie Kunden immer daran, dass vergangene Wertentwicklungen kein Indikator für zukünftige Ergebnisse sind. Betonen Sie jedoch unsere konsistente Erfolgsbilanz, die Branchendurchschnitte in allen Portfoliotypen übertrifft.": "Всегда напоминайте клиентам, что прошлые результаты не гарантируют будущих. Однако подчёркивайте нашу стабильную историю превышения среднеотраслевых показателей по всем типам портфелей.",
    "Beim Umgang mit Einwänden verwenden Sie diesen dreistufigen Prozess:": "При работе с возражениями используйте этот трёхэтапный процесс:",
    "Broker müssen in der Lage sein, diese Konzepte den Kunden klar zu erklären:": "Брокеры должны уметь ясно объяснять эти концепции клиентам:",
    "Verwenden Sie diese Zahlen, wenn Sie unsere Erfolgsbilanz mit potenziellen Kunden besprechen:": "Используйте эти цифры при обсуждении нашего трек-рекорда с потенциальными клиентами:",
}

with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Кнопка RU
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
    
    # Ищем перевод
    ru_text = None
    # Сначала в длинных переводах
    for key, val in LONG_TRANS.items():
        if key in line:
            ru_text = val
            break
    # Потом в коротких
    if not ru_text:
        for key, val in TRANS.items():
            if key in line:
                ru_text = val
                break
    
    if ru_text:
        ru_line = line.replace('class="lang-de"', 'class="lang-ru"')
        # Заменяем текст в строке
        # Для простых случаев — заменяем всё между > и <
        if '>' + ru_text + '</' in ru_line:
            pass  # Уже есть
        else:
            # Заменяем немецкий текст на русский
            for de_text in sorted(TRANS.keys(), key=len, reverse=True):
                if de_text in ru_line and de_text != ru_text:
                    ru_line = ru_line.replace(de_text, ru_text)
                    break
            else:
                # Если не нашли точное совпадение — просто заменяем класс
                pass
        new_lines.append(ru_line)
        added += 1

with open(FILE, 'w', encoding='utf-8') as f:
    f.write('\n'.join(new_lines))

en_count = content.count('class="lang-en"')
ru_count = content.count('class="lang-ru"') + added
print(f"section9: added {added} lang-ru, total en={en_count} ru={ru_count}")
