def generate_thought():
    try:
        with open('data/phrases.json', 'r', encoding='utf-8') as f:
            phrases = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Ошибка загрузки phrases.json: {e}")
        phrases = {}

    # Расширенные резервные значения
    default_phrases = {
        'intro': ['Голос из ниоткуда шепчет'],
        'noun': ['неопознанный феномен'],
        'verb': ['воздействует'],
        'concept': ['на ткань реальности'],
        'quote': ['«Всё есть ничто»'],
        'author': ['Анонимный провидец'],
        'absurd_comment': ['Спросите ещё раз']
    }

    # Логирование отсутствующих ключей
    missing_keys = [key for key in ['quote', 'author', 'absurd_comment'] if key not in phrases]
    if missing_keys:
        print(f"⚠️ В phrases.json отсутствуют ключи: {missing_keys}")

    structure = random.choice([
        ["intro", "noun", "verb", "concept"],
        ["quote", "author", "absurd_comment"]
    ])

    try:
        return ' '.join([
            random.choice(
                phrases.get(part, default_phrases.get(part, ["..."])
            ) for part in structure
        ])
    except Exception as e:
        print(f"Ошибка генерации мысли: {e}")
        return "💥 Мысль сгорела в квантовом вакууме"