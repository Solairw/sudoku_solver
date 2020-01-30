from collections import Counter
import pdb
import copy
import numpy as np

possible_vals = list(range(1, 10)) # possible values for any Sudoku cell

# class SudokuSolutions:
#     def __init__(self):
#         self.solutions = []
#
#     def add_solution(self, row_num, col_num, possible_nums):
#         self.solutions.append([row_num, col_num, possible_nums])
#
#     def get_shortest(self):
#         # temp = self.solutions
#         print('before sort', self.solutions[0])
#         self.solutions.sort(key=lambda x: len(x[2]))
#         print('shortest sol', self.solutions[0])
#         return self.solutions[0]
#
#
# def is_solvable(board):
#     """Return True if board is solvable; return False if not"""
#     possible_nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
#     for row_num, row in enumerate(board):
#         deck = []
#         for col_num, cell in enumerate(row):
#             if cell > 0:
#                 deck.append(cell)
#             else:
#                 temp = check_possible(get_square(board, row_num, col_num), possible_nums)
#                 temp = check_possible(get_column(board, col_num), temp)
#                 temp = check_possible(row, temp)
#                 deck += temp
#         if list(set(deck)) != possible_nums:
#             print('false', row_num, col_num, set(deck))
#             return [False, row_num]
#     return [True]
#     # for col_num, cell in enumerate(row):
#     #     if cell == 0:
#     #         temp = check_possible(get_square(board, row_num, col_num), possible_nums)
#     #         temp = check_possible(get_column(board, col_num), temp)
#     #         temp = check_possible(row, temp)
#     #     else:
#
#
# def get_column(array, col):
#     """Transforms column to line"""
#     column = []
#     for row in array:
#         column.append(row[col])
#     return column
#
#
# def check_duplicates(numbers):
#     return Counter(numbers).values()
#
#
# def get_square(array, row_num, col_num):
#     """Returns numbers in corresponding square"""
#     nums = []
#     k = row_num // 3
#     l = col_num // 3
#     for row in range(k * 3, k * 3 + 3):
#         for col in range(l * 3, l * 3 + 3):
#             if array[row][col] > 0:
#                 nums.append(array[row][col])
#     return nums
#
#
# def check_possible(nums, possible_nums):
#     """Gets possible nums in line/column/square and existing ones.
#     Return numbers what are possible to be added"""
#     return [x for x in possible_nums if x not in nums]
#
#
# def count_elements(array):
#     """Return number of non-zero elements in array"""
#     return sum(x > 0 for row in array for x in row)


# def sudoku(puzzle):
#     original_puzzle = copy.deepcopy(puzzle)
#     possible_nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
#     # original_puzzle[2] is puzzle[2]
#     # pdb.set_trace()
#     solved_cells = count_elements(puzzle)
#     while solved_cells < 81:
#         solutions = SudokuSolutions()
#         for row_num, row in enumerate(puzzle):
#             for col_num, cell in enumerate(row):
#                 if cell == 0:
#                     temp = check_possible(get_square(puzzle, row_num, col_num), possible_nums)
#                     temp = check_possible(get_column(puzzle, col_num), temp)
#                     temp = check_possible(row, temp)
#                     if temp:
#                         solutions.add_solution(row_num, col_num, temp)
#                     print(row_num, col_num, temp)
#                     # if len(temp) == 1:
#                     #     puzzle[row_num][col_num] = temp[0]
#                     #     solved_cells = count_elements(puzzle)
#         temp = solutions.get_shortest()
#         # print(temp)
#         # print(type(temp))
#         candidate = temp[2].pop()
#         puzzle[temp[0]][temp[1]] = candidate
#         while True:
#             output = is_solvable(puzzle)
#             if not output[0]:
#                 if temp[2]:
#                     candidate = temp[2].pop()
#                     puzzle[temp[0]][temp[1]] = candidate
#                 else:
#                     print('orig', original_puzzle[output[1]])
#                     print('output1', output[1])
#                     # puzzle[output[1]] = original_puzzle[output[1]].copy()
#                     puzzle[temp[0]] = original_puzzle[temp[0]].copy()
#                     if not is_solvable(puzzle)[0]:
#                         pdb.set_trace()
#             else:
#                 break
#         solved_cells = count_elements(puzzle)
#         print(puzzle)
#     return puzzle
#
#
# def done_or_not(board):
#     """Return True if the puzzle is solved correctly.
#     Return False if there is a mistake"""
#     for row_num, row in enumerate(board):
#         for col_num, cell in enumerate(row):
#             temp1 = Counter(row).values()
#             temp2 = Counter(get_column(board, col_num)).values()
#             temp3 = Counter(get_square(board, row_num, col_num)).values()
#             if len(temp1) < 9 or len(temp2) < 9 or len(temp3) < 9:
#                 return False
#     return True
#
#
# # class SudokuLine:
# #     def __init__(self, line, n_row, n_col):
# #         self.line = line
# #         self.n_row = n_row
# #         self.n_col = n_col
#
# class InvalidVal(Exception):
#     """Raise this when the value is invalid"""
#     pass

class CursorOutOfBounds(Exception):
    """Raise this when the cursor goes out of bound"""
    pass


class SudokuCell:

    def __init__(self, n_row, n_col, val=0):
        self.n_row = n_row  # number of row of cell
        self.n_col = n_col  # number of column of cell
        self.val = val  # value of cell
        self.solved = bool(val)  # flag if cell is already solved
        self.possible_vals = list(range(1, 10))  # possible values for current cell
        if val:
            self.possible_vals.remove(val)
        self.tried_vals = []  # values already tried in current run

    def next_value(self):
        vals_to_choose_from = [val for val in self.possible_vals if val not in self.tried_vals]
        next_value = vals_to_choose_from[0]
        self.possible_vals.remove(next_value)
        self.val = next_value
        self.tried_vals.append(next_value)
        return len(vals_to_choose_from)


class SudokuBoard:

    def __init__(self, board):
        self.board = board
        self.cells = []  # initializing cells
        self.cells = np.empty(shape=(9, 9), dtype=object)
        # self.cells = np.zeros((9, 9))  # filling cells with zeros
        for row_num, row in enumerate(board):  # filling cells with values from board list of lists
            for col_num, value in enumerate(row):
                self.cells[row_num, col_num] = SudokuCell(row_num, col_num, board[row_num][col_num])
        self.cursor = [0, 0]  # current position of cursor for solving
        self.turns = []
        self.solved = False
        self.printed = None
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
            row = self.get_row(r)
            for c in range(self.cursor[1], 9):
                self.cells[r, c].possible_vals = [val for val in self.cells[r, c].possible_vals if val not in row]

        for c in range(self.cursor[1], 9):  # check each column
            col = self.get_col(c)
            for r in range(self.cursor[0], 9):
                self.cells[r, c].possible_vals = [val for val in self.cells[r, c].possible_vals if val not in col]

        for sq in range(self.convert_to_square(), 9):
            square = self.get_square(sq)
            if sq == self.convert_to_square():  # check if current square represent position of cursor
                start_row = self.cursor[0]
                start_col = self.cursor[1]
            else:
                start_row = (sq // 3) * 3
                start_col = (sq % 3) * 3
            end_row = (sq // 3) * 3 + 3  # get ending row for current square
            end_col = (sq % 3) * 3 + 3  # get ending column for current square
            for r in range(start_row, end_row):
                for c in range(start_col, end_col):
                    self.cells[r, c].possible_vals = [val for val in self.cells[r, c].possible_vals if val not in square]

    def put_next_val(self):
        if self.cells[self.cursor[0], self.cursor[1]].possible_vals:
            if self.cells[self.cursor[0], self.cursor[1]].next_value() > 1:
                self.turns.append([self.cursor[0], self.cursor[1]])
            return True
        else:
            return False

    def come_back(self):
        print(self.turns)
        print(self)
        last_turn = self.turns.pop()
        self.cursor = last_turn.copy()

    def move_cursor(self):
        if self.cursor[1] < 8:
            self.cursor[1] += 1
            return True
        else:
            if self.cursor[0] < 8:
                self.cursor[1] = 0
                self.cursor[0] += 1
                return True
            else:
                return False  # cursor out of bounds
                # raise CursorOutOfBounds

    def reinitialize(self):
        last_position = self.cursor.copy()
        while self.move_cursor():
            self.cells[self.cursor[0], self.cursor[1]] = \
                SudokuCell(self.cursor[0], self.cursor[1], self.board[self.cursor[0]][self.cursor[1]])
        self.cursor = last_position.copy()

    def __str__(self):
        solved_board = np.zeros((9, 9))
        for row in self.cells:
            for cell in row:
                solved_board[cell.n_row, cell.n_col] = cell.val
        self.solved_board = solved_board
        return f'{self.solved_board}'


problem = [[9, 0, 0, 0, 8, 0, 0, 0, 1],
           [0, 0, 0, 4, 0, 6, 0, 0, 0],
           [0, 0, 5, 0, 7, 0, 3, 0, 0],
           [0, 6, 0, 0, 0, 0, 0, 4, 0],
           [4, 0, 1, 0, 6, 0, 5, 0, 8],
           [0, 9, 0, 0, 0, 0, 0, 2, 0],
           [0, 0, 7, 0, 3, 0, 2, 0, 0],
           [0, 0, 0, 7, 0, 5, 0, 0, 0],
           [1, 0, 0, 0, 4, 0, 0, 0, 7]]

# print(sudoku(problem))

sudoku_board = SudokuBoard(problem)
sudoku_board.update_possible_vals()
# while sudoku_board.cursor[0] < 8 or sudoku_board.cursor[1] < 8:
while sudoku_board.cursor[0] < 8:
    row, col = sudoku_board.cursor[0], sudoku_board.cursor[1]
    if sudoku_board.cells[row, col].solved:
        sudoku_board.move_cursor()
    else:
        if sudoku_board.put_next_val():
            sudoku_board.move_cursor()
            sudoku_board.update_possible_vals()
        else:
            sudoku_board.come_back()
            sudoku_board.reinitialize()

print(sudoku_board)