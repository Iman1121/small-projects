
sudoku = [
    [0,6,8,0,0,0,0,0,0],
    [1,9,0,6,3,0,4,5,2],
    [3,0,0,0,5,0,7,0,6],
    [0,0,0,0,1,0,0,0,3],
    [8,5,0,0,9,4,6,2,0],
    [4,0,3,0,0,0,0,0,0],
    [6,0,0,1,2,3,0,0,0],
    [7,3,0,5,0,9,0,6,1],
    [0,0,0,7,4,6,0,3,5]
]
def possible(row, column, number):
    global sudoku
    x = column//3*3
    y = row//3*3
    for i in range(0,9):
        if sudoku[row][i] == number:
            return False
    for i in range(9):
        if sudoku[i][column] == number:
            return False
    for i in range(0,3):
        for j in range(0,3):
            if sudoku[y+i][x+i] == number:
                return False
    return True

def solve():
    global sudoku
    for row in range(0,9):
        for column in range(0,9):
            if sudoku[row][column] == 0:
                for num in range(1,10):
                    if possible(row, column, num):
                        
                        sudoku[row][column] = num
                        solve()
                        sudoku[row][column] = 0
                return
    print(sudoku)
    input("More?")
                   


solve()