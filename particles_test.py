import pygame
import random

# Инициализация Pygame
pygame.init()
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Определение класса частицы
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
        self.size -= 0.1  # Уменьшаем размер
        self.life -= 0.1  # Уменьшаем жизнь

    def draw(self, screen):
        if self.life > 0 and self.size > 0:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.size))

# Хранение частиц
particles = []

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Добавление новых частиц
    if random.random() < 0.5:  # Небольшой шанс создать новую частицу
        particles.append(Particle(screen_width // 2, screen_height // 2))
    
    # Обновление частиц
    for particle in particles[:]:
        particle.update()
        if particle.life <= 0 or particle.size <= 0:
            particles.remove(particle)
    
    # Очистка экрана и рисование частиц
    screen.fill((0, 0, 0))
    for particle in particles:
        particle.draw(screen)
    
    pygame.display.flip()

pygame.quit()
