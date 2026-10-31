#!/usr/bin/env python3
"""
Process HTML files to add lang-ru translations after each lang-de element.
Strategy: Read file, find lines with lang-de class, translate the text content,
insert a new line with lang-ru class after each.
"""
import re
import sys

def extract_de_text(html_line):
    """Extract the German text content from a lang-de line."""
    # Match text inside the tag (after the last >)
    # Handle both self-closing and regular tags
    m = re.search(r'>([^<]*)<', html_line)
    if m:
        return m.group(1).strip()
    # For lines like <blockquote> or <p> that contain text after >
    m = re.search(r'>(.*)', html_line)
    if m:
        return m.group(1).strip()
    return None

def replace_class(line, old_class, new_class):
    """Replace a class name in an HTML line."""
    return line.replace(f'class="{old_class}"', f'class="{new_class}"')

# Build translation dict by reading the current files and creating a mapping
# We'll process each file separately

def main():
    files = [
        r'C:\Users\crypt\.openclaw\workspace\belfort\section6_special_handling.html',
        r'C:\Users\crypt\.openclaw\workspace\belfort\section8_phone_skills.html', 
        r'C:\Users\crypt\.openclaw\workspace\belfort\section9_resources.html',
    ]
    
    # Translation dictionary built from reading the files
    # This maps German text -> Russian text
    DE_TO_RU = get_translations()
    
    for filepath in files:
        process_file(filepath, DE_TO_RU)

def process_file(filepath, de_to_ru):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        new_lines.append(line)
        
        # Check if this line contains lang-de
        if 'class="lang-de"' in line:
            de_text = extract_de_text(line)
            if de_text and de_text in de_to_ru:
                ru_text = de_to_ru[de_text]
                ru_line = replace_class(line, 'lang-de', 'lang-ru')
                # Replace the German text with Russian
                ru_line = ru_line.replace(de_text, ru_text, 1)
                new_lines.append(ru_line)
            elif de_text:
                # Text not in our dictionary - try to find partial match or skip with warning
                print(f"WARNING: No translation found for: {de_text[:80]}...")
                # Still insert a placeholder so structure is maintained
                ru_line = replace_class(line, 'lang-de', 'lang-ru')
                new_lines.append(ru_line)
        
        i += 1
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print(f"Processed: {filepath}")

def get_translations():
    """Return the German -> Russian translation dictionary."""
    return {
        # === SECTION 6 ===
        "Stratton Oakmont Schulungshandbuch für Vertrieb": "Учебное пособие по продажам Stratton Oakmont",
        "Besondere Handhabungssituationen": "Особые ситуации обращения",
        "← Zurück zu Besondere Situationen": "← Назад к особым ситуациям",
        "Weiter: Motivation und Denkweise →": "Далее: Мотивация и настрой →",
        "Umgang mit Interessentenszenarien": "Работа со сценариями взаимодействия с клиентами",
        "Der Interessent, den Sie anrufen, ist feindselig": "Клиент, которому вы звоните, настроен враждебно",
        "Erstens: Entschuldigen Sie sich für die Unannehmlichkeiten und versprechen Sie, sie von Ihrer Liste zu streichen. Legen Sie höflich auf.": "Во-первых: извинитесь за неудобства и пообещайте убрать его из вашего списка. Вежливо повесьте трубку.",
        "Zweitens: Bewahren Sie die Karte mit einem großen H darauf auf, und jeden Monat werde ich sie sammeln, um sie aus unserer Datei zu löschen.": "Во-вторых: сохраните карточку с большой буквой «H» — я буду забирать их раз в месяц для удаления из базы.",
        "Verbindungsabbrüche": "Обрывы связи",
        "Tun Sie dasselbe wie oben. Bewahren Sie die Karte zur Löschung aus unserer Liste mit einem darüber geschriebenen D auf.": "Действуйте так же, как выше. Сохраните карточку для удаления из списка, написав на ней букву «D».",
        "Wenn ein Interessent sagt, dass er mit seinem Broker zufrieden ist": "Когда клиент говорит, что доволен своим брокером",
        "Wenn er andeutet, dass er am Markt ist und auflegt -- BEWAHREN SIE DEN LEAD AUF! Heute ist vielleicht nicht Ihr Tag, aber Sie werden andere haben. Schreiben Sie auf die Karte (O/B), was ANDERER BROKER bedeutet, und halten Sie daran fest!": "Если он намекает, что у него есть брокер и кладёт трубку — СОХРАНЯЕТЕ ЛИД! Сегодня может не быть вашим днём, но будут другие. Напишите на карточке (O/B) — «ДРУГОЙ БРОКЕР» — и сохраните её!",
        "Qualifizierung für Geld": "Квалификация по сумме инвестиций",
        "Erfahrene Börsenmakler werden Ihnen sagen, dass es praktisch keinen Unterschied in dem Aufwand gibt, der für den Abschluss eines Kontos für 5.000 $ oder 50.000 $ aufgewendet wird, und der Kunde wird eine bessere Chance haben, erfolgreich zu sein.": "Опытные брокеры скажут вам, что практически нет разницы в усилиях для открытия счёта на 5 000 или 50 000 долларов, а клиент получит гораздо больше шансов на успех.",
        'Leider gehen viele Broker, wenn es um die Qualifizierung für Geld geht, falsch vor. Die übliche Qualifikation der meisten Amateurmakler ist: "Wie viel Risikokapital haben Sie für Spekulationen". Wenn danach gefragt wird, werden die meisten Interessenten fragen: "Was ist das Minimum" oder Ihnen eine Zahl nennen, die viel niedriger ist, als sie investieren könnten.': 'К сожалению, многие брокеры неправильно подходят к вопросу квалификации по сумме. Типичный вопрос любительского брокера: «Какой объём рискового капитала у вас для спекуляций?» На такой вопрос большинство клиентов ответят: «Какой минимальный размер?» или назовут сумму значительно меньше той, которую они готовы инвестировать.',
        "Ich empfehle, die folgende Qualifikation als Leitfaden zu betrachten, wann immer Sie sich für Geld qualifizieren:": "Рекомендую придерживаться следующего подхода к квалификации по сумме:",
        "Wenn der Interessent angibt, dass 100.000 $ zu viel Geld sind, könnten Sie sagen:": "Если клиент говорит, что 100 000 долларов — это слишком, вы можете сказать:",
        'Mit diesem Ansatz qualifizieren Sie sich für viel größere Geldbeträge. Wenn Sie sich auf ein Portfolio von 100, 50 oder sogar 25 tausend Dollar konzentrieren und der Interessent nervös oder besorgt ist, ein Konto zu eröffnen, als letzten Ausweg, "Drop Closing" auf einen geringeren Betrag, wird es dem Interessenten oft ermöglichen, sich wohl genug zu fühlen, um Ihr Kunde zu werden. Es ist immer einfacher, nach unten zu gehen als nach oben.': "Такой подход позволит вам работать с гораздо большими суммами. Если вы концентрируетесь на портфеле в 100, 50 или даже 25 тысяч долларов, а клиент нервничает или сомневается — в крайнем случае можно снизить сумму. Часто этого достаточно, чтобы клиент почувствовал себя комфортно и стал вашим клиентом. Снижать сумму всегда проще, чем повышать.",
        "Denken Sie daran, wenn der Investor in der finanziellen Position ist, ist es nicht schwieriger, ein Konto von 160.000 $ als eines von 10.000 $ abzuschließen.": "Помните: если у инвестора есть финансовое положение, закрыть сделку на 160 000 долларов не сложнее, чем на 10 000.",
        "Qualifizieren Sie sich für große Konten, denken und sprechen Sie immer über große Konten, und Ihre Gedanken und harte Arbeit werden eine Anziehungskraft bilden, die sie zu Ihnen bringt.": "Работайте с крупными счетами, думайте и говорите о крупных счетах — ваши мысли и упорный труд создадут притягательную силу, которая приведёт их к вам.",
        "Korrekte Qualifikation": "Правильная квалификация",
        'Einer der größten Fehler, den der Novize-Broker machen wird, ist eine "schwache" Qualifikation. "Schwache" Qualifikationen stellen große Hindernisse auf Ihrem Weg zum Erfolg dar, weil sie selten als Kunden enden und dabei Ihr Vertrauensniveau als Abschließer verringern.': "Одна из самых частых ошибок начинающих брокеров — «слабая» квалификация. «Слабые» квалификации представляют собой серьёзные препятствия на пути к успеху, потому что такие люди редко становятся клиентами и при этом подрывают вашу уверенность как специалиста по закрытию сделок.",
        "Sie müssen verstehen, dass Ihre Zeit Ihr wertvollstes Gut ist. So grob es auch klingen mag, Sie haben keine Zeit für Informationssuchende und Personen, die nicht interessiert oder in der Lage sind, welche Art von Konto auch immer Sie präsentieren, zu eröffnen. Sie haben nur so viel Zeit, mit einer bestimmten Anzahl von Menschen zu arbeiten: Zeit ist Geld, also geben Sie es weise aus!": "Вы должны понимать, что ваше время — ваш самый ценный ресурс. Как бы грубо это ни звучало, у вас нет времени на тех, кто просто ищет информацию или не заинтересован и не готов открыть счёт того типа, который вы предлагаете. У вас有限ное количество людей: время — деньги, тратьте их мудро!",
        '"Schwache" Qualifikationen führen zu dem, was ich einen "Verkaufsminderwertigkeitskomplex" nenne. Der Interessent nimmt selten Ihre Anrufe entgegen und klingt, als würde er Ihnen einen Gefallen tun, indem er nur mit Ihnen spricht.': "«Слабая» квалификация приводит к тому, что я называю «комплексом неполноценности продавца». Клиент редко берёт трубку и звучит так, будто делает вам одолжение, просто соглашаясь поговорить.",
        'Wenn ein Interessent Ihnen den Eilakt gibt und sagt, schicken Sie einfach die Literatur, können Sie relativ sicher sein, dass es ausnahmslos eine "schwache" Qualifikation sein wird. Die Literatur, die Sie senden, wird wahrscheinlich in der "Kreisdatei" des Interessenten landen, allgemein bekannt als Papierkorb.': "Если клиент торопит вас и просит просто выслать материалы, можете быть практически уверены — это «слабая» квалификация. Отправленные материалы, скорее всего, окажутся в «круглом файле» — то есть в мусорной корзине.",
        "Meiner Meinung nach ist die einzig richtige Qualifikation diejenige, von der Sie glauben, dass sie ein ausgezeichneter Kandidat ist, um Ihr Kunde zu werden, und die folgenden Bestandteile erfüllt:": "По моему мнению, единственная правильная квалификация — это когда вы считаете, что перед вами превосходный кандидат в клиенты, и он соответствует следующим критериям:",
        "Geeignet für Spekulation": "Подходит для спекуляций",
        "Interessent ist bereit, ein kalkuliertes Risiko für die Möglichkeit eines erheblichen Gewinns einzugehen.": "Клиент готов пойти на рассчитанный риск ради возможности существенной прибыли.",
        "Aufgeschlossen und bereit zu investieren": "Открыт к инвестированию и готов вкладывать",
        "Interessent ist ein ernsthafter Investor und hat eine offene Einstellung zu dem, was Sie präsentieren, wo er bereit und in der Lage ist zu investieren, wenn ihm gefällt, was er sieht.": "Клиент — серьёзный инвестор с открытым умом к вашему предложению; он готов и способен инвестировать, если его убедит то, что он увидит.",
        "In einer liquiden Position zum Investieren": "Имеет ликвидные средства для инвестирования",
        "Der Interessent verfügt jetzt über einen bestimmten Betrag an flüssigem Risikokapital oder kann Aktien oder andere liquide Vermögenswerte innerhalb von 30 Tagen liquidieren, um diesen Betrag zu erhalten, wenn er investieren möchte.": "Клиент располагает определённой суммой ликвидного рискового капитала или может продать акции или другие ликвидные активы в течение 30 дней, чтобы получить эту сумму для инвестирования.",
        "Wird Literatur lesen": "Будет изучать материалы",
        "Interessent verspricht, zu lesen, was Sie senden werden, und die professionelle Höflichkeit, es mit Ihnen zu überprüfen.": "Клиент обещает изучить высланные материалы и проявить профессиональную вежливость — обсудить их с вами.",
        "Es ist viel besser, sofort herauszufinden, dass der Interessent nicht interessiert oder geeignet ist, als ihm nachzujagen und Ihre Zeit für mehrere Wochen zu verschwenden. Wenn Sie den Interessenten zu einem ungünstigen Zeitpunkt erwischt haben und die vorherigen vier Punkte nicht bestätigen können, qualifizieren Sie später oder am nächsten Tag neu.": "Гораздо лучше сразу понять, что клиент не заинтересован или не подходит, чем преследовать его и тратить недели впустую. Если вы застали клиента в неподходящий момент и не можете подтвердить четыре предыдущих пункта, вернитесь к квалификации позже или на следующий день.",
        "Wenn Sie über einen guten Vorrat an Leads verfügen, insbesondere bei dem derzeitigen gestiegenen öffentlichen Interesse an Aktien, sollten Sie nach 20 bis 30 Kontakten an einem Tag durchschnittlich 8 bis 10 starke Qualifikationen erreichen. (Wenn Sie viel mehr als das bekommen, qualifizieren Sie wahrscheinlich nicht richtig oder Sie verwenden sehr teure frisch beworbene Leads). Vierzig bis fünfzig starke Qualifikationen pro Woche sollten mindestens 5 bis 8 Geschäfte wöchentlich und die Grundlage für den Aufbau eines erfolgreichen Geschäfts darstellen.": "Если у вас хорошая база лидов, особенно учитывая нынешний рост общественного интереса к акциям, из 20–30 контактов в день вы должны получать в среднем 8–10 качественных квалификаций. (Если больше — возможно, вы неправильно квалифицируете или используете дорогие «горячие» лиды). 40–50 качественных квалификаций в неделю должны давать минимум 5–8 сделок и成为 основой вашего успешного бизнеса.",
        "Vergessen Sie nicht: Zeit ist Geld. Sie würden nicht daran denken, Ihr Geld zu verschwenden, also verschwenden Sie niemals Zeit. Der Weg zum Reichtum beginnt mit der richtigen Qualifikation!": "Не забывайте: время — деньги. Вы бы не стали тратить деньги впустую, так не тратьте и время. Путь к богатству начинается с правильной квалификации!",
        "Umgang mit Sonderfällen": "Работа со сложными случаями",
        "Bruder/Freund/Cousin": "Брат / Друг / Двоюродный брат",
        '"Lassen Sie nicht zu, dass Ihre persönlichen Beziehungen Ihre Fähigkeit beeinträchtigen, am Markt Geld zu verdienen. Stratton Oakmont gibt nur eine Handvoll Empfehlungen pro Jahr, also werden Sie nicht zu oft von mir hören. Ganz einfach, wenn wir bei unserer nächsten Investitionsmöglichkeit vorankommen, möchte ich Sie anrufen und es mit Ihnen besprechen können."': "«Не позволяйте личным отношениям мешать вам зарабатывать на рынке. Stratton Oakmont делает лишь несколько рекомендаций в год, так что вы будете получать от меня звонки нечасто. Просто когда у нас появится следующая инвестиционная возможность, я хотел бы позвонить вам и обсудить её с вами.»",
        "Immobilieninvestoren": "Инвесторы в недвижимость",
        '"Großartige Investition, aber Sie haben nicht die Liquidität oder die Diversifizierung des Marktes? In dieser Art von (Investitions-/Wirtschaftsumfeld) sollten Sie keinen Schritt ohne das machen."': "«Отличная инвестиция, но у вас нет ликвидности или диверсификации рынка? В такой инвестиционной и экономической обстановке не стоит делать шаг без этого.»",
        "Nicht interessiert": "Не заинтересован",
        '"Sind Sie derzeit am Markt?"': "«Вы сейчас работаете на рынке?»",
        "(Wenn ja, klären Sie das):": "(Если да, уточните):",
        '"Wir geben nur eine Handvoll Empfehlungen pro Jahr."': "«Мы делаем лишь несколько рекомендаций в год.»",
        "(Wenn nein,也许 hat er noch nichts getan)": "(Если нет — возможно, он ещё ничего не делал)",
        "Soweit ich verstehe, haben Sie in der Vergangenheit investiert.\\\"": "«Насколько я понимаю, вы раньше инвестировали.»",
        'oder "Soweit ich verstehe, investieren Sie mit einem lokalen Broker?"': "или «Насколько я понимаю, вы работаете с местным брокером?»",
        "NUR FÜR SCHULUNGSZWECKE": "ТОЛЬКО ДЛЯ ЦЕЛЕЙ ОБУЧЕНИЯ",
        
        # === SECTION 8 ===
        "Telefonkompetenzen": "Телефонные навыки",
        "← Zurück zu Motivation und Denkweise": "← Назад к мотивации и настрою",
        "Weiter: Ressourcen →": "Далее: Ресурсы →",
        "Voice Training": "Постановка голоса",
        "Developing Your Telephone Persona": "Формирование вашего телефонного образа",
        "Your voice is your most powerful tool when selling over the phone. Unlike face-to-face sales, clients cannot see your expressions or body language - they can only hear you. How you sound directly impacts your success rate.": "Голос — ваш самый мощный инструмент при продажах по телефону. В отличие от очных продаж, клиент не видит вашей мимики и языка тела — он слышит только голос. От того, как вы звучите, напрямую зависит ваш успех.",
        "Voice Exercises": "Упражнения для голоса",
        "Take 5 deep breaths, filling your diaphragm completely.": "Сделайте 5 глубоких вдохов, полностью наполняя диафрагму.",
        "Hum at different pitches for 30 seconds.": "Напевайте на разных тонах в течение 30 секунд.",
        'Practice articulation with "My money makes money" repeated 10 times with increasing speed.': "Отрабатывайте артикуляцию фразой «My money makes money», повторяя её 10 раз с нарастающей скоростью.",
        "Read a paragraph from the Wall Street Journal aloud, focusing on clarity and appropriate pacing.": "Прочитайте вслух абзац из Wall Street Journal, сосредоточившись на чёткости и правильном темпе.",
        "Practice your opening pitch in three different tones: enthusiastic, authoritative, and conversational.": "Потренируйтесь произносить вступление в трёх тонах: энергичном, авторитетном и беседовом.",
        "Daily Voice Warm-up Routine": "Ежедневная разминка для голоса",
        "Phone Rules": "Правила телефонных звонков",
        "Essential Guidelines for Phone Success": "Основные правила телефонных продаж",
        "Be prepared before dialing.": "Будьте готовы перед набором номера.",
        "Have your script, prospect information, and objection responses ready. Never fumble through papers while on a call.": "Подготовьте скрипт, информацию о клиенте и ответы на возражения. Никогда не листайте бумаги во время разговора.",
        "Stand up when making important calls.": "Вставайте при совершении важных звонков.",
        "Your posture affects your voice; standing improves your energy and projection.": "Ваша осанка влияет на голос; стоячее положение повышает энергию и силу звучания.",
        "Smile while speaking.": "Улыбайтесь во время разговора.",
        "Though they can't see you, clients can hear a smile in your voice. Keep a small mirror at your desk as a reminder.": "Хотя клиенты вас не видят, они слышат улыбку в вашем голосе. Держите на столе маленькое зеркало как напоминание.",
        "Never interrupt the prospect.": "Никогда не перебивайте клиента.",
        "Let them finish speaking, even if their objection is one you've heard a thousand times. This demonstrates respect and builds rapport.": "Дайте ему закончить, даже если его возражение вы слышали тысячу раз. Это демонстрирует уважение и укрепляет доверие.",
        "Use the prospect's name.": "Используйте имя клиента.",
        "Not excessively, but strategically at key points in the conversation, particularly when asking for the order.": "Не слишком часто, но осознанно — в ключевых моментах разговора, особенно при запросе заказа.",
        "Always confirm contact information.": "Всегда подтверждайте контактные данные.",
        "Verify phone numbers, spelling of names, and mailing addresses for follow-up materials.": "Проверяйте номера телефонов, написание имён и почтовые адреса для отправки материалов.",
        "Control the pace of the conversation.": "Контролируйте темп разговора.",
        "Don't allow long silences or let the prospect dictate the entire flow. Maintain leadership position while being respectful.": "Не позволяйте длинным паузам затягиваться и не отдавайте инициативу клиенту. Сохраняйте лидерскую позицию, оставаясь уважительным.",
        "Avoid industry jargon with new clients.": "Избегайте отраслевого жаргона с новыми клиентами.",
        "Speak in clear, compelling language that conveys benefits without alienating the prospect with terminology they may not understand.": "Говорите ясным, убедительным языком,传达 преимущества без отпугивания клиента непонятными терминами.",
        "Keep detailed call notes.": "Ведите подробные заметки о звонках.",
        "Document every interaction with specific details for follow-up calls. Reference previous conversations to build continuity and show attentiveness.": "Фиксируйте каждое взаимодействие с конкретными деталями для последующих звонков. Ссылайтесь на предыдущие разговоры для создания преемственности и демонстрации внимательности.",
        "End every call with a clear next step.": "Заканчивайте каждый звонок чётким следующим шагом.",
        "Whether it's sending information, scheduling a follow-up call, or confirming an order, always establish what happens next.": "Будь то отправка информации, назначение повторного звонка или подтверждение заказа — всегда определяйте, что будет дальше.",
        "Phone Sales Tips": "Советы по телефонным продажам",
        "12 Common Phone Errors to Avoid": "12 частых телефонных ошибок, которых стоит избегать",
        "Poor qualification.": "Плохая квалификация.",
        "Not determining if the prospect has the financial capacity or interest to invest.": "Неспособность определить, есть ли у клиента финансовы能力和兴趣 к инвестированию.",
        "Excessive talking.": "Чрезмерная говорливость.",
        "Dominating the conversation without learning about the client's needs.": "Засорять разговор, не выясняя потребности клиента.",
        "Inadequate objection handling.": "Недостаточная работа с возражениями.",
        "Becoming defensive or argumentative when facing resistance.": "Становиться防御ным или спорить при столкновении с сопротивлением.",
        "Reading directly from scripts.": "Чтение по скрипту дословно.",
        "Sounding robotic and impersonal.": "Звучать механически и безлично.",
        "Calling without a strategy.": "Звонки без стратегии.",
        "Winging it without clear objectives.": "Импровизация без чётких целей.",
        "Failing to build rapport.": "Неспособность建立ить контакт.",
        "Rushing to the pitch without establishing connection.": "Спешить к презентации, не установив контакт.",
        "Neglecting to ask for the sale.": "Забывать попросить о заказе.",
        "Ending calls without a clear closing attempt.": "Завершать звонки без попытки закрыть сделку.",
        "Using filler words.": "Использование слов-паразитов.",
        'Overuse of "um," "like," and "you know."': "Чрезмерное использование «э-э», «типа» и «знаешь».",
        "Lack of enthusiasm.": "Недостаток энтузиазма.",
        "Projecting fatigue or boredom, especially after multiple rejections.": "Проектирование усталости или скуки, особенно после нескольких отказов.",
        "Poor follow-through.": "Плохое выполнение обещаний.",
        "Failing to deliver on promises made during calls.": "Невыполнение обещаний, данных во время звонков.",
        "Inconsistent calling patterns.": "Непоследовательность в звонках.",
        "Sporadic calling instead of systematic prospecting.": "Эпизодические звонки вместо систематического поиска клиентов.",
        "Fear of rejection.": "Страх отказа.",
        "Allowing previous rejections to affect confidence on new calls.": "Позволять предыдущим отказам влиять на уверенность в новых звонках.",
        "Success Tactics for Phone Sales": "Тактики успеха в телефонных продажах",
        "Call blocks.": "Блоки звонков.",
        "Schedule uninterrupted 90-minute calling sessions for maximum effectiveness. Take 15-minute breaks between blocks.": "Планируйте непрерывные 90-минутные сессии звонков для максимальной эффективности. Делайте 15-минутные перерывы между блоками.",
        "The 3-second rule.": "Правило трёх секунд.",
        "After dialing, prepare yourself mentally in the 3 seconds before they answer. Visualize success.": "После набора номера морально подготовьтесь за 3 секунды до ответа. Визуализируйте успех.",
        "Pattern interrupts.": "Нарушение шаблона.",
        "Use unexpected statements or questions to break through the prospect's preconceived resistance to sales calls.": "Используйте неожиданные фразы или вопросы, чтобы преодолеть предвзятое сопротивление клиента звонкам продавцов.",
        "Voice mirroring.": "Зеркальное отражение голоса.",
        "Subtly match the prospect's speaking pace and tone to build unconscious rapport.": "Тонко подстраивайте темп и тон речи клиента для создания подсознательного контакта.",
        "Strategic silence.": "Стратегическая пауза.",
        "After asking for the order, remain silent. The first person to speak after the closing question often loses the psychological advantage.": "После запроса заказа замолчите. Первый, кто заговорит после вопроса о закрытии сделки, часто теряет психологическое преимущество.",
        "Benefit stacking.": "Концентрация преимуществ.",
        "Present benefits in groups of three for maximum impact and memorability.": "Представляйте преимущества группами по три для максимального воздействия и запоминаемости.",
        "Storytelling.": "Истории.",
        "Use brief success stories about similar clients to illustrate potential outcomes.": "Используйте краткие истории успеха аналогичных клиентов для иллюстрации возможных результатов.",
        "Trial closes.": "Пробное закрытие.",
        "Use small agreement questions throughout the call to build momentum toward the final close.": "Задавайте небольшие вопросы, на которые легко ответить «да», на протяжении всего разговора для создания импульса к финальному закрытию.",
        "Assumptive language.": "Язык предположения.",
        'Phrase questions and statements with the assumption that the prospect will move forward: "When we set up your account..." rather than "If you decide to invest..."': "Формулируйте вопросы и утверждения, исходя из того, что клиент действует: «Когда мы откроем ваш счёт...» вместо «Если вы решите инвестировать...»",
        "The callback strategy.": "Стратегия повторного звонка.",
        "When facing strong resistance, sometimes the best approach is to politely end the call and schedule a specific time to call back, giving the prospect time to consider.": "При сильном сопротивлении лучший подход — вежливо завершить звонок и назначить конкретное время для повторного звонка, дав клиенту время на размышление.",
        
        # === SECTION 9 ===
        "Ressourcen": "Ресурсы",
        "← Zurück zu Telefonkompetenzen": "← Назад к телефонным навыкам",
        "Zurück zur Startseite": "На главную",
        "Recommended Reading": "Рекомендуемая литература",
        "Essential Books for Sales Excellence": "Основные книги для мастерства в продажах",
        "Der grundlegende Text über Erfolgspsychologie und Vermögensbildung. Besondere Aufmerksamkeit sollte den Kapiteln über Verlangen, Glaube und Ausdauer gewidmet werden.": "Фундаментальный труд по психологии успеха и созданию богатства. Особое внимание стоит уделить главам о желании, вере и настойчивости.",
        "Umfassender Leitfaden zu Verkaufstechniken mit besonderer Relevanz für unseren Kaltakquise-Ansatz und Methoden zur Einwandbehandlung.": "Исчерпывающее руководство по техникам продаж, особенно актуальное для нашего подхода к холодным звонкам и методам работы с возражениями.",
        "Das Verständnis der sechs Prinzipien der Beeinflussung wird Ihre Fähigkeit, Interessenten zu überzeugen, dramatisch verbessern.": "Понимание шести принципов влияния значительно улучшит вашу способность убеждать клиентов.",
        "Wesentlicher Grundkurs zu Finanzmärkten und -instrumenten, den jeder Broker beherrschen sollte.": "Основы финансовых рынков и инструментов, которые должен знать каждый брокер.",
        "Klassischer Text über Marktpsychologie und wie Emotionen finanzielle Entscheidungen beeinflussen.": "Классический труд о психологии рынка и влиянии эмоций на финансовые решения.",
        "Einfache, zugängliche Finanzplanungsanleitung, die Ihnen hilft, die Denkweise von Privatanlegern zu verstehen.": "Простое и доступное руководство по финансовому планированию, помогающее понять образ мышления частных инвесторов.",
        "Interviews mit Top-Händlern, die wertvolle Einblicke in Marktpsychologie und Handelsstrategien liefern.": "Интервью с ведущими трейдерами, дающие ценные представления о психологии рынка и торговых стратегиях