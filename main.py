# Press the green button in the gutter to run the script.
import random


# Crear tablero
class Cell:
    def __init__(self, row, col):
        self.bomb = False
        self.hidden = True
        self.proximity = None
        self.marked = False

    def set_bomb(self):
        self.bomb = True

    def set_proximity(self, value):
        self.proximity = value

    def increase_danger(self):
        if not self.proximity:
            self.proximity = 0
        self.proximity += 1

    def set_visible(self):
        self.hidden = False

    def toStr(self, show=False):
        if not self.hidden or show:
            if not self.bomb:
                return ' ' + str(self.proximity or 0) + ' '
            else:
                return " * "
        elif self.marked:
            return ":::"
        else:
            return "   "


class Board:
    def __init__(self, size, test):

        if test:
            self.size = 10
        else:
            self.size = size
        self.matriz = [[Cell(i, j) for j in range(self.size)] for i in range(self.size)]
        if test:
            self.put_mines_test()
        else:
            self.put_mines()
        self.hidden_pos = self.size * self.size

    def put_mines(self):
        mines = 0
        for i in range(self.size):
            for j in range(self.size):
                if not (2 < i < 7 and 3 < j < 7):
                    if random.randint(0, 1) > 0 and i > 0 and j > 0:
                        self.matriz[i][j].set_bomb()
                        mines += 1
        print(f"--------- Total mines: {mines} ---------")

    def put_mines_test(self):
        bombs_positions = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
            [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        ]
        mines = 0

        for i in range(10):
            for j in range(10):
                if bombs_positions[i][j] == 1:
                    self.matriz[i][j].set_bomb()
                    mines += 1
        self.print_board(True)
        print(f"--------- Total mines: {mines} ---------")

    def get_available_spots(self):
        available = 0
        for row in self.matriz:
            for cell in row:
                if cell.hidden and not cell.bomb:
                    available += 1
        return available

    def print_board(self, show_all=False):
        columns = [str(i) + "   " for i in range(self.size)]
        print(4 * ' ' + ''.join(columns) + 3 * ' ')
        print(3 * '-' + self.size * '----' + '-')
        for row_idx, row in enumerate(self.matriz):
            row_str = ""
            for col_idx, col in enumerate(self.matriz[row_idx]):
                row_str += self.matriz[row_idx][col_idx].toStr(show_all) + '|'
            print(str(row_idx) + ' |' + row_str)

    def pick(self):
        print("Use m0,0 format to mark mines or unmark mines.")
        picking_pos = input("Where would you like to dig? Input as row, col: 0,0")

        mark = False
        if picking_pos.startswith('m'):
            picking_pos = picking_pos.lstrip('m')
            mark = True

        [row, col] = map(lambda idx: int(idx), picking_pos.replace(" ", "").split(","))
        if mark:
            self.matriz[row][col].marked = not self.matriz[row][col].marked
            return

        if not self.matriz[row][col].hidden:
            print("That spot is already discovered! Pick again!")
            self.pick()

        self.matriz[row][col].set_visible()
        if self.matriz[row][col].bomb:
            self.print_board()
            print("Game Over!")
            self.hidden_pos = 0
        else:
            self.calc_proximity(row, col)
            self.print_board()

        if self.get_available_spots() == 0:
            print("Congratulations, you won the game!")
            self.hidden_pos = 0

    def calc_proximity(self, x, y):
        self.matriz[x][y].hidden = False
        self.matriz[x][y].set_proximity(0)
        for row in range(-1, 2):
            nex_row = x + row
            if 0 <= nex_row <= self.size - 1:
                for col in range(-1, 2):
                    next_col = y + col
                    if 0 <= next_col <= self.size - 1:
                        if self.matriz[nex_row][next_col].bomb:
                            self.matriz[x][y].increase_danger()

        if self.matriz[x][y].proximity == 0:
            for (row, col) in self.get_ady(x,y):
                if self.matriz[row][col].proximity is None:
                    self.calc_proximity(row, col)

    def get_ady(self, x, y):
        ady = list()
        if x > 0:
            ady.append((x - 1, y))
        if x < self.size - 1:
            ady.append((x + 1, y))
        if y > 0:
            ady.append((x, y - 1))
        if y < self.size - 1:
            ady.append((x, y + 1))
        return ady

    def calc_hidden_pos(self):
        cant = 0
        for i in range(self.matriz.count()):
            for j in range(self.matriz[i].count()):
                if not self.matriz[i][j].visible:
                    cant += 1
        self.hidden_pos = cant

    def start(self):
        while self.hidden_pos > 0:
            board.print_board()
            board.pick()
        board.print_board(True)


if __name__ == '__main__':
    board = Board(10, False)
    board.start()
