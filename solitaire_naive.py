from chess import Chessboard, ChessboardReader
from collections import deque
import heapq
from time import perf_counter

def solve(initialState, verbose = False):
    # Bench mark variable
    start = perf_counter()
    gen = 0
    # Basic bfs queue
    board_queue_state = deque()
    initialBoard = Chessboard(initialState, None, None, 0)

    board_queue_state.append(initialBoard)
    current_state = None

    while (board_queue_state):
        current_state = board_queue_state.popleft()
        if (len(current_state.board) == 1):
            if verbose == True: print("Find a feasable solutions: ")
            break
        for chess in current_state.board:
            for other_chess in current_state.board:
                if current_state.can_capture(chess, other_chess) == True:
                    
                    gen+=1
                    next_state = Chessboard(None, None, None, 0)

                    # Append for the next new list
                    for new, value in current_state.board.items():
                        if not (new[0] == chess[0] and new[1] == chess[1]) and not (new[0] == other_chess[0] and new[1] == other_chess[1]):
                            next_state.add(new, value)

                    next_state.add(other_chess, current_state.board[chess])
                    next_state.moves = ((chess[0], chess[1]), (other_chess[0], other_chess[1]))
                    next_state.parent = current_state

                    board_queue_state.append(next_state)

    end = perf_counter()
    if verbose == True: 
        moves = []

        while current_state is not None:
            parent_state = current_state.parent
            if parent_state is not None:
                if parent_state.moves is None:
                    moves.append("Start")
                else:
                    moves.append(parent_state.moves)
            current_state = parent_state

        # Print moves in reverse order
        for move in reversed(moves):
            if move == "Start":
                print(move)
            else:
                print((chr(ord('a') + move[0][0] - 1), move[0][1]), "->", (chr(ord('a') + move[1][0] - 1), move[1][1]))
        print("-------------------Result-------------------")
        print("Total solving time:", end - start)
        print("Total generated moves:", gen)
    return (end - start, gen)