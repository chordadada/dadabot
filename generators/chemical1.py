import random

# Списки для неорганических соединений
inorganic = {
    "prefixes": ["ди", "три", "тетра", "пента", "гекса"],
    "roots": ["хлор", "бром", "нитро", "гидрокси", "карбонил"],
    "suffixes": ["ил", "ен", "ан", "овая кислота", "сульфид"]
}

# Списки для органических соединений
organic = {
    "types": {
        "алканы": {
            "roots": ["проп", "бут", "пент", "гекс"],
            "suffixes": ["ан", "ил"]
        },
        "алкены": {
            "roots": ["проп", "бут", "пент"],
            "suffixes": ["ен", "диен"]
        },
        "спирты": {
            "roots": ["этан", "пропан", "бутан"],
            "suffixes": ["ол", "диол"]
        }
    },
    "prefixes": ["ди", "три", "тетра"]
}

def generate_iupac_name():
    # Случайный выбор типа соединения (50/50)
    if random.choice([True, False]):
        # Генерация органического соединения
        compound_type = random.choice(list(organic["types"].keys()))
        data = organic["types"][compound_type]
        return (
            f"{random.choice(organic['prefixes'])}"
            f"{random.choice(data['roots'])}"
            f"{random.choice(data['suffixes'])}"
        ).title()
    else:
        # Генерация неорганического соединения
        return (
            f"{random.choice(inorganic['prefixes'])}"
            f"{random.choice(inorganic['roots'])}-"
            f"{random.choice(inorganic['roots'])}"
            f"{random.choice(inorganic['suffixes'])}"
        ).title()