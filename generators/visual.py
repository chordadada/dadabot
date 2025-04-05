from PIL import Image, ImageDraw, ImageFont
import random
import math
import os

def generate_pseudoscience_chart(user_id: int):
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