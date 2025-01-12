import os
import sys
import random
import pygame

# Изображение не получится загрузить
# без предварительной инициализации pygame
pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


fps = 60
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
sprite = pygame.sprite.Sprite()
sprite.image = load_image("yl2.png")
sprite.rect = sprite.image.get_rect()
all_sprites.add(sprite)
sprite.rect.y = 350


class Landing(pygame.sprite.Sprite):
    image = load_image("bullet (1).png")

    def __init__(self, pos):
        super().__init__(all_sprites)
        self.image = Landing.image
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self):
        # если ещё в небе
        # if not pygame.sprite.collide_mask(self, mountain):
        self.rect = self.rect.move(0, -10)


running = True
right = False
left = False
while running:
    if right:
        if sprite.rect.x < width - 120:
            sprite.rect.x += 10
    if left:
        if sprite.rect.x > -30:
            sprite.rect.x -= 10

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
            Landing((sprite.rect.x + 64, sprite.rect.y + 30))
    screen.fill((255, 255, 255))
    all_sprites.draw(screen)
    all_sprites.update()
    clock.tick(fps)
    pygame.display.flip()
pygame.quit()
