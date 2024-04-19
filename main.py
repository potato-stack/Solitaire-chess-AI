import os
from chess import ChessboardReader
import solitaire_best
import solitaire_naive
import sys

if len(sys.argv) < 2:
    print("Usage: python script.py <board_size: 4 6 8 11> <verbose: True False>")
    sys.exit(1)

# Extract the board size from the command-line argument
piece_nums = int(sys.argv[1])
ver_bose = True if len(sys.argv) >= 3 and sys.argv[2] == True else False
folder_path = f"C:/Users/hatru/OneDrive/Desktop/NMTTNT/Input/{piece_nums}"
total_performance = 0
total_naive = 0
total_fast = 0
total_test = 0

print(f'{"":<18s}{"BFS":<12s}{"BestFS":<12s}{"BFS_gen":<12s}{"BestFS_gen":<12s}Performance')

for idx, filename in enumerate(os.listdir(folder_path)):
    file_path = os.path.join(folder_path, filename)
    if os.path.isfile(file_path):
        reader = ChessboardReader()
        
        initialState = reader.read_chessboard_from_file(file_path)
        naive_time, naive_gen = solitaire_naive.solve(initialState, verbose=ver_bose)
        fast_time, fast_gen = solitaire_best.solve(initialState, verbose=ver_bose)
        performance = naive_time/fast_time -1 

        print(f"Input #{idx + 1}\t{naive_time:8.4f}{fast_time:12.4f}{naive_gen:13.0f}{fast_gen:15.0f}", end=" ")

        if performance == 0:
            print(performance)
        elif performance > 0:
            print("\033[92m {:.4f}%\033[00m" .format(performance * 100))
        elif performance < 0:
            print("\033[91m {:.4f}%\033[00m" .format(performance * 100))

        total_performance += performance
        total_naive += naive_time
        total_fast += fast_time
        total_test += 1
        
print(f"Bench mark for chess board with {piece_nums} piece:")
print(f"└ BFS: {(total_naive / total_test * 100):.4f} seconds avg per testcase.")
print(f"└ BestFS:  {(total_fast / total_test * 100):.4f} seconds avg per testcase.") 
if total_performance / piece_nums > 0:
    print(f"└ \033[92m {(total_performance / piece_nums * 100):.4f}% \033[00m boost avg.")

if total_performance / piece_nums < 0:
    print(f"└ \033[91m {(total_performance / piece_nums * 100):.4f}% \033[00m slowed down avg.")
                
