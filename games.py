import pygame
import os
import sys
import random

pygame.init()
size = width, height = 1000, 1000
screen = pygame.display.set_mode(size)
fps = 60
clock = pygame.time.Clock()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Landing(pygame.sprite.Sprite):
    image = load_image("r1.png")

    def __init__(self):
        super().__init__(all_sprites)
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


all_sprites = pygame.sprite.Group()
sprite = pygame.sprite.Sprite()
sprite.image = load_image("r1.png")
sprite.rect = sprite.image.get_rect()
all_sprites.add(sprite)
SPAWN = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN, 800)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == SPAWN:
            Landing()
    screen.fill('white')
    all_sprites.draw(screen)
    all_sprites.update()
    clock.tick(fps)
    pygame.display.flip()
