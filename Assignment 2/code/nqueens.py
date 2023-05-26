import sys
import random
import math

MAXQ = 100


def in_conflict(column, row, other_column, other_row):
    """
    Checks if two locations are in conflict with each other.
    :param column: Column of queen 1.
    :param row: Row of queen 1.
    :param other_column: Column of queen 2.
    :param other_row: Row of queen 2.
    :return: True if the queens are in conflict, else False.
    """
    if column == other_column:
        return True  # Same column
    if row == other_row:
        return True  # Same row
    if abs(column - other_column) == abs(row - other_row):
        return True  # Diagonal

    return False


def in_conflict_with_another_queen(row, column, board):
    """
    Checks if the given row and column correspond to a queen that is in conflict with another queen.
    :param row: Row of the queen to be checked.
    :param column: Column of the queen to be checked.
    :param board: Board with all the queens.
    :return: True if the queen is in conflict, else False.
    """
    for other_column, other_row in enumerate(board):
        if in_conflict(column, row, other_column, other_row):
            if row != other_row or column != other_column:
                return True
    return False


def count_conflicts(board):
    """
    Counts the number of queens in conflict with each other.
    :param board: The board with all the queens on it.
    :return: The number of conflicts.
    """
    cnt = 0

    for queen in range(0, len(board)):
        for other_queen in range(queen+1, len(board)):
            if in_conflict(queen, board[queen], other_queen, board[other_queen]):
                cnt += 1

    return cnt


def evaluate_state(board):
    """
    Evaluation function. The maximal number of queens in conflict can be 1 + 2 + 3 + 4 + .. +
    (nquees-1) = (nqueens-1)*nqueens/2. Since we want to do ascending local searches, the evaluation function returns
    (nqueens-1)*nqueens/2 - countConflicts().

    :param board: list/array representation of columns and the row of the queen on that column
    :return: evaluation score
    """
    return (len(board)-1)*len(board)/2 - count_conflicts(board)


def print_board(board):
    """
    Prints the board in a human readable format in the terminal.
    :param board: The board with all the queens.
    """
    print("\n")

    for row in range(len(board)):
        line = ''
        for column in range(len(board)):
            if board[column] == row:
                line += 'Q' if in_conflict_with_another_queen(row, column, board) else 'q'
            else:
                line += '.'
        print(line)


def init_board(nqueens):
    """
    :param nqueens integer for the number of queens on the board
    :returns list/array representation of columns and the row of the queen on that column
    """

    board = []

    for column in range(nqueens):
        board.append(random.randint(0, nqueens-1))

    return board


"""
------------------ Do not change the code above! ------------------
"""


def allNeighbour(board):
    states = []
    for col in range(0, len(board)):
        queen = board[col]
        for row in range (0, len(board)):
            if queen != row:
                newBoard = board.copy()
                newBoard[col] = row
                states.append(newBoard)
    return states

def findBestNeighbour(boards):
    bestBoards = []
    min = 2147483647
    for neighbour in boards:
        nmbrConflicts = count_conflicts(neighbour)
        if nmbrConflicts < min:
            min = nmbrConflicts
            bestBoards = []
        if min == nmbrConflicts:
            bestBoards.append(neighbour)
    return bestBoards[random.randint(0, len(bestBoards) - 1)]

def random_search(board):
    """
    This function is an example and not an efficient solution to the nqueens problem. What it essentially does is flip
    over the board and put all the queens on a random position.
    :param board: list/array representation of columns and the row of the queen on that column
    """

    i = 0
    optimum = (len(board) - 1) * len(board) / 2

    while evaluate_state(board) != optimum:
        i += 1
        print('iteration ' + str(i) + ': evaluation = ' + str(evaluate_state(board)))
        if i == 1000:  # Give up after 1000 tries.
            break

        for column, row in enumerate(board):  # For each column, place the queen in a random row
            board[column] = random.randint(0, len(board)-1)

    if evaluate_state(board) == optimum:
        print('Solved puzzle!')

    print('Final state is:')
    print_board(board)

def hill_climbing(board):
    """
    Implement this yourself.
    :param board:
    :return:
    """

    current = board.copy()

    while True:
        neighbour = findBestNeighbour(allNeighbour(current)) # finds the neighbour with lowest hereustic value
        if evaluate_state(current) >= evaluate_state(neighbour):
            print_board(current)
            return
        current = neighbour

def randomNeighbour(board):
    randomBoard = allNeighbour(board)
    return randomBoard[random.randint(0, len(randomBoard) - 1)]

def time_to_temperature(t):
    T = 1/t - 0.001
    return T

def simulated_annealing(board):
    """
    Implement this yourself.
    :param board:
    :return:
    """
    current = board.copy()
    for t in range (1,2147483647):
        T = time_to_temperature(t)
        if T == 0:
            print_board(current)
            return
        neighbour = randomNeighbour(current)
        delta_e = evaluate_state(neighbour) - evaluate_state(current)
        if delta_e > 0:
            current = neighbour
        else:
            probability = math.exp(delta_e / T)
            if (probability > random.uniform(0.0, 1.0)):
                current = neighbour

def reproduce(x, y):
    n = len(x)
    c = random.randint(0, n)
    return (x[0:c] + y[c:n])
    
def random_selection(population):
    fitness = []
    total_pairs = 0 #the sum of the non attacking pairs of the generations

    for i in range(len(population)):
        save = evaluate_state(population[i])
        fitness.append(save)
        total_pairs += save
    
    probability = random.randint(0, total_pairs - 1)
    index = 0
    choosingSum = 0
    for save in fitness:
        choosingSum += save
        if probability < choosingSum:
            return population[index]
        index += 1

def mutate(board):
    index = random.randint(0, len(board) - 1)
    board[index] = random.randint(0, len(board) - 1)
    return board

def genetic_algorithm(board, pairs):
    indexUpperBound = len(board)
    population = []
    for i in range(pairs):
        population.append(init_board(indexUpperBound))
    stopCondition = True
    while stopCondition:
        newPopulation = []
        for i in range(len(population)):
            x = random_selection(population)
            y = random_selection(population)
            child = reproduce(x,y)
            if random.randint(0, 1) == 0:
                child = mutate(child)
            newPopulation.append(child)
            if count_conflicts(child) == 0:
                print('\n Solution Found')
                print_board(child)
                return
        population = newPopulation.copy()

def main():
    """
    Main function that will parse input and call the appropriate algorithm. You do not need to understand everything
    here!
    """

    try:
        if len(sys.argv) != 2:
            raise ValueError

        n_queens = int(sys.argv[1])
        if n_queens < 1 or n_queens > MAXQ:
            raise ValueError

    except ValueError:
        print('Usage: python n_queens.py NUMBER')
        return False

    print('Which algorithm to use?')
    algorithm = input('1: random, 2: hill-climbing, 3: simulated annealing, 4: genetic algorithm \n')

    try:
        algorithm = int(algorithm)

        if algorithm not in range(1, 5):
            raise ValueError

    except ValueError:
        print('Please input a number in the given range!')
        return False

    board = init_board(n_queens)
    print('Initial board: \n')
    print_board(board)

    if algorithm == 1:
        random_search(board)
    if algorithm == 2:
        hill_climbing(board)
    if algorithm == 3:
        simulated_annealing(board)
    if algorithm == 4:
        genetic_algorithm(board, 8)


# This line is the starting point of the program.
if __name__ == "__main__":
    main()
