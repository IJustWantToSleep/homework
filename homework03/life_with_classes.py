import pygame
from pygame.locals import *
import random
from copy import deepcopy


class GameOfLife:

    def __init__(self, width=640, height=480, cell_size=10, speed=10):
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_grid(self):
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            # рисуются линии по оси ox
            pygame.draw.line(self.screen, pygame.Color('black'),
                    (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            # рисуются линии по оси oy
            pygame.draw.line(self.screen, pygame.Color('black'),
                    (0, y), (self.width, y))

    def draw_cell_list(self, rects: list):
        """
        Отображение списка клеток 'rects' с закрашиванием их в
        соответствующе цвета
        """
        x = 0
        y = 0
        for row in range(self.cell_height):
            x = 0
            # перебор элеметов внутреннего списка
            for col in range(self.cell_width):
                # создание ячейки rect для внутреннего списка
                rect1 = pygame.Rect((x, y, self.cell_size, self.cell_size))
                # раскрасить ячейку нужным цветом
                if rects[row][col]:
                    pygame.draw.rect(self.screen, pygame.Color('green'), rect1)
                else:
                    pygame.draw.rect(self.screen, pygame.Color('white'), rect1)

                # увеличение значения по оси x
                x += self.cell_size


            # увеличение значения по оси y
            y += self.cell_size


    def run(self):
        """ Запустить игру """
        pygame.init()
        # создание объекта для контроля времени
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))

        # Создание списка клеток
        # PUT YOUR CODE HERE
        clist = game.cell_list(randomize=True)

        running = True
        while running:
            # цикл для получения событий игры
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            # обновить клетки
            clist = self.update_cell_list(clist).copy()

            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            self.draw_cell_list(clist)

            # рисуется сетка
            self.draw_grid()
            # обновить полный экран
            pygame.display.flip()
            # обновить время (в зависимости от скорости протекания игры)
            clock.tick(self.speed)

        pygame.quit()


    def cell_list(self, randomize:bool = False)-> list:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1.
        В противном случае клетка считается мертвой, то
        есть ее значение равно 0.
        Если параметр randomize = True, то создается список, где
        каждая клетка может быть равновероятно живой или мертвой.
        """

        #создадим пустой список клеток
        clist = []
        #перебор элементов по высоте
        for row in range(self.cell_height):
            # создание внутреннего списка и перебор по ширине
            lst_width = []
            for col in range(self.cell_width):
                # получение рандомного значения 0 или 1
                if randomize:
                    value = random.randint(0, 1)
                else:
                    value = 0
                lst_width.append(value)

             # добавление элемента внутреннего списка в список
            clist.append(lst_width)
        return clist

    def get_neighbours(self, cell: tuple)->list:
        """ Вернуть список соседей для указанной ячейки

        :param cell: Позиция ячейки в сетке, задается кортежем вида (row, col)
        :return: Одномерный список ячеек, смежных к ячейке cell
        """
        # создание списка соседей
        neighbours = []
        row = cell[0]
        col = cell[1]
        # получить ячейку слева
        if row > 0:
            neighbours.append((row - 1, col))
        # получить ячейку справа
        if row < (self.cell_height - 1):
            neighbours.append((row + 1, col))
        # получить ячейку сверху
        if col > 0:
            neighbours.append((row, col - 1))
        # получить ячейку снизу
        if col < (self.cell_width - 1) and row < (self.cell_height - 1):
            neighbours.append((row + 1, col))
        # получить ячейку слева снизу по диагонали
        if row > 0 and col < (self.cell_width - 1):
            neighbours.append((row - 1, col - 1))
        # получить ячейку справа снизу по диагонали
        if row < (self.cell_height - 1) and col < (self.cell_width - 1):
            neighbours.append((row + 1, col + 1))
        # получить ячейку слева сверху по диагонали
        if row > 0 and col > 0:
            neighbours.append((row - 1, col - 1))
        # получить ячейку справа сверху по диагонали
        if row > 0 and col < (self.cell_width - 1):
            neighbours.append((row - 1, col + 1))

        return neighbours


    def is_life_cell(self, cell: tuple, grid: list)-> bool:
        """функция обращается к элементам списка, определяет, живая клетка, или нет
        """
        if grid[cell[0]][cell[1]] == 1:
            return True
        else:
            return False

    def alive_neighbours(self, cell_list: list, grid: list)-> list:
        """функция возвращает список живых соседей
        :param cell_list: список всех соседей
        :param grid: матрица
        """
        alive_lst = []
        for idx, val in enumerate(cell_list):
            if self.is_life_cell(val, grid):
                alive_lst.append(val)

        return alive_lst

    def update_cell_list(self, cell_list):
        """ Выполнить один шаг игры.

        Обновление всех ячеек происходит одновременно. Функция возвращает
        новое игровое поле.

        :param cell_list: Игровое поле, представленное в виде матрицы
        :return: Обновленное игровое поле
        """

        new_clist = cell_list.copy()

        for row in range(self.cell_height):
            for col in range(self.cell_width):
                if col == self.cell_width:
                    print(col)
                cell = (row, col)
                # получить список соседей
                lst_n = self.get_neighbours(cell)
                # получить список живых соседей
                lst_alive = self.alive_neighbours(lst_n, cell_list)
                # если соседей 2 или 3, то рождается новое существо
                if len(lst_alive) == 2 or (len(lst_alive) == 1):
                    if not self.is_life_cell(cell, cell_list):
                        new_clist[row][col] = 1
                else:
                    new_clist[row][col] = 0

        return new_clist

class Cell:

    def __init__(self, row, col, state=False):
        pass

    def is_alive(self):
        pass


class CellList:

    def __init__(self, nrows, ncols, randomize=False):

        pass

    def get_neighbours(self, cell):
        neighbours = []
        #
        # PUT YOUR CODE HERE
        return neighbours

    def update(self):
        new_clist = deepcopy(self)
        # PUT YOUR CODE HERE
        return self

    def __iter__(self):
        pass

    def __next__(self):
        pass

    def __str__(self):
        pass

    @classmethod
    def from_file(cls, filename):
        pass


if __name__ == '__main__':
    game = GameOfLife(320, 240, 20, 3)

    game.run()

