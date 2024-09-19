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

# Defining the core function of UI
def questions():
    """Function to start the core app."""
    # First question to choose the medium.
    type = questionary.select("Select item", choices=["Anime", "Book", "Manga", "Music", "TV/Movie", "Exit"]).ask()
    if type == "Anime":
        # Second question to choose the Website.
        search_term = input("Enter the title of the Anime: ")
        select = questionary.select("Select item", choices=["TokyoInsider", "Nyaa", "Kayoanime", "Reset"]).ask()
        if select == "TokyoInsider":
            # Third question to choose how to download
            download_select = questionary.select("Select item", choices=["Batch Download", "Single Download"]).ask()
            if download_select == "Batch Download":
                # Fourth question to choose filter.
                sub_select = questionary.select("Select item", choices=["Completed", "Still Airing"]).ask()
                if sub_select == "Completed":
                    choice = 1
                    anime.Tokyoinsider().tokyoinsider_batch(search_term, choice)
                else: 
                    choice = 2
                    anime.Tokyoinsider().tokyoinsider_batch(search_term, choice)
            else:
                # Fourth question to choose filter.
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
        # Second question to choose the Website.
        search_term = input("Enter the title or the author of the Book: ")
        select = questionary.select("Select item", choices=["Libgen", "Annas Archive", "1337x", "Reset"]).ask()
        if select == "Libgen":
            # Third question to choose filter.
            sub_select = questionary.select("Select item", choices=["Search by Title", "Search by Author"]).ask()
            if sub_select == "Search by Title":
                choice = 1
                books.Libgen().libgen_search(search_term, choice)
            else:
                choice = 2
                books.Libgen().libgen_search(search_term, choice)
        elif select == "Annas Archive":
            # Third question to choose filter.
            sub_select = questionary.select("Select item", choices=["Search by Title", "Search by Author"]).ask()
            if sub_select == "Search by Title":
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
        # Second question to choose the Website.
        search_term = input("Enter the title of the Manga: ")
        select = questionary.select("Select item", choices=["Bato", "Mangasee", "ComicExtra", "Reset"]).ask()
        if select == "Bato":
            # Third question to choose how to download
            download_select = questionary.select("Select item", choices=["Batch Download", "Single Download"]).ask()
            if download_select == "Batch Download":
                manga.Bato().bato_batch(search_term)
            else:
                manga.Bato().bato_search(search_term)
        elif select == "Mangasee":
            # Third question to choose how to download
            download_select = questionary.select("Select item", choices=["Batch Download", "Single Download"]).ask()
            if download_select == "Batch Download":
                manga.Mangasee().mangasee_batch(search_term)
            else:
                manga.Mangasee().mangasee_search(search_term)
        elif select == "ComicExtra":
            # Third question to choose how to download
            download_select = questionary.select("Select item", choices=["Batch Download", "Single Download"]).ask()
            if download_select == "Batch Download":
                manga.Comicextra().comicextra_batch(search_term)
            else:
                manga.Comicextra().comicextra_search(search_term)
        else:
            questions()
    elif type == "Music":
        # Second question to choose the Website.
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
        # Second question to choose the Website.
        search_term = input("Enter the title of the TV-Series/Movie: ")
        select = questionary.select("Select item", choices=["Vadapav", "1337x", "Documentaries", "Reset"]).ask()
        if select == "Vadapav":
            # Third question to choose how to download
            download_select = questionary.select("Select item", choices=["Batch Download", "Single Download"]).ask()
            if download_select == "Batch Download":
                tv.Vadapav().vadapav_batch(search_term)
            else:
                tv.Vadapav().vadapav_search(search_term)
        elif select == "1337x":
            # Third question to choose the filter
            sub_select = questionary.select("Select item", choices=["Search Movies", "Search TV-Series"]).ask()
            if sub_select == "Search Movies":
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

# Creating and changing to Download folder.
dir = "Download"
if not os.path.isdir(dir):
    os.mkdir(dir)
    os.chdir(dir)
else:
    os.chdir(dir)

# General UI and introduction with guide.
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

(*) = Website uses Torrent, (-) = Website does not have download capablities

Anime: TokyoInsider, Nyaa(*), Kayoanime
Books: Libgen, Annas Archive(-), 1337x(*)
Manga: Bato, Mangasee, ComicExtra
Music: Light Audio, Bomb Music, PlayerFM
TV-Series/Movies: Vadapav, 1337x(*), Documentaries
"""
subprocess.call(["clear"])
print(logo.center(20))

questions()
choice = 0
