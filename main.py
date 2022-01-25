import pygame
import sys
import os
from entities import *


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не удаётся загрузить:', name)
        raise SystemExit(message)
    # try:
    image = image.convert_alpha()
    # except Exception as error:
    #     print(error)
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


class Cell:  # общий класс клетки
    def __init__(self, x, y, screen, size):
        self.name = self.__class__.__name__
        self.x, self.y = x, y
        self.size = size
        self.screen = screen

    def __str__(self):  # удобное преобразование в строку
        return self.name

    def draw(self):
        pygame.draw.rect(self.screen, 'white', (self.x, self.y, self.size, self.size), 1)

    def set_size(self, size):  # установить новые размеры клетки
        self.size = size


class Road_cell(Cell):  # клетка дороги для мобов
    def __init__(self, x, y, screen, size):
        super().__init__(x, y, screen, size)

    def draw(self):
        pygame.draw.rect(self.screen, 'blue', (self.x, self.y, self.size, self.size), 5)


class Pass_cell(Cell):  # пустая клетка (декоративная)
    def __init__(self, x, y, screen, size):
        super().__init__(x, y, screen, size)


class Building_cell(Cell):  # клетка для стороительства башен
    def __init__(self, x, y, screen, size, tower=None):
        super().__init__(x, y, screen, size)
        self.tower = tower

    def set_tower(self, tower):  # установить башня в клетку
        self.tower = tower

    def draw(self): # отрисовка клетки и башни
        pygame.draw.rect(self.screen, 'green', (self.x, self.y, self.size, self.size), 5)


class Enemy(pygame.sprite.Sprite):  # класс враждебного моба
    def __init__(self, x, y, screen, health, image, damage=10, price=10, speed=1):
        super().__init__(entities, enemies)
        self.name = self.__class__.__name__
        self.pos = x, y
        self.screen = screen
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
        self.set_path(enemy_path)

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
            self.kill()
        else:
            self.health -= damage


class Tower(pygame.sprite.Sprite):  # класс башни
    def __init__(self, x, y, screen, image, damage=50, radius=200, reload=1000, price=500,
                 is_splash=False, splash_radius=75):
        super().__init__(towers, entities)
        self.name = self.__class__.__name__
        self.pos = x, y
        self.screen = screen
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
    def __init__(self, screen, height=10, width=10, cell_size=80):
        self.screen = screen
        self.hieght = height
        self.width = width
        self.cell_size = cell_size
        self.board = [[Pass_cell(self.cell_size * i, self.cell_size * h, self.screen, self.cell_size)
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
        cell_x = pos[0] // self.cell_size
        cell_y = pos[1] // self.cell_size
        if cell_y < 0 or cell_y >= self.width or cell_x < 0 or cell_x >= self.hieght:
            print('error')
            return Pass_cell(0, 0, None, 80)
        return self.board[cell_x][cell_y], (cell_x, cell_y)

    def get_click(self, mouse_pos, tower_price=500, tower_data=None):  # проверка на какую клетку нажали и установка башни
        # (пока только одного типа)
        cell, pos = self.get_cell(mouse_pos)
        if cell and cell.name == 'Building_cell':
            global gold
            if cell.tower == None:
                if gold >= tower_price and tower_data != None:
                    cell.set_tower(Tower(pos[0] * self.cell_size + 10, pos[1] * self.cell_size + 10, self.screen,
                                         *tower_data))
                    gold -= tower_price
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
    list_entities = []
    for y in range(len(level_map)):
        lst = []
        for x in range(len(level_map[y])):
            if level_map[y][x] == '.':
                lst.append(Pass_cell(x * cell_size, y * cell_size, screen, cell_size))
            elif level_map[y][x] == '0':
                lst.append(Building_cell(x * cell_size, y * cell_size, screen, cell_size))
            elif level_map[y][x] == '#':
                lst.append(Road_cell(x * cell_size, y * cell_size, screen, cell_size))
            elif level_map[y][x] == '@':
                lst.append(Road_cell(x * cell_size, y * cell_size, screen, cell_size))
                spawn_pos = (x, y)
        list_entities.append(lst)
    return list_entities, spawn_pos


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


# константы используемые объектами или функциями
castle_health = 100
gold = 1500
entities = pygame.sprite.Group()
enemies = pygame.sprite.Group()
towers = pygame.sprite.Group()
towers_reload = {}
enemy_path = load_path('data/enemy_path.txt')
size = width, height = 1280, 720


def main():
    # создание окна
    pygame.init()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('First board')

    # создания поля
    my_board = Board(screen, 16, 9)
    my_board.set_cell_size(80)
    current_level = 0

    # загрузка карты
    current_wave, enemy_type = 0, 0
    levels_data = [load_level('data/map1.map', 'data/waves1.txt')]
    lvl, waves, wave_enemies = levels_data[current_level]
    level, start_pos = generate_level(lvl, 80, screen)
    for x in range(len(level)):
        for y in range(len(level[x])):
            my_board.set_cell(x, y, level[x][y])

    # стандартные таймеры событий
    spawn_enemy = pygame.USEREVENT + 1
    my_event = pygame.USEREVENT + 2
    pygame.time.set_timer(my_event, 15)
    pygame.time.set_timer(spawn_enemy, waves[current_wave][1])
    pause_wave = 10000

    enemy_default_settings = (start_pos[0] * 80 + my_board.cell_size // 4, start_pos[1] * 80 + my_board.cell_size // 4,
                              screen)
    enemy_types = [default_enemy, haste_enemy, armored_enemy]
    n_enemies = [0 for _ in range(len(enemy_types))]
    towers_types = [default_tower, sniper_tower, mortire]
    type_tower = 0
    current_tower = towers_types[type_tower]

    running = True
    while running:
            screen.fill((0, 0, 0))
            if castle_health <= 0:
                running = False
                finish_screen(screen)
                break
            for event in pygame.event.get():
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
                                print(current_wave)
                                current_wave += 1
                                n_enemies = [0 for _ in range(len(enemy_types))]
                                print(current_wave)
                                pygame.time.set_timer(spawn_enemy, pause_wave)
                            if current_wave < len(wave_enemies) and n_enemies[enemy_type % len(enemy_types)] < wave_enemies\
                                [current_wave][enemy_type % len(enemy_types)]:
                                pygame.time.set_timer(spawn_enemy, waves[current_wave][1])
                                Enemy(*enemy_default_settings, *enemy_types[enemy_type % len(enemy_types)])
                                n_enemies[enemy_type % len(enemy_types)] += 1
                                enemy_type += 1
                                flag = False
                                break
                        except Exception as error:
                            print(error)
                            if not enemies:
                                current_level += 1
                                pygame.time.set_timer(spawn_enemy, 0)
                                if current_level < len(levels_data):
                                    lvl, waves, wave_enemies = levels_data[current_level]
                            flag = False
                            break
                if event.type in towers_reload.values():  # выстрел башни по окончании перезрядки
                    find_key(towers_reload, event.type).fire()
            # отрисовка
            my_board.render()
            entities.update()
            entities.draw(screen)
            pygame.display.flip()


if __name__ == '__main__':
    main()
