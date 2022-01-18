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


class Inscription(pygame.sprite.Sprite):    # Декоротивная тобличка с назвением игры
    def __init__(self, group, size):
        super().__init__(group)
        pass


class AchievementBut(pygame.sprite.Sprite):     # Кнобка в меню
    def __init__(self, group, size):
        super().__init__(group)
        pass

    def click(self, pos):
        pass


class ExitBut(pygame.sprite.Sprite):    # Кнобка в меню
    def __init__(self, group, size):
        super().__init__(group)
        self.done = True
        pass

    def click(self, pos):
        self.done = False
        pass

    def close_start_menu(self):
        return self.done


class InfoBut(pygame.sprite.Sprite):    # Кнобка в меню
    def __init__(self, group, size):
        super().__init__(group)
        pass

    def click(self, pos):
        pass


class LearningBut(pygame.sprite.Sprite):    # Кнобка в меню
    def __init__(self, group, size):
        super().__init__(group)
        pass

    def click(self, pos):
        pass


class MenuClouds(pygame.sprite.Sprite):     # Облока в меню (облока в основкой игре меньше
    def __init__(self, group, size):        # и имеют другой диопозон кординат спавна)
        super().__init__(group)
        pass

    def update(self):
        pass


class StartMenu:    # стартовое меню
    def __init__(self, start_menu_sprites):
        self.start_menu_sprites = start_menu_sprites

    def start_menu_display(self, screen, size):
        done = True
        while done:
            background = pygame.transform.scale(load_image('start_menu_background.png'), size)
            screen.blit(background, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()  # Выхлд из игры
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    self.start_menu_sprites.click(pos)
                    done = self.start_menu_sprites.close_start_menu()   # Закрывает стартовое окно
            self.start_menu_sprites.draw(screen)                        # для выхода в меню выбора уровня
            pygame.display.flip()


def main():
    pygame.init()
    size = width, height = 1280, 720
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('First board')
    # ----  Дополненая часть к прописаному мэйно(до игрового цикла)
    start_menu_sprites = pygame.sprite.Group()  # Эта група спрайтов отображаемых в стартовом меню
    start_menu = StartMenu(start_menu_sprites)    # Создание обекта стартового миню
    start_menu.start_menu_display(screen, size)   # Вывод меню при включение
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