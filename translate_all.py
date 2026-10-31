#!/usr/bin/env python3
"""
Переводчик section-файлов: добавляет lang-ru после каждого lang-de.
Использует словарь переводов + эвристику для непереведённых элементов.
"""
import re
import os

BASE = os.path.dirname(os.path.abspath(__file__))

# Полный словарь переводов DE→RU
DE_TO_RU = {
    # === ОБЩИЕ ===
    "Stratton Oakmont Schulungshandbuch für Vertrieb": "Stratton Oakmont. Руководство по продажам",
    "Motivation und Denkweise": "Мотивация и мышление",
    "Selbstverbesserung": "Самосовершенствование",
    "Verkaufskraft": "Сила продаж",
    "Verkaufstechniken": "Техники продаж",
    "Bewährte Methoden": "Лучшие практики",
    "Besondere Situationen": "Особые ситуации",
    "Besondere Handhabungssituationen": "Особые ситуации работы с клиентами",
    "Telefonkompetenzen": "Навыки телефонных продаж",
    "Ressourcen": "Ресурсы",
    "Download Original PDF": "Скачать оригинальный PDF",
    "NUR FÜR SCHULUNGSZWECKE": "ТОЛЬКО ДЛЯ ЦЕЛЕЙ ОБУЧЕНИЯ",
    
    # === НАВИГАЦИЯ ===
    "← Zurück zur Startseite": "← Назад на главную",
    "← Zurück zu Besondere Handhabungssituationen": "← Назад к особым ситуациям",
    "← Zurück zu Besondere Situationen": "← Назад к особым ситуациям",
    "← Zurück zu Bewährte Methoden": "← Назад к лучшим практикам",
    "← Zurück zu Verkaufstechniken": "← Назад к техникам продаж",
    "← Zurück zu Motivation und Denkweise": "← Назад к мотивации и мышлению",
    "← Zurück zu Telefonkompetenzen": "← Назад к телефонным навыкам",
    "Weiter: Verkaufskraft →": "Далее: Сила продаж →",
    "Weiter: Verkaufstechniken →": "Далее: Техники продаж →",
    "Weiter: Bewährte Methoden →": "Далее: Лучшие практики →",
    "Weiter: Besondere Situationen →": "Далее: Особые ситуации →",
    "Weiter: Besondere Handhabungssituationen →": "Далее: Особые ситуации работы с клиентами →",
    "Weiter: Motivation und Denkweise →": "Далее: Мотивация и мышление →",
    "Weiter: Telefonkompetenzen →": "Далее: Телефонные навыки →",
    "Weiter: Ressourcen →": "Далее: Ресурсы →",
    
    # === SECTION 7: MOTIVATION ===
    "Die Anatomie des Erfolgs: Die richtigen Gewohnheiten entwickeln": "Анатомия успеха: развитие правильных привычек",
    "Menschen sind alle Gewohnheitstiere: sowohl gute als auch schlechte. Sobald wir in einer \"Spur\" sind, ist es schwer, die Gleise zu wechseln. Dies kann entweder für oder gegen uns arbeiten. Im Folgenden finden Sie häufige Gewohnheiten und Eigenschaften der meisten erfolgreichen Menschen. Kommen Sie in die \"Spur\" des Erfolgs, indem Sie diese Affirmationen wiederholen und befolgen:": "Человек — существо привычек: как хороших, так и плохих. Когда мы входим в «колею», сменить её нелегко. Это может работать как на нас, так и против. Ниже перечислены распространённые привычки и черты большинства успешных людей. Войдите в «колею» успеха, повторяя и следуя этим утверждениям:",
    "Ich habe klar definierte Ziele und identifiziere die notwendigen Schritte, um diese Ziele zu erreichen.": "Я чётко определяю свои цели и определяю шаги, необходимые для их достижения.",
    "Ich habe einen durchdachten \"Schlachtplan\" zur Erreichung meiner Ziele, den ich mit unerbittlicher Beharrlichkeit, Selbstaufopferung und Disziplin verfolge.": "Я продумал «план действий» для достижения своих целей, которого придерживаюсь с неутомимой настойчивостью, самопожертвованием и дисциплиной.",
    "Ich glaube an mich selbst und meine Bestimmung zum Erfolg.": "Я верю в себя и в своё предназначение для успеха.",
    "Ich habe ein intensives Verlangen nach Erfolg, das eine Energiekraft erzeugt, die es mir ermöglicht, den Preis der Selbstaufopferung, harter Arbeit, Beharrlichkeit und Selbstdisziplin zu zahlen, um meine Ziele zu erreichen.": "Я испытываю жгучее желание успеха, которое создаёт энергетическую силу, позволяющую заплатить цену самопожертвования, упорного труда, настойчивости и самодисциплины для достижения моих целей.",
    "Ich stelle mir vor meinem geistigen Auge die Belohnungen des Erfolgs vor, die als \"Treibstoff\" dienen, um meinen Motor am Laufen zu halten.": "Я вижу перед мысленным взором награды успеха, которые служат «топливом» для поддержания огня моего двигателя.",
    "Ich weiß, dass ich für den Erfolg bestimmt bin. Alles, was in meinem Leben geschieht, dient dem Zweck, meinen Erfolg zu erlangen. Ich betrachte Rückschläge als Lernerfahrungen, die unweigerlich Chancen bieten werden. Probleme sind niemals Probleme, sondern Herausforderungen, die mit sorgfältigem Nachdenken und Handeln überwunden werden.": "Я знаю, что предназначен для успеха. Всё, что происходит в моей жизни, служит цели достижения моего успеха. Я рассматриваю неудачи как учебный опыт, который неизменно несёт в себе зёрна возможностей. Проблемы — это никогда не проблемы, а вызовы, которые преодолеваются вдумчивым подходом и действиями.",
    "Ich weiß, dass Wut, Eifersucht, Rachsucht und negative Gedanken wie eine Plage zu vermeiden sind. Sie sind Viren, die den Geist eines Menschen infizieren und den Willen zum Erfolg zerstören. Ich weiß, dass mich nichts wütend machen kann, es sei denn, ich lasse es zu.": "Я знаю, что гнев, зависть, жажда мести и негативные мысли нужно избегать, как чумы. Это вирусы, заражающие разум человека и уничтожающие волю к успеху. Я знаю, что ничто не может вывести меня из себя, если я сам этого не позволю.",
    "Ich fühle mich großartig.": "Я чувствую себя великолепно.",
    "Gewöhnen Sie sich an, die Dinge zu sagen und zu tun, die erfolgreiche Menschen tun, und Sie werden eine Anziehungskraft schaffen, die es Ihnen ermöglicht, Ihr eigener Zaubergeist zu sein, mit nicht drei, sondern einer unbegrenzten Anzahl von Wünschen, die Sie sich selbst erfüllen können. Wiederholen Sie einfach täglich diese positiven Affirmationen und praktizieren Sie, was Sie predigen: Ihre Wünsche werden Ihr eigener Befehl sein!": "Войдите в привычку говорить и делать то, что делают успешные люди — и вы создадите силу притяжения, которая позволит вам стать собственным волшебным духом, с не тремя, а неограниченным количеством желаний. Просто повторяйте ежедневно эти позитивные утверждения и практикуйте то, что проповедуете: ваши желания повиноваться вам!",
    "Manifest der Gewinner": "Манифест победителей",
    "Wir alle haben die Kraft, uns durch die Gedanken und Anliegen unseres Geistes zu \"formen\". Wiederholen und befolgen Sie das \"Manifest der Gewinner\" und schließen Sie sich dem Team an!": "У всех нас есть власть «формировать» себя с помощью мыслей и помыслов нашего разума. Повторяйте и следуйте «Манифесту победителей» — и присоединяйтесь к команде!",
    "Ich bin ein Gewinner, weil ich wie ein Gewinner denke, mich wie ein Gewinner vorbereite und wie ein Gewinner handle.": "Я победитель, потому что думаю как победитель, готовлюсь как победитель и действую как победитель.",
    "Ich bin ein Gewinner, weil ich hohe, aber erreichbare Ziele setze, mit Entschlossenheit und Beharrlichkeit auf diese Ziele hinarbeite und niemals aufhöre, bis ich sie erreicht habe.": "Я победитель, потому что ставлю высокие, но достижимые цели, работаю над ними с решимостью и настойчивостью и не останавливаюсь, пока не достигну их.",
    "Ich bin ein Gewinner, weil ich stark genug bin, \"Nein!\" zu den Dingen zu sagen, die mich weniger als mein Bestes sein lassen würden, und \"Ja!\" zu den Herausforderungen und Möglichkeiten zu sagen, die mich wachsen lassen und mein Leben verbessern werden.": "Я победитель, потому что достаточно силён, чтобы сказать «Нет!» тому, что делает меня хуже, и сказать «Да!» вызовам и возможностям, которые помогут мне расти и улучшать свою жизнь.",
    "Ich bin ein Gewinner, weil totales Engagement mein ständiger Begleiter ist und persönliche Integrität mein lebenslanger Mentor ist.": "Я победитель, потому что полная отданность — мой постоянный спутник, а личная честность — мой наставник на всю жизнь.",
    "Ich bin ein Gewinner, weil ich lerne, die verlockenden Abkürzungen zu vermeiden, die zu Enttäuschungen führen können, und die ungesunden Gewohnheiten, die zu einer Niederlage führen könnten.": "Я победитель, потому что учусь избегать соблазнительных коротких путей, ведущих к разочарованию, и вредных привычек, которые могут привести к поражению.",
    "Ich bin ein Gewinner, weil ich ein wohlverdientes Selbstvertrauen habe.": "Я победитель, потому что заслужил уверенность в себе.",
    "Ich bin ein Gewinner, weil ich gelernt habe, Kritik nicht als Bedrohung anzunehmen, sondern als Gelegenheit, meine Einstellungen zu überprüfen und meine Fähigkeiten zu verbessern.": "Я победитель, потому что научился принимать критику не как угрозу, а как возможность проверить свои установки и улучшить навыки.",
    "Ich bin ein Gewinner, weil ich inmitten von Hindernissen durchhalte und im Angesicht der Niederlage weiterkämpfe.": "Я победитель, потому что нахожу в себе силы преодолевать преграды и сражаться, несмотря на поражение.",
    "Ich bin ein Gewinner wegen meiner Begeisterung für das Leben, meiner Freude an der Gegenwart und meinem Vertrauen in die Zukunft.": "Я победитель благодаря своей страсти к жизни, радости настоящего момента и вере в будущее.",
    "Ich bin ein Gewinner, weil ich ein Stratton Oakmont Mitarbeiter bin.": "Я победитель, потому что я сотрудник Stratton Oakmont.",
    "Mentale Stärke": "Сила разума",
    "Von: Ira Boshnack<br>Geschäftsführender Direktor": "Автор: Ира Бошнак<br>Управляющий директор",
    "\"Alles, was der menschliche Geist vernünftigerweise konzipieren und glauben kann, kann auch erreicht werden.\"": "«Всё в пределах разума, что человек может вообразить и во что может поверить, может быть достигнуто.»",
    "Mentale Obsessionen haben körperliche Manifestationen: Ihr Körper reagiert auf die Gedanken und Sorgen des Geistes. Ihre Gedanken können Sie krank machen oder Endorphine freisetzen (über 50-mal potenter als Morphium), die Hochgefühl und gute Gesundheit verursachen. Ein emotional aufgebrachtes Individuum ist anfälliger für Unfälle und schlechte Gesundheit als ein emotional stabiles Individuum.": "Ментальная одержимость имеет физические проявления: ваше тело реагирует на мысли и помыслы разума. Ваши мысли могут вас заболить или выдвинуть эндорфины (в 50 раз мощнее морфина), которые вызывают приподнятость и здоровье. Эмоционально неустойчивый человек более подвержен травмам и болезням, чем эмоционально стабильный.",
    "Wie können wir sicherstellen, dass wir nicht zu Opfern unserer Ängste werden? Da der Geist dem Körper sagt, wie er handeln soll, denken Sie die höchsten, erhebendsten Gedanken, die Sie sich vorstellen können. Hier sind einige Tipps, die Ihnen helfen, die Kraft Ihres Geistes zu nutzen:": "Как убедиться, что мы не станем жертвами своих тревог? Разум подсказывает телу, как действовать, — думайте о самых возвышенных, воодушевляющих мыслях, которые только можете представить. Вот несколько советов по использованию силы вашего разума:",
    "Visualisieren Sie positive Situationen.": "Представляйте себе позитивные ситуации.",
    "Denken und sprechen Sie gut über Ihre Gesundheit.": "Думайте и говорите хорошее о своём здоровье.",
    "Nutzen Sie Ihre Visualisierungskraft.": "Используйте силу визуализации.",
    "Verwenden Sie täglich positive Selbstgespräche.": "Практикуйте позитивный внутренний диалог каждый день.",
    "Verweilen Sie nicht bei Beschwerden, sonst werden sie zur Gewohnheit und kehren wieder.": "Не зацикливайтесь на недугах — иначе они войдут в привычку и будут возвращаться.",
    "Machen Sie irgendeine Art von Übung, alles, was die Herz-Kreislauf-Aktivität fördert.": "Занимайтесь физическими упражнениями — любыми, которые стимулируют сердечно-сосудистую систему.",
    "Regelmäßige Bewegung kann dem Leben eines Menschen zehn Jahre gesundes Leben hinzufügen.": "Регулярные занятия спортом могут продлить здоровую жизнь на десять лет.",
    "Setzen Sie sich Ziele und nutzen Sie Begeisterung, um sie zu erreichen.": "Ставьте цели и используйте энтузиазм для их достижения.",
    "Beharrlichkeit und Entschlossenheit zusammen sind allmächtig. Sie scheitern nie, es sei denn, Sie geben auf. Erfolgreiche Menschen haben klar definierte Spielpläne, die sie ständig überprüfen. Sie wissen, wohin sie jeden Tag, jeden Monat und jedes Jahr gehen. Die Dinge passieren nicht einfach in ihrem Leben: sie lassen sie geschehen. Lassen Sie nichts in Ihrem Weg stehen. Ihr Maß an Beharrlichkeit angesichts von Widrigkeiten und Enttäuschungen wird ein Maß des Glaubens an sich selbst sein. Verbinden Sie sich mit Menschen, die Ihre Ziele und Arbeitsgewohnheiten teilen. Sie müssen den Führern folgen, die die Besten in dem sind, was sie tun.": "Настойчивость и решимость вместе всемогущи. Вы никогда не терпите неудачу, пока не сдаётесь. Успешные люди чётко определяют свои планы и постоянно их пересматривают. Они знают, куда идут каждый день, каждый месяц и каждый год. В их жизни ничего не происходит само по себе: они заставляют это происходить. Не позволяйте ничему стоять на вашем пути. Ваш уровень настойчивости перед лицом трудностей и разочарований — мера вашей веры в себя. Окружайте себя людьми, разделяющими ваши цели и трудовые привычки. Вы должны следовать за лидерами — лучшими в том, что они делают.",
    "Wahrscheinlich ist das Schwierigste, in die richtige Richtung zu starten. Eine Verkaufskarriere zu beginnen ist wie ein Flugzeug zu fliegen. Um vom Boden abzuheben, müssen Sie Vollgas geben. Aber Sie können die Geschwindigkeit nicht beibehalten, sonst brennt der Motor aus. Wenn das Flugzeug die Reisehöhe erreicht, nehmen Sie ein wenig Gas zurück. So sind unsere Verkaufskarrieren. Bis zu einem gewissen Punkt müssen Sie Vollgas geben, um abzuheben und die Höhen zu erreichen, wo Sie dann gleiten können.": "Пожалуй, самое сложное — начать движение в правильном направлении. Начать карьеру в продажах — как пилотировать самолёт. Чтобы оторваться от земли, нужен полный газ. Но нельзя удерживать такую скорость, иначе сгорит мотор. Когда самолёт набирает крейсерскую высоту, вы немного ослабляете газ. Вот так устроен наш путь в продажах. До определённого момента нужно дать полный газ, чтобы взлететь и набрать высоту, а потом можно лететь巡航но.",
    "Sobald Sie ein gewisses Maß an Erfolg erreicht haben, können Sie sich mit mehr Zeit für Ihr Vergnügen belohnen.": "Как только вы достигнете определённого уровня успеха, вы сможете наградить себя большим количеством времени для удовольствий.",
    "Ein Einblick, wie man ein besserer Vertriebsprofi wird": "Путь к тому, чтобы стать лучшим специалистом по продажам",
    "\"Wir werden zu dem, worüber wir am meisten nachdenken\"": "«Мы становимся тем, о чём думаем чаще всего.»",
    "Vertriebsprofis haben Amerika groß gemacht. Sie fördern unsere kapitalistische demokratische Gesellschaft. Ohne Verkäufer hätten IBM, Xerox, Merrill Lynch oder jedes andere große Unternehmen niemals finanziellen Erfolg haben können. Der professionelle Verkäufer ist das bestbezahlte Segment unserer Gesellschaft.": "Профессионалы продаж сделали Америку великой. Они продвигают нашу капиталистическую демократическую систему. Без продавцов ни IBM, ни Xerox, ни Merrill Lynch, ни одна крупная компания не смогла бы достичь финансового успеха. Профессиональный продавец — самая высокооплачиваемая категория нашего общества.",
    "Ich habe nie einen geborenen Vertriebsprofi getroffen, egal wie gut er oder sie sein mag. Jeder Superverkäufer ist ein ausgebildeter Profi. Sie sind bereit, den Preis des Erfolgs zu zahlen. Sie haben sich verpflichtet, die Schlüsselelemente des Erfolgs in ihrem Bereich zu üben, zu trainieren und zu proben. Niemandem wurde das Recht auf Reichtum und Erfolg von jemand anderem als sich selbst verwehrt. Was Sie vor sich haben, ist ein enormer Bedarf an einer Sache namens Anstrengung. Professionelle Anstrengung, Studium und Anwendung. Sie verdienen heute genau das, was Ihre Fähigkeiten, Anstrengungen und Willenskraft Ihnen zu verdienen erlaubt haben.": "Я никогда не встречал прирождённого продавца, каким бы талантливым он ни был. Каждый суперпродавец — обученный профессионал. Они готовы платить цену успеха. Они взяли на себя обязательство практиковать, отрабатывать и репетировать ключевые элементы успеха в своей области. Никто никогда не лишал права на богатство и успех, кроме них самих. Перед вами — огромная потребность в чём-то, что называется усилием. Профессиональное усилие, изучение и применение. Вы зарабатываете ровно столько, сколько ваши навыки, усилия и сила воли позволяют вам зарабатывать сегодня.",
    "Jeder hat tief in sich drin ein riesiges Reservoir an Talent und Energie, das angezapft und auf das Erreichen von Supererfolg gerichtet werden kann. Alles, was Sie tun müssen, ist, ein brennendes Verlangen und die Bereitschaft zu haben, den Preis der Selbstdisziplin, harter Arbeit und Beharrlichkeit beim Erreichen Ihrer Verkaufsziele zu zahlen.": "У каждого глубоко внутри есть огромный запас таланта и энергии, который можно направить на достижение грандиозного успеха. Всё, что нужно — это жгучее желание и готовность заплатить цену самодисциплины, упорного труда и настойчивости для достижения ваших целей в продажах.",
    "Eines der Geheimnisse für erfolgreichen Verkauf ist positives Denken und die Fähigkeit, mentale visuelle Bilder zu nutzen. Unser Verhalten wird von Bildern des Erfolgs gesteuert, und ohne diese Bilder können wir uns nicht mobilisieren und motivieren, unsere Ziele zu erreichen. Die Kraft der mentalen Visualisierung kann eine Flut von sensorischen visuellen Bildern nutzen, um einen intellektuell formulierten Plan zu verstärken, der eine unbegrenzte Quelle an Begeisterung freisetzen wird, um sie auf gesteigerte Verkäufe anzuwenden. Wenn Ihre Vorstellungskraft gebündelt und auf die Vorteile und Belohnungen des Erfolgs ausgerichtet ist, werden die Feuer der Motivation zusammen mit der Selbstdisziplin und dem Opfer entzündet, um Ihre Ziele zu erreichen. Die Kraft der mentalen Visualisierung sollte nicht als selbstverständlich angesehen werden.": "Один из секретов успешных продаж — позитивное мышление и умение использовать ментальную визуализацию. Наше поведение управляется картинками достижения, и без этих картинок мы не можем мобилизовать и мотивировать себя для достижения целей. Сила ментальной визуализации может собрать поток чувственных визуальных образов для укрепления интеллектуально разработанного плана, который высвободит неограниченный источник энтузиазма для увеличения продаж. Когда ваше воображение сфокусировано на выгодах и наградах успеха, зажигаются огоньки мотивации вместе с самодисциплиной и жертвенностью для достижения ваших целей. Силой ментальной визуализации не стоит пренебрегать.",
    "Die Kraft des Geistes und der visuellen Vorstellungskraft kann weiter verstanden werden, indem man einfach daran denkt, wie, wenn wir hungrig sind und an unser Lieblingsessen denken, unser Mund zu wässern beginnt, oder wenn wir fantastische Nachrichten hören, uns ein Schwall guter Gefühle umhüllt; oder wenn wir schreckliche Nachrichten hören, wir ein reißendes Gefühl in der Magengrube spüren. Denken Sie daran, dass jedes große Werk und jede Entdeckung zuerst im Geist eines Menschen als lebendiges Bild existierte. Jede Handlung und Tat, die es der Menschheit ermöglicht hat, zu glänzen und Erfolg zu erzielen, wurde zuerst im Geist eines Menschen geboren. Machen Sie sich keine Illusionen, intensives positives Denken und visuelle Bilder können all Ihre Leben verändern. Die Fähigkeit, die eigenen Hoffnungen und Bestrebungen in positive, sensorisch reiche Bilder zu übersetzen, ist die Schneidkante, die den Hochleister vom Durchschnittsmenschen trennt. Die anhaltende Intensität Ihrer positiven Gedanken und detaillierten mentalen Visualisierung wird der entscheidende Faktor für den Grad Ihres Erfolgs im Verkauf sowie im Leben sein!": "Силу разума и визуальных образов можно понять ещё лучше, если вспомнить, как, когда мы голодны и думаем о любимой еде, у нас начинает текти слюна, или когда мы слышим потрясающие новости — нас окутывает волна хороших чувств; или когда мы слышим ужасные новости — мы чувствуем раздирающее ощущение в подложечке. Помните, что каждое великое произведение и каждое открытие сначала существовали в чьём-то сознании как яркий образ. Каждое действие и поступок, позволивший человечеству преуспеть и достичь успеха, родился сначала в чьей-то голове. Сомневаться не приходится: интенсивное позитивное мышление и визуальные образы способны изменить вашу жизнь. Способность превращать надежды и стремления в позитивные, богатые ощущениями образы — то острое лезвие, которое отделяет высокого достижителя от рядового обывателя. Устойчивая интенсивность ваших позитивных мыслей и детальной ментальной визуализации будет решающим фактором степени вашего успеха в продажах — и в жизни!",
}


def translate_section(filepath):
    """Добавляет lang-ru после каждого lang-de в файле."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    new_lines = []
    added = 0
    
    for i, line in enumerate(lines):
        new_lines.append(line)
        
        # Проверяем есть ли lang-de в строке
        if 'class="lang-de"' not in line:
            continue
        
        # Проверяем, есть ли уже lang-ru после этой строки
        if i + 1 < len(lines) and 'class="lang-ru"' in lines[i + 1]:
            continue
        
        # Ищем перевод в словаре — сравниваем текст между тегами
        text_match = re.search(r'>(.*?)</', line)
        if not text_match:
            continue
        
        de_text = text_match.group(1)
        
        # Ищем точное совпадение в словаре
        ru_text = None
        for key, val in DE_TO_RU.items():
            if key in de_text or de_text in key:
                ru_text = val
                break
        
        if ru_text:
            ru_line = line.replace('class="lang-de"', 'class="lang-ru"')
            # Заменяем текст
            ru_line = re.sub(r'>(.*?)<', f'>{ru_text}<', ru_line, count=1)
            new_lines.append(ru_line)
            added += 1
    
    if added > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
    
    return added


def add_ru_button(filepath):
    """Добавляет кнопку RU в language-selector, если её нет."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'data-lang="ru"' in content:
        return False
    
    # Добавляем кнопку RU после кнопки DE
    content = content.replace(
        'onclick="switchLanguage(\'de\')">DE</button>',
        'onclick="switchLanguage(\'de\')">DE</button>\n        <button class="language-btn" data-lang="ru" onclick="switchLanguage(\'ru\')">RU</button>'
    )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    return True


def main():
    files = [
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
    
    for fname in files:
        fpath = os.path.join(BASE, fname)
        if not os.path.exists(fpath):
            print(f"❌ {fname}: not found")
            continue
        
        # Добавляем кнопку RU
        btn = add_ru_button(fpath)
        
        # Добавляем переводы
        added = translate_section(fpath)
        
        # Считаем статистику
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        en_count = content.count('class="lang-en"')
        ru_count = content.count('class="lang-ru"')
        
        status = "DONE" if ru_count >= en_count and ru_count > 0 else "PARTIAL" if ru_count > 0 else "TODO"
        print(f"{status} {fname}: en={en_count} ru={ru_count} (+{added} added)")


if __name__ == "__main__":
    main()
