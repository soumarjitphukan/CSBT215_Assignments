from abc import ABC, abstractmethod


class LibraryItem(ABC):

    _total_items = 0

    def __init__(self, title: str, year: int):
        if not title or not title.strip():
            raise ValueError("Title must not be empty.")
        if not isinstance(year, int) or year < 1000 or year > 2100:
            raise ValueError("Year must be a valid 4-digit integer.")

        self.title = title.strip()
        self.year = year
        LibraryItem._total_items += 1

    @classmethod
    def get_total_items(cls) -> int:
        return cls._total_items

    @abstractmethod
    def display_info(self):
        print(f"  Title : {self.title}")
        print(f"  Year  : {self.year}")

    def __str__(self) -> str:
        return f"{self.__class__.__name__}: {self.title} ({self.year})"


class Book(LibraryItem):

    def __init__(self, title: str, year: int, author: str, pages: int = 0):
        super().__init__(title, year)
        if not author or not author.strip():
            raise ValueError("Author must not be empty.")
        if not isinstance(pages, int) or pages < 0:
            raise ValueError("Pages must be a non-negative integer.")

        self.author = author.strip()
        self.pages = pages

    @classmethod
    def from_dict(cls, data: dict) -> "Book":
        return cls(
            title=data["title"],
            year=data["year"],
            author=data["author"],
            pages=data.get("pages", 0),
        )

    def display_info(self):
        super().display_info()
        print(f"  Author: {self.author}")
        print(f"  Pages : {self.pages if self.pages > 0 else 'N/A'}")
        print(f"  Type  : Book")


class DVD(LibraryItem):

    VALID_GENRES = {"action", "drama", "comedy", "documentary", "thriller", "horror", "sci-fi"}

    def __init__(self, title: str, year: int, duration: int, genre: str = "Unknown"):
        super().__init__(title, year)
        if not isinstance(duration, int) or duration <= 0:
            raise ValueError("Duration must be a positive integer (minutes).")
        if genre.lower() not in self.VALID_GENRES and genre != "Unknown":
            raise ValueError(f"Genre must be one of: {', '.join(sorted(self.VALID_GENRES))}.")

        self.duration = duration
        self.genre = genre.capitalize()

    def display_info(self):
        super().display_info()
        hours, minutes = divmod(self.duration, 60)
        duration_str = f"{hours}h {minutes}m" if hours > 0 else f"{minutes}m"
        print(f"  Genre   : {self.genre}")
        print(f"  Duration: {duration_str} ({self.duration} min)")
        print(f"  Type    : DVD")


if __name__ == "__main__":

    print("\nBUILDING LIBRARY CATALOG\n")

    items: list[LibraryItem] = [
        Book("Clean Code", 2008, "Robert C. Martin", 431),
        Book("The Pragmatic Programmer", 1999, "David Thomas"),
        Book.from_dict({"title": "Design Patterns", "year": 1994, "author": "Gang of Four", "pages": 395}),
        DVD("Inception", 2010, 148, "Sci-Fi"),
        DVD("Planet Earth II", 2016, 360, "Documentary"),
        DVD("The Dark Knight", 2008, 152, "Action"),
    ]

    print(f"Total items registered: {LibraryItem.get_total_items()}\n")

    print("FULL CATALOG (Polymorphic Display)\n")
    for item in items:
        item.display_info()
        print()

    print("FILTERED VIEW — BOOKS ONLY\n")
    books = [item for item in items if isinstance(item, Book)]
    for book in books:
        print(f"  {book}")

    print("\nFILTERED VIEW — DVDs ONLY\n")
    dvds = [item for item in items if isinstance(item, DVD)]
    for dvd in dvds:
        print(f"  {dvd}")

    print("\nSTATIC COUNTER DEMO\n")
    print(f"Items before adding new ones : {LibraryItem.get_total_items()}")
    Book("Refactoring", 2018, "Martin Fowler", 448)
    DVD("Interstellar", 2014, 169, "Sci-Fi")
    print(f"Items after adding 2 more    : {LibraryItem.get_total_items()}")

    print("\nVALIDATION TESTS\n")

    try:
        Book("", 2020, "Someone")
    except ValueError as e:
        print(f"Caught: {e}")

    try:
        DVD("Test", 2020, -10, "Action")
    except ValueError as e:
        print(f"Caught: {e}")

    try:
        DVD("Test", 2020, 90, "Romance")
    except ValueError as e:
        print(f"Caught: {e}")

    try:
        Book("Test", 1800, "Author")
    except ValueError as e:
        print(f"Caught: {e}")

    print("\nAll validations passed successfully.")