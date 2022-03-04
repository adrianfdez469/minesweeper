# Press the green button in the gutter to run the script.
import random


# Crear tablero
class Cell:
    def __init__(self, row, col):
        self.bomb = False
        self.hidden = True
        self.proximity = 0

    def set_bomb(self):
        self.bomb = True

    def set_proximity(self, value):
        self.proximity = value

    def set_visible(self):
        self.hidden = False

    def toStr(self, show=False):
        if not self.hidden or show:
            if not self.bomb:
                return ' ' + str(self.proximity) + ' '
            else:
                return " * "
        else:
            return "   "


class Board:
    def __init__(self, size):
        self.matriz = [[Cell(i, j) for j in range(size)] for i in range(size)]
        mines = 0
        for i in range(size):
            for j in range(size):
                if random.randint(0, 1) > 0 and i > 0 and j > 0:
                    self.matriz[i][j].set_bomb()
                    mines += 1
        print(f"--------- Total mines: {mines} ---------")
        self.hidden_pos = size * size

    def print_board(self, show_all=False):
        columns = [str(i) + "   " for i in range(len(self.matriz))]
        print(4 * ' ' + ''.join(columns) + 3 * ' ')
        print(3 * '-' + (len(self.matriz))*'----' + '-')
        for row_idx, row in enumerate(self.matriz):
            row_str = ""
            for col_idx, col in enumerate(self.matriz[row_idx]):
                row_str += self.matriz[row_idx][col_idx].toStr(show_all) + '|'
            print(str(row_idx) + ' |' + row_str)

    def pick(self):
        picking_pos = input("Where would you like to dig? Input as row, col: 0,0 ")
        [row, col] = map(lambda idx: int(idx), picking_pos.replace(" ", "").split(","))

        self.matriz[row][col].set_visible()
        if self.matriz[row][col].bomb:
            self.print_board()
            print("Game Over!")
            self.hidden_pos = 0
        else:
            proximity = self.calc_proximity(row, col)
            self.matriz[row][col].set_proximity(proximity)
            self.matriz[row][col].set_visible()
            self.calc_hidden_pos()
            self.print_board()

    def calc_proximity(self, x, y):
        ady = self.get_ady(x, y)
        proximity = 0
        for (cell_x, cell_y) in ady:
            print(cell_x, cell_y)
            if self.matriz[cell_x][cell_y].bomb:
                proximity += 1
            else:
                self.matriz[cell_x][cell_y].set_visible()
                self.calc_proximity(cell_x, cell_y)
        return proximity


    def get_ady(self, x, y):
        ady = list()
        for i in range(-1, 2):
            if 0 <= x + i <= len(self.matriz) - 1:
                for j in range(-1, 2):
                    if 0 <= x + j <= len(self.matriz[i]) - 1:
                        ady.append((x+i, x+j))
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
    board = Board(10)
    board.start()

