from PIL import Image, ImageDraw, ImageFont
import random
import math
import os
import json


def generate_collapse(user_id: int):
    img = Image.new('RGB', (800, 600), color='black')
    draw = ImageDraw.Draw(img)
    
    # Генерация хаотичных линий
    for _ in range(100):
        x = random.randint(0, 800)
        y = random.randint(0, 600)
        draw.line(
            (x, y, 
             x + int(50 * math.sin(y/50)), 
             y + int(50 * math.cos(x/50))),
            fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
            width=3
        )
    
    # Добавление псевдонаучных надписей
    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        font = ImageFont.load_default()
    
    draw.text((50, 550), "Fig. 1: Ψ(x,t) = ℏ²/2m ∇²ψ + Vψ", 
              fill=(255, 0, 0), 
              font=ImageFont.truetype("arial.ttf", 16))
    
    # Сохранение в папку data/media
    os.makedirs("data/media", exist_ok=True)
    path = f"data/media/chart_{user_id}.png"
    img.save(path)
    return path
    

def generate_pseudoscience_chart(user_id: int):
    img = Image.new('RGB', (1200, 800), color='black')
    draw = ImageDraw.Draw(img)
    
    # Загрузка абсурдных фраз из data/phrases.json
    try:
        with open('data/phrases.json', 'r', encoding='utf-8') as f:
            phrases = json.load(f)
    except FileNotFoundError:
        raise Exception("Файл phrases.json не найден в папке data!")

    # Выбор случайных подписей
    title = random.choice(phrases['chart_titles'])
    x_label = random.choice(phrases['axis_labels']['x'])
    y_label = random.choice(phrases['axis_labels']['y'])
    legend_text = random.choice(phrases['legends'])
    data_labels = random.sample(phrases['data_labels'], 3)

    # Стили текста
    try:
        title_font = ImageFont.truetype("arialbd.ttf", 28)
        axis_font = ImageFont.truetype("arial.ttf", 18)
        legend_font = ImageFont.truetype("ariali.ttf", 16)
    except:
        title_font = ImageFont.load_default()
        axis_font = ImageFont.load_default()
        legend_font = ImageFont.load_default()

    # Псевдонаучный фон
    for _ in range(100):
        draw.line(
            (random.randint(0, 1200), random.randint(0, 800),
             random.randint(0, 1200), random.randint(0, 800)),
            fill=(random.randint(0, 50), random.randint(0, 50), random.randint(50, 100)),
            width=3
        )

    # Диаграмма-хаос
    def draw_chaos_elements():
        # Спирали
        for _ in range(5):
            cx, cy = random.randint(100, 1000), random.randint(100, 600)
            for i in range(0, 360, 10):
                radius = random.randint(50, 200)
                x = cx + radius * math.cos(math.radians(i))
                y = cy + radius * math.sin(math.radians(i))
                draw.ellipse((x-3, y-3, x+3, y+3), fill=(0, 255, 255))

        # Столбцы безумия
        for x in range(100, 1100, 70):
            height = random.randint(50, 400)
            draw.rectangle(
                [x, 800-height, x+40, 800],
                fill=(random.randint(0,255), 
                random.randint(0,255), 
                random.randint(0,255)))
            
    draw_chaos_elements()

    # Текстовые элементы
    draw.text((1200//2 - 400, 20), title, 
              fill=(255, 69, 0), 
              font=title_font,
              stroke_width=2,
              stroke_fill='white')

    # Подписи осей с искажением
    draw.text((400, 750), x_label, 
              fill=(255, 215, 0), 
              font=axis_font, 
              rotate=random.randint(-15, 15))
    
    draw.text((50, 400), y_label, 
              fill=(0, 255, 255), 
              font=axis_font, 
              rotate=90 + random.randint(-10, 10))

    # Легенда в облаке
    legend_box = [800, 50, 1150, 200]
    draw.rounded_rectangle(legend_box, radius=15, fill=(30, 30, 30), outline='yellow')
    draw.multiline_text((820, 70), 
                       f"★ {legend_text} ★\n" + "\n".join(data_labels),
                       fill=(255, 105, 180), 
                       font=legend_font,
                       spacing=10)

    # Псевдосетка
    for x in range(0, 1200, 30):
        draw.line((x, 0, x, 800), 
                fill=(random.randint(50,100), 0, 0), 
                width=1 + random.randint(0,2))
    
    # Сохранение в data/media
    os.makedirs("data/media", exist_ok=True)
    path = f"data/media/dada_chart_{user_id}.png"
    img.save(path)
    return path