# 🏎️ My Racing Game

**My Racing Game** — аркадна гоночна гра на Python з використанням Pygame. Гравець керує автомобілем, уникання ворогів і збирає бонуси для збільшення рахунку.  

---

## 🎮 Особливості
- Повнокаркасна гоночна дорога з скролінгом
- Керування автомобілем гравця: стрілки ← → ↑ ↓
- Вороги рухаються по смугах дороги
- Бонуси для збільшення рахунку
- Пауза (SPACE) та рестарт після поразки (ENTER)
- Фоновий звук (MP3) при наявності файлу

---

## ⬇️ Встановлення

1. Склонуй репозиторій:
```bash
git clone https://github.com/ViktorPro1/my_racing_game.git
cd my_racing_game

Створи віртуальне середовище (рекомендовано):

python3 -m venv .venv
source .venv/bin/activate  # Linux / macOS
.venv\Scripts\activate     # Windows

Встанови залежності:

pip install pygame
🚀 Запуск гри
python main.py

ESC — вихід з гри
SPACE — пауза / відновлення
ENTER — рестарт після поразки

🎨 Структура проекту
my_racing_game/
│
├─ assets/              # Зображення та музика
│   ├─ background.mp3
│   ├─ road.png
│   ├─ player_car.png
│   ├─ enemy_car.png
│   └─ bonus.png
│
├─ main.py              # Основний код гри
└─ README.md
📝 Примітки

Якщо відсутні файли в assets/, гра створює базові графічні об'єкти

Для найкращого досвіду рекомендується використовувати повний екран

Гра написана на Python 3.x та Pygame

🏆 Мета

Уникати ворогів, збирати бонуси та набирати максимальний рахунок!


---

💡 Порада:  
- Збережи цей текст як `README.md` у корені проекту.  
- Потім зроби коміт і пуш на GitHub:  

```bash
git add README.md
git commit -m "Add README"
git push
