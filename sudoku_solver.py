def get_column(array, col):
    column = []
    for row in array:
        column.append(row[col])
    return column


def check_square(array, row_num, col_num):
    nums = []
    k = row_num // 3
    l = col_num // 3
    for row in range(k * 3, k * 3 + 3):
        for col in range(l * 3, l * 3 + 3):
            if array[row][col] > 0:
                nums.append(array[row][col])
    return nums


def check_possible(nums, possible_nums):
    return [x for x in possible_nums if x not in nums]


def count_elements(array):
    return sum(x > 0 for row in array for x in row)


def sudoku(puzzle):
    possible_nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    solved_cells = count_elements(puzzle)
    while solved_cells < 81:
        for row_num, row in enumerate(puzzle):
            for col_num, cell in enumerate(row):
                if cell == 0:
                    temp = check_possible(check_square(puzzle, row_num, col_num), possible_nums)
                    temp = check_possible(get_column(puzzle, col_num), temp)
                    temp = check_possible(row, temp)
                    if len(temp) == 1:
                        puzzle[row_num][col_num] = temp[0]
                        solved_cells = count_elements(puzzle)
    return puzzle


puzzle = [[5,3,0,0,7,0,0,0,0],
          [6,0,0,1,9,5,0,0,0],
          [0,9,8,0,0,0,0,6,0],
          [8,0,0,0,6,0,0,0,3],
          [4,0,0,8,0,3,0,0,1],
          [7,0,0,0,2,0,0,0,6],
          [0,6,0,0,0,0,2,8,0],
          [0,0,0,4,1,9,0,0,5],
          [0,0,0,0,8,0,0,7,9]]

# print(get_column(puzzle, 0))

# print(get_nums([0,1,0,2,0,3]))

sudoku(puzzle)