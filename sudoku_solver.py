import numpy as np


# TODO: make improvements in performance


class SudokuCell:

    def __init__(self, n_row, n_col, val=0):
        self.n_row = n_row  # number of row of cell
        self.n_col = n_col  # number of column of cell
        self.val = val  # value of cell
        self.solved = bool(val)  # flag if cell is already solved
        self.possible_vals = list(range(1, 10))  # possible values for current cell
        self.tried_vals = []  # values already tried in current run

    def next_value(self):
        vals_to_choose_from = [val for val in self.possible_vals if val not in self.tried_vals]
        temp = len(vals_to_choose_from)
        next_value = vals_to_choose_from.pop()
        self.possible_vals.remove(next_value)
        self.val = next_value
        self.tried_vals.append(next_value)
        return temp


class SudokuBoard:

    def __init__(self, board):
        self.board = board
        self.cells = []  # initializing cells
        self.cells = np.empty(shape=(9, 9), dtype=object)
        for row_num, row in enumerate(board):  # filling cells with values from board list of lists
            for col_num, value in enumerate(row):
                self.cells[row_num, col_num] = SudokuCell(row_num, col_num, val=board[row_num][col_num])
        self.cursor = [0, 0]  # current position of cursor for solving
        self.turns = []
        self.solved_board = board

    def get_row(self, row_num):
        return [cell.val for cell in self.cells[row_num, :] if cell.val]  # get list of non-zero values in row

    def get_col(self, col_num):
        return [cell.val for cell in self.cells[:, col_num] if cell.val]  # get list of non-zero values in column

    def get_square(self, sq_num):  # get list of non-zero values in 3*3 square
        nums = []
        start_row = (sq_num // 3) * 3  # starting row of corresponding square
        start_col = (sq_num % 3) * 3  # starting col of corresponding square

        for row in range(start_row, start_row + 3):
            for col in range(start_col, start_col + 3):
                if self.cells[row, col].val:
                    nums.append(self.cells[row, col].val)
        return nums

    def convert_to_square(self):  # convert row and col num to square number
        return (self.cursor[0] // 3) * 3 + self.cursor[1] // 3

    def update_possible_vals(self):
        for r in range(self.cursor[0], 9):  # check each row
            row = self.get_row(r)  # get non-zero values from each row

            for c in range(self.cursor[1], 9):
                self.cells[r, c].possible_vals = [val for val in self.cells[r, c].possible_vals if val not in row]

        for c in range(self.cursor[1], 9):  # check each column
            col = self.get_col(c)  # get non-zero values from each row

            for r in range(self.cursor[0], 9):
                self.cells[r, c].possible_vals = [val for val in self.cells[r, c].possible_vals if val not in col]

        for sq in range(self.convert_to_square(), 9):
            square = self.get_square(sq)  # get non-zero values from each 3*3 square

            start_row = (sq // 3) * 3
            start_col = (sq % 3) * 3

            end_row = start_row + 3  # get ending row for current square
            end_col = start_col + 3  # get ending column for current square

            if start_row < self.cursor[0]:
                start_row = self.cursor[0]
            if start_col < self.cursor[1]:
                start_col = self.cursor[1]

            for r in range(start_row, end_row):
                for c in range(start_col, end_col):
                    self.cells[r, c].possible_vals = [val for val in self.cells[r, c].possible_vals if val not in square]
                    if not self.cells[r, c].possible_vals and not self.cells[r, c].solved:
                        return False  # no further solution is possible
        return True  # solution is still possible

    def put_next_val(self):
        if self.cells[self.cursor[0], self.cursor[1]].possible_vals:
            if self.cells[self.cursor[0], self.cursor[1]].next_value() > 1:
                self.turns.append([self.cursor[0], self.cursor[1]])
            return True
        else:
            return False

    def come_back(self):
        last_turn = self.turns.pop()
        self.cursor = last_turn.copy()

    def move_cursor(self):

        if self.cursor[1] < 8:
            self.cursor[1] += 1
            return True
        else:
            if self.cursor[0] < 8:
                self.cursor[0] += 1
                self.cursor[1] = 0
                return True
            else:
                return False  # cursor out of bounds

    def is_solved(self):
        for row in self.cells[self.cursor[0]:, self.cursor[1]:]:
            for cell in row:
                if not cell.val:
                    return False
        return True

    def reinitialize(self):
        last_position = self.cursor.copy()
        while self.move_cursor():
            self.cells[self.cursor[0], self.cursor[1]] = \
                SudokuCell(self.cursor[0], self.cursor[1], val=self.board[self.cursor[0]][self.cursor[1]])
        self.cursor = last_position.copy()

    def __str__(self):
        solved_board = np.zeros((9, 9))
        for row in self.cells:
            for cell in row:
                solved_board[cell.n_row, cell.n_col] = cell.val
        self.solved_board = solved_board
        return f'{self.solved_board}'


def solve(board):
    sudoku_board = SudokuBoard(board)
    sudoku_board.update_possible_vals()
    while not sudoku_board.is_solved():
        row, col = sudoku_board.cursor[0], sudoku_board.cursor[1]
        if sudoku_board.cells[row, col].solved:
            sudoku_board.move_cursor()
        else:
            if sudoku_board.put_next_val():
                sudoku_board.move_cursor()
                if not sudoku_board.update_possible_vals():
                    sudoku_board.come_back()
                    sudoku_board.reinitialize()
            else:
                sudoku_board.come_back()
                sudoku_board.reinitialize()
    return sudoku_board.__str__()


problem = [[9, 0, 0, 0, 8, 0, 0, 0, 1],
           [0, 0, 0, 4, 0, 6, 0, 0, 0],
           [0, 0, 5, 0, 7, 0, 3, 0, 0],
           [0, 6, 0, 0, 0, 0, 0, 4, 0],
           [4, 0, 1, 0, 6, 0, 5, 0, 8],
           [0, 9, 0, 0, 0, 0, 0, 2, 0],
           [0, 0, 7, 0, 3, 0, 2, 0, 0],
           [0, 0, 0, 7, 0, 5, 0, 0, 0],
           [1, 0, 0, 0, 4, 0, 0, 0, 7]]


print(solve(problem))
