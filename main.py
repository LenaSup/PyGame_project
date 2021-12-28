import pygame
import os


class Cell: # общий класс клетки
    def __init__(self, x, y, screen, size, can_build):
        self.name = self.__class__.__name__
        self.can_build = can_build
        self.x, self.y = x, y
        self.size = size
        self.screen = screen

    def __str__(self):
        return self.name

    def is_can_build(self):
        if self.can_build:
            return 'Yes'
        return 'No'

    def draw(self):
        pygame.draw.rect(self.screen, 'white', (self.x, self.y, self.size, self.size), 1)

    def set_size(self, size):
        self.size = size


class Road_cell(Cell): # клетка догори для мобов
    def __init__(self, x, y, screen, size):
        super().__init__(x, y, screen, size, False)

    def draw(self):
        pygame.draw.rect(self.screen, 'blue', (self.x, self.y, self.size, self.size), 5)


class Pass_cell(Cell): # пустая клетка, декоративная
    def __init__(self, x, y, screen, size):
        super().__init__(x, y, screen, size, False)


class Building_cell(Cell): # клетка для стороительства башен
    def __init__(self, x, y, screen, size, tower=None):
        super().__init__(x, y, screen, size, True)
        self.tower = tower

    def set_tower(self, tower):
        self.tower = tower

    def draw(self):
        pygame.draw.rect(self.screen, 'green', (self.x, self.y, self.size, self.size), 5)
        if self.tower != None:
            self.tower.draw()


class Entity: # общий класс существ
    def __init__(self, x, y, screen):
        self.name = self.__class__.__name__
        self.pos = x, y
        self.screen = screen

    def __str__(self):
        return self.name

    def focus_check(self, mouse_pos):
        pass


class Enemy(Entity): # класс враждебного моба
    def __init__(self, x, y, screen, width, height, health, image, damage=1, bps=1, speed=1):
        super().__init__(x, y, screen)
        self.size = self.width, self.height = width, height
        self.health = health
        self.damage = damage
        self.speed = speed
        self.image = image
        self.bps = bps
        self.path = None
        self.current_step = None
        self.step = None
        self.steps = None
        self.is_move = True

    def load_step(self, index): # загрузка следующего направления движения
        self.step = self.path[self.current_step]
        if self.step[0] < 0 or self.step[1] < 0:
            self.speed = abs(self.speed) * -1
        else:
            self.speed = abs(self.speed)

    def move(self): # передвижение моба по пути из файла
        if self.is_move:
            if self.step[0] == 0:
                if abs(self.step[1]) == self.steps and self.current_step == len(self.path) - 1:
                    self.is_move = False
                elif abs(self.step[1]) == self.steps:
                    self.steps = 0
                    self.current_step += 1
                    self.load_step(self.current_step)
                else:
                    self.pos = self.pos[0], self.pos[1] + self.speed
                    self.steps += 1
            else:
                if abs(self.step[0]) == self.steps and self.current_step == len(self.path) - 1:
                    self.is_move = False
                elif abs(self.step[0]) == self.steps:
                    self.steps = 0
                    self.current_step += 1
                    self.load_step(self.current_step)
                else:
                    self.pos = self.pos[0] + self.speed, self.pos[1]
                    self.steps += 1

    def check(self, cell1, cell2): # проверка(моб не может выйти за пределы дороги)
        if self.speed > 0 and cell1.name == 'Road_cell':
            self.move()
        if self.speed < 0 and cell2.name == 'Road_cell':
            self.move()

    def set_path(self, path):
        self.path = path
        self.current_step = 0
        self.steps = 0
        self.load_step(0)
        print('Шагов в пути врага:', len(self.path))

    def draw(self):
        pygame.draw.rect(self.screen, 'red', (self.pos[0], self.pos[1], self.width, self.height), 0)


class Tower(Entity): # класс башни
    def __init__(self, x, y, screen, size, health, images, damage=1, radius=0, sps=1, level=1):
        super().__init__(x, y, screen)
        self.health = health
        self.size = size
        self.damage = damage
        self.radius = radius
        self.sps = sps
        self.level = level
        self.images = images

    def draw(self):
        pygame.draw.rect(self.screen, 'yellow', (self.pos[0], self.pos[1], self.size, self.size))


class Board:
    def __init__(self, screen, height=10, width=10, cell_size=80):
        self.screen = screen
        self.hieght = height
        self.width = width
        self.cell_size = cell_size
        self.board = [[Pass_cell(self.cell_size * i, self.cell_size * h, self.screen, self.cell_size)
                       for h in range(width)] for i in range(height)]
        self.spis = ['white', 'red', 'blue']

    def set_cell_size(self, cell_size): # установить новый размер клетки
        self.cell_size = cell_size
        for h in range(self.hieght):
            for i in range(self.width):
                self.board[h][i].set_size(self.cell_size)

    def render(self): #
        for i in range(self.hieght):
            for g in range(self.width):
                self.board[i][g].draw()

    def set_cell(self, x, y, cell): # заменить одну клетку на другую
        self.board[y][x] = cell

    def get_cell(self, pos): # проверка на какую клетку нажали
        cell_x = pos[0] // self.cell_size
        cell_y = pos[1] // self.cell_size
        if cell_y < 0 or cell_y >= self.width or cell_x < 0 or cell_x >= self.hieght:
            print('error')
            return Pass_cell(0, 0, None, 80)
        return self.board[cell_x][cell_y], (cell_x, cell_y)

    def get_click(self, mouse_pos): # проверка на какую клетку нажали
        cell, pos = self.get_cell(mouse_pos)
        if cell and cell.name == 'Building_cell':
            if cell.tower == None:
                cell.set_tower(Tower(pos[0] * self.cell_size + 10, pos[1] * self.cell_size + 10, self.screen,
                                     60, 100, None))
            else:
                cell.set_tower(None)
            return cell
        elif cell != None:
            return cell


def load_level(file_level, file_settings):
    with open(file_level, 'r')as Map:
        level_map = [line for line in Map]
    return level_map


def generate_level(level_map, cell_size, screen):
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
        list_entities.append(lst)
    return list_entities


def load_path(name):
    if os.path.isfile(name):
        file = open(name).readlines()
        path = []
        try:
            for string in file:
                path.append([int(i) for i in string.split(' ')])
            return path
        except Exception:
            print('Неверный формат файла:', name)


def main():
    pygame.init()
    size = width, height = 1280, 720
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('First board')
    my_board = Board(screen, 16, 9)
    my_board.set_cell_size(80)
    level = generate_level(load_level('data/map.map', 'data/settings.txt'), 80, screen)
    for x in range(len(level)):
        for y in range(len(level[x])):
            my_board.set_cell(x, y, level[x][y])
    test_tower = Building_cell(0, 0, screen, 80, Tower(10, 10, screen, 60, 100, None))
    my_board.set_cell(0, 0, test_tower)
    my_board.board[4][8].set_tower(Tower(4 * 80 + 10, 8 * 80 + 10, screen, 60, 100, None))
    entities = []
    my_event = pygame.USEREVENT + 1
    pygame.time.set_timer(my_event, 10)
    enemy = Enemy(20, 340, screen, 40, 40, 100, None)
    enemy.set_path(load_path('data/enemy_path.txt'))
    entities.append(enemy)

    running = True
    while running:
            screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    print(my_board.get_click(event.pos))
                if event.type == my_event:
                    cell1 = my_board.get_click((enemy.pos[0] + enemy.size[0], enemy.pos[1] + enemy.size[1]))
                    cell2 = my_board.get_click((enemy.pos[0] - 1, enemy.pos[1] - 1))
                    enemy.check(cell1, cell2)
            my_board.render()
            enemy.draw()
            for entity in entities:
                entity.draw()
            pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()
