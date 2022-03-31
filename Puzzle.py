from heapq import heappop, heappush
import time


def ReadFile():
    while True:
        try:
            puzzle_board = []
            filename = input("Masukkan nama file (tanpa .txt): ")
            for raw_lines in open("tests/" + filename + ".txt", 'r'):
                lines = raw_lines.replace("\n", "").split()
                for line in lines:
                    puzzle_board.append(int(line))
            return puzzle_board
        except:
            print("Nama file tidak ditemukan, ulangi")


def PrintPuzzle(puzzle_board):
    for i in range(16):
        print(puzzle_board[i], end=" ")
        if i % 4 == 3:
            print()


def ListKurang(puzzle_board):
    list_kurang = []
    sum = 0
    for i in range(1, 17):
        count = 0
        i_idx = puzzle_board.index(i)
        for j in range(i_idx+1, 16):
            if(i > puzzle_board[j]):
                count += 1
        list_kurang.append(count)
        sum += count
    return sum, list_kurang


def GetGCost(puzzle_board):
    cost = 0
    for i in range(15):
        if(i+1 != puzzle_board[i]):
            cost += 1
    return cost


def Swap(puzzle_board, idx1, idx2):
    puzzle_board[idx1], puzzle_board[idx2] = puzzle_board[idx2], puzzle_board[idx1]


def GetPossibleNodes(prioq_bnb, puzzle_board, depth, previous_movement):
    empty_idx = puzzle_board.index(16)
    copy_board = []
    if ((empty_idx + 1) % 4 != 0 and previous_movement != "left"):
        copy_board = puzzle_board.copy()
        Swap(copy_board, empty_idx, empty_idx + 1)
        heappush(prioq_bnb, (GetGCost(copy_board) + depth, copy_board, "right"))
    if(empty_idx % 4 != 0 and previous_movement != "right"):
        copy_board = puzzle_board.copy()
        Swap(copy_board, empty_idx, empty_idx - 1)
        heappush(prioq_bnb, (GetGCost(copy_board) + depth, copy_board, "left"))
    if(empty_idx - 3 > 0 and previous_movement != "down"):
        copy_board = puzzle_board.copy()
        Swap(copy_board, empty_idx, empty_idx - 4)
        heappush(prioq_bnb, (GetGCost(copy_board) + depth, copy_board, "up"))
    if(empty_idx + 3 < 15 and previous_movement != "up"):
        copy_board = puzzle_board.copy()
        Swap(copy_board, empty_idx, empty_idx + 4)
        heappush(prioq_bnb, (GetGCost(copy_board) + depth, copy_board, "down"))


def BranchAndBoundSolve(puzzle_board):
    prioq_bnb = []
    urutan_list = []
    GetPossibleNodes(prioq_bnb, puzzle_board, 0, "")
    depth = 1
    g_cost = 999
    _, current_puzzle, previous_movement = heappop(prioq_bnb)
    urutan_list.append(current_puzzle)
    while g_cost != 0:
        GetPossibleNodes(prioq_bnb, current_puzzle, depth, previous_movement)
        _, current_puzzle, previous_movement = heappop(prioq_bnb)
        urutan_list.append(current_puzzle)
        depth += 1
        g_cost = GetGCost(current_puzzle)
    return urutan_list


if __name__ == "__main__":
    puzzle_board = ReadFile()
    print("Program dalam progress...")
    runtime_start = time.time()
    sum, list_kurang = ListKurang(puzzle_board)
    sum += (puzzle_board.index(16) + 1) % 2
    print("\nMatriks posisi awal: ")
    PrintPuzzle(puzzle_board)
    print("\nNilai Kurang(i): ")
    for i in range(16):
        print(f"Kurang({i+1}) = {list_kurang[i]}")
    print(f"Total Kurang(i) + X = {sum}\n")

    if sum % 2 != 0:
        print("Puzzle tidak bisa diselesaikan!")
    elif GetGCost(puzzle_board) == 0:
        print("Puzzle sudah terselesaikan, cari puzzle yang lain!")
    else:
        print("Puzzle bisa diselesaikan, solusi sebagai berikut:")
        urutan_list = BranchAndBoundSolve(puzzle_board)
        print("Matriks posisi awal: ")
        PrintPuzzle(puzzle_board)
        for i in range(len(urutan_list)):
            print(f"\nMatriks langkah ke-{i+1}: ")
            PrintPuzzle(urutan_list[i])
        print(f"\nWaktu eksekusi: {(time.time() - runtime_start) * 1000} ms")
