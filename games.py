import pygame
import os
import sys
import random
import asyncio

pygame.init()
size = width, height = 1000, 1000
screen = pygame.display.set_mode(size)
fps = 60
clock = pygame.time.Clock()
health = 3
health_array = ['0.png', '1.png', '2.png', '3.png']


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


all_sprites = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
bomb_group = pygame.sprite.Group()
SPAWN = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN, 800)

sprite = pygame.sprite.Sprite()
sprite.image = load_image("fon.png")
sprite.rect = sprite.image.get_rect()
all_sprites.add(sprite)
sprite.rect.x = -1

sprite2 = pygame.sprite.Sprite()
sprite2.image = load_image("yl2.png")
sprite2.rect = sprite2.image.get_rect()
all_sprites.add(sprite2)
sprite2.rect.y = height - 200


class Landing(pygame.sprite.Sprite):
    image = load_image("r1.png")

    def __init__(self):
        super().__init__(bomb_group)
        self.add(bomb_group)
        self.image = Landing.image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(width - 61)
        self.rect.y = 0
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        # если ещё в небе
        if self.rect.y < height - 85:
            self.rect = self.rect.move(0, 2)
        else:
            Health(health - 1)
            self.remove(bomb_group)
        if pygame.sprite.spritecollideany(self, bullet_group):
            self.image = load_image("boom.png")
            self.remove(bomb_group)


class Health(pygame.sprite.Sprite):
    image = load_image(health_array[health])

    def __init__(self, healtth):
        super().__init__(all_sprites)
        self.healtth = healtth
        self.k = 0
        self.rect = self.image.get_rect()
        self.image = load_image(health_array[self.healtth - self.k])
        self.k -= 1


class Bullet(pygame.sprite.Sprite):
    image = load_image("bullet (1).png")

    def __init__(self, pos):
        super().__init__(bullet_group)
        self.add(bullet_group)
        self.image = Bullet.image
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self):
        # если ещё в небе
        self.rect = self.rect.move(0, -10)


running = True
right = False
left = False
while running:
    if right:
        if sprite2.rect.x < width - 120:
            sprite2.rect.x += 10
    if left:
        if sprite2.rect.x > -30:
            sprite2.rect.x -= 10
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                right = True
            if event.key == pygame.K_LEFT:
                left = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                right = False
            if event.key == pygame.K_LEFT:
                left = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            Bullet((sprite2.rect.x + 64, sprite2.rect.y + 30))
        if event.type == SPAWN:
            Landing()
    screen.fill('white')
    all_sprites.draw(screen)
    all_sprites.update()
    bullet_group.draw(screen)
    bullet_group.update()
    bomb_group.draw(screen)
    bomb_group.update()
    clock.tick(fps)

    pygame.display.flip()
