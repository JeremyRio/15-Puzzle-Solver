import java.util.Scanner;
import java.util.ArrayList;
import java.io.File;

public class Puzzle {

  static public ArrayList<Integer> ReadFile() {
    ArrayList<Integer> board = new ArrayList<Integer>();
    String FILENAME;
    Scanner FILE = null;
    Scanner input = new Scanner(System.in);
    boolean file_found = false;

    while (!file_found) {
      System.out.print("Masukkan nama file (tanpa .txt): ");
      FILENAME = input.nextLine();
      try {
        FILE = new Scanner(new File(FILENAME));
        file_found = true;
      } catch (Exception e) {
        System.out.println("Nama file tidak ada, ulangi");
      }
    }

    if (FILE != null) {
      while (FILE.hasNext()) {
        board.add(FILE.nextInt());
      }
    }

    input.close();
    FILE.close();
    return board;
  }

  static public int[] IsSolvablePuzzle(ArrayList<Integer> board) {
    int idx;
    int[] kurang_value = new int[16];
    for (int i = 1; i < 17; i++) {
      idx = board.indexOf(i);
      if (idx != -1) {
        for (int j = idx + 1; j < 16; j++) {
          if (board.get(j) != 16 && i > board.get(j)) {
            kurang_value[i - 1]++;
          }
        }
      }
    }
    return kurang_value;
  }

  public static void main(String[] args) {
    ArrayList<Integer> board = new ArrayList<Integer>();
    board = ReadFile();
    IsSolvablePuzzle(board);
    int[] kurang_value = IsSolvablePuzzle(board);

    int sum = 0;
    for (int i = 0; i < 16; i++) {
      System.out.println("KURANG(" + (i + 1) + ") = " + kurang_value[i]);
      sum += kurang_value[i];
    }
    int total_sum = sum + ((board.indexOf(16) + 1) % 2);
    System.out.println("KURANG(i) + X = " + total_sum);

    if (total_sum % 2 != 0) {
      System.out.println("Matriks tidak bisa diselesaikan");
    } else {
      boolean found = false;
      while (!found) {

      }
    }
  }
}
