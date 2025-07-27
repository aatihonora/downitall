"""Global_Functions"""

import os
import re
import shutil
import subprocess
import sys
import time

import pandas as pd
import questionary
import requests
import tqdm
from bs4 import BeautifulSoup
from cbz_generator import create_cbz_archive as cbz_generator
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from term_image.image import from_url
from tqdm.auto import tqdm


class Globalfunctions:
    """Global_Functions"""

    def webdriver(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--headless=new")
        options.add_argument("--disable-renderer-backgrounding")
        options.add_argument("--disable-background-timer-throttling")
        options.add_argument("--disable-backgrounding-occluded-windows")
        options.add_argument("--disable-client-side-phishing-detection")
        options.add_argument("--disable-crash-reporter")
        options.add_argument("--disable-oopr-debug-crash-dump")
        options.add_argument("--no-crash-upload")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-low-res-tiling")
        options.add_argument("--log-level=3")
        options.add_argument("--silent")
        options.page_load_strategy = "eager"
        driver = webdriver.Chrome(options=options)
        bookcli = os.getcwd()
        return driver, bookcli

    ############################################################################
    def directory(self, name):
        if not os.path.isdir(name):
            os.mkdir(name)
            os.chdir(name)
        else:
            os.chdir(name)

    ############################################################################
    # Defining the function for moving through pages, it takes name, pages(total pages) and, index(starting of pages).
    def page_navigation(self, name, pages, index):
        # If statement to confirm what user choose, next or previous page.
        if name == "Next Page":
            # If statement to check whether it isn't the last page, if not add one else reset the count.
            if index < pages:
                index += 1
            else:
                index = 1
        else:
            # If statement to check whether it isn't the first page, if not add one else don't change the count.
            if index != 1:
                index -= 1
            else:
                index = 1
        return index

    ############################################################################
    # Defining the function to check if an element exists in the current page.
    def exists(self, element):
        driver = Globalfunctions().webdriver()[0]
        # Using try except to use the error catching as false argument.
        try:
            driver.find_element(By.CSS_SELECTOR, element)
        except NoSuchElementException:
            return False
        return True

    ############################################################################
    # Defining the function for tables through pandas, table is the element.
    def visual_tables(self, table):
        # Finding the table body from table element.
        tbody = table.find("tbody")
        # Creating data list and row list. Looping to find all table rows and cells while appending cell text to row list and appending row list to data list.
        data = []
        for row in tbody.find_all("tr"):
            row_data = []
            for cell in row.find_all("td"):
                cell_info = cell.text.strip()
                clean_cell = re.sub(r"\s+", " ", cell_info)
                row_data.append(clean_cell[:90])
            data.append(row_data)
        # Creating a pandas dataframe
        df = pd.DataFrame(data)
        pd.set_option("display.max_rows", None)
        return df

    ############################################################################
    # Defining the function for player to choose the index.
    def user_choice(self, name_list, link_list, index_list, label):
        # Appendind data for next and previous page.
        # Creating two dictionary that take key as index and value as items from "link_list" and "name_list" respectively.
        url_dict = {index_list[i]: link_list[i] for i in range(len(link_list))}
        name_dict = {index_list[i]: name_list[i] for i in range(len(name_list))}
        try:
            # If statement in case no manga/chapter was found.
            if label == "no_page" and not name_list:
                print("\nCould not find any thing :(")
                sys.exit()
            elif label == "paged" and len(name_list) == 2:
                print("\nCould not find any thing :(")
                sys.exit()
            elif label == "next_only" and len(name_list) == 1:
                print("\nCould not find any thing :(")
                sys.exit()
            else:
                # Matching the user selection with "urls_dict" dictionary to get its value.
                selection = int(input("\n\nSelect the index number: "))
                if selection in url_dict:
                    # Getting the name and link by matching the index number from dictionaries.
                    link = f"{url_dict[selection]}"
                    name = f"{name_dict[selection]}"
                    print("\nFetching, please wait...")
                    subprocess.call(["clear"])
                    return [link, name, selection]
                else:
                    raise ValueError
        except ValueError:
            print("\nInvalid integer. The number must be in the range.")

    ############################################################################
    def retry(self):
        from downitall.core import Core

        # Using match case argument to see which class called the function.
        answer = questionary.select(
            "Do you want to download another file? ", choices=["Yes", "No"]
        ).ask()
        if answer == "Yes":
            Core().questions()
        else:
            sys.exit()


############################################################################
############################################################################


class Anime:
    """Anime functions"""

    # Defining the function for player to choose the index.
    def xdcc_choice(self, link_list, index_list, label):
        # Appendind data for next and previous page.
        # Creating two dictionary that take key as index and value as items from "link_list" and "name_list" respectively.
        url_dict = {index_list[i]: link_list[i] for i in range(len(link_list))}
        try:
            # If statement in case no manga/chapter was found.
            if label == "no_page" and not link_list:
                print("\nCould not find any thing :(")
                sys.exit()
            elif label == "paged" and len(link_list) == 2:
                print("\nCould not find any thing :(")
                sys.exit()
            elif label == "next_only" and len(link_list) == 1:
                print("\nCould not find any thing :(")
                sys.exit()
            else:
                while True:
                    # Matching the user selection with "urls_dict" dictionary to get its value.
                    start = int(input("\n\nSelect the starting index number: "))
                    end = int(input("\n\nSelect the ending index number: "))
                    if start in url_dict and end in url_dict:
                        # Getting the name and link by matching the index number from dictionaries.
                        start_link = f"{url_dict[start]}"
                        end_link = f"{url_dict[end]}"
                        start_index = start
                        end_index = end
                        print("\nFetching, please wait...")
                        subprocess.call(["clear"])
                        return [start_link, end_link, start_index, end_index]
                    else:
                        raise ValueError
        except ValueError:
            print("\nInvalid integer. The number must be in the range.")

    ############################################################################
    def download(self, name, url):
        bookcli = Globalfunctions().webdriver()[1]
        # Making the folder and opening it
        anime = re.sub("[^a-z,0-9]", "_", name, flags=re.IGNORECASE)
        if not os.path.isdir(anime):
            os.mkdir(anime)
            os.chdir(anime)
        elif bookcli.split("/")[-1] == anime:
            pass
        else:
            os.chdir(anime)
        # Downloading the file with wget as it is fast and has its own progress bar.
        args = ["wget", url]
        subprocess.call(args)
        print("\nDownload Complete.")


############################################################################
############################################################################


class Book:

    def download(self, name, url):
        # Reformatting the book name to a standard name and sending a request to server with connection as active.
        book_name = re.sub("[^a-z,0-9.]", "_", name, flags=re.IGNORECASE)
        with requests.get(url, stream=True) as res:
            # Checking header to get the content length, in bytes.
            total_length = int(res.headers.get("Content-Length"))
            # Checking if request was valid.
            if res.status_code == 200:
                # Implement progress bar via tqdm.
                with tqdm.wrapattr(res.raw, "read", total=total_length, desc="") as raw:
                    # Downloading image via shutil.
                    with open(book_name, "wb") as f:
                        shutil.copyfileobj(raw, f)
                print("\nBook sucessfully Downloaded: ", book_name)
            else:
                print("\nBook couldn't be retrieved")


############################################################################
############################################################################


class Manga:

    def confirmation(self, selection, index_list, img_list):
        img_dict = {
            index_list[i]: img_list[j]
            for i, j in enumerate(range(len(img_list)), start=1)
        }
        img = f"{img_dict[selection]}"
        image = from_url(img)
        subprocess.call(["clear"])
        print(f"\n{image}\n\n")
        answer = questionary.select("Is this the manga?", choices=["Yes", "No"]).ask()
        if answer == "Yes":
            subprocess.call(["clear"])
            return True
        else:
            subprocess.call(["clear"])
            return False

    ############################################################################
    def download_directory(self, manga_name, chapter_name):
        manga = re.sub("[^a-z,0-9]", "_", manga_name, flags=re.IGNORECASE)
        chapter = re.sub("[^a-z,0-9]", "_", chapter_name, flags=re.IGNORECASE)
        if not os.path.isdir(manga):
            os.mkdir(manga)
            os.chdir(manga)
            path = os.getcwd()
            if not os.path.isdir(chapter):
                os.mkdir(chapter)
                os.chdir(chapter)
            else:
                os.chdir(chapter)
        elif os.path.isdir(manga):
            os.chdir(manga)
            path = os.getcwd()
            if not os.path.isdir(chapter):
                os.mkdir(chapter)
                os.chdir(chapter)
            else:
                os.chdir(chapter)
        else:
            os.chdir(manga)
            path = os.getcwd()
            os.chdir(chapter)
        return [path, manga, chapter]

    ############################################################################
    def download_compress(self, manga_name, chapter_name, img_links_list):
        # Using regex to get the standard naming protocols for easy folder making.
        try:
            data = Manga().download_directory(manga_name, chapter_name)
            path = data[0]
            manga = data[1]
            chapter = data[2]
            Manga().download(img_links_list, manga, chapter, path)
            # Accessing the manga folder to compress chapter folder into cbz file.
            os.chdir(path)
            # Compressing chapter folder into cbz file using cbz_generator module.
            cbz_generator.create_cbz_archive(chapter, path, f"{manga}_{chapter}")
            print("\nDownload Complete")
        except OSError as e:
            print("\n", e)

    ############################################################################
    def download(self, img_links_list, manga, chapter, path):
        # Enumerating the "img_links_list" to get each link with index.
        for i, img in enumerate(img_links_list):
            # Sending request to the image link.
            with requests.get(img, stream=True) as res:
                # Checking header to get the content length, in bytes.
                total_length = int(res.headers.get("Content-Length"))
                # Checking if request was valid.
                if res.status_code == 200:
                    # Naming the image and storing it.
                    image = f"{chapter} Image {i}.jpg"
                    # Implement progress bar via tqdm.
                    with tqdm.wrapattr(
                        res.raw, "read", total=total_length, desc=""
                    ) as raw:
                        # Downloading image via shutil.
                        with open(image, "wb") as f:
                            shutil.copyfileobj(raw, f)
                    print(f"Image sucessfully Downloaded: {image}\n")
                else:
                    print("Image Couldn't be retrieved")

    ############################################################################
    def batch_download(self, name_list, link_list, name):
        download_dir = os.getcwd()
        total_links = len(link_list)
        if os.path.isfile(f".{name}.txt"):
            file = open(f".{name}.txt", "r+")
            data = file.read()
            start = len(data)
        else:
            open(f".{name}.txt", "x")
            file = open(f".{name}.txt", "r+")
            start = 0
        for chapter_name in name_list[start:]:
            data = Manga().download_directory(name, chapter_name)
            path = data[0]
            manga = data[1]
            chapter = data[2]
            os.chdir(path)
            if not os.path.isdir("Cbz"):
                os.mkdir("Cbz")
            os.chdir("Cbz")
            cbz = os.getcwd()
            os.chdir(download_dir)
            for url in link_list[start:]:
                driver = Globalfunctions().webdriver()[0]
                driver.get(url)
                time.sleep(2)
                os.chdir(path)
                os.chdir(chapter)
                soup = BeautifulSoup(driver.page_source, "html.parser")
                # Getting the working download link from html webpage.
                # Finding all the mentioned elements from webpage.
                html_tag = soup.find_all(
                    "img", src=lambda line: "manga" in line or "comic" in line
                )
                # Creating the list to store image url.
                img_links_list = []
                # Finding all the mentioned elements from img_html_chapter.
                for imgs in html_tag:
                    img_links_list.append(imgs["src"].strip())
                Manga().download(img_links_list, manga, chapter, path)
                link_list.pop(0)
                new_total_links = len(link_list)
                # Accessing the manga folder to compress chapter folder into cbz file.
                os.chdir(path)
                # Compressing chapter folder into cbz file using cbz_generator module.
                cbz_generator.create_cbz_archive(chapter, cbz, f"{manga}_{chapter}")
                os.chdir(download_dir)
                file.write(str(total_links - new_total_links))
                data = file.read()
                start = len(data)
                break
        os.remove(f".{name}.txt")
        print("\nDownload Complete.")


############################################################################
############################################################################


class Music:

    def download(self, name, url):
        # Downloading the file with wget as it is fast and has its own progress bar.
        args = ["wget", "-O", name, f"{url}"]
        subprocess.call(args)
        print("\nDownload Complete.")


############################################################################
############################################################################


class Stream:

    def link_check(self, url):
        try:
            res = requests.get(url)
            if res.status_code == 200:
                answer = questionary.select(
                    "Select item", choices=["Best", "Worst"]
                ).ask()
                if answer == "Best":
                    quality = "best"
                else:
                    quality = "worst"
                ## VLC is for android and MPV is for Window
                # subprocess.call(["vlc", url, quality])
                subprocess.call(["mpv", "--really-quiet", "--fs", url])
                return True
            else:
                print("Dead link")
                return False
        except requests.exceptions.RequestException:
            return False


############################################################################
############################################################################
