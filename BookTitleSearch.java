import java.util.ArrayList;
import java.util.Scanner;

public class BookTitleSearch {
    public static void main(String[] args) {
        ArrayList<String> bookTitles = new ArrayList<>();

        bookTitles.add("The Great Gatsby");
        bookTitles.add("To Kill a Mockingbird");
        bookTitles.add("1984");
        bookTitles.add("Pride and Prejudice");
        bookTitles.add("The Catcher in the Rye");
        bookTitles.add("Harry Potter and the Sorcerer's Stone");

        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter a word to search in book titles: ");
        String searchWord = scanner.nextLine().toLowerCase();

        System.out.println("Books containing the word '" + searchWord + "':");
        boolean found = false;
        for (String title : bookTitles) {
            if (title.toLowerCase().contains(searchWord)) {
                System.out.println(title);
                found = true;
            }
        }

        if (!found) {
            System.out.println("No books found containing the word '" + searchWord + "'.");
        }

        scanner.close();
    }
}
