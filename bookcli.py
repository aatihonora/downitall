"""Bookcli"""

# Importing packages required for the program.
import os

import questionary

from resources import (Animesources, Booksources, Mangasources, Musicsources,
                       Tvsources)

# Global variables.
books = Booksources()
manga = Mangasources()
anime = Animesources()
tv = Tvsources()
music = Musicsources()
# Space for functions start from here

def choice():
    """Function to start the core app."""

    type = questionary.select("Select item", choices=["Anime", "Book", "Manga", "Music", "TV/Movie", "Exit"]).ask()
    if type == "Anime":
        search_term = input("Enter the title of the Anime: ")
        select = questionary.select("Select item", choices=["TokyoInsider", "Nyaa", "Kayoanime", "Reset"]).ask()
        if select == "TokyoInsider":
            sub_select = questionary.select("Select item", choices=["Completed", "Still Airing"]).ask()
            if sub_select == "Completed":
                choice = 1
                anime.Tokyoinsider().tokyoinsider_search(search_term, choice)
            else:
                choice = 2
                anime.Tokyoinsider().tokyoinsider_search(search_term, choice)
        elif select == "Nyaa":
            anime.Nyaa().nyaa_search(search_term)
        elif select == "Kayoanime":
            sub_select = questionary.select("Select item", choices=["Search by Title", "Show all Ongoing Anime"]).ask()
            if sub_select == "Search by Title":
                choice = 1
                anime.Kayoanime().kayoanime_search(search_term, choice)
            else:
                choice = 2
                anime.Kayoanime().kayoanime_search(search_term, choice)
        else:
            choice()
    elif type == "Book":
        search_term = input("Enter the title or the author of the Book: ")
        select = questionary.select("Select item", choices=["Libgen", "Annas Archive", "1337x", "Reset"]).ask()
        if select == "Libgen":
            sub_select = questionary.select("Select item", choices=["Search by Title", "Search by Author"]).ask()
            if sub_select == "Search by Title":
                choice = 1
                books.Libgen().libgen_search(search_term, choice)
            else:
                choice = 2
                books.Libgen().libgen_search(search_term, choice)
        elif select == "Annas Archive":
            select = questionary.select("Select item", choices=["Search by Title", "Search by Author"]).ask()
            if select == "Search by Title":
                choice = 1
                books.Libgen().libgen_search(search_term, choice)
            else:
                choice = 2
                books.Libgen().libgen_search(search_term, choice)
        elif select == "1337x":
            books.Torrent().torrent_search(search_term)
        else:
            choice()
    elif type == "Manga":
        search_term = input("Enter the title of the Manga: ")
        select = questionary.select("Select item", choices=["Bato", "Mangasee", "ComicExtra", "Reset"]).ask()
        if select == "Bato":
            manga.bato(search_term)
        elif select == "Mangasee":
            manga.mangasee(search_term)
        elif select == "ComicExtra":
            manga.comicextra(search_term)
        else:
            choice()
    elif type == "Music":
        search_term = input("Enter the title of the Music: ")
        select = questionary.select("Select item", choices=["Lightaudio", "Bomb-music", "Pagalnew", "Reset"]).ask()
        if select == "Lightaudio":
            music.lightaudio(search_term)
        elif select == "Bomb-music":
            music.bombmusic(search_term)
        elif select == "Pagalnew":
            music.pagalnew(search_term)
        else:
            choice()
    elif type == "TV/Movie":
        search_term = input("Enter the title of the TV-Series/Movie: ")
        select = questionary.select("Select item", choices=["Vadapav", "1337x", "LimeTorrent", "Reset"]).ask()
        if select == "Vadapav":
            tv.vadapav(search_term)
        elif select == "1337x":
            tv.torrent(search_term)
        elif select == "LimeTorrent":
            tv.lime(search_term)
        else:
            choice()
    elif type == "Exit":
        pass

dir = "Download"
if not os.path.isdir(dir):
    os.mkdir(dir)
    os.chdir(dir)
else:
    os.chdir(dir)

choice()
