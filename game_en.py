import pygame
import random
import math

pygame.init()

display_info = pygame.display.Info()
screen_width = display_info.current_w
screen_height = display_info.current_h

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Lexicant, the word wizzard.")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

background_image = pygame.image.load("src/background.png")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
screen_width = display_info.current_w
screen_height = display_info.current_h

background_image_original = pygame.image.load("src/background.png")
original_width, original_height = background_image_original.get_size()
scale_factor = screen_height / original_height
new_width = int(original_width * scale_factor)

background_image = pygame.transform.scale(background_image_original, (new_width, screen_height))

x_pos = 0

player_width = 240
player_height = 240
player_x = 85
player_y = screen_height - player_height - 250
player = pygame.Rect(player_x, player_y, player_width, player_height)
player_health = 3
player_score = 0
levitation_range = 10
levitation_speed = 0.03
levitation_angle = 0

pygame_events = [
    pygame.QUIT,
    pygame.KEYDOWN,
    pygame.MOUSEBUTTONDOWN
]
pygame.event.set_allowed(pygame_events)


platform_height = 175
platform = pygame.Rect(0, screen_height - platform_height, screen_width, platform_height)

max_flying_monster_height = screen_height - player_height - 300

monsters = []
particles = []

with open('src/summary_en.txt', encoding='utf-8') as words:
    words_to_use = words.readlines()

font = pygame.font.Font('src/EpilepsySans.ttf', 36)

monster_images = {
    "wisp": pygame.transform.scale(pygame.image.load("src/wisp.png").convert_alpha(), (110, 110)),
    "slime": pygame.transform.scale(pygame.image.load("src/slime.png").convert_alpha(), (130, 130))
}

monster_images['ponasenkov'] = pygame.transform.scale(pygame.image.load("src/ponasenkov.png").convert_alpha(), (200, 363))

red_button = pygame.image.load('src/red_button.png')
red_button = pygame.transform.scale(red_button, (640//2,234//2))
full_heart_image = pygame.image.load("src/full_heart.png").convert_alpha()
full_heart_image = pygame.transform.scale(full_heart_image, (80, 80))

player_image = pygame.image.load("src/player.png")
player_image = pygame.transform.scale(player_image, (240, 240))

die_sound = pygame.mixer.Sound('src/die.wav')
shot_sound = pygame.mixer.Sound('src/shot.wav')
pygame.mixer.music.set_volume(1.1)
pygame.mixer.music.load('src/ponasenkov.wav')



class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(5, 10)
        self.life = random.randint(20, 50)
        self.color = (random.randint(200, 255), random.randint(100, 200), 0)
        self.x_vel = random.uniform(-1, 1)
        self.y_vel = random.uniform(-1, 1)

    def update(self):
        self.x += self.x_vel
        self.y += self.y_vel
        self.size -= 0.1
        self.life -= 0.1

    def draw(self, screen):
        if self.life > 0 and self.size > 0:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.size))


def create_monster():

    if any(m[2] == 'ponasenkov' for m in monsters):
        return

    monster_type = random.choice(["wisp", "slime"])
    monster_image = monster_images[monster_type]
    monster_width = monster_image.get_width()
    monster_height = monster_image.get_height()
    monster_x = screen_width
    word_length = 100
    
    monster_word = random.choice(words_to_use).replace('\n','')

    if len(monster_word) < 7 and 'ё' not in monster_word:
        if monster_type == "wisp":
            monster_y = random.randint(50, max_flying_monster_height)
        else:
            monster_y = screen_height - platform_height - monster_height + 35
            
        levitation_angle = 0 
        monster = pygame.Rect(monster_x, monster_y, monster_width, monster_height)
        base_y = monster_y
        monsters.append((monster, monster_word, monster_type, levitation_angle, base_y))
    else:
        create_monster()


def update_monsters():
    global player_health, monsters

    for i, (monster, word, monster_type, angle, base_y) in enumerate(monsters):
        if monster_type == 'ponasenkov':
            monster.x -= player_health
            if monster.x + monster.width < 0:
                player_health -= 1
                monster.x = screen_width
            if word == "":
                monsters.pop(i)
                continue
        else:
            monster.x -= 3*align_to_hard
            if monster.right < 0:
                monsters.pop(i)
                player_health -= 1
                break

        if monster_type == 'wisp':
            angle += 0.05
            levitation_range = 10
            monster.y = base_y + levitation_range * math.sin(angle)

        monsters[i] = (monster, word, monster_type, angle, base_y)


def update_player():
    global player

    if player.colliderect(platform):
        player.bottom = platform.top


def create_particles(x, y):
    for _ in range(20):
        particles.append(Particle(x, y))


def game_over():
    game_over_text = font.render("You've been ponasenkoved :(", True, RED)
    try_again_button = pygame.Rect(screen_width // 2 - 320 // 2, screen_height // 2, 320, 117)
    try_again_text = font.render("Try again!", True, WHITE)
    score = font.render(f"Your final score: {player_score}", True, GREEN)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if try_again_button.collidepoint(event.pos):
                    running = False

        screen.blit(background_image, (0, 0))
        screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - 200))
        screen.blit(red_button, (screen_width // 2 - 320 // 2, screen_height // 2))
        screen.blit(try_again_text, (try_again_button.centerx - try_again_text.get_width() // 2, try_again_button.centery - try_again_text.get_height() // 2))
        screen.blit(score, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - 150))

        pygame.display.flip()

    main()


def reset_game():
    global player_health, player_score, x_pos, monsters, boss_appeared, align_to_hard

    player_health = 3
    player_score = 0
    x_pos = 0
    boss_appeared = False
    align_to_hard = 1

    monsters = []


def show_menu():
    title_text = font.render("Lexicant - the word cat", True, BLACK)
    play_button = pygame.Rect(0, 0, 200, 80)
    
    play_button.center = (screen_width // 2, screen_height // 2 + 50)
    
    running = True
    while running:
        screen.blit(background_image, (0,0))
        
        title_x = screen_width // 2 - title_text.get_width() // 2
        title_y = screen_height // 2 - 100
        screen.blit(title_text, (title_x, title_y))
        
        play_text = font.render("Play", True, WHITE)
        screen.blit(red_button, (title_x, title_y+105))       
        screen.blit(play_text, (play_button.centerx - play_text.get_width() // 2, play_button.centery - play_text.get_height() // 2))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    running = False

        pygame.display.flip()


def main():
    global player_health, player_score, x_pos, levitation_angle, boss_killed, align_to_hard

    reset_game()
    show_menu()
    player_health = 3
    boss_appeared = False
    monster_timer = 0
    user_input = ""
    clock = pygame.time.Clock()
    boss_appeared = False
    boss_phrase = "never gonna give you up never gonna let you down never gonna run around and desert you never gonna make you cry never gonna say goodbye never gonna tell a lie and hurt you".split()
    current_boss_word_index = 0
    boss_killed = False
    running = True
    
    while running:
        align_to_hard = float(player_score/50000)+1
        image_width = background_image.get_width()    
        screen.blit(background_image, (x_pos, 0))
        
        if x_pos < 0:
            screen.blit(background_image, (x_pos + image_width, 0))
        
        x_pos -= 2.2
        
        if -x_pos >= image_width:
            x_pos = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_SPACE) or (event.key == pygame.K_RETURN):
                    if boss_appeared and monsters[0][2] == 'ponasenkov' and not boss_killed:
                        boss, word, boss_type, angle, base_y = monsters[0]
                        if user_input.strip() == word:
                            current_boss_word_index += 1
                            if current_boss_word_index >= len(boss_phrase):
                                monsters.pop(0)
                                boss_appeared = False
                                user_input = ""
                                boss_killed = True
                            else:
                                if not boss_killed:
                                    monsters[0] = (boss, boss_phrase[current_boss_word_index], boss_type, angle, base_y)
                                    user_input = ""
                        else:
                            pass
                    else:
                        for i, (monster, word, monster_type, angle, base_y) in enumerate(monsters):
                            if word == user_input:
                                shot_sound.play()
                                create_particles(monster.x, monster.y)
                                monsters.pop(i)
                                player_score += 750
                                break
                        user_input = ""
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                elif event.key is pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                else:
                    if 'a' <= event.unicode <= 'z' or 'A' <= event.unicode <= 'Z':
                        user_input += event.unicode.lower()

        if player_score >= 10000 and not boss_appeared and not boss_killed:
            monsters.clear()
            pygame.mixer.music.set_volume(0.4)
            pygame.mixer.music.play()
            boss_x = screen_width - 200
            boss_y = screen_height // 2 - 100
            boss = pygame.Rect(boss_x, boss_y, 200, 200)
            monsters.append((boss, boss_phrase[current_boss_word_index], 'ponasenkov', 0, boss_y))
            boss_appeared = True

        
        monster_timer += 1
        if monster_timer >= 90:  
            create_monster()
            monster_timer = 0 

        update_player()
        update_monsters()
        
        levitation_angle += levitation_speed
        levitation_offset = levitation_range * math.sin(levitation_angle)
        player.y = player_y + levitation_offset

        for particle in particles[:]:
            particle.update()
            if particle.life <= 0:
                particles.remove(particle)

        for particle in particles:
            particle.draw(screen)

        screen.blit(player_image, player)
        for monster, word, monster_type, angle, base_y in monsters:
            screen.blit(monster_images[monster_type], (monster.x, monster.y))
            word_text = font.render(word, True, BLACK)
            screen.blit(word_text, (monster.centerx - word_text.get_width() // 2, monster.y - word_text.get_height() - 10))

        print(player_health)
        if player_health == 0:
            game_over()

        for i in range(player_health):
            screen.blit(full_heart_image, (10 + i * 90, 10))

        score_text = font.render(f"Score -  {player_score}", True, BLACK)
        screen.blit(score_text, (10, 100))

        input_text = font.render(user_input, True, BLACK)
        screen.blit(input_text, (75, player.y-36))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


main()
pygame.quit()