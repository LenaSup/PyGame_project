import pygame
import sys
import os
import random
# 731836


def load_image(neme, color_key=None):   # Вся графика хронится в папке graphics
    fullname = os.path.join('graphics', neme)   # Все png с прозрачным фоном, кроме задних планов

    try:
        image = pygame.image.load(fullname)
    except pygame.error as massage:
        raise SystemExit(massage)
    image = image.convert_alpha()
    return image
#2313

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
        self.image = load_image('info_button.png')
        self.image = pygame.transform.scale(self.image, ((size[0] // 320) * 17, (size[1] // 180) * 17))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = (size[0] // 320) * 7, (size[1] // 180) * 75
        self.size = size

    def click(self, pos, screen):
        pass


class PlayBut(pygame.sprite.Sprite):
    def __init__(self, group, size, start_menu):
        super().__init__(group)
        self.start_menu = start_menu
        self.image = load_image('play_button.png')
        self.image = pygame.transform.scale(self.image, ((size[0] // 320) * 120, (size[1] // 180) * 57))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = (size[0] // 320) * 100, (size[1] // 180) * 110
        self.size = size
        self.map_ = 0

    def click(self, pos, screen):
        if self.rect.collidepoint(pos):
            levels = Levels()
            levels.levels_display(screen, self.size)
            self.map_ = levels.selected()
            self.start_menu.close()

    def map(self):
        return self.map_


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


class CrossBtn(pygame.sprite.Sprite):
    def __init__(self, size):
        super().__init__()
        pass


class ArrowBtnLeft():
    def __init__(self, size):
        super().__init__()
        pass


class ArrowBtnRight():
    def __init__(self, size):
        super().__init__()
        pass


class StartMenu:    # стартовое меню
    def __init__(self, start_menu_sprites):
        self.start_menu_sprites = start_menu_sprites
        self.done = True

    def start_menu_display(self, screen, size):
        fps = 60
        clock = pygame.time.Clock()
        background = pygame.transform.scale(load_image('start_menu_background.png'), size)
        while self.done:
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
            clock.tick(fps)

    def close(self):
        self.done = False


class Education:    # Окно обучения
    def __init__(self):
        pass

    def education_display(self, screen, size):
        done = True
        fps = 60
        clock = pygame.time.Clock()
        background = pygame.transform.scale(load_image('empty_field.png'), size)
        while done:
            screen.blit(background, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            pygame.display.flip()
            clock.tick(fps)


class Achievement:    # Меню очевок
    def __init__(self):
        pass

    def achievement_display(self, screen, size):
        done = True
        fps = 60
        clock = pygame.time.Clock()
        background = pygame.transform.scale(load_image('empty_field.png'), size)
        while done:
            screen.blit(background, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            pygame.display.flip()
            clock.tick(fps)


class Info():
    pass


class Levels():
    def __init__(self):
        self.selected_map = 0

    def levels_display(self, screen, size):
        done = True
        fps = 60
        clock = pygame.time.Clock()
        f = pygame.font.Font('7X7PixelizedRegular.ttf', 50)
        level_1 = f.render('уровень 1', False, (0, 0, 0))
        level_2 = f.render('уровень 2', False, (0, 0, 0))
        level_3 = f.render('уровень 3', False, (0, 0, 0))
        level_4 = f.render('уровень 4', False, (0, 0, 0))
        level_5 = f.render('уровень 5', False, (0, 0, 0))
        levels = [level_1, level_2, level_3, level_4, level_5]
        coord = [((size[0] // 320) * 41, (size[1] // 180) * (33 + i * 22)) for i in range(5)]
        background = pygame.transform.scale(load_image('empty_field.png'), size)
        while done:
            screen.blit(background, (0, 0))
            for i in range(5):
                screen.blit(levels[i], coord[i])
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if pos[0] in range(coord[0][0], coord[0][0] + levels[0].get_width())\
                            and pos[1] in range(coord[0][1], coord[0][1] + levels[0].get_height()):
                        self.selected_map = 1
                        done = False
                    if pos[0] in range(coord[1][0], coord[1][0] + levels[1].get_width())\
                            and pos[1] in range(coord[1][1], coord[1][1] + levels[1].get_height()):
                        self.selected_map = 2
                        done = False
                    if pos[0] in range(coord[2][0], coord[2][0] + levels[2].get_width())\
                            and pos[1] in range(coord[2][1], coord[2][1] + levels[2].get_height()):
                        self.selected_map = 3
                        done = False
                    if pos[0] in range(coord[3][0], coord[3][0] + levels[3].get_width())\
                            and pos[1] in range(coord[3][1], coord[3][1] + levels[3].get_height()):
                        self.selected_map = 4
                        done = False
                    if pos[0] in range(coord[4][0], coord[4][0] + levels[4].get_width())\
                            and pos[1] in range(coord[4][1], coord[4][1] + levels[4].get_height()):
                        self.selected_map = 5
                        done = False
            pygame.display.flip()
            clock.tick(fps)

    def selected(self):
        return self.selected_map


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
    info_btn = InfoBut(start_menu_sprites, size)
    start_menu = StartMenu(start_menu_sprites)  # Создание обекта стартового миню
    play_but = PlayBut(start_menu_sprites, size, start_menu)
    start_menu.start_menu_display(screen, size)   # Вывод меню при включение
    map_ = play_but.map()   # номер карты
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