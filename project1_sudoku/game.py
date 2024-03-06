from sudoku import Sudoku
import queue
import copy
import math
import time
import timeit

'''
Parameters: Takes as input the curr_board state and the puzzle
Returns: True if the current board state is the goal and False if not
Note: Existing version solves the puzzle everytime you test for goal
      feel free to change the implementation to save time
'''
def test_goal(curr_board,puzzle):
    puzzle_solution=puzzle.solve()
    try:
        solution_board=puzzle_solution.board
        for i in range(len(solution_board)):
            for j in range(len(solution_board[i])):
                assert(curr_board[i][j]==solution_board[i][j])
        return True
    except Exception as e:
        return False

'''
Parameters: Takes as input a puzzle board and puzzle size
Returns: True if the puzzle board is valid and False if not
'''    
def valid_puzzle(puzzle_size,puzzle_board):
    puzzle=Sudoku(puzzle_size,board=puzzle_board)
    return puzzle.validate()

'''
Parameters: Takes as input a puzzle board
Returns: Returns all the cells in the grid that are empty
'''
def empty_cells(puzzle_board):
    empty_cell_list=[]
    for i in range(len(puzzle_board)):
        for j in range(len(puzzle_board[i])):
            if puzzle_board[i][j] is None:
                empty_cell_list.append([i,j])
    return empty_cell_list

'''
params: Takes the current puzzle as input
Return: The puzzle board corresponding to the goal
Note: You can modify the function definition as you see fit
'''
def bfs(puzzle, board):
    #Write Code here
    frontier = queue.Queue()
    frontier.put(board)

    while not frontier.empty():
        curr_board = frontier.get()
        if test_goal(curr_board, puzzle):
            return curr_board

        for empty_cell in empty_cells(curr_board):
            for i in range(1,puzzle.size + 1):
                child = Sudoku._copy_board(curr_board)
                child[empty_cell[0]][empty_cell[1]] = i
                frontier.put(child)

    return None

'''
params: Takes the current puzzle as input
Return: The puzzle board corresponding to the goal
Note: You can modify the function definition as you see fit
'''
def dfs(puzzle):
    #Write Code here
    frontier = queue.LifoQueue()
    frontier.put(puzzle)
    
    while not frontier.empty():
        curr_board = frontier.get().board
        if(test_goal(curr_board, puzzle)):
            return curr_board
        
        empty_cell_list = empty_cells(curr_board)
        
        for empty in empty_cell_list:
            for i in range(1,puzzle.size + 1):
                child = Sudoku(puzzle.width, puzzle.height, Sudoku._copy_board(curr_board))
                child.board[empty[0]][empty[1]] = i
                #Sudoku(2, 2, child).show()
                frontier.put(child)
                dfs(child)

'''
params: Takes the current puzzle as input
Return: The puzzle board corresponding to the goal
Note: You can modify the function definition as you see fit
'''
def bfs_with_prunning(puzzle, board):
    #Write Code here
    frontier = queue.Queue()
    frontier.put(board)

    while not frontier.empty():
        curr_board = frontier.get()
        if test_goal(curr_board, puzzle):
            return curr_board

        for empty_cell in empty_cells(curr_board):
            for i in range(1,puzzle.size + 1):
                child = Sudoku._copy_board(curr_board)
                child[empty_cell[0]][empty_cell[1]] = i
                if valid_puzzle(int(math.sqrt(len(child))), child):
                    frontier.put(child)

    return None

'''
params: Takes the current puzzle as input
Return: The puzzle board corresponding to the goal
Note: You can modify the function definition as you see fit
'''
def dfs_with_prunning(puzzle):
    #Write Code here
    frontier = queue.LifoQueue()
    frontier.put(puzzle)
    
    while not frontier.empty():
        curr_board = frontier.get().board
        if(test_goal(curr_board, puzzle)):
            return curr_board
        
        empty_cell_list = empty_cells(curr_board)
        
        for empty in empty_cell_list:
            for i in range(1,puzzle.size + 1):
                child = Sudoku(puzzle.width, puzzle.height, Sudoku._copy_board(curr_board))
                child.board[empty[0]][empty[1]] = i
                if valid_puzzle(int(math.sqrt(len(child.board))), child.board):
                    frontier.put(child)
                dfs_with_prunning(child)
    return None


if __name__ == "__main__":

    
    puzzle=Sudoku(2,2).difficulty(0.5) # Constructs a 2 x 2 puzzle
    puzzle.show_full() # Pretty prints the puzzle
    print(valid_puzzle(2,puzzle.board)) # Checks if the puzzle is valid
    print(test_goal(puzzle.board,puzzle)) # Checks if the given puzzle board is the goal for the puzzle
    print(empty_cells(puzzle.board)) # Prints the empty cells as row and column values in a list for the current puzzle board
    
    # Running each searche and printing the solution along with the runtime (which is an average of 10 runs)
    # print("____________________________________________________________________________________")
    # print("BFS solution: ", bfs(puzzle, puzzle.board))
    # print("Time for BFS: ", timeit.timeit('bfs(puzzle, puzzle.board)', number=1, globals=globals()))
    # print("____________________________________________________________________________________")
    # print("DFS solution: ", dfs(puzzle))
    # print("Time for DFS: ", timeit.timeit('dfs(puzzle)', number=1, globals=globals()))
    # print("____________________________________________________________________________________")
    # print("BFS with pruning solution: ", bfs_with_prunning(puzzle, puzzle.board))
    # print("Time for BFS with pruning: ", timeit.timeit('bfs_with_prunning(puzzle, puzzle.board)', number=1, globals=globals()))
    # print("____________________________________________________________________________________")
    # print("DFS with pruning solution: ", dfs_with_prunning(puzzle))
    # print("Time for DFS with pruning: ", timeit.timeit('dfs_with_prunning(puzzle)', number=1, globals=globals()))
    # print("____________________________________________________________________________________")