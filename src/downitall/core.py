"""Bookcli"""

# Importing packages required for the program.
import os
import subprocess

import questionary
from downitall_windows.resources import (
    Animesources,
    Booksources,
    Mangasources,
    Musicsources,
    Streamsources,
    Tvsources,
)

# Space for functions start from here


############################################################################
# Defining the core function of UI
def anime():
    # Second question to choose the Website.
    search_term = input("Enter the title of the Anime: ")
    select = questionary.select(
        "Select item",
        choices=["TokyoInsider", "Nyaa", "Kayoanime", "Nibl", "Animk", "Reset", "Exit"],
    ).ask()
    if select == "TokyoInsider":
        # Third question to choose how to download
        download_select = questionary.select(
            "Select item", choices=["Single Download", "Batch Download", "Exit"]
        ).ask()
        if download_select == "Single Download":
            # Fourth question to choose filter.
            sub_select = questionary.select(
                "Select item", choices=["Completed", "Still Airing", "Exit"]
            ).ask()
            if sub_select == "Completed":
                choice = 1
                Animesources().Tokyoinsider().tokyoinsider_search(search_term, choice)
            elif sub_select == "Still Airing":
                choice = 2
                Animesources().Tokyoinsider().tokyoinsider_search(search_term, choice)
            else:
                pass
        elif download_select == "Batch Download":
            # Fourth question to choose filter.
            sub_select = questionary.select(
                "Select item", choices=["Completed", "Still Airing", "Exit"]
            ).ask()
            if sub_select == "Completed":
                choice = 1
                Animesources().Tokyoinsider().tokyoinsider_batch(search_term, choice)
            elif sub_select == "Still Airing":
                choice = 2
                Animesources().Tokyoinsider().tokyoinsider_batch(search_term, choice)
            else:
                pass
        else:
            pass
    elif select == "Nyaa":
        Animesources().Nyaa().nyaa_search(search_term)
    elif select == "Kayoanime":
        Animesources().Kayoanime().kayoanime_search(search_term)
    elif select == "Nibl":
        download_select = questionary.select(
            "Select item", choices=["Single Download", "Batch Download", "Exit"]
        ).ask()
        if download_select == "Single Download":
            Animesources().Nibl().nibl_search(search_term)
        elif download_select == "Batch Download":
            Animesources().Nibl().nibl_batch(search_term)
        else:
            pass
    elif select == "Animk":
        download_select = questionary.select(
            "Select item", choices=["Single Download", "Batch Download", "Exit"]
        ).ask()
        if download_select == "Single Download":
            Animesources().Animk().animk_search(search_term)
        elif download_select == "Batch Download":
            Animesources().Animk().animk_batch(search_term)
        else:
            pass
    elif select == "Reset":
        Core().questions()
    else:
        pass


############################################################################
def books():
    # Second question to choose the Website.
    search_term = input("Enter the title or the author of the Book: ")
    select = questionary.select(
        "Select item",
        choices=[
            "Libgen",
            "Annas Archive",
            "1337x",
            "Rutracker",
            "Golden Audio Books",
            "Reset",
            "Exit",
        ],
    ).ask()
    if select == "Libgen":
        # Third question to choose filter.
        sub_select = questionary.select(
            "Select item", choices=["Search by Title", "Search by Author", "Exit"]
        ).ask()
        if sub_select == "Search by Title":
            choice = 1
            Booksources().Libgen().libgen_search(search_term, choice)
        elif sub_select == "Search by Author":
            choice = 2
            Booksources().Libgen().libgen_search(search_term, choice)
        else:
            pass
    elif select == "Annas Archive":
        # Third question to choose filter.
        sub_select = questionary.select(
            "Select item", choices=["Search by Title", "Search by Author", "Exit"]
        ).ask()
        if sub_select == "Search by Title":
            choice = 1
            Booksources().Annas_Archive().annas_archive_search(search_term, choice)
        elif sub_select == "Search by Author":
            choice = 2
            Booksources().Annas_Archive().annas_archive_search(search_term, choice)
        else:
            pass
    elif select == "1337x":
        Booksources().Torrent().torrent_search(search_term)
    elif select == "Rutracker":
        # Third question to choose filter.
        sub_select = questionary.select(
            "Select item",
            choices=["Search General Courses", "Search Computer Courses", "Exit"],
        ).ask()
        if sub_select == "Search General Courses":
            choice = 1
            Booksources().Rutracker().rutracker(choice)
        elif sub_select == "Search Computer Courses":
            choice = 2
            Booksources().Rutracker().rutracker(choice)
        else:
            pass
    elif select == "Golden Audio Books":
        Booksources().Goldenaudiobooks().goldenaudiobooks(search_term)
    elif select == "Reset":
        Core().questions()
    else:
        pass


############################################################################
def manga():
    # Second question to choose the Website.
    search_term = input("Enter the title of the Manga: ")
    select = questionary.select(
        "Select item",
        choices=[
            "Bato",
            "Weebcentral",
            "Nyaa",
            "Rawotaku",
            "Readallcomics",
            "Reset",
            "Exit",
        ],
    ).ask()
    if select == "Bato":
        Mangasources().Bato().bato_search(search_term)
    elif select == "Weebcentral":
        # Third question to choose how to download
        download_select = questionary.select(
            "Select item", choices=["Single Download", "Batch Download", "Exit"]
        ).ask()
        if download_select == "Single Download":
            Mangasources().Weebcentral().weebcentral(search_term)
        elif download_select == "Batch Download":
            Mangasources().Weebcentral().weebcentral_batch(search_term)
        else:
            pass
    elif select == "Nyaa":
        Mangasources().Nyaa().nyaa_search(search_term)
    elif select == "Rawotaku":
        Mangasources().Rawotaku().rawotaku(search_term)
    elif select == "Readallcomics":
        Mangasources().Readallcomics().readallcomics(search_term)
    elif select == "Reset":
        Core().questions()
    else:
        pass


############################################################################
def music():
    # Second question to choose the Website.
    search_term = input("Enter the title of the Music or Podcast: ")
    select = questionary.select(
        "Select item",
        choices=[
            "Tancpol",
            "Podcast Index",
            "PlayerFM",
            "Youtube Music",
            "1337x",
            "Reset",
            "Exit",
        ],
    ).ask()
    if select == "Podcast Index":
        Musicsources().Podcastindex().podcastindex(search_term)
    elif select == "Tancpol":
        Musicsources().Tancpol().tancpol(search_term)
    elif select == "PlayerFM":
        Musicsources().Player_fm().player(search_term)
    elif select == "Youtube Music":
        Musicsources().Youtubemusic().youtubemusic(search_term)
    elif select == "1337x":
        Musicsources().Torrent().torrent_search(search_term)
    elif select == "Reset":
        Core().questions()
    else:
        pass


############################################################################
def tv():
    # Second question to choose the Website.
    search_term = input("Enter the title of the TV-Series/Movie: ")
    select = questionary.select(
        "Select item",
        choices=[
            "Vadapav",
            "1337x",
            "Documentaries",
            "Vegamovies",
            "Asian Dramas",
            "Reset",
            "Exit",
        ],
    ).ask()
    if select == "Vadapav":
        # Third question to choose how to download
        download_select = questionary.select(
            "Select item", choices=["Single Download", "Batch Download", "Exit"]
        ).ask()
        if download_select == "Single Download":
            Tvsources().Vadapav().vadapav_search(search_term)
        elif download_select == "Batch Download":
            Tvsources().Vadapav().vadapav_batch(search_term)
        else:
            pass
    elif select == "1337x":
        # Third question to choose the filter
        sub_select = questionary.select(
            "Select item",
            choices=[
                "Search Movies",
                "Search TV-Series",
                "Search Documentaries",
                "Exit",
            ],
        ).ask()
        if sub_select == "Search Movies":
            choice = 1
            Tvsources().Torrent().torrent_search(search_term, choice)
        elif sub_select == "Search TV-Series":
            choice = 2
            Tvsources().Torrent().torrent_search(search_term, choice)
        elif sub_select == "Search Documentaries":
            choice = 3
            Tvsources().Torrent().torrent_search(search_term, choice)
        else:
            pass
    elif select == "Documentaries":
        Tvsources().Documentary().documentary()
    elif select == "Vegamovies":
        Tvsources().Vegamovies().vegamovies(search_term)
    elif select == "Asian Dramas":
        Tvsources().Asian_Dramas().asian_dramas()
    elif select == "Reset":
        Core().questions()
    else:
        pass


############################################################################
def stream():
    # Second question to choose the Website.
    search_term = input("Enter the title of the media you want to Stream: ")
    select = questionary.select(
        "Select item",
        choices=[
            "Anizone",
            "Miruro",
            "Hydrahd",
            "Cxtvlive",
            "IPTV",
            "Reset",
            "Exit",
        ],
    ).ask()
    if select == "Anizone":
        Streamsources().Anizone().anizone(search_term)
    elif select == "Miruro":
        Streamsources().Miruro().miruro(search_term)
    elif select == "Hydrahd":
        Streamsources().Hydrahd().hydrahd(search_term)
    elif select == "Cxtvlive":
        Streamsources().Cxtvlive().cxtvlive()
    elif select == "IPTV":
        sub_select = questionary.select(
            "Select item", choices=["Global IPTV", "South Asian IPTV", "Exit"]
        ).ask()
        if sub_select == "Global IPTV":
            choice = 1
            Streamsources().Iptv().iptv(choice)
        elif sub_select == "South Asian IPTV":
            choice = 2
            Streamsources().Iptv().iptv(choice)
        else:
            pass
    elif select == "Reset":
        Core().questions()
    else:
        pass


############################################################################
class Core:
    def questions(self):
        """Function to start the core app."""
        # First question to choose the medium.
        type = questionary.select(
            "Select item",
            choices=["Anime", "Book", "Manga", "Music", "TV/Movie", "Stream", "Exit"],
        ).ask()
        if type == "Anime":
            anime()
        elif type == "Book":
            books()
        elif type == "Manga":
            manga()
        elif type == "Music":
            music()
        elif type == "TV/Movie":
            tv()
        elif type == "Stream":
            stream()
        elif type == "Exit":
            pass

    # Creating and changing to Download folder.
    os.chdir("/mnt/e/Downloads/")
    dir = "Downitall"
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
    
    Anime: TokyoInsider, Nyaa(*), Kayoanime, Nibl, Animk
    Books: Libgen, Annas Archive(-), 1337x(*), Rutracker(*), Golden Audio Books
    Manga: Bato, Weebcentral, Rawotaku, Nyaa(*), Readallcomics
    Music: Tancpol, Podcast Index, PlayerFM, 1337x(*), Youtube Music
    TV-Series/Movies: Vadapav, 1337x(*), Documentaries, Vegamovies, Asian Dramas
    Stream: Anizone, Miruro, Hydrahd, Cxtvlive, IPTV
    """
    subprocess.call(["clear"])
    print(logo.center(20))


choice = 0
