import pygame
import sys
import os
import random


def load_image(neme, color_key=None):   # Вся графика хронится в папке graphics
    fullname = os.path.join('graphics', neme)   # Все png с прозрачным фоном, кроме задних планов

    try:
        image = pygame.image.load(fullname)
    except pygame.error as massage:
        raise SystemExit(massage)
    image = image.convert_alpha()
    return image


class AchievementBut(pygame.sprite.Sprite):
    def __init__(self, group, size):
        super().__init__(group)
        pass


class ExitBut(pygame.sprite.Sprite):
    def __init__(self, group, size):
        super().__init__(group)
        pass


class InfoBut(pygame.sprite.Sprite):
    def __init__(self, group, size):
        super().__init__(group)
        pass


class LearningBut(pygame.sprite.Sprite):
    def __init__(self, group, size):
        super().__init__(group)
        pass


class MenuClouds(pygame.sprite.Sprite):
    def __init__(self, group, size):
        super().__init__(group)
        pass


class StartMenu:    # стартовое меню
    def __init__(self, start_menu_sprites, size):
        self.start_menu_sprites = start_menu_sprites
        pass

    def start_menu_display(self, screen):
        while True:
            screen.blit(load_image('start_menu_background.png'), (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            self.start_menu_sprites.draw(screen)
            pygame.display.flip()


def main():
    pygame.init()
    size = width, height = 1280, 720
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('First board')
    # ----
    start_menu_sprites = pygame.sprite.Group()
    start_menu = StartMenu(start_menu_sprites, size)    # Создание обекта стартового миню
    start_menu.start_menu_display(screen)   # Вывод меню при включение (до основного цикла игры)
    # ----
    running = True
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()
    pass


if __name__ == '__main__':
    main()