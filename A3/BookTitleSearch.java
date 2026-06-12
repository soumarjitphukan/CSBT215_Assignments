import java.util.ArrayList;
import java.util.Scanner;

public class BookTitleSearch {
    public static void main(String[] args) {
        ArrayList<String> books = new ArrayList<>();
        Scanner scanner = new Scanner(System.in);

        System.out.print("How many books do you want to add? ");
        int numBooks;
        while (true) {
            try {
                numBooks = Integer.parseInt(scanner.nextLine().trim());
                if (numBooks > 0) break;
                System.out.print("Please enter a positive number: ");
            } catch (NumberFormatException e) {
                System.out.print("Please enter a valid number: ");
            }
        }

        System.out.println("\nEnter the book titles:");
        for (int i = 1; i <= numBooks; i++) {
            System.out.print("Book " + i + ": ");
            String title = scanner.nextLine().trim();
            if (!title.isEmpty()) {
                books.add(title);
            } else {
                System.out.println("Empty title skipped.");
                i--;
            }
        }

        System.out.println("\nAll books in the list (" + books.size() + " books):");
        for (String book : books) {
            System.out.println("  - " + book);
        }

        System.out.print("\nEnter a word to search in book titles: ");
        String searchWord = scanner.nextLine().trim().toLowerCase();

        System.out.println("\nBooks containing \"" + searchWord + "\":");
        boolean found = false;

        for (String book : books) {
            if (book.toLowerCase().contains(searchWord)) {
                System.out.println("  - " + book);
                found = true;
            }
        }

        if (!found) {
            System.out.println("No books found containing \"" + searchWord + "\".");
        }

        scanner.close();
    }
}