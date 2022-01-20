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


class CloseBut(pygame.sprite.Sprite):   # -
    pass


class Inscription(pygame.sprite.Sprite):    # Декоротивная тобличка с назвением игры
    def __init__(self, group, size):
        super().__init__(group)
        pass


class AchievementBut(pygame.sprite.Sprite):     # Кнобка в меню
    def __init__(self, group, size, screen):
        super().__init__(group)
        self.image = load_image('achievement_button.png')
        self.image = pygame.transform.scale(self.image, ((size[0] // 320) * 27, (size[1] // 180) * 27))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = (size[0] // 320) * 7, (size[1] // 180) * 41
        self.size = size

    def click(self, pos, screen):
        if self.rect.collidepoint(pos):
            achievement = Achievement()
            achievement.achievement_display(screen, self.size)


class ExitBut(pygame.sprite.Sprite):    # Кнобка в меню
    def __init__(self, group, size):
        super().__init__(group)
        self.image = load_image('exit_button.png')
        self.image = pygame.transform.scale(self.image, ((size[0] // 320) * 27, (size[1] // 180) * 27))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = (size[0] // 320) * 286, (size[1] // 180) * 7
        self.size = size

    def click(self, pos, screen):
        if self.rect.collidepoint(pos):
            sys.exit()


class InfoBut(pygame.sprite.Sprite):    # Кнобка в меню
    def __init__(self, group, size):
        super().__init__(group)
        pass

    def click(self, pos, screen):
        pass


class PlayBut(pygame.sprite.Sprite):
    pass


class LearningBut(pygame.sprite.Sprite):    # Кнобка в меню

    def __init__(self, group, size, screen):
        super().__init__(group)
        self.image = load_image('learning_button.png')
        self.image = pygame.transform.scale(self.image, ((size[0] // 320) * 27, (size[1] // 180) * 27))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = (size[0] // 320) * 7, (size[1] // 180) * 7
        self.size = size

    def click(self, pos, screen):
        if self.rect.collidepoint(pos):
            learning = Education()
            learning.education_display(screen, self.size)


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
            self.start_menu_sprites.draw(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()  # Выхлд из игры
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for i in self.start_menu_sprites:
                        i.click(pos, screen)
            pygame.display.flip()


class Education:    # Окно обучения
    def __init__(self):
        pass

    def education_display(self, screen, size):
        done = True
        while done:
            background = pygame.transform.scale(load_image('empty_field.png'), size)
            screen.blit(background, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            pygame.display.flip()


class Achievement:    # Меню очевок
    def __init__(self):
        pass

    def achievement_display(self, screen, size):
        done = True
        while done:
            background = pygame.transform.scale(load_image('empty_field.png'), size)
            screen.blit(background, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            pygame.display.flip()


def main():
    pygame.init()
    size = width, height = 1280, 720
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('First board')
    # ----  Дополненая часть к прописаному мэйно(до игрового цикла)
    start_menu_sprites = pygame.sprite.Group()  # Эта група спрайтов отображаемых в стартовом меню
    achievement_but = AchievementBut(start_menu_sprites, size, screen)
    learning_but = LearningBut(start_menu_sprites, size, screen)
    exit_but = ExitBut(start_menu_sprites, size)
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