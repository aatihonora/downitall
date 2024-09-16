"""Bookcli"""

# Importing packages required for the program.
import os
import subprocess

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

def questions():
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
            anime.Kayoanime().kayoanime_search(search_term)
        else:
            questions()
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
                books.Annas_Archive().annas_archive_search(search_term, choice)
            else:
                choice = 2
                books.Annas_Archive().annas_archive_search(search_term, choice)
        elif select == "1337x":
            books.Torrent().torrent_search(search_term)
        else:
            questions()
    elif type == "Manga":
        search_term = input("Enter the title of the Manga: ")
        select = questionary.select("Select item", choices=["Bato", "Mangasee", "ComicExtra", "Reset"]).ask()
        if select == "Bato":
            manga.Bato().bato(search_term)
        elif select == "Mangasee":
            manga.Mangasee().mangasee(search_term)
        elif select == "ComicExtra":
            manga.Comicextra().comicextra(search_term)
        else:
            questions()
    elif type == "Music":
        search_term = input("Enter the title of the Music or Podcast: ")
        select = questionary.select("Select item", choices=["Lightaudio", "Bomb-music", "PlayerFM", "Reset"]).ask()
        if select == "Lightaudio":
            music.Light_audio().lightaudio(search_term)
        elif select == "Bomb-music":
            music.Bomb_music().bombmusic(search_term)
        elif select == "PlayerFM":
            music.Player_fm().player(search_term)
        else:
            questions()
    elif type == "TV/Movie":
        search_term = input("Enter the title of the TV-Series/Movie: ")
        select = questionary.select("Select item", choices=["Vadapav", "1337x", "Documentaries", "Reset"]).ask()
        if select == "Vadapav":
            tv.Vadapav().vadapav(search_term)
        elif select == "1337x":
            select = questionary.select("Select item", choices=["Search Movies", "Search TV-Series"]).ask()
            if select == "Search Movies":
                choice = 1
                tv.Torrent().torrent_search(search_term, choice)
            else:
                choice = 2
                tv.Torrent().torrent_search(search_term, choice)
        elif select == "Documentaries":
            tv.Documentary().documentary()
        else:
            questions()
    elif type == "Exit":
        pass

dir = "Download"
if not os.path.isdir(dir):
    os.mkdir(dir)
    os.chdir(dir)
else:
    os.chdir(dir)

logo = """
########   #######   #######  ##    ##  ######  ##       ####
##     ## ##     ## ##     ## ##   ##  ##    ## ##        ## 
##     ## ##     ## ##     ## ##  ##   ##       ##        ## 
########  ##     ## ##     ## #####    ##       ##        ## 
##     ## ##     ## ##     ## ##  ##   ##       ##        ## 
##     ## ##     ## ##     ## ##   ##  ##    ## ##        ## 
########   #######   #######  ##    ##  ######  ######## ####
\n\n

Welcome, here is a short guide about websites

(+) = Website uses Selenium, (*) = Website uses Torrent, (-) = Website does not have download capablities

Anime: TokyoInsider, Nyaa(*), Kayoanime
Books: Libgen, Annas Archive(-), 1337x(*)
Manga: Bato, Mangasee(+), ComicExtra
Music: Light Audio, Bomb Music, PlayerFM(+)
TV-Series/Movies: Vadapav, 1337x(*), Documentaries
"""
subprocess.call(["clear"])
print(logo.center(20))

questions()
choice = 0
