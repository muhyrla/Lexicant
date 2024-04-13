import pygame
import random
from wonderwords import RandomWord

r = RandomWord()
pygame.init()

display_info = pygame.display.Info()
screen_width = display_info.current_w
screen_height = display_info.current_h

screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Lexicant, the word wizzard.")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Загрузка и масштабирование фонового изображения
background_image = pygame.image.load("src/background.png")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Создание игрока
player_width = 50
player_height = 150
player_x = 50
player_y = screen_height - player_height - 50
player = pygame.Rect(player_x, player_y, player_width, player_height)
player_speed = 5
player_jump_height = 200
is_jumping = False
player_health = 3
player_score = 0

# Здесь появиться оптимизация
pygame_events = [
    pygame.QUIT,
    pygame.KEYDOWN,
    pygame.MOUSEBUTTONDOWN
]
pygame.event.set_allowed(pygame_events)


# Создание платформы
platform_height = 50
platform = pygame.Rect(0, screen_height - platform_height, screen_width, platform_height)

# Списки для хранения сущностей
walking_monsters = []
flying_monsters = []
words_to_use = r.random_words(200)

# Загрузка шрифта
font = pygame.font.Font('src/8bitlim.ttf', 36)

# Загрузка изображений монстров
monster_images = {
    "banshee": pygame.transform.scale(pygame.image.load("src/banshee.png").convert_alpha(), (80, 80)),
    "slime": pygame.transform.scale(pygame.image.load("src/slime.png").convert_alpha(), (60, 60)),
    "skeleton": pygame.transform.scale(pygame.image.load("src/skeleton.png").convert_alpha(), (70, 70)),
    "fire_elemental": pygame.transform.scale(pygame.image.load("src/fire_elemental.png").convert_alpha(), (90, 90)),
    "ent": pygame.transform.scale(pygame.image.load("src/ent.png").convert_alpha(), (100, 100))
}

# Загрузка изображения сердца
full_heart_image = pygame.image.load("src/full_heart.png").convert_alpha()
full_heart_image = pygame.transform.scale(full_heart_image, (80, 80))  # Увеличение размера сердца

# Функция для создания монстров
def create_monster():
    monster_type = random.choice(list(monster_images.keys()))
    monster_image = monster_images[monster_type]
    monster_width = monster_image.get_width()
    monster_height = monster_image.get_height()
    monster_x = screen_width
    monster_word = random.choice(words_to_use)

    if monster_type in ["banshee", "fire_elemental"]:
        monster_y = random.randint(screen_height - platform_height - 150, screen_height - platform_height - 140) 
        monster = pygame.Rect(monster_x, monster_y, monster_width, monster_height)
        flying_monsters.append((monster, monster_word, monster_type))
    else:
        monster_y = screen_height - platform_height - 60
        monster = pygame.Rect(monster_x, monster_y, monster_width, monster_height)
        walking_monsters.append((monster, monster_word, monster_type))

# Функция для обновления позиции игрока
def update_player():
    global player, is_jumping

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.left > 0:
        player.x -= player_speed
    if keys[pygame.K_RIGHT] and player.right < screen_width:
        player.x += player_speed
    if keys[pygame.K_UP] and not is_jumping and player.bottom >= platform.top:
        is_jumping = True

    if is_jumping:
        player.y -= player_jump_height
        player_jump_height -= 1
        if player_jump_height < -20:
            player_jump_height = 20
            is_jumping = False

    if player.colliderect(platform):
        player.bottom = platform.top


def update_monsters():
    for monster, word, monster_type in walking_monsters:
        monster.x -= 5
        if monster.right < 0:
            walking_monsters.remove((monster, word, monster_type))

    for monster, word, monster_type in flying_monsters:
        monster.x -= 3
        if monster.right < 0:
            flying_monsters.remove((monster, word, monster_type))


def check_collision():
    global player_health, player_score

    for monster, word, monster_type in walking_monsters:
        if player.colliderect(monster):
            player_health -= 1
            walking_monsters.remove((monster, word, monster_type))
            if player_health <= 0:
                game_over()

    for monster, word, monster_type in flying_monsters:
        if player.colliderect(monster):
            player_health -= 1
            flying_monsters.remove((monster, word, monster_type))
            if player_health <= 0:
                game_over()


def game_over():
    game_over_text = font.render("You failed", True, RED)
    try_again_button = pygame.Rect(0, 0, 200, 80)
    try_again_button.center = (screen_width // 2, screen_height // 2 + 50)

    running = True
    while running:
        screen.fill(BLACK)
        screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - 50))
        pygame.draw.rect(screen, GREEN, try_again_button)
        try_again_text = font.render("Try Again", True, WHITE)
        screen.blit(try_again_text, (try_again_button.centerx - try_again_text.get_width() // 2, try_again_button.centery - try_again_text.get_height() // 2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

def show_menu():
    title_text = font.render("Lexicant, the Word Wizard", True, WHITE)
    play_button = pygame.Rect(0, 0, 200, 80)
    play_button.center = (480, 480)

    running = True
    while running:
        screen.fill(BLACK)
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, screen_height // 2 - 100))
        pygame.draw.rect(screen, GREEN, play_button)
        play_text = font.render("Play", True, WHITE)
        screen.blit(play_text, (play_button.centerx - play_text.get_width() // 2, play_button.centery - play_text.get_height() // 2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    running = False

        pygame.display.flip()


def main():
    global player_health, player_score

    show_menu()

    monster_timer = 0
    user_input = ""
    clock = pygame.time.Clock()

    running = True
    while running:
        screen.blit(background_image, (0, 0))
        pygame.draw.rect(screen, GREEN, platform)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    for monster, word, monster_type in walking_monsters:
                        if word == user_input:
                            walking_monsters.remove((monster, word, monster_type))
                            player_score += 500
                            break
                    for monster, word, monster_type in flying_monsters:
                        if word == user_input:
                            flying_monsters.remove((monster, word, monster_type))
                            player_score += 500
                            break
                    user_input = ""
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                else:
                    if event.unicode.isalpha():
                        user_input += event.unicode.lower()

        monster_timer += 1
        if monster_timer == 120:
            monster_timer = 0
            create_monster()

        update_player()
        update_monsters()
        check_collision()

        pygame.draw.rect(screen, RED, player)
        for monster, word, monster_type in walking_monsters:
            screen.blit(monster_images[monster_type], (monster.x, monster.y))
            word_text = font.render(word, True, WHITE)
            screen.blit(word_text, (monster.centerx - word_text.get_width() // 2, monster.y - word_text.get_height() - 10))
        for monster, word, monster_type in flying_monsters:
            screen.blit(monster_images[monster_type], (monster.x, monster.y))
            word_text = font.render(word, True, WHITE)
            screen.blit(word_text, (monster.centerx - word_text.get_width() // 2, monster.y - word_text.get_height() - 10))

        for i in range(player_health):
            screen.blit(full_heart_image, (10 + i * 90, 10))

        score_text = font.render(f"Score: {player_score}", True, WHITE)
        screen.blit(score_text, (10, 100))

        input_text = font.render(user_input, True, WHITE)
        screen.blit(input_text, (50, screen_height - player_height - 87))
        pygame.display.flip()
        clock.tick(60)


main()
pygame.quit()