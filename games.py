import os
import sys
import random
import pygame
from button import ImageButton

# Изображение не получится загрузить
# без предварительной инициализации pygame
pygame.init()
size = width, height = 1000, 1000
screen = pygame.display.set_mode(size)
fps = 60
clock = pygame.time.Clock()
health_array = ['0.png', '1.png', '2.png', '3.png']
play_button = ImageButton(width / 2 - (400 / 2), 200, 400, 150, "PLAY",
                          "data\\green_button.png", "data\\green_button_hover2.png")
diff_button = ImageButton(width / 2 - (400 / 2), 400, 400, 150, "DIFFICULTY",
                          "data\\green_button.png", "data\\green_button_hover2.png")
quit_button = ImageButton(width / 2 - (400 / 2), 600, 400, 150, "QUIT",
                          "data\\green_button.png", "data\\green_button_hover2.png")

easy_button = ImageButton(width / 2 - (400 / 2), 200, 400, 150, "EASY",
                          "data\\green_button.png", "data\\green_button_hover2.png")
normal_button = ImageButton(width / 2 - (400 / 2), 400, 400, 150, "NORMAL",
                            "data\\green_button.png", "data\\green_button_hover2.png")
hard_button = ImageButton(width / 2 - (400 / 2), 600, 400, 150, "HARD",
                          "data\\green_button.png", "data\\green_button_hover2.png")


def main_game(spawn_rate):
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
    GOG = pygame.sprite.Group()
    bomb_group = pygame.sprite.Group()
    SPAWN = pygame.USEREVENT + 1
    pygame.time.set_timer(SPAWN, spawn_rate)

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

    class Health(pygame.sprite.Sprite):
        health = 3
        image = load_image(health_array[health])

        def __init__(self, health=health):
            super().__init__(all_sprites)
            self.add(all_sprites)
            self.image = Health.image
            self.health = health
            self.rect = self.image.get_rect()

        def Hurt(self):
            self.health -= 1
            self.image = load_image(health_array[self.health])
            if self.health == 0:
                hp.GameOver()

        def GameOver(self):
            global running
            running = False
            spritee = pygame.sprite.Sprite(GOG)
            spritee.image = load_image("gameover.png")
            spritee.rect = sprite.image.get_rect()
            GOG.add(spritee)
            spritee.rect.x = -width
            dist = 250
            #
            ch = True
            while ch:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                        ch = False
                if spritee.rect.x <= -2.5:
                    spritee.rect.x += dist * clock.tick() / 100
                screen.fill((255, 255, 255))
                GOG.draw(screen)
                score.show_score(screen)
                pygame.display.flip()

    hp = Health()

    class Score(object):
        def __init__(self):
            self.black = 255, 165, 0
            self.count = 0
            self.font = pygame.font.SysFont("comicsans", 50, True, True)
            self.text = self.font.render("Score : " + str(self.count), True, self.black)

        def show_score(self, screen):
            screen.blit(self.text, (700, 0))

        def score_up(self):
            self.count += 1
            self.text = self.font.render("Score : " + str(self.count), True, self.black)

    score = Score()

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
                hp.Hurt()
                self.remove(bomb_group)
            if pygame.sprite.spritecollideany(self, bullet_group):
                self.remove(bomb_group)
                score.score_up()

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
        score.show_score(screen)
        clock.tick(fps)

        pygame.display.flip()


def main_menu():
    running_2 = True
    while running_2:
        screen.fill((255, 255, 255))

        font = pygame.font.Font(None, 72)
        txt_surface = font.render("ZOV BOMB", True, (0, 0, 0))
        txt_rect = txt_surface.get_rect(center=(500, 100))
        screen.blit(txt_surface, txt_rect)
        for event2 in pygame.event.get():
            if event2.type == pygame.QUIT:
                running_2 = False
                pygame.quit()
                sys.exit()

            if event2.type == pygame.USEREVENT and event2.button == play_button:
                main_game(800)
                running_2 = False
            if event2.type == pygame.USEREVENT and event2.button == diff_button:
                diff()
                running_2 = False
            if event2.type == pygame.USEREVENT and event2.button == quit_button:
                running_2 = False
                pygame.quit()
                sys.exit()

            play_button.handle_event(event2)
            diff_button.handle_event(event2)
            quit_button.handle_event(event2)

        play_button.check_hover(pygame.mouse.get_pos())
        play_button.draw(screen)
        diff_button.check_hover(pygame.mouse.get_pos())
        diff_button.draw(screen)
        quit_button.check_hover(pygame.mouse.get_pos())
        quit_button.draw(screen)
        pygame.display.flip()


def diff():
    running_2 = True
    while running_2:
        screen.fill((255, 255, 255))

        font = pygame.font.Font(None, 72)
        txt_surface = font.render("DIFFICULTY", True, (0, 0, 0))
        txt_rect = txt_surface.get_rect(center=(500, 100))
        screen.blit(txt_surface, txt_rect)
        for event2 in pygame.event.get():
            if event2.type == pygame.QUIT:
                running_2 = False
                pygame.quit()
                sys.exit()

            if event2.type == pygame.USEREVENT and event2.button == easy_button:
                main_game(800)
                running_2 = False
            if event2.type == pygame.USEREVENT and event2.button == normal_button:
                main_game(400)
                running_2 = False

            if event2.type == pygame.USEREVENT and event2.button == hard_button:
                main_game(200)
                running_2 = False

            easy_button.handle_event(event2)
            normal_button.handle_event(event2)
            hard_button.handle_event(event2)

        easy_button.check_hover(pygame.mouse.get_pos())
        easy_button.draw(screen)
        normal_button.check_hover(pygame.mouse.get_pos())
        normal_button.draw(screen)
        hard_button.check_hover(pygame.mouse.get_pos())
        hard_button.draw(screen)
        pygame.display.flip()


if __name__ == "__main__":
    main_menu()
