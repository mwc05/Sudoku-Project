import random
# import math

class SudokuGenerator:
    def __init__(self, row_length, removed_cells):
        self.removed_cells = removed_cells
        self.row_length = row_length
        self.box_length = self.row_length**0.5
        self.board = [[0]*self.row_length for _ in range(self.row_length)]

    # def clone(self):
    #     new_sudoku = SudokuGenerator(self.row_length, self.removed_cells)
    #     new_sudoku.board = self.board
    #     return new_sudoku

    def get_board(self):
        return self.board

    def print_board(self):
        for i in self.board:
            print(*i)

    def valid_in_row(self, row, num):
        return num not in self.board[row]

    def valid_in_col(self, col, num):
        col_vals = [i[int(col)] for i in self.board]
        return num not in col_vals

    def valid_in_box(self, row_start, col_start, num):
        box = [i[col_start:col_start+3] for i in self.board[row_start:row_start+3]]
        return num not in [i for x in box for i in x]

    def is_valid(self, row, col, num):
        return self.valid_in_box(max(i for i in [0,3,6] if i <= row), max(i for i in [0,3,6] if i <= col), num) & self.valid_in_col(col, num) & self.valid_in_row(row, num)

    def fill_box(self, row_start, col_start):
        random_list = [i for i in range(1,10)]
        random.shuffle(random_list)
        self.board[row_start][col_start:col_start+3] = random_list[0:3]
        self.board[row_start+1][col_start:col_start+3] = random_list[3:6]
        self.board[row_start+2][col_start:col_start+3] = random_list[6:]

    def fill_diagonal(self):
        self.fill_box(0, 0)
        self.fill_box(3, 3)
        self.fill_box(6, 6)

    def fill_remaining(self, row, col):
        if col >= self.row_length and row < self.row_length - 1:
            row += 1
            col = 0
        if row >= self.row_length and col >= self.row_length:
            return True
        if row < self.box_length:
            if col < self.box_length:
                col = self.box_length
        elif row < self.row_length - self.box_length:
            if col == int(row // self.box_length * self.box_length):
                col += self.box_length
        else:
            if col == self.row_length - self.box_length:
                row += 1
                col = 0
                if row >= self.row_length:
                    return True
        
        for num in range(1, self.row_length + 1):
            if self.is_valid(row, col, num):
                self.board[int(row)][int(col)] = num
                if self.fill_remaining(row, col + 1):
                    return True
                self.board[int(row)][int(col)] = 0
        return False

    def fill_values(self):
        self.fill_diagonal()
        self.fill_remaining(0, self.box_length)

    def remove_cells(self):
        remove_coordinates = []
        while len(remove_coordinates) < self.removed_cells:
            temp_coordinate = (random.randint(0, self.row_length-1), random.randint(0, self.row_length-1))
            if temp_coordinate not in remove_coordinates:
                remove_coordinates.append(temp_coordinate)
        for i in remove_coordinates:
            self.board[i[0]][i[1]] = 0


def generate_sudoku(size, removed):
    sudoku = SudokuGenerator(size, removed)
    sudoku.fill_values()
    board = sudoku.get_board()
    sudoku.remove_cells()
    board = sudoku.get_board()
    return board
