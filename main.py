import pygame
import sys
import os
import random
import sqlite3
from entities import *


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
        clouds = pygame.sprite.Group()
        menu_clouds = []
        for i in range(random.randint(2, 3)):
            menu_clouds.append(MenuClouds(clouds, size))
        fps = 60
        clock = pygame.time.Clock()
        background = pygame.transform.scale(load_image('start_menu_background.png'), size)
        while self.done:
            screen.blit(background, (0, 0))
            clouds.draw(screen)
            self.start_menu_sprites.draw(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()  # Выхлд из игры
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for i in self.start_menu_sprites:
                        i.click(pos, screen)
            clouds.update()
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


class Achievement:    # Меню очевок
    def __init__(self):
        f = pygame.font.Font('7X7PixelizedRegular.ttf', 50)
        text = ''

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
    def __init__(self, x, y, health, image, damage=10, price=10, speed=1, path=None):
        super().__init__(entities, enemies)
        self.name = self.__class__.__name__
        self.pos = x, y
        self.health = health
        self.damage = damage
        self.speed = speed
        self.image = load_image(image)
        self.price = price
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.pos[0], self.pos[1]
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

    def check(self, cell1, cell2):  # проверка(враг не может выйти за пределы дороги)
        if self.speed > 0 and cell1.name == 'Road_cell':
            self.move()
        if self.speed < 0 and cell2.name == 'Road_cell':
            self.move()

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


class Tower(pygame.sprite.Sprite):  # класс башни
    def __init__(self, x, y, image, damage=50, radius=200, reload=1000, price=500, is_splash=False, splash_radius=75):
        super().__init__(towers, entities)
        self.name = self.__class__.__name__
        self.pos = x, y
        self.price = price
        self.damage = damage
        self.radius = radius
        self.reload = reload
        self.image = load_image(image)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.pos[0], self.pos[1]
        self.radius = radius
        self.focus = None
        self.is_splash = is_splash
        self.splash_radius = splash_radius

    def fire(self):  # выстрел по захваченой цели
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

    def render(self):  # отрисовка поля, клеток и башен на нём
        for i in range(self.hieght):
            for g in range(self.width):
                self.board[i][g].draw()

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


def generate_level(level_map, cell_size, screen):  # генерация карты
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
    achievement_but = AchievementBut(start_menu_sprites, size, screen)
    learning_but = LearningBut(start_menu_sprites, size, screen)
    exit_but = ExitBut(start_menu_sprites, size)
    info_btn = InfoBut(start_menu_sprites, size)
    start_menu = StartMenu(start_menu_sprites)  # Создание обекта стартового миню
    play_but = PlayBut(start_menu_sprites, size, start_menu)
    start_menu.start_menu_display(screen, size)   # Вывод меню при включение
    return play_but.map()   # номер карты

# константы используемые объектами или функциями
db = sqlite3.connect('user_data.sqlite3')
db.cursor()
castle_health = 100
gold = 1500
entities = pygame.sprite.Group()
enemies = pygame.sprite.Group()
towers = pygame.sprite.Group()
cells = pygame.sprite.Group()
towers_reload = {}
enemy_paths = [load_path('data/enemy_path.txt')]
size = width, height = 1280, 720
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
    current_level = main_menu(screen)
    playing_field = pygame.transform.scale(load_image('background_0.png'), size)
    #

    # загрузка карты
    current_wave, enemy_type = 0, 0
    levels_data = [load_level('data/map_1.map', 'data/waves_1.txt')]
    lvl, waves, wave_enemies = levels_data[current_level]
    level, start_pos = generate_level(lvl, 80, screen)
    for x in range(len(level)):
        for y in range(len(level[x])):
            my_board.set_cell(x, y, level[x][y])

    # стандартные таймеры событий
    spawn_enemy = pygame.USEREVENT + 1
    my_event = pygame.USEREVENT + 2
    time_is_passing = pygame.USEREVENT + 3
    pygame.time.set_timer(my_event, 15)
    pygame.time.set_timer(spawn_enemy, waves[current_wave][1])
    pygame.time.set_timer(time_is_passing, 1000)
    pause_wave = 10000
    time_level = 0
    global castle_health, entities, enemies, towers, towers_reload, gold, cells

    enemy_default_settings = (start_pos[0] * 80 + my_board.top,
                              start_pos[1] * 80 + my_board.cell_size // 4 + my_board.bot)
    enemy_types = [default_enemy, haste_enemy, armored_enemy]
    n_enemies = [0 for _ in range(len(enemy_types))]
    towers_types = [default_tower, sniper_tower, mortire]
    type_tower = 0
    current_tower = towers_types[type_tower]

    running = True

    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                current_level = main_menu(screen)
                # загрузка карты
                current_wave, enemy_type = 0, 0
                lvl, waves, wave_enemies = levels_data[current_level]
                level, start_pos = generate_level(lvl, 80, screen)
                for x in range(len(level)):
                    for y in range(len(level[x])):
                        my_board.set_cell(x, y, level[x][y])

                # стандартные таймеры событий
                spawn_enemy = pygame.USEREVENT + 1
                my_event = pygame.USEREVENT + 2
                time_is_passing = pygame.USEREVENT + 3
                pygame.time.set_timer(my_event, 15)
                pygame.time.set_timer(spawn_enemy, waves[current_wave][1])
                pygame.time.set_timer(time_is_passing, 1000)
                pause_wave = 10000
                time_level = 0

                n_enemies = [0 for _ in range(len(enemy_types))]
                type_tower = 0
                current_tower = towers_types[type_tower]

                castle_health = 100
                gold = 1500
                entities = pygame.sprite.Group()
                enemies = pygame.sprite.Group()
                towers = pygame.sprite.Group()
                towers_reload = {}
            if event.type == pygame.QUIT:  # выход из игры
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # проверка на какую вклетку нажали,
                # если строительная то ставиться башня
                print(my_board.get_click(event.pos, current_tower[4], current_tower))
                type_tower = (type_tower + 1) % len(towers_types)
                current_tower = towers_types[type_tower]
            if event.type == my_event:  # проверка выходит ли враг за дорогу
                for enemy in enemies:
                    cell1 = my_board.get_click((enemy.pos[0] + enemy.rect.width, enemy.pos[1] + enemy.rect.height))
                    cell2 = my_board.get_click((enemy.pos[0] + enemy.speed, enemy.pos[1] + enemy.speed))
                    enemy.check(cell1, cell2)
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
                            current_level += 1
                            pygame.time.set_timer(spawn_enemy, 0)
                            if current_level < len(levels_data):
                                lvl, waves, wave_enemies = levels_data[current_level]
                                db.execute(f"UPDATE statistic SET meaning = {time_level} WHERE Id ="
                                           f"{current_level + 1} AND meaning > {time_level}")
                        flag = False
                        break
            if event.type == time_is_passing:
                time_level += 1
            if event.type in towers_reload.values():  # выстрел башни по окончании перезрядки
                find_key(towers_reload, event.type).fire()
        if castle_health <= 0:
            current_level = main_menu(screen)
            # загрузка карты
            current_wave, enemy_type = 0, 0
            levels_data = [load_level('data/map1.map', 'data/waves_1.txt')]
            lvl, waves, wave_enemies = levels_data[current_level]
            level, start_pos = generate_level(lvl, 80, screen)
            for x in range(len(level)):
                for y in range(len(level[x])):
                    my_board.set_cell(x, y, level[x][y])

            # стандартные таймеры событий
            spawn_enemy = pygame.USEREVENT + 1
            my_event = pygame.USEREVENT + 2
            time_is_passing = pygame.USEREVENT + 3
            pygame.time.set_timer(my_event, 15)
            pygame.time.set_timer(spawn_enemy, waves[current_wave][1])
            pygame.time.set_timer(time_is_passing, 1000)
            pause_wave = 10000
            time_level = 0

            n_enemies = [0 for _ in range(len(enemy_types))]
            type_tower = 0
            current_tower = towers_types[type_tower]

            castle_health = 100
            gold = 1500
            entities = pygame.sprite.Group()
            enemies = pygame.sprite.Group()
            towers = pygame.sprite.Group()
            towers_reload = {}
        # отрисовка
        screen.blit(background, (0, 0))  # Фон с небом
        screen.blit(playing_field, (0, 0))      # Игровое поле
        cells.update()
        cells.draw(screen)
        entities.update()
        entities.draw(screen)
        pygame.display.flip()


if __name__ == '__main__':
    main()
