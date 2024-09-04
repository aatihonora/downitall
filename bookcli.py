"""Bookcli"""

# Importing packages required for the program.
import os
import sys

from resources import (Animesources, Booksources, Mangasources, Musicsources,
                       Schoolsources, Tvsources)

# Global variables.
books = Booksources()
manga = Mangasources()
anime = Animesources()
school = Schoolsources()
tv = Tvsources()
music = Musicsources()
# Space for functions start from here

def clear():
    """Function for terminal clear."""
    print("\033c")


def choice():
    """Function to start the core app."""
    match input(
        "\nSelect the category: \n1. Books\n2. Manga\n3. Anime"
        "\n4. TV-Series/Movies\n5. Music\n6. Exit\n\nEnter index number: "
    ):
        case "1":
            search_term = input("\nEnter the title of the Book: ")
            match input(
                "\nSelect the website: \n1. Libgen [Books]\n2. Anna's Archive [Books]"
                "\n3. Glodls [Courses] [Torrent]\n4. Restart\n5. Exit"
                "\n\nEnter index number: "
            ):
                case "1":
                    books.libgen(search_term)
                case "2":
                    books.anna_archive(search_term)
                case "3":
                    books.glodls(search_term)
                case "4":
                    clear()
                    choice()
                case "5":
                    clear()
                    sys.exit()
                case _:
                    print("\nInvalid value")

        case "2":
            search_term = input("\nEnter the title of the Manga: ")
            match input(
                "\nSelect the website: \n1. Bato [Manga/Manhwa/Manhua]\n2. Mangasee [Manga]"
                "\n3. ComicExtra [Comics]\n4. Restart\n5. Exit"
                "\n\nEnter index number: "
            ):
                case "1":
                    manga.bato(search_term)
                case "2":
                    manga.mangasee(search_term)
                case "3":
                    manga.comicextra(search_term)
                case "4":
                    clear()
                    choice()
                case "5":
                    clear()
                    sys.exit()
                case _:
                    print("\nInvalid value")
        case "3":
            search_term = input("\nEnter the title of the Anime: ")
            match input(
                "\nSelect the website: \n1. TokyoInsider [Anime]\n2. Nyaa [Anime] [Torrent]"
                "\n3. Kayoanime [Anime]\n4. Restart\n5. Exit"
                "\n\nEnter index number: "
            ):
                case "1":
                    anime.tokyoinsider(search_term)
                case "2":
                    anime.nyaa(search_term)
                case "3":
                    anime.kayoanime(search_term)
                case "4":
                    clear()
                    choice()
                case "5":
                    clear()
                    sys.exit()
                case _:
                    print("\nInvalid value")
        case "4":
            search_term = input("\nEnter the title of the TV series/Movie: ") 
            match input(
                "\nSelect the website: \n1. Vadapav [TV-Series/Movies/Anime]\n2. 1337x [Everything] [Torrent]"
                "\n3. LimeTorrent [Everything] [Torrent]\n4. Restart\n5. Exit"
                "\n\nEnter index number: "
            ):
                case "1":
                    tv.vadapav(search_term)
                case "2":
                    tv.torrent(search_term)
                case "3":
                    tv.lime(search_term)
                case "4":
                    clear()
                    choice()
                case "5":
                    clear()
                    sys.exit()
                case _:
                    print("\nInvalid value")
        case "5":
            search_term = input("\nEnter the title of the Music: ")
            match input(
                "\nSelect the website: \n1. Lightaudio [Songs]\n2. Bomb-music [Songs]"
                "\n3. Pagalnew [Hindi Songs]\n4. Restart\n5. Exit"
                "\n\nEnter index number: "
            ):
                case "1":
                    music.lightaudio(search_term)
                case "2":
                    music.bombmusic(search_term)
                case "3":
                    music.pagalnew(search_term)
                case "4":
                    clear()
                    choice()
                case "5":
                    clear()
                    sys.exit()
                case _:
                    print("\nInvalid value")
        case "6":
            clear()
            sys.exit()
        case "18":
            search_term = input("\nEnter the title of the anime: ")
            match input(
                "\nSelect the website: \n1. R38\n2. Nyaa"
                "\n3. Kayoanime\n4. Restart\n5. Exit"
                "\n\nEnter index number: "
            ):
                case "1":
                    school.r34(search_term)


        case _:
            print("\nInvalid value")

dir = "Download"
if not os.path.isdir(dir):
    os.mkdir(dir)
    os.chdir(dir)
else:
    os.chdir(dir)

choice()
