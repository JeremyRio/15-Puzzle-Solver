from heapq import heappop, heappush
import time


class PuzzleNode:
    # Kelas PuzzleNode untuk menyimpan depth
    # dan parent dari suatu node
    g_cost = 999

    def __init__(self, puzzle_board, depth, parent):
        self.puzzle_board = puzzle_board.copy()
        self.depth = depth
        self.parent = parent


def ReadFile():
    # Membaca file matriks puzzle dan memasukkannya
    # ke dalam list puzzle_board
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
    # Mencetak list puzzle_board ke layar dalam bentuk puzzle matriks
    for i in range(16):
        print("|" + str(puzzle_board[i]).ljust(2), end="")
        if i % 4 == 3:
            print("|")


def GetX(idx):
    # Mendapatkan nilai X untuk penjumlahan Kurang(i) + X
    list_x = [1, 3, 4, 6, 9, 11, 12, 14]
    if idx in list_x:
        return 1
    else:
        return 0


def GetListKurangAndSum(puzzle_board):
    # Mendapatkan semua nilai Kurang(i) dan total nilai Kurang(i) + X
    list_kurang = []
    kurang_sum = 0
    for i in range(1, 17):
        count = 0
        i_idx = puzzle_board.index(i)
        for j in range(i_idx+1, 16):
            if(i > puzzle_board[j]):
                count += 1
        list_kurang.append(count)
        kurang_sum += count
    kurang_sum += GetX(i_idx)
    return kurang_sum, list_kurang


def Get_g_cost(puzzle_board):
    # Menghitung jumlah ubin tidak kosong dalam list puzzle_board yang tidak berada pada # tempat sesuai susunan akhir (goal state)
    cost = 0
    for i in range(15):
        if(i+1 != puzzle_board[i]):
            cost += 1
    return cost


def Swap(puzzle_board, idx1, idx2):
    # Menukar nilai idx1 dan idx2 pada list puzzle_board
    puzzle_board[idx1], puzzle_board[idx2] = puzzle_board[idx2], puzzle_board[idx1]


def GetPossibleNodes(node_count, prioq_bnb, puzzle_node):
    # Mengembalikan semua simpul yang dapat dibangkitkan dari puzzle_node
    # serta mengembalikan jumlah simpul yang dibangkitkan
    empty_idx = puzzle_node.puzzle_board.index(16)
    puzzle_board = puzzle_node.puzzle_board
    new_depth = puzzle_node.depth + 1

    if ((empty_idx + 1) % 4 != 0):
        node_count += 1
        new_node = PuzzleNode(puzzle_board, new_depth, puzzle_board)
        Swap(new_node.puzzle_board, empty_idx, empty_idx + 1)
        new_node.g_cost = Get_g_cost(new_node.puzzle_board)
        heappush(prioq_bnb, (new_depth + new_node.g_cost, node_count, new_node))

    if(empty_idx % 4 != 0):
        node_count += 1
        new_node = PuzzleNode(puzzle_board, new_depth, puzzle_board)
        Swap(new_node.puzzle_board, empty_idx, empty_idx - 1)
        new_node.g_cost = Get_g_cost(new_node.puzzle_board)
        heappush(prioq_bnb, (new_depth + new_node.g_cost, node_count, new_node))

    if(empty_idx - 3 > 0):
        node_count += 1
        new_node = PuzzleNode(puzzle_board, new_depth, puzzle_board)
        Swap(new_node.puzzle_board, empty_idx, empty_idx - 4)
        new_node.g_cost = Get_g_cost(new_node.puzzle_board)
        heappush(prioq_bnb, (new_depth + new_node.g_cost, node_count, new_node))

    if(empty_idx + 3 < 15):
        node_count += 1
        new_node = PuzzleNode(puzzle_board, new_depth, puzzle_board)
        Swap(new_node.puzzle_board, empty_idx, empty_idx + 4)
        new_node.g_cost = Get_g_cost(new_node.puzzle_board)
        heappush(prioq_bnb, (new_depth + new_node.g_cost, node_count, new_node))

    return node_count


def BranchAndBoundSolve(puzzle_board):
    # Algoritma Branch And Bound untuk mencari solusi dari 15 Puzzle
    prioq_bnb = []
    node_path = {}
    node_count = 0
    current_node = PuzzleNode(puzzle_board, 0, "ROOT")
    node_path[str(puzzle_board)] = "ROOT"
    g_cost = Get_g_cost(puzzle_board)
    if g_cost != 0:
        node_count = GetPossibleNodes(node_count, prioq_bnb, current_node)
        current_node = heappop(prioq_bnb)[2]
    # Dilakukan iterasi sampai semua ubin yang tidak kosong dalam list puzzle_board
    # sesuai pada tempatnya (goal node)
    while g_cost != 0:
        if(str(current_node.puzzle_board) not in node_path):
            node_path[str(current_node.puzzle_board)
                      ] = current_node.parent
            node_count = GetPossibleNodes(node_count, prioq_bnb, current_node)
        current_node = heappop(prioq_bnb)[2]
        g_cost = current_node.g_cost
    node_path[str(current_node.puzzle_board)] = current_node.parent
    return current_node.puzzle_board, node_path, node_count


if __name__ == "__main__":
    # Driver utama file
    # Membaca file
    puzzle_board = ReadFile()
    print("Program dalam progress...")

    # Memulai perhitungan eksekusi waktu
    runtime_start = time.time()
    kurang_sum, list_kurang = GetListKurangAndSum(puzzle_board)
    if kurang_sum % 2 != 0:
        message = "Puzzle tidak bisa diselesaikan!"
    else:
        message = "Puzzle bisa diselesaikan, solusi sebagai berikut:"
        puzzle, node_path, node_count = BranchAndBoundSolve(puzzle_board)

    # Mematikan perhitungan eksekusi waktu
    runtime_end = time.time()

    # Output program
    print("\nMatriks posisi awal: ")
    PrintPuzzle(puzzle_board)
    print("\nNilai Kurang(i): ")
    for i in range(16):
        print(f"Kurang({i+1}) = {list_kurang[i]}")
    print(f"Total Kurang(i) + X = {kurang_sum}\n")
    print(message)
    if(kurang_sum % 2 == 0):
        node_solution = [puzzle]
        while str(puzzle) != str(puzzle_board):
            node_solution.insert(0, node_path[str(puzzle)])
            puzzle = node_path[str(puzzle)]
        node_solution.pop(0)
        print("Matriks posisi awal: ")
        PrintPuzzle(puzzle_board)
        for i in range(len(node_solution)):
            print(f"\nMatriks langkah ke-{i+1}: ")
            PrintPuzzle(node_solution[i])
        print(f"\nWaktu eksekusi: {(runtime_end - runtime_start) * 1000} ms")
        print(f"Jumlah simpul yang dibangkitkan: {node_count}")
