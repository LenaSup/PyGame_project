import pygame


class Cell: # общий класс клетки
    def __init__(self, x=0, y=0, screen=None, size=80):
        self.name = self.__class__.__name__
        self.can_build = False
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
    def __init__(self, x, y, screen, size=80):
        super().__init__(x, y, screen, size)

    def draw(self):
        pygame.draw.rect(self.screen, 'blue', (self.x, self.y, self.size, self.size), 1)


class Pass_cell(Cell): # пустая клетка, декоративная
    def __init__(self, x, y, screen, size=80):
        super().__init__(x, y, screen, size)


class Building_cell(Cell): # клетка для стороительства башен
    def __init__(self, x, y, screen, size=80):
        super().__init__(x, y, screen, size)
        self.can_build = True


class Entity: # общий класс существ
    def __init__(self, x, y, screen, is_enemy=False):
        self.name = self.__class__.__name__
        self.is_enemy = is_enemy
        self.pos = x, y
        self.screen = screen

    def __str__(self):
        if self.is_enemy:
            return self.name
        return self.name

    def focus_check(self, mouse_pos): #
        pass


class Enemy(Entity): # класс враждебного моба
    def __init__(self, x, y, screen, size, health, image, damage=1, speed=-1):
        super().__init__(x, y, screen, True)
        self.size = size
        self.health = health
        self.damage = damage
        self.speed = speed
        self.image = image

    def move(self): # передвижение моба
        self.pos = self.pos[0] + self.speed, self.pos[1]

    def check(self, cell1, cell2): # проверка(моб не может выйти за пределы дороги)
        if self.speed > 0 and cell1.name == 'Road_cell':
            self.move()
        if self.speed < 0 and cell2.name == 'Road_cell':
            self.move()

    def draw(self):
        pygame.draw.rect(self.screen, 'red', (self.pos[0], self.pos[1], self.size, self.size), 0)


class Tower(Entity): # класс башни
    def __init__(self, x, y, screen, size, health, images, damage=1, radius=0, sps=1, level=1):
        super().__init__(x, y, screen, False)
        self.health = health
        self.size = size
        self.damage = damage
        self.radius = radius
        self.sps = sps
        self.level = level
        self.images = images

    def draw(self):
        pygame.draw.rect(self.screen, 'green', (self.pos[0], self.pos[1], self.size, self.size))



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
        if cell_x < 0 or cell_x >= self.width or cell_y < 0 or cell_y >= self.hieght:
            return Pass_cell(0, 0, None)
        return self.board[cell_y][cell_x]

    def get_click(self, mouse_pos): # проверка на какую клетку нажали
        cell = self.get_cell(mouse_pos)
        if cell:
            return cell


def main():
    pygame.init()
    size = width, height = 1280, 720
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('First board')
    my_board = Board(screen, 16, 9)
    my_board.set_cell_size(80)
    for h in range(1, 5):
        for i in range(1, 5):
            my_board.set_cell(i, h, Road_cell(h * 80, i * 80, screen, 80))
    entities = []
    my_board.set_cell(1, 1, Tower(80, 80, screen, 80, 1000, None))
    my_event = pygame.USEREVENT + 1
    pygame.time.set_timer(my_event, 10)
    enemy = Enemy(250, 250, screen, 40, 100, None)
    entities.append(enemy)
    entities.append(my_board.board[1][1])

    running = True
    while running:
            screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print(my_board.get_click(event.pos))
                if event.type == my_event:
                    cell1 = my_board.get_click((enemy.pos[0] + enemy.size, enemy.pos[1] + enemy.size))
                    cell2 = my_board.get_click((enemy.pos[0] - 1, enemy.pos[1] - 1))
                    enemy.check(cell1, cell2)
            my_board.render()
            enemy.draw()
            entities[1].draw()
            pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()
