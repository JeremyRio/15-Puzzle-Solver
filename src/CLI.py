from PuzzleSolver import *

# Driver utama CLI program
if __name__ == "__main__":

    # Membaca file
    puzzle_board = ReadFile()
    print("Program dalam progress...")

    # Mendapatkan perhitungan waktu awal program
    runtime_start = time.time()

    # Mengecek apakah puzzle_board dapat diselesaikan
    kurang_sum, list_kurang = GetListKurangAndSum(puzzle_board)
    if kurang_sum % 2 != 0:
        message = "Puzzle tidak bisa diselesaikan!"
    else:
        message = "Puzzle bisa diselesaikan, solusi sebagai berikut:"
        puzzle, node_path = BranchAndBoundSolve(puzzle_board)

    # Mendapatkan perhitungan waktu akhir program
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
        print("\nWaktu eksekusi: {:.4f} detik".format(
            runtime_end-runtime_start))
        print(f"Jumlah simpul yang dibangkitkan: {len(node_path)}")
