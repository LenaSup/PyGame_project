import pygame
import sys
import os
import random


def load_image(neme, color_key=None):   # ---
    fullname = os.path.join('data', neme)

    try:
        image = pygame.image.load(fullname)
    except pygame.error as massage:
        raise SystemExit(massage)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
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

    def start_menu_display(self):
        runnind = True
        while runnind:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    runnind = False
            pass


def main():
    pygame.init()
    size = width, height = 1280, 720
    screen = pygame.display.set_mode(size)
    pass


if __name__ == '__main__':
    main()