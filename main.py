import pygame
import sys
import random

pygame.init()
clock = pygame.time.Clock()

# Музика
try:
    pygame.mixer.music.load("assets/background.mp3")
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)
except:
    print("⚠️ Музика не завантажена")

# Екран
SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = SCREEN.get_size()
pygame.display.set_caption("🏎️ Racing Game")

# Завантаження зображень
try:
    road_img = pygame.image.load("assets/road.png")
    road_img = pygame.transform.scale(road_img, (WIDTH, HEIGHT))
except:
    print("⚠️ Фон дороги не завантажено, створюємо базовий")
    road_img = pygame.Surface((WIDTH, HEIGHT))
    road_img.fill((50, 50, 50))
    for i in range(0, HEIGHT, 100):
        pygame.draw.rect(road_img, (255, 255, 255), (WIDTH // 2 - 10, i, 20, 50))

PLAYER_WIDTH = 120
PLAYER_HEIGHT = 180

try:
    player_car = pygame.image.load("assets/player_car.png")
    player_car = pygame.transform.scale(player_car, (PLAYER_WIDTH, PLAYER_HEIGHT))
except:
    print("⚠️ Машина гравця не завантажена")
    player_car = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
    player_car.fill((0, 100, 255))
    pygame.draw.rect(player_car, (255, 255, 255), (10, 10, PLAYER_WIDTH - 20, PLAYER_HEIGHT - 20))

try:
    enemy_car_img = pygame.image.load("assets/enemy_car.png")
    enemy_car_img = pygame.transform.scale(enemy_car_img, (60, 120))
except:
    print("⚠️ Машина ворога не завантажена")
    enemy_car_img = pygame.Surface((60, 120))
    enemy_car_img.fill((255, 0, 0))
    pygame.draw.rect(enemy_car_img, (200, 0, 0), (5, 5, 50, 110))

try:
    bonus_img = pygame.image.load("assets/bonus.png")
    bonus_img = pygame.transform.scale(bonus_img, (40, 40))
except:
    print("⚠️ Бонус не завантажено")
    bonus_img = pygame.Surface((40, 40), pygame.SRCALPHA)
    pygame.draw.circle(bonus_img, (255, 215, 0), (20, 20), 20)
    pygame.draw.polygon(bonus_img, (255, 255, 0), [(20, 5), (25, 15), (35, 15), (27, 22), (30, 35), (20, 25), (10, 35), (13, 22), (5, 15), (15, 15)])

# Параметри гри
player_speed_x = 10
player_speed_y = 7

ROAD_LEFT_BOUND = 250
ROAD_RIGHT_BOUND = WIDTH - 250
ROAD_TOP_BOUND = HEIGHT // 3
ROAD_BOTTOM_BOUND = HEIGHT - 140

NUM_LANES = 6
LANE_WIDTH = (ROAD_RIGHT_BOUND - ROAD_LEFT_BOUND) // NUM_LANES
LANES_X = [ROAD_LEFT_BOUND + i * LANE_WIDTH + LANE_WIDTH // 2 - 30 for i in range(NUM_LANES)]

def create_enemy():
    x = random.choice(LANES_X)
    y = -120
    speed = random.randint(4, 7)
    return {'pos': [x, y], 'speed': speed}

def create_bonus():
    x = random.randint(ROAD_LEFT_BOUND, ROAD_RIGHT_BOUND - 40)
    y = random.randint(ROAD_TOP_BOUND, ROAD_BOTTOM_BOUND - 40)
    direction = random.choice([-1, 1])
    speed = random.randint(2, 4)
    return {'pos': [x, y], 'dir': direction, 'speed': speed}

def rects_collision_with_horizontal_buffer(rect1, rect2, horizontal_buffer=10):
    reduced_rect1 = pygame.Rect(
        rect1.left + horizontal_buffer // 2,
        rect1.top,
        rect1.width - horizontal_buffer,
        rect1.height
    )
    return reduced_rect1.colliderect(rect2)

# Ігрові змінні
enemies = [create_enemy() for _ in range(3)]
bonuses = [create_bonus() for _ in range(2)]
score = 0
font = pygame.font.SysFont(None, 40)
big_font = pygame.font.SysFont(None, 60)

def draw_text(text, x, y, color=(255, 255, 255), font_obj=None):
    if font_obj is None:
        font_obj = font
    label = font_obj.render(text, True, color)
    SCREEN.blit(label, (x, y))

paused = False
game_over = False

def reset_game():
    global enemies, bonuses, player_x, player_y, score, game_over, paused
    enemies = [create_enemy() for _ in range(3)]
    bonuses = [create_bonus() for _ in range(2)]
    player_x = WIDTH // 2 - PLAYER_WIDTH // 2
    player_y = ROAD_BOTTOM_BOUND
    score = 0
    game_over = False
    paused = False
    print("🔄 Гра перезапущена!")

# Фон (скролінг)
bg_y1 = 0
bg_y2 = -HEIGHT
bg_speed = 5

# Початкова позиція гравця
player_x = WIDTH // 2 - PLAYER_WIDTH // 2
player_y = ROAD_BOTTOM_BOUND

print("🎮 Гра запущена! ESC - вихід, SPACE - пауза")

# Головний цикл
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                print("👋 Вихід з гри")
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_SPACE and not game_over:
                paused = not paused
                print("⏸️ Пауза" if paused else "▶️ Продовження")
            if event.key == pygame.K_RETURN and game_over:
                reset_game()

    # ЗАВЖДИ малюємо фон (навіть на паузі!)
    bg_y1 += bg_speed if not paused and not game_over else 0
    bg_y2 += bg_speed if not paused and not game_over else 0
    
    SCREEN.blit(road_img, (0, bg_y1))
    SCREEN.blit(road_img, (0, bg_y2))
    
    if bg_y1 >= HEIGHT:
        bg_y1 = bg_y2 - HEIGHT
    if bg_y2 >= HEIGHT:
        bg_y2 = bg_y1 - HEIGHT

    if not paused and not game_over:
        # Керування
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > ROAD_LEFT_BOUND:
            player_x -= player_speed_x
        if keys[pygame.K_RIGHT] and player_x < ROAD_RIGHT_BOUND - PLAYER_WIDTH:
            player_x += player_speed_x
        if keys[pygame.K_UP] and player_y > ROAD_TOP_BOUND:
            player_y -= player_speed_y
        if keys[pygame.K_DOWN] and player_y < ROAD_BOTTOM_BOUND:
            player_y += player_speed_y

        player_rect = pygame.Rect(player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT)

        # Оновлення ворогів
        for i, enemy in enumerate(enemies):
            enemy['pos'][1] += enemy['speed']
            if enemy['pos'][1] > HEIGHT:
                enemies[i] = create_enemy()  # ✅ ВИПРАВЛЕНО

            enemy_rect = pygame.Rect(enemy['pos'][0], enemy['pos'][1], 60, 120)

            if rects_collision_with_horizontal_buffer(player_rect, enemy_rect, horizontal_buffer=10):
                game_over = True
                print(f"💥 Зіткнення! Фінальний рахунок: {score}")

        # Оновлення бонусів
        for i, bonus in enumerate(bonuses):
            bonus['pos'][0] += bonus['dir'] * bonus['speed']
            if bonus['pos'][0] < ROAD_LEFT_BOUND or bonus['pos'][0] > ROAD_RIGHT_BOUND - 40:
                bonus['dir'] *= -1

            bonus_rect = pygame.Rect(bonus['pos'][0], bonus['pos'][1], 40, 40)

            if bonus_rect.colliderect(player_rect):
                score += 10
                bonuses[i] = create_bonus()  # ✅ ВИПРАВЛЕНО
                print(f"⭐ Бонус! Рахунок: {score}")

    # Малювання об'єктів (завжди!)
    SCREEN.blit(player_car, (player_x, player_y))
    
    for enemy in enemies:
        SCREEN.blit(enemy_car_img, enemy['pos'])
    
    for bonus in bonuses:
        SCREEN.blit(bonus_img, bonus['pos'])

    # HUD
    draw_text(f"⭐ Очки: {score}", 30, 30, (255, 215, 0))

    # Overlay для пауз
    if paused:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        SCREEN.blit(overlay, (0, 0))
        
        draw_text("⏸️ ПАУЗА", WIDTH // 2 - 100, HEIGHT // 2 - 60, (255, 255, 0), big_font)
        draw_text("Натисніть ПРОБІЛ для продовження", WIDTH // 2 - 250, HEIGHT // 2 + 20, (255, 255, 255))
    
    elif game_over:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        SCREEN.blit(overlay, (0, 0))
        
        draw_text("💥 GAME OVER 💥", WIDTH // 2 - 180, HEIGHT // 2 - 80, (255, 0, 0), big_font)
        draw_text(f"Ваш рахунок: {score}", WIDTH // 2 - 120, HEIGHT // 2 - 10, (255, 215, 0))
        draw_text("Натисніть ENTER для початку заново", WIDTH // 2 - 240, HEIGHT // 2 + 50, (255, 255, 255))
        draw_text("або ESC для виходу", WIDTH // 2 - 140, HEIGHT // 2 + 90, (200, 200, 200))

    pygame.display.update()
    clock.tick(60)






