import PySimpleGUI as sg
from PuzzleSolver import *
import time

# Pembuatan Layout GUI
sg.theme('DarkAmber')
kurang_layout_1 = [
    [sg.Text(key="-KURANG(1)-", font=("Cascadia Code", 11))],
    [sg.Text(key="-KURANG(2)-", font=("Cascadia Code", 11))],
    [sg.Text(key="-KURANG(3)-", font=("Cascadia Code", 11))],
    [sg.Text(key="-KURANG(4)-", font=("Cascadia Code", 11))]
]

kurang_layout_2 = [
    [sg.Text(key="-KURANG(5)-", font=("Cascadia Code", 11))],
    [sg.Text(key="-KURANG(6)-", font=("Cascadia Code", 11))],
    [sg.Text(key="-KURANG(7)-", font=("Cascadia Code", 11))],
    [sg.Text(key="-KURANG(8)-", font=("Cascadia Code", 11))]
]

kurang_layout_3 = [
    [sg.Text(key="-KURANG(9)-", font=("Cascadia Code", 11))],
    [sg.Text(key="-KURANG(10)-", font=("Cascadia Code", 11))],
    [sg.Text(key="-KURANG(11)-", font=("Cascadia Code", 11))],
    [sg.Text(key="-KURANG(12)-", font=("Cascadia Code", 11))]
]

kurang_layout_4 = [
    [sg.Text(key="-KURANG(13)-", font=("Cascadia Code", 11))],
    [sg.Text(key="-KURANG(14)-", font=("Cascadia Code", 11))],
    [sg.Text(key="-KURANG(15)-", font=("Cascadia Code", 11))],
    [sg.Text(key="-KURANG(16)-", font=("Cascadia Code", 11))]
]

input_output_layout = [
    [sg.Text(text="15-Puzzle Solver", justification="center",
             font=("Cascadia Code", 20))],
    [sg.Text(text="Masukkan matriks puzzle:", font=("Cascadia Code", 12))],
    [
        sg.FileBrowse(button_text="Pilih File",
                      file_types=(("Text Files", "*.txt"),), font=("Cascadia Code", 10)),
        sg.In(size=(20, 1), enable_events=True, font=(
            "Cascadia Code", 10), key="-FILE INPUT-")
    ],
    [
        sg.Button(button_text="Solve", font=(
            "Cascadia Code", 10), key="-SOLVE-")
    ],
    [sg.Column(kurang_layout_1),
     sg.Column(kurang_layout_2),
     sg.Column(kurang_layout_3),
     sg.Column(kurang_layout_4)],
    [sg.Text(key="-KURANG(i)+X-", font=("Cascadia Code", 11))],
    [sg.Text(key="-WAKTU EKSEKUSI-", font=("Cascadia Code", 11))],
    [sg.Text(key="-NODE BANGKIT-", font=("Cascadia Code", 11))]
]

puzzle_layout_1 = [
    [sg.Image(key="-SLOT1-", filename="./assets/block1.png")],
    [sg.Image(key="-SLOT5-", filename="./assets/block5.png")],
    [sg.Image(key="-SLOT9-", filename="./assets/block9.png")],
    [sg.Image(key="-SLOT13-", filename="./assets/block13.png")]
]

puzzle_layout_2 = [
    [sg.Image(key="-SLOT2-", filename="./assets/block2.png")],
    [sg.Image(key="-SLOT6-", filename="./assets/block6.png")],
    [sg.Image(key="-SLOT10-", filename="./assets/block10.png")],
    [sg.Image(key="-SLOT14-", filename="./assets/block14.png")]
]

puzzle_layout_3 = [
    [sg.Image(key="-SLOT3-", filename="./assets/block3.png")],
    [sg.Image(key="-SLOT7-", filename="./assets/block7.png")],
    [sg.Image(key="-SLOT11-", filename="./assets/block11.png")],
    [sg.Image(key="-SLOT15-", filename="./assets/block15.png")]
]

puzzle_layout_4 = [
    [sg.Image(key="-SLOT4-", filename="./assets/block4.png")],
    [sg.Image(key="-SLOT8-", filename="./assets/block8.png")],
    [sg.Image(key="-SLOT12-", filename="./assets/block12.png")],
    [sg.Image(key="-SLOT16-", filename="./assets/block16.png")]
]

layout = [
    [
        sg.Column(puzzle_layout_1),
        sg.Column(puzzle_layout_2),
        sg.Column(puzzle_layout_3),
        sg.Column(puzzle_layout_4),
        sg.Column(""),
        sg.Column(""),
        sg.Column(""),
        sg.Column(input_output_layout),
    ]
]

# Driver Utama GUI
window = sg.Window("15-Puzzle Solver", layout)
while True:
    event, values = window.read()
    if event == "-FILE INPUT-":
        try:
            puzzle_board = ReadFileGUI(values["-FILE INPUT-"])
            for i in range(16):
                window[f"-SLOT{i+1}-"].update(
                    filename="./assets/block" + str(puzzle_board[i]) + ".png")
        except:
            sg.popup("File tidak ditemukan")

    if event == "-SOLVE-":
        # Mendapatkan perhitungan waktu awal program
        runtime_start = time.time()

        # Mengecek apakah puzzle_board dapat diselesaikan
        kurang_sum, list_kurang = GetListKurangAndSum(puzzle_board)
        if kurang_sum % 2 != 0:
            sg.popup("Puzzle ini tidak dapat diselesaikan")
        else:
            puzzle, node_path = BranchAndBoundSolve(puzzle_board)
            # Mendapatkan perhitungan waktu akhir program
            runtime_end = time.time()

            # Output program dan pergerakan Puzzle
            node_solution = [puzzle]
            while str(puzzle) != str(puzzle_board):
                node_solution.insert(0, node_path[str(puzzle)])
                puzzle = node_path[str(puzzle)]
            for i in range(16):
                window[f"-KURANG({i+1})-"].update(f"Kurang({i+1}) = {list_kurang[i]}")
            window["-KURANG(i)+X-"].update(
                f"Total Kurang(i) + X = {kurang_sum}")
            window["-WAKTU EKSEKUSI-"].update("Waktu eksekusi: {: .4f} detik".format(
                runtime_end-runtime_start))
            window["-NODE BANGKIT-"].update(
                f"Jumlah simpul yang dibangkitkan: {len(node_path)}")
            for i in range(len(node_solution)):
                for j in range(len(node_solution[i])):
                    window[f"-SLOT{j+1}-"].update(
                        filename="assets/block" + str(node_solution[i][j]) + ".png")
                window.read(timeout=550)
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
window.close()
