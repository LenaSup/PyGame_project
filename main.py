import pygame
import sys
import os
import random
import sqlite3
from entities import *


def load_image(neme):   # Вся графика хронится в папке graphics
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
        self.image = load_image('info_button.png')
        self.image = pygame.transform.scale(self.image, ((size[0] // 320) * 17, (size[1] // 180) * 17))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = (size[0] // 320) * 7, (size[1] // 180) * 75
        self.size = size

    def click(self, pos, screen):
        if self.rect.collidepoint(pos):
            info = Info()
            info.info_display(screen, self.size)


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


class MenuClouds(pygame.sprite.Sprite):     # Облока в меню
    def __init__(self, group, size):
        super().__init__(group)
        self.speed = random.randint(1, 2)
        self.direction = random.choice([1, -1])
        self.timer = 0
        print(self.direction, self.speed)
        f = 'start_menu_cloud_' + str(random.randint(1, 4)) + '.png'
        self.image = load_image(f)
        rect = self.image.get_rect().size
        self.image = pygame.transform.scale(self.image, ((size[0] // 320) * rect[0], (size[1] // 180) * rect[1]))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = (size[0] // 320) * random.randint(1, 250),\
                                        (size[1] // 180) * random.randint(1, 110)
        self.size = size

    def update(self):
        if self.timer == self.speed:
            self.timer = 0
            self.rect.left += self.direction
        else:
            self.timer += 1
        if self.rect.left > self.size[0] or self.rect.width + self.rect.left < 0:
            self.direction = -self.direction


class CrossBtn(pygame.sprite.Sprite):
    def __init__(self, size, group):
        super().__init__(group)
        self.image = load_image('x.png')
        rect = self.image.get_rect().size
        self.image = pygame.transform.scale(self.image, ((size[0] // 320) * rect[0], (size[1] // 180) * rect[1]))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = (size[0] // 320) * (287 - rect[0]), (size[1] // 180) * 30
        self.size = size

    def click(self, pos):
        if self.rect.collidepoint(pos):
            return False
        else:
            return True


class ArrowBtnLeft(pygame.sprite.Sprite):
    def __init__(self, size, group):
        super().__init__(group)
        self.image = load_image('arrow.png')
        rect = self.image.get_rect().size
        self.image = pygame.transform.scale(self.image, ((size[0] // 320) * rect[0], (size[1] // 180) * rect[1]))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = (size[0] // 320) * 34, (size[1] // 180) * 135
        self.size = size

    def click(self, pos):
        if self.rect.collidepoint(pos):
            return True
        else:
            return False


class ArrowBtnRight(pygame.sprite.Sprite):
    def __init__(self, size, group):
        super().__init__(group)
        self.image = pygame.transform.flip(load_image('arrow.png'), True, False)
        rect = self.image.get_rect().size
        self.image = pygame.transform.scale(self.image, ((size[0] // 320) * rect[0], (size[1] // 180) * rect[1]))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = (size[0] // 320) * 270, (size[1] // 180) * 135
        self.size = size

    def click(self, pos):
        if self.rect.collidepoint(pos):
            return True
        else:
            return False


class StartMenu:    # стартовое меню
    def __init__(self, start_menu_sprites):
        self.start_menu_sprites = start_menu_sprites
        self.done = True

    def start_menu_display(self, screen, size):
        clouds = pygame.sprite.Group()
        menu_clouds = []
        for i in range(random.randint(2, 3)):
            menu_clouds.append(MenuClouds(clouds, size))
        fps = 60
        clock = pygame.time.Clock()
        background = pygame.transform.scale(load_image('start_menu_background.png'), size)
        castle_defense = pygame.transform.scale(load_image('castle_defense.png'), ((size[0] // 320) * 164,
                                                                                   (size[1] // 180) * 93))
        while self.done:
            screen.blit(background, (0, 0))
            clouds.draw(screen)
            self.start_menu_sprites.draw(screen)
            clouds.update()
            screen.blit(castle_defense, ((size[0] // 320) * 76, (size[1] // 180) * 6))
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


class EndScreen:
    def __init__(self, win):
        if win:
            background = pygame.transform.scale(load_image('win.png'), size)
        else:
            background = pygame.transform.scale(load_image('game_over.png'), size)


class Education:    # Окно обучения
    def __init__(self):
        with open('education.txt', 'rt', encoding='UTF-8') as text:
            self.pages = text.read().split('\n---\n')
        self.number_page = 0
        self.f = pygame.font.Font('7X7PixelizedRegular.ttf', 32)

    def education_display(self, screen, size):
        done = True
        fps = 60
        clock = pygame.time.Clock()
        background = pygame.transform.scale(load_image('empty_field.png'), size)
        btn = pygame.sprite.Group()
        cross_btn = CrossBtn(size, btn)
        arrow_btn_right = ArrowBtnRight(size, btn)
        arrow_btn_left = ArrowBtnLeft(size, btn)
        while done:
            page = self.pages[self.number_page].split('\n')
            screen.blit(background, (0, 0))
            for i in range(len(page)):
                screen.blit(self.f.render(page[i], False, (0, 0, 0)), ((size[0] // 320) * 30,
                                                                       (size[1] // 180) * (30 + 13 * i)))
            btn.draw(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    done = cross_btn.click(pos)
                    if arrow_btn_right.click(pos) and self.number_page < len(self.pages) - 1:
                        self.number_page += 1
                    if arrow_btn_left.click(pos) and self.number_page != 0:
                        self.number_page -= 1
            pygame.display.flip()
            clock.tick(fps)


class Achievement:    # Меню очевок
    def __init__(self):
        con = sqlite3.connect('user_data.sqlite3')
        cur = con.cursor()
        self.f_1 = pygame.font.Font('7X7PixelizedRegular.ttf', 26)
        self.f_2 = pygame.font.Font('7X7PixelizedRegular.ttf', 22)
        enemies = list(map(lambda x: x[0],
                           cur.execute("""SELECT DISTINCT Meaning FROM statistic WHERE Id == 7""").fetchall()))[0]
        gold = list(map(lambda x: x[0],
                        cur.execute("""SELECT DISTINCT Meaning FROM statistic WHERE Id == 6""").fetchall()))[0]
        time1 = list(map(lambda x: x[0],
                         cur.execute("""SELECT DISTINCT Meaning FROM statistic WHERE Id == 1""").fetchall()))[0]
        time2 = list(map(lambda x: x[0],
                         cur.execute("""SELECT DISTINCT Meaning FROM statistic WHERE Id == 2""").fetchall()))[0]
        time3 = list(map(lambda x: x[0],
                         cur.execute("""SELECT DISTINCT Meaning FROM statistic WHERE Id == 3""").fetchall()))[0]
        time4 = list(map(lambda x: x[0],
                         cur.execute("""SELECT DISTINCT Meaning FROM statistic WHERE Id == 4""").fetchall()))[0]
        time5 = list(map(lambda x: x[0],
                         cur.execute("""SELECT DISTINCT Meaning FROM statistic WHERE Id == 5""").fetchall()))[0]
        data = [enemies, gold, time1, time2, time3, time4, time5]
        with open('achievement_text.txt', 'rt', encoding='UTF-8') as text:
            text = text.read().split('\n')
            for i in range(len(text) // 2):
                text[i * 2 + 1] = 'Ваш результат: ' + str(data[i])
        self.text = text
        con.close()

    def achievement_display(self, screen, size):
        done = True
        fps = 60
        clock = pygame.time.Clock()
        background = pygame.transform.scale(load_image('empty_field.png'), size)
        btn = pygame.sprite.Group()
        cross_btn = CrossBtn(size, btn)
        while done:
            screen.blit(background, (0, 0))
            btn.draw(screen)
            for i in range(len(self.text) // 2):
                screen.blit(self.f_1.render(self.text[i * 2], False, (0, 0, 0)), ((size[0] // 320) * 36,
                                                                       (size[1] // 180) * (27 + 17 * i)))
            for i in range(len(self.text) // 2):
                screen.blit(self.f_2.render(self.text[i * 2 + 1], False, (51, 51, 102)), ((size[0] // 320) * 36,
                                                                       (size[1] // 180) * (37 + 17 * i)))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    done = cross_btn.click(pos)
            pygame.display.flip()
            clock.tick(fps)


class Info():
    def __init__(self):
        pass

    def info_display(self, screen, size):
        done = True
        fps = 60
        clock = pygame.time.Clock()
        background = pygame.transform.scale(load_image('empty_field.png'), size)
        btn = pygame.sprite.Group()
        cross_btn = CrossBtn(size, btn)
        while done:
            screen.blit(background, (0, 0))
            btn.draw(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    done = cross_btn.click(pos)
            pygame.display.flip()
            clock.tick(fps)


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
                        self.selected_map = 0
                        done = False
                    if pos[0] in range(coord[1][0], coord[1][0] + levels[1].get_width())\
                            and pos[1] in range(coord[1][1], coord[1][1] + levels[1].get_height()):
                        self.selected_map = 1
                        done = False
                    if pos[0] in range(coord[2][0], coord[2][0] + levels[2].get_width())\
                            and pos[1] in range(coord[2][1], coord[2][1] + levels[2].get_height()):
                        self.selected_map = 2
                        done = False
                    if pos[0] in range(coord[3][0], coord[3][0] + levels[3].get_width())\
                            and pos[1] in range(coord[3][1], coord[3][1] + levels[3].get_height()):
                        self.selected_map = 3
                        done = False
                    if pos[0] in range(coord[4][0], coord[4][0] + levels[4].get_width())\
                            and pos[1] in range(coord[4][1], coord[4][1] + levels[4].get_height()):
                        self.selected_map = 4
                        done = False
            pygame.display.flip()
            clock.tick(fps)

    def selected(self):
        return self.selected_map


class Tower1Btn(pygame.sprite.Sprite):
    def __init__(self, group, size):
        super().__init__(group)
        self.type = 1
        self.image = load_image('tower1_button.png')
        rect = self.image.get_rect().size
        self.image = pygame.transform.scale(self.image, ((size[0] // 320) * rect[0], (size[1] // 180) * rect[1]))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = (size[0] // 320) * 242, (size[1] // 180) * 2
        self.size = size

    def update(self, pos):
        if self.rect.collidepoint(pos):
            return 1
        return 0


class Tower2Btn(pygame.sprite.Sprite):
    def __init__(self, group, size):
        super().__init__(group)
        self.type = 2
        self.image = load_image('tower2_button.png')
        rect = self.image.get_rect().size
        self.image = pygame.transform.scale(self.image, ((size[0] // 320) * rect[0], (size[1] // 180) * rect[1]))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = (size[0] // 320) * 268, (size[1] // 180) * 2
        self.size = size

    def update(self, pos):
        if self.rect.collidepoint(pos):
            return 2
        return 0


class Tower3Btn(pygame.sprite.Sprite):
    def __init__(self, group, size):
        super().__init__(group)
        self.type = 3
        self.image = load_image('tower3_button.png')
        rect = self.image.get_rect().size
        self.image = pygame.transform.scale(self.image, ((size[0] // 320) * rect[0], (size[1] // 180) * rect[1]))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = (size[0] // 320) * 294, (size[1] // 180) * 2
        self.size = size

    def update(self, pos):
        if self.rect.collidepoint(pos):
            return 3
        return 0


class UpgradeBtn(pygame.sprite.Sprite):
    def __init__(self, group, size):
        super().__init__(group)
        self.type = 3
        self.image = load_image('upgrade_button.png')
        rect = self.image.get_rect().size
        self.image = pygame.transform.scale(self.image, ((size[0] // 320) * rect[0], (size[1] // 180) * rect[1]))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = (size[0] // 320) * 216, (size[1] // 180) * 2
        self.size = size

    def update(self, pos):
        if self.rect.collidepoint(pos):
            return -1
        return 0


class Cell(pygame.sprite.Sprite):  # общий класс клетки
    def __init__(self, x, y, size, image=None):
        self.name = self.__class__.__name__
        self.size = size
        if image != None:
            self.image = pygame.transform.scale(image, (size, size))
            super().__init__(cells)
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = x, y

    def __str__(self):  # удобное преобразование в строку
        return self.name


class Road_cell(Cell):  # клетка дороги для мобов
    def __init__(self, x, y, size, image):
        super().__init__(x, y, size, image)


class Pass_cell(Cell):  # пустая клетка (декоративная)
    def __init__(self, x, y, size, image=None):
        super().__init__(x, y, size, image)


class Building_cell(Cell):  # клетка для стороительства башен
    def __init__(self, x, y, size, image, tower=None):
        super().__init__(x, y, size, image)
        self.tower = tower

    def set_tower(self, tower):  # установить башня в клетку
        self.tower = tower


class Enemy(pygame.sprite.Sprite):  # класс враждебного моба
    def __init__(self, x, y, health, image, cols, damage=10, price=10, speed=1, path=None):
        super().__init__(enemies)
        self.name = self.__class__.__name__
        # для анимаций
        number_of_frames = cols
        self.frames = self.cut_sheet(load_image(image), number_of_frames)
        self.cur_frame = 0
        self.pos = x, y
        self.health = health
        self.damage = damage
        self.speed = speed
        self.image = self.frames[self.cur_frame]
        self.price = price
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.rect.y, self.rect.x = self.rect.y - (self.rect.bottom - self.rect.y - 40), self.rect.x - \
                                   (self.rect.right - self.rect.x - 60)
        self.pos = self.rect.x, self.rect.y
        self.path = None
        self.current_step = None
        self.step = None
        self.steps = None
        self.is_move = True
        self.set_path(path)

    def load_step(self, index):  # загрузка следующего направления движения из пути
        self.step = self.path[index]
        if self.step[0] < 0 or self.step[1] < 0:
            self.speed = abs(self.speed) * -1
        else:
            self.speed = abs(self.speed)

    def move(self):  # передвижение врага по пути из файла
        if self.is_move:
            if self.rect.x + self.rect.width + self.speed >= width:
                self.is_move = False
                self.explosion()
            elif self.rect.y + self.rect.height + self.speed >= height:
                self.is_move = False
                self.explosion()
            else:
                if self.step[0] == 0:
                    if abs(self.step[1]) <= self.steps and self.current_step == len(self.path) - 1:
                        self.is_move = False
                        self.explosion()
                    elif abs(self.step[1]) <= self.steps:
                        self.steps = 0
                        self.current_step += 1
                        self.load_step(self.current_step)
                    else:
                        self.pos = self.pos[0], self.pos[1] + self.speed
                        self.steps += abs(self.speed)
                        self.rect.x, self.rect.y = self.pos[0], self.pos[1]
                else:
                    if abs(self.step[0]) <= self.steps and self.current_step == len(self.path) - 1:
                        self.is_move = False
                        self.explosion()
                    elif abs(self.step[0]) <= self.steps:
                        self.steps = 0
                        self.current_step += 1
                        self.load_step(self.current_step)
                    else:
                        self.pos = self.pos[0] + self.speed, self.pos[1]
                        self.steps += abs(self.speed)
                        self.rect.x, self.rect.y = self.pos[0], self.pos[1]

    def explosion(self):  # суицидальный взрыв при подходу к замку наносящий урон
        global castle_health
        castle_health -= self.damage
        print(castle_health)
        self.health = 0
        self.kill()

    def set_path(self, path):  # задать путь
        self.path = path
        self.current_step = 0
        self.steps = 0
        self.load_step(0)

    def get_damage(self, damage):  # получение урона от башни
        if self.health - damage <= 0:
            self.health = 0
            self.is_move = False
            global gold
            gold += self.price
            db.execute(f"UPDATE statistic SET Meaning = "
                       f"{db.execute(f'SELECT Meaning FROM statistic WHERE Id = 7').fetchone()[0] + 1} WHERE Id = 7")
            db.commit()
            self.kill()
        else:
            self.health -= damage

    def cut_sheet(self, sheet, columns, rows=1):    # разрезка кадров
        frames = []
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                image = sheet.subsurface(pygame.Rect(frame_location, self.rect.size))
                rect = image.get_rect().size
                image = pygame.transform.scale(image, ((size[0] // 320) * rect[0], (size[1] // 180) * rect[1]))
                frames.append(image)
        return frames

    def update(self):   # смена кадров
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class Tower(pygame.sprite.Sprite):  # класс башни
    def __init__(self, x, y, images, cols, damage=50, radius=200, reload=1000, price=500, is_splash=False, splash_radius=75, flag=False):
        super().__init__(towers)
        self.name = self.__class__.__name__
        self.frames = self.cut_sheet(load_image(images), cols)
        self.cur_frame = 0
        self.image = pygame.transform.scale(self.frames[self.cur_frame], (80, 120))
        self.price = price
        self.flag = flag
        self.damage = damage
        self.reload = reload
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x - 10, y - 50
        self.radius = radius
        self.focus = None
        self.is_splash = is_splash
        self.splash_radius = splash_radius

    def cut_sheet(self, sheet, columns):
        frames = []
        rows = 1
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))
        return frames

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = pygame.transform.scale(self.frames[self.cur_frame], (80, 120))

    def fire(self):  # выстрел по захваченой цели либо по области вокруг себя
        if self.flag:
            for enemy in enemies:
                if pygame.sprite.collide_circle(enemy, self):
                    enemy.get_damage(self.damage)
        else:
            if self.focus != None and self.focus.health != 0 and pygame.sprite.collide_circle(self.focus, self):
                if self.is_splash:
                    self.focus.radius = self.splash_radius
                    for enemy in enemies:
                        if pygame.sprite.collide_circle(enemy, self.focus):
                            enemy.get_damage(self.damage)
                else:
                    self.focus.get_damage(self.damage)
            else:
                self.focus_enemy()

    def focus_enemy(self):  # захват цели (при убийстве прошлой)
        for enemy in enemies:
            if pygame.sprite.collide_circle(enemy, self):
                self.focus = enemy
                self.fire()
                break


class Board:  # класс поля
    def __init__(self, screen, height=10, width=10, top=0, bot=240, cell_size=80):
        self.screen = screen
        self.hieght = height
        self.width = width
        self.top = top
        self.bot = bot
        self.cell_size = cell_size
        self.board = [[Pass_cell(self.cell_size * i, self.cell_size * h, self.cell_size)
                       for h in range(width)] for i in range(height)]
        self.spis = ['white', 'red', 'blue']
        self.n = 11

    def set_cell_size(self, cell_size):  # установить новый размер клетки
        self.cell_size = cell_size
        for h in range(self.hieght):
            for i in range(self.width):
                self.board[h][i].set_size(self.cell_size)

    def set_cell(self, x, y, cell):  # заменить одну клетку на другую
        self.board[y][x] = cell

    def get_cell(self, pos):  # проверка на какую клетку нажали
        cell_x = (pos[0] - self.top) // self.cell_size
        cell_y = (pos[1] - self.bot) // self.cell_size
        if cell_y < 0 or cell_y >= self.width or cell_x < 0 or cell_x >= self.hieght:
            return Pass_cell(0, 0, 80), (cell_x, cell_y)
        return self.board[cell_x][cell_y], (cell_x, cell_y)

    def get_click(self, mouse_pos, tower_price=500, tower_data=None):  # проверка на какую клетку нажали и установка башни
        cell, pos = self.get_cell(mouse_pos)
        if cell and cell.name == 'Building_cell':
            global gold
            if cell.tower == None:
                if gold >= tower_price and tower_data != None:
                    cell.set_tower(Tower(pos[0] * self.cell_size + 10 + self.top, pos[1] * self.cell_size + 10 + self.bot,
                                         *tower_data))
                    gold -= tower_price
                    db.execute(f"UPDATE statistic SET meaning ="
                               f"{db.execute(f'SELECT meaning FROM statistic WHERE Id = 6').fetchone()[0] + tower_price}"
                               f" WHERE Id = 6")
                    db.commit()
                    towers_reload[cell.tower] = pygame.USEREVENT + self.n
                    pygame.time.set_timer(towers_reload[cell.tower], cell.tower.reload)
                    self.n += 1
                else:
                    print(f'вам не хватает {tower_price - gold} золота')
            else:
                del towers_reload[cell.tower]
                gold += cell.tower.price // 2
                cell.tower.kill()
                cell.set_tower(None)
            return cell
        elif cell != None:
            return cell


def load_level(file_level, file_waves):  # загрузка уровня и настроек игры из файлов
    with open(file_level, 'r') as Map:
        level_map = [line for line in Map]
    with open(file_waves, 'r') as Waves:
        waves_data = []
        waves_enemies = []
        waves = [line for line in Waves]
        for wave in [i.split(' ') for i in waves]:
            waves_data.append([int(i) for i in wave[0].split(':')])
            waves_enemies.append([int(i) for i in wave[1:]])
    return level_map, waves_data, waves_enemies


def generate_level(level_map, cell_size):  # генерация карты
    list_cells = []
    for y in range(len(level_map)):
        lst = []
        for x in range(len(level_map[y])):
            if level_map[y][x] == '.':
                lst.append(Pass_cell(x * cell_size, y * cell_size, cell_size))
            elif level_map[y][x] == '0':
                lst.append(Building_cell(x * cell_size + top, y * cell_size + bot, cell_size, load_image('base.png')))
            elif level_map[y][x] == '#':
                lst.append(Road_cell(x * cell_size + top, y * cell_size + bot, cell_size, pygame.transform.rotate(load_image('road_4.png'), 90)))
                spawn_pos = (x, y)
            elif level_map[y][x] == '@':
                lst.append(Road_cell(x * cell_size + top, y * cell_size + bot, cell_size, pygame.transform.rotate(load_image('road_4.png'), 180)))
                spawn_pos = (x, y)
            elif level_map[y][x] == '$':
                lst.append(Road_cell(x * cell_size + top, y * cell_size + bot, cell_size, load_image('road_4.png')))
            elif level_map[y][x] == '%':
                lst.append(Road_cell(x * cell_size + top, y * cell_size + bot, cell_size, pygame.transform.rotate(load_image('road_4.png'), 270)))
            elif level_map[y][x] == 'f':
                lst.append(Road_cell(x * cell_size + top, y * cell_size + bot, cell_size, load_image('road_1.png')))
            elif level_map[y][x] == 'r':
                lst.append(Road_cell(x * cell_size + top, y * cell_size + bot, cell_size, pygame.transform.rotate(load_image('road_1.png'), 90)))
            elif level_map[y][x] == 's':
                lst.append(Road_cell(x * cell_size + top, y * cell_size + bot, cell_size, load_image('road_3.png')))
            elif level_map[y][x] == 'd':
                lst.append(Road_cell(x * cell_size + top, y * cell_size + bot, cell_size, pygame.transform.rotate(load_image('road_3.png'), 180)))
            elif level_map[y][x] == 'w':
                lst.append(Road_cell(x * cell_size + top, y * cell_size + bot, cell_size, pygame.transform.rotate(load_image('road_3.png'), 270)))
            elif level_map[y][x] == 'a':
                lst.append(Road_cell(x * cell_size + top, y * cell_size + bot, cell_size, pygame.transform.rotate(load_image('road_3.png'), 90)))
        list_cells.append(lst)
    return list_cells, spawn_pos


def load_path(name):  # загрузка пути врага
    if os.path.isfile(name):
        file = open(name).readlines()
        path = []
        try:
            for string in file:
                path.append([int(i) for i in string.split(' ')])
            return path
        except Exception:
            print('Неверный формат файла:', name)


def find_key(dictionary, needle):  # найти башню которая перезарядилась
    for key in dictionary.keys():
        if dictionary[key] == needle:
            return key


def terminate():  # закрытие программы
    db.close()
    pygame.quit()
    sys.exit()


def finish_screen(screen):
    run = True
    while run:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type in (pygame.K_ESCAPE, pygame.K_RETURN) or\
                    (event.type == pygame.MOUSEBUTTONUP and event.button == 1):
                run = False
                break
            elif event.type == pygame.QUIT:
                run = False
                break
        pygame.display.flip()

def main_menu(screen):
    start_menu_sprites = pygame.sprite.Group()  # Эта група спрайтов отображаемых в стартовом меню
    AchievementBut(start_menu_sprites, size, screen)
    LearningBut(start_menu_sprites, size, screen)
    ExitBut(start_menu_sprites, size)
    InfoBut(start_menu_sprites, size)
    start_menu = StartMenu(start_menu_sprites)  # Создание обекта стартового миню
    play_but = PlayBut(start_menu_sprites, size, start_menu)
    start_menu.start_menu_display(screen, size)   # Вывод меню при включение
    return play_but.map()   # номер карты


def in_game_captions(screen):     # зисло золота и хп замка
    global gold, castle_health
    f = pygame.font.Font('7X7PixelizedRegular.ttf', 40)
    gold_text = f.render(f'{gold}', False, (51, 51, 102))
    screen.blit(gold_text, (200, 30))
    background = pygame.transform.scale(load_image('coin.png'), (24, 36))
    screen.blit(background, (170, 37))
    f = pygame.font.Font('7X7PixelizedRegular.ttf', 50)
    gold_text = f.render(f'HP:{castle_health}', False, (51, 51, 102))
    screen.blit(gold_text, (400, 20))


def tower_selection(clickable_interface_elements, pos):     # Выбор башни/улучшение
    a = list(map(lambda x: x.update(pos), clickable_interface_elements))
    return sum(a)


def load_menu(my_board, screen, enemy_types, towers_types):
    global current_level, castle_health, gold, enemies, towers, cells, towers_reload, current_wave, \
        enemy_type, levels_data, lvl, waves, wave_enemies, level, start_pos, enemy_default_settings, \
        n_levels, spawn_enemy, move_enemy, time_is_passing, animated_towers, time_level, n_enemies, type_tower, \
        current_tower, animated_enemies
    current_level = main_menu(screen)
    # загрузка карты
    castle_health = 100
    gold = 1500
    enemies = pygame.sprite.Group()
    towers = pygame.sprite.Group()
    cells = pygame.sprite.Group()
    towers_reload = {}

    current_wave, enemy_type = 0, 0
    levels_data = [load_level(f'data/map_{i + 1}.map', f'data/waves_{i + 1}.txt') for i in range(n_levels)]
    lvl, waves, wave_enemies = levels_data[current_level]
    level, start_pos = generate_level(lvl, 80)
    enemy_default_settings = (start_pos[0] * 80 + my_board.top,
                              start_pos[1] * 80 + my_board.cell_size // 4 + my_board.bot)
    for x in range(len(level)):
        for y in range(len(level[x])):
            my_board.set_cell(x, y, level[x][y])

    # стандартные таймеры событий
    spawn_enemy = pygame.USEREVENT + 1
    move_enemy = pygame.USEREVENT + 2
    time_is_passing = pygame.USEREVENT + 3
    animated_towers = pygame.USEREVENT + 4
    animated_enemies = pygame.USEREVENT + 5
    pygame.time.set_timer(move_enemy, 25)
    pygame.time.set_timer(spawn_enemy, waves[current_wave][1])
    pygame.time.set_timer(time_is_passing, 1000)
    pygame.time.set_timer(animated_towers, 50)
    pygame.time.set_timer(animated_enemies, 150)
    time_level = 0

    n_enemies = [0 for _ in range(len(enemy_types))]
    type_tower = 0
    current_tower = towers_types[type_tower]


# константы используемые объектами или функциями
db = sqlite3.connect('user_data.sqlite3')
db.cursor()
castle_health = 100
gold = 1500
enemies = pygame.sprite.Group()
towers = pygame.sprite.Group()
cells = pygame.sprite.Group()
towers_reload = {}
n_levels = 5
enemy_paths = [load_path(f'data/path_{i + 1}.txt') for i in range(n_levels)]
size = width, height = 1280, 720
cell_size = 80
top, bot = 0, 240


def main():
    # создание окна
    pygame.init()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('First board')

    # создания поля
    my_board = Board(screen, 14, 6)

    # часть Лены
    background = pygame.transform.scale(load_image('sky.png'), size)

    castle = pygame.transform.scale(load_image('castle.png'), ((size[0] // 320) * 40, (size[1] // 180) * 132))
    current_level = main_menu(screen)
    playing_field = pygame.transform.scale(load_image(f'background_{current_level + 1}.png'), size)
    print(f'background_{current_level}.png')
    #
    clickable_interface_elements = pygame.sprite.Group()
    UpgradeBtn(clickable_interface_elements, size)
    Tower1Btn(clickable_interface_elements, size)
    Tower2Btn(clickable_interface_elements, size)
    Tower3Btn(clickable_interface_elements, size)
    # -
    # загрузка карты
    current_wave, enemy_type = 0, 0
    levels_data = [load_level(f'data/map_{i + 1}.map', f'data/waves_{i + 1}.txt') for i in range(n_levels)]
    lvl, waves, wave_enemies = levels_data[current_level]
    level, start_pos = generate_level(lvl, 80)
    for x in range(len(level)):
        for y in range(len(level[x])):
            my_board.set_cell(x, y, level[x][y])

    # стандартные таймеры событий
    enemy_animation = pygame.USEREVENT + 5
    pygame.time.set_timer(enemy_animation, 50)
    spawn_enemy = pygame.USEREVENT + 1
    move_enemy = pygame.USEREVENT + 2
    time_is_passing = pygame.USEREVENT + 3
    animated_towers = pygame.USEREVENT + 4
    animated_enemies = pygame.USEREVENT + 5
    pygame.time.set_timer(move_enemy, 20)
    pygame.time.set_timer(spawn_enemy, waves[current_wave][1])
    pygame.time.set_timer(time_is_passing, 1000)
    pygame.time.set_timer(animated_towers, 150)
    pause_wave = 10000
    time_level = 0
    global castle_health, enemies, towers, towers_reload, gold, cells

    enemy_default_settings = (start_pos[0] * 80 + my_board.top,
                              start_pos[1] * 80 + my_board.cell_size // 4 + my_board.bot)
    enemy_types = [default_enemy, haste_enemy, armored_enemy]
    n_enemies = [0 for _ in range(len(enemy_types))]
    towers_types = [default_tower, mortire, flamethrower]
    type_tower = 0
    current_tower = towers_types[type_tower]
    print_radius = (0, 0), 0

    running = True

    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                load_menu(my_board, screen, enemy_types, towers_types)
            if event.type == pygame.QUIT:  # выход из игры
                terminate()
            if event.type == pygame.MOUSEMOTION:
                cell, pos = my_board.get_cell(event.pos)
                if cell.name == 'Building_cell' and cell.tower != None:
                    print_radius = cell.tower.rect.center, cell.tower.radius
                else:
                    print_radius = (0, 0), 0
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # проверка на какую вклетку нажали,
                chosen = tower_selection(clickable_interface_elements, event.pos)   # Номер нажетой кнопки
                print(chosen)
                # если строительная то ставиться башня
                print(my_board.get_click(event.pos, current_tower[4], current_tower))
                type_tower = (type_tower + 1) % len(towers_types)
                current_tower = towers_types[type_tower]
            if event.type == move_enemy:  # проверка выходит ли враг за дорогу
                for enemy in enemies:
                    enemy.move()
            if event.type == spawn_enemy:  # создание врага раз в заданое кол-во секунд (сейчас 2.5) секунды
                flag = True
                while flag:
                    try:
                        if sum(n_enemies) == sum(wave_enemies[current_wave]):
                            current_wave += 1
                            n_enemies = [0 for _ in range(len(enemy_types))]
                            pygame.time.set_timer(spawn_enemy, pause_wave)
                            flag = False
                            break
                        if current_wave < len(wave_enemies) and n_enemies[enemy_type] < wave_enemies[current_wave][enemy_type]:
                            pygame.time.set_timer(spawn_enemy, waves[current_wave][1])
                            Enemy(*enemy_default_settings, *enemy_types[enemy_type], enemy_paths[current_level])
                            n_enemies[enemy_type] += 1
                            enemy_type = (enemy_type + 1) % len(enemy_types)
                            flag = False
                            break
                        enemy_type = (enemy_type + 1) % len(enemy_types)
                    except Exception as error:
                        print(error)
                        if not enemies:
                            pygame.time.set_timer(spawn_enemy, 0)
                            if current_level < len(levels_data):
                                db.execute(f"UPDATE statistic SET meaning = {time_level} WHERE Id ="
                                           f"{current_level + 1} AND meaning > {time_level}")
                        flag = False
                        break
            if event.type == time_is_passing:
                time_level += 1
            if event.type in towers_reload.values():  # выстрел башни по окончании перезрядки
                find_key(towers_reload, event.type).fire()
            if event.type == animated_towers:
                towers.update()
            if event.type == enemy_animation:
                enemies.update()
        if castle_health <= 0:
            load_menu(my_board, screen, enemy_types, towers_types)
        # отрисовка
        screen.blit(background, (0, 0))  # Фон с небом
        screen.blit(playing_field, (0, 0))      # Игровое поле
        screen.blit(castle, ((size[0] // 320) * 280, (size[1] // 180) * 48))     # замок
        clickable_interface_elements.draw(screen)  # элименты игтерфейса игры
        in_game_captions(screen)    # отрисовка натписей
        cells.update()
        cells.draw(screen)
        enemies.draw(screen)
        towers.draw(screen)
        pygame.draw.circle(screen, 'white', *print_radius, 1)
        pygame.display.flip()


if __name__ == '__main__':
    main()