from collections import Counter


class SudokuSolutions:
    def __init__(self):
        self.solutions = []

    def add_solution(self, row_num, col_num, possible_nums):
        self.solutions.append([row_num, col_num, possible_nums])

    def get_shortest(self):
        # temp = self.solutions
        print('before sort', self.solutions[0])
        self.solutions.sort(key=lambda x: len(x[2]))
        print('shortest sol', self.solutions[0])
        return self.solutions[0]


def get_column(array, col):
    """Transforms column to line"""
    column = []
    for row in array:
        column.append(row[col])
    return column


def check_duplicates(numbers):
    return Counter(numbers).values()


def get_square(array, row_num, col_num):
    """Returns numbers in corresponding square"""
    nums = []
    k = row_num // 3
    l = col_num // 3
    for row in range(k * 3, k * 3 + 3):
        for col in range(l * 3, l * 3 + 3):
            if array[row][col] > 0:
                nums.append(array[row][col])
    return nums


def check_possible(nums, possible_nums):
    """Gets possible nums in line/column/square and existing ones.
    Return numbers what are possible to be addded"""
    return [x for x in possible_nums if x not in nums]


def count_elements(array):
    """Return number of non-zero elements in array"""
    return sum(x > 0 for row in array for x in row)


def sudoku(puzzle):
    possible_nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    solved_cells = count_elements(puzzle)
    while solved_cells < 81:
        solutions = SudokuSolutions()
        for row_num, row in enumerate(puzzle):
            for col_num, cell in enumerate(row):
                if cell == 0:
                    temp = check_possible(get_square(puzzle, row_num, col_num), possible_nums)
                    temp = check_possible(get_column(puzzle, col_num), temp)
                    temp = check_possible(row, temp)
                    if temp:
                        solutions.add_solution(row_num, col_num, temp)
                    print(row_num, col_num, temp)
                    # if len(temp) == 1:
                    #     puzzle[row_num][col_num] = temp[0]
                    #     solved_cells = count_elements(puzzle)
        temp = solutions.get_shortest()
        # print(temp)
        # print(type(temp))
        puzzle[temp[0]][temp[1]] = temp[2][0]
        solved_cells = count_elements(puzzle)
        print(puzzle)
    return puzzle


def done_or_not(board):
    """Return True if the puzzle is solved correctly.
    Return False if there is a mistake"""
    for row_num, row in enumerate(board):
        for col_num, cell in enumerate(row):
            temp1 = Counter(row).values()
            temp2 = Counter(get_column(board, col_num)).values()
            temp3 = Counter(get_square(board, row_num, col_num)).values()
            if len(temp1) < 9 or len(temp2) < 9 or len(temp3) < 9:
                return False
    return True


problem = [[9, 0, 0, 0, 8, 0, 0, 0, 1],
 [0, 0, 0, 4, 0, 6, 0, 0, 0],
 [0, 0, 5, 0, 7, 0, 3, 0, 0],
 [0, 6, 0, 0, 0, 0, 0, 4, 0],
 [4, 0, 1, 0, 6, 0, 5, 0, 8],
 [0, 9, 0, 0, 0, 0, 0, 2, 0],
 [0, 0, 7, 0, 3, 0, 2, 0, 0],
 [0, 0, 0, 7, 0, 5, 0, 0, 0],
 [1, 0, 0, 0, 4, 0, 0, 0, 7]]

print(sudoku(problem))
