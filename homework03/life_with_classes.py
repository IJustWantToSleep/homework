import random
from copy import deepcopy

import pygame
from pygame.locals import *


class GameOfLife:

    def __init__(self, width=640, height=480, cell_size=10, speed=10) -> None:
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

    def draw_grid(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            # рисуются линии по оси ox
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            # рисуются линии по оси oy
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (0, y), (self.width, y))

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        # создание объекта для контроля времени
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))

        # Создание списка клеток. для получения из файла выставить randomize=False
        # и разкомментировать строчку с deepcopy
        clist = CellList(self.cell_height, self.cell_width, randomize=True)
        # clist = deepcopy(clist.from_file('grid.txt'))

        running = True
        while running:
            # цикл для получения событий игры
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            clist.draw_cell_list(self.screen, self.cell_size)

            # обновить клетки
            clist = deepcopy(clist.update())

            # рисуется сетка
            self.draw_grid()

            # обновить полный экран
            pygame.display.flip()
            # обновить время (в зависимости от скорости протекания игры)
            clock.tick(self.speed)

        pygame.quit()


class Cell:
    """ класс - клетка
    """

    def __init__(self, row: int, col: int, state: bool = False) -> None:
        self.row = row
        self.col = col
        self.state = state

    def is_alive(self) -> bool:
        return self.state


class CellList:
    """ заполнение списка клеток данными из файла
    """

    def __init__(self, nrows: int, ncols: int, randomize: bool = False) -> None:
        self.nrows = nrows
        self.ncols = ncols
        self.cur_cell = Cell(0, 0)
        # создадим пустой список клеток
        self.clist = []
        self.cell_list(randomize)

    def cell_list(self, randomize: bool = False) -> tuple:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1.
        В противном случае клетка считается мертвой, то
        есть ее значение равно 0.
        Если параметр randomize = True, то создается список, где
        каждая клетка может быть равновероятно живой или мертвой.
        """
        i = 0
        # создадим  список клеток
        if not randomize:
            self.clist = [[Cell(i, j, 0) for j in range(self.ncols)]
                          for i in range(self.nrows)]
        else:
            self.clist = [[Cell(i, j, random.randint(0, 1)) for j in range(self.ncols)]
                          for i in range(self.nrows)]

    def get_neighbours(self, cell: Cell) -> list:
        # создание списка соседей
        neighbours = []
        row = cell.row
        col = cell.col

        # получить значение слева
        if col > 0:
            neighbours.append(self.clist[row][col - 1])
        # получить значение справа
        if col < (self.ncols - 1):
            neighbours.append(self.clist[row][col + 1])
        # получить значение сверху
        if row > 0:
            neighbours.append(self.clist[row - 1][col])
        # получить значение снизу
        if row < (self.nrows - 1):
            neighbours.append(self.clist[row + 1][col])
        # получить значение слева снизу по диагонали
        if row < (self.nrows - 1) and col > 0:
            neighbours.append(self.clist[row + 1][col - 1])
        # получить значение справа снизу по диагонали
        if row < (self.nrows - 1) and col < (self.ncols - 1):
            neighbours.append(self.clist[row + 1][col + 1])
        # получить значение слева сверху по диагонали
        if row > 0 and col > 0:
            neighbours.append(self.clist[row - 1][col - 1])
        # получить значение справа сверху по диагонали
        if row > 0 and col < (self.ncols - 1):
            neighbours.append(self.clist[row - 1][col + 1])

        return neighbours

    def update(self) -> object:
        """ Выполнить один шаг игры.

        Обновление всех ячеек происходит одновременно. Функция возвращает
        новое игровое поле.

        :return: Обновленное игровое поле
        """

        new_clist = deepcopy(self.clist)

        for row in range(self.nrows):
            for col in range(self.ncols):
                cell = (self.clist[row][col])
                # получить список соседей
                lst_n = self.get_neighbours(cell)
                # перебор ячеек с накоплением суммы живых ячеек. если ячейка живая, +1
                res = 0
                for idx in lst_n:
                    if idx.is_alive():
                        res += 1
                # если соседей меньше 2 или больше 3, в след. поколении клетка мертва
                if res < 2 or res > 3:
                    new_clist[row][col].state = 0
                # если  3 соседа, в след. поколении в клетке живое существо
                elif res == 3:
                    new_clist[row][col].state = 1

        self.clist = deepcopy(new_clist)

        return self

    def draw_cell_list(self, screen: SWSURFACE, cell_size: int) -> None:
        """
        Отображение списка клеток 'rects' с закрашиванием их в
        соответствующе цвета
        """
        x = 0
        y = 0
        for row in range(self.nrows):
            x = 0
            # перебор элеметов внутреннего списка
            for col in range(self.ncols):
                # создание ячейки rect для внутреннего списка
                rect1 = pygame.Rect((x, y, cell_size, cell_size))
                cell = self.clist[row][col]
                # раскрасить ячейку нужным цветом
                if cell.is_alive():
                    pygame.draw.rect(screen, pygame.Color('green'), rect1)
                else:
                    pygame.draw.rect(screen, pygame.Color('white'), rect1)

                # увеличение значения по оси x
                x += cell_size

            # увеличение значения по оси y
            y += cell_size

    def __iter__(self):
        """
        инициализация итератора
        """
        self.cur_cell.row = 0
        self.cur_cell.col = 0
        return self

    def __next__(self) -> Cell:
        if self.cur_cell.row < self.nrows:
            cell = self.clist[self.cur_cell.row][self.cur_cell.col]
            self.cur_cell.col += 1
            if self.cur_cell.col == self.ncols:
                self.cur_cell.row += 1
                self.cur_cell.col = 0
            return cell
        else:
            raise StopIteration

    def __str__(self) -> str:
        str = ''
        for i in range(self.nrows):
            for j in range(self.ncols):
                if self.clist[i][j].state:
                    str += '1 '
                else:
                    str += '0 '
            str += '\n'
        return str

    @classmethod
    def from_file(cls, filename: str):
        lst = []
        # with даёт автоматическое открытие и корректное закрытие файла
        with open(filename) as file:

            for i, line in enumerate(file):
                lst_width = []
                j = 0
                for val in line:
                    if val not in "\n":
                        lst_width.append(Cell(i, j, int(val)))
                    j += 1
                lst.append(lst_width)
        # создание экземплляра класса CellList с установкой значений количества строк и столбцов
        cell_list = CellList(i + 1, j - 1, False)
        cell_list.clist = lst

        return cell_list


if __name__ == '__main__':
    game = GameOfLife(320, 240, 20)
    game.run()
