"""Bookcli"""

# Importing packages required for the program.
import sys

from resources import Booksources

# Global variables
books = Booksources()

# Space for functions start from here


def file_open(soup):
    """Function for opening file and appending soup."""
    with open("file.txt", "a", encoding="utf-8") as f:
        f.write(soup.prettify())
        f.close()


def retry():
    """Function for restarting."""
    match input(
        "\nDo you want to search another book:\n1. Yes\n2. No"
        "\nType the index number: "
    ):
        case "1":
            choice()
            clear()
        case "2":
            clear()
            sys.exit()
        case _:
            print("\nInvalid value")
            retry()


def clear():
    """Function for terminal clear."""
    print("\033c")


def choice():
    """Function to start the core app."""
    match input(
        "\nSelect the category: \n1. Books\n2. Manga\n3. Anime"
        "\n4. Exit\n\nEnter index number: "
    ):
        case "1":
            search_term = input("\nEnter the title of the book: ")
            match input(
                "\nSelect the website: \n1. Libgen\n2. Anna's Archive"
                "\n3. Zlibrary\n4. Restart\n5. Exit"
                "\n\nEnter index number: "
            ):
                case "1":
                    books.libgen(search_term)
                case "2":
                    books.anna_archive(search_term)
                case "3":
                    books.zlibrary(search_term)
                case "4":
                    clear()
                    choice()
                case "5":
                    clear()
                    sys.exit()
                case _:
                    print("\nInvalid value")

        case "2":
            match input(
                "\nSelect the website: \n1. MangaSee\n2. Comick"
                "\n3. Bato\n4. Restart\n5. Exit"
                "\n\nEnter index number: "
            ):
                case "1":
                    pass
                case "2":
                    pass
                case "3":
                    pass
                case "4":
                    clear()
                    choice()
                case "5":
                    clear()
                    sys.exit()
                case _:
                    print("\nInvalid value")
        case "3":
            match input(
                "\nSelect the website: \n1. Anime1\n2. Anime2"
                "\n3. Anime3\n4. Restart\n5. Exit"
                "\n\nEnter index number: "
            ):
                case "1":
                    pass
                case "2":
                    pass
                case "3":
                    pass
                case "4":
                    clear()
                    choice()
                case "5":
                    clear()
                    sys.exit()
                case _:
                    print("\nInvalid value")
        case "4":
            clear()
            sys.exit()
        case _:
            print("\nInvalid value")


# Space for functions ends here.


choice()
