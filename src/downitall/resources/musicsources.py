"""Music Sources"""

# Importing necessary modules
import os
import re
import subprocess
import sys
import time

import pandas as pd
import questionary
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    SessionNotCreatedException,
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver.common.by import By
from term_image.image import from_url
from ytmusicapi import YTMusic

# Global variables.
# Selenium Chrome options to lessen the memory usage.
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
# Getting the current directory.
bookcli = os.getcwd()
ytmusic = YTMusic()


class Musicsources:
    """Music functions"""

    ############################################################################
    def directory(self):
        if not os.path.isdir("Music"):
            os.mkdir("Music")
            os.chdir("Music")
        else:
            os.chdir("Music")

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
                row_data.append(cell_info)
            data.append(row_data)
        # Creating a pandas dataframe
        df = pd.DataFrame(data)
        return df

    ############################################################################
    # Defining the function for player to choose the index.
    def user_choice(self, name_list, link_list, index_list, label):
        # Appendind data for next and previous page.
        # Creating two dictionary that take key as index and value as items from "link_list" and "name_list" respectively.
        url_dict = {index_list[i]: link_list[i] for i in range(len(link_list))}
        name_dict = {index_list[i]: name_list[i] for i in range(len(name_list))}
        print("\n")
        for key, value in name_dict.items():
            print(f"{key}. {value}")
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
    def download(self, name, url):
        # Downloading the file with wget as it is fast and has its own progress bar.
        args = ["wget", "-O", name, f"{url}"]
        subprocess.call(args)
        print("\nDownload Complete.")

    ############################################################################
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
    # Defining the function for retrying the user_choice function.
    def retry(self):
        # Using match case argument to see which class called the function.
        answer = questionary.select(
            "Do you want to download another file? ", choices=["Yes", "No"]
        ).ask()
        if answer == "Yes":
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
                    "Exit",
                ],
            ).ask()
            if select == "Podcast Index":
                Musicsources().Podcastindex.podcastindex(search_term)
            elif select == "Tancpol":
                Musicsources().Tancpol().tancpol(search_term)
            elif select == "PlayerFM":
                Musicsources().Player_fm().player(search_term)
            elif select == "Youtube Music":
                Musicsources().Youtubemusic().youtubemusic(search_term)
            elif select == "1337x":
                Musicsources().Torrent().torrent_search(search_term)
            else:
                pass

    ############################################################################
    ############################################################################
    class Podcastindex:
        def podcastindex(self, search_term):
            Musicsources().directory()
            # Declaring function level variables.
            label = "paged"
            index = 1
            # Making search term better for url through regex.
            term = re.sub("\W", "+", search_term)
            # Url to access webpage.
            web_url = f"https://podcastindex.org/search?q={search_term}&type=all"
            # Url to be used for page navigation.
            # Url to access the base website
            base_url = "https://podcastindex.org"
            try:
                # Sending request to the webpage.
                driver.get(web_url)
                time.sleep(3)
                # Getting html page with BeautifulSoup module
                index_list = []
                name_list = []
                link_list = []
                index_list.append(0)
                name_list.append("Next Page")
                link_list.append("")
                while True:
                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    # Finding all the mentioned elements from webpage.
                    html_tag = soup.find_all("div", class_="result-title")
                    # Finding the links and making link list.
                    for i, tag in enumerate(html_tag, start=1):
                        index_list.append(i)
                        for links in tag.find_all("a"):
                            name_list.append(links.text)
                            link_list.append(base_url + links["href"])
                    # Calling the user choice function.
                    data = Musicsources().user_choice(
                        name_list, link_list, index_list, label
                    )
                    url = data[0]
                    name = data[1]
                    if name == "Next Page":
                        driver.execute_script(
                            "window.scrollTo(0, document.body.scrollHeight);"
                        )
                        time.sleep(5)
                    else:
                        break
                driver.get(url)
                time.sleep(3)
                index_list = []
                name_list = []
                link_list = []
                index_list.append(0)
                name_list.append("Next Page")
                link_list.append("")
                while True:
                    # Getting html page with BeautifulSoup module
                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    # Finding all the mentioned elements from webpage.
                    html_tag = soup.find_all("a", class_="episode-link")
                    name_tag = soup.find_all("div", class_="episode-title")
                    # Finding the links and making link list.
                    for i, links in enumerate(html_tag, start=1):
                        index_list.append(i)
                        link_list.append(links["href"])
                    for names in name_tag:
                        name_list.append(names.text)
                    # Calling the user choice function.
                    data = Musicsources().user_choice(
                        name_list, link_list, index_list, label
                    )
                    url = data[0]
                    name = data[1]
                    if name == "Next Page":
                        driver.execute_script(
                            "window.scrollTo(0, document.body.scrollHeight);"
                        )
                        time.sleep(2)
                    else:
                        name = data[1] + ".mp3"
                        break
                Musicsources().download(name, url)
                Musicsources().retry()
            except SessionNotCreatedException:
                print(
                    "\nIf you are not using android then install from win_linux_requirement.txt file"
                )
            except (
                requests.exceptions.RequestException,
                WebDriverException,
                TimeoutException,
            ):
                print("\nNetwork Error!")
            except TypeError as e:
                pass
            except (IndexError, AttributeError, UnboundLocalError):
                print("\nCould not find any thing :(")
            except KeyboardInterrupt:
                print("\n\nCancelled by user.")

    ############################################################################
    ############################################################################
    class Tancpol:
        def tancpol(self, search_term):
            Musicsources().directory()
            # Declaring function level variables.
            source = "bombmusic"
            label = "no_page"
            # Url to access webpage.
            web_url = f"https://st-tancpol.ru/music/{search_term}"
            # Url to access the base website
            base_url = "https://st-tancpol.ru"
            try:
                # Sending request to the webpage.
                driver.get(web_url)
                # Getting html page with BeautifulSoup module
                soup = BeautifulSoup(driver.page_source, "html.parser")
                # Finding all the mentioned elements from webpage.
                html_tag = soup.find_all("p", class_="item-subtitle nowrap pajax-link")
                index_list = []
                name_list = []
                link_list = []
                # Finding the links and making link list.
                for i, links in enumerate(html_tag, start=1):
                    index_list.append(i)
                    link_list.append(base_url + links["href"])
                    name_list.append(links.text)
                # Calling the user choice function.
                data = Musicsources().user_choice(
                    name_list, link_list, index_list, label
                )
                url = data[0]
                name = data[1] + ".mp3"
                driver.get(web_url)
                # Getting html page with BeautifulSoup module
                soup = BeautifulSoup(driver.page_source, "html.parser")
                # Finding all the mentioned elements from webpage.
                url = (
                    "https:"
                    + soup.find(
                        "div",
                        class_="item-track fx-row fx-middle song playitem track-item",
                    )["data-file"]
                )
                print(url)
                Musicsources().download(name, url)
                Musicsources().retry()
            except SessionNotCreatedException:
                print(
                    "\nIf you are not using android then install from win_linux_requirement.txt file"
                )
            except (
                requests.exceptions.RequestException,
                WebDriverException,
                TimeoutException,
            ):
                print("\nNetwork Error!")
            except TypeError as e:
                pass
            except (IndexError, AttributeError, UnboundLocalError):
                print("\nCould not find any thing :(")
            except KeyboardInterrupt:
                print("\n\nCancelled by user.")

    ############################################################################
    ############################################################################
    class Player_fm:
        def player(self, search_term):
            Musicsources().directory()
            # Declaring function level variables.
            label = "next_only"
            # Making search term better for url through regex.
            term = re.sub("\W", "+", search_term)
            # Url to access webpage.
            web_url = f"https://player.fm/search/{term}"
            # Url to access the base website
            base_url = "https://player.fm"
            try:
                # Sending request to the webpage.
                driver.get(web_url)
                index_list = []
                name_list = []
                link_list = []
                # Finding the links and making link list.
                index_list.append(0)
                name_list.append("Next Page")
                link_list.append("")
                while True:
                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    # Finding all the mentioned elements from webpage.
                    html_tag = soup.find_all(["h3", "h2"], class_="title")
                    for i, links in enumerate(html_tag, start=1):
                        link = links.find("a")
                        index_list.append(i)
                        name_list.append(link.text.strip())
                        link_list.append(base_url + link["href"].strip())
                    # Calling the user choice function.
                    data = Musicsources().user_choice(
                        name_list, link_list, index_list, label
                    )
                    url = data[0]
                    name = data[1]
                    if name == "Next Page":
                        scroll_amount = 1000
                        driver.execute_script(f"window.scrollBy(0, {scroll_amount})")
                        time.sleep(2)
                    else:
                        break
                driver.get(url)
                index_list = []
                name_list = []
                link_list = []
                index_list.append(0)
                name_list.append("Next Page")
                link_list.append("")
                while True:
                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    html_tag = soup.find_all("main")[3]
                    html_tag_name = html_tag.find_all("h3", class_="title")
                    html_tag_link = html_tag.find_all(
                        "a", class_="normal action playable round-button info-right"
                    )
                    for i, tag in enumerate(html_tag_name, start=1):
                        for names in tag.find_all("a"):
                            index_list.append(i)
                            name_list.append(names.text.strip())
                    for links in html_tag_link:
                        link_list.append(links["href"])
                    data = Musicsources().user_choice(
                        name_list, link_list, index_list, label
                    )
                    url = data[0]
                    name = data[1]
                    if name == "Next Page":
                        scroll_amount = 1000
                        driver.execute_script(f"window.scrollBy(0, {scroll_amount})")
                        time.sleep(2)
                    else:
                        name = re.sub("\W", "_", data[1]) + ".mp3"
                        break
                Musicsources().download(name, url)
                Musicsources().retry()
            except SessionNotCreatedException:
                print(
                    "\nIf you are not using android then install from win_linux_requirement.txt file"
                )
            except (
                requests.exceptions.RequestException,
                WebDriverException,
                TimeoutException,
            ):
                print("\nNetwork Error!")
            except TypeError as e:
                pass
            except (IndexError, AttributeError, UnboundLocalError):
                print("\nCould not find any thing :(")
            except KeyboardInterrupt:
                print("\n\nCancelled by user.")

    ############################################################################
    ############################################################################
    class Youtubemusic:
        def youtubemusic(self, search_term):
            try:
                Musicsources().directory()
                base_url = "https://music.youtube.com/watch?v="
                label = "no_page"
                search = ytmusic.search(search_term, "songs", limit=50)
                index_list = []
                name_list = []
                link_list = []
                for i, element in enumerate(search, start=1):
                    index_list.append(i)
                    name_list.append(
                        element["title"] + " - " + element["album"]["name"]
                    )
                    link_list.append(base_url + element["videoId"])
                data = Musicsources().user_choice(
                    name_list, link_list, index_list, label
                )
                url = data[0]
                name = data[1]
                new_name = re.sub("[^a-z,0-9]", "_", name, flags=re.IGNORECASE)
                subprocess.call(
                    ["yt-dlp", "-x", "--audio-format", "mp3", "-o", new_name, url]
                )
                Musicsources().retry()
            except SessionNotCreatedException:
                print(
                    "\nIf you are not using android then install from win_linux_requirement.txt file"
                )
            except (
                requests.exceptions.RequestException,
                WebDriverException,
                TimeoutException,
            ):
                print("\nNetwork Error!")
            except TypeError as e:
                pass
            except (IndexError, AttributeError, UnboundLocalError):
                print("\nCould not find any thing :(")
            except KeyboardInterrupt:
                print("\n\nCancelled by user.")

    ############################################################################
    ############################################################################
    class Torrent:
        def torrent_search(self, search_term):
            Musicsources().directory()
            label = "paged"
            index = 1
            term = re.sub("\W", "+", search_term)
            # Url to access the searching.
            web_url = (
                f"https://1337x.to/sort-category-search/{term}/Music/seeders/desc/1/"
            )
            page_url = (
                f"https://1337x.to/sort-category-search/{term}/Music/seeders/desc/"
            )
            # Url to access the base website
            base_url = "https://1337x.to"
            try:
                while True:
                    # Sending request to the webpage.
                    driver.get(web_url)
                    # Getting html page with BeautifulSoup module
                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    if Musicsources().exists(element=".pagination"):
                        html_tag = soup.find("div", class_="pagination")
                        if html_tag.find("li", class_="last"):
                            tag = html_tag.find("li", class_="last")
                            pages = int(
                                tag.find("a")["href"].split("desc/")[1].strip("/")
                            )
                        else:
                            pages = 1
                    else:
                        pages = 1
                    # Finding all the mentioned elements from webpage.
                    table = soup.find(
                        "table",
                        class_="table-list table table-responsive table-striped",
                    )
                    df = Musicsources().visual_tables(table)
                    df_table = df.iloc[:, [0, 1]]
                    df_table.index += 1
                    index_list = df_table.index.tolist()
                    name_list = df[df.columns[0]].values.tolist()
                    link_list = []
                    td_tag = table.find_all("td", class_="coll-1 name")
                    for a_tag in td_tag:
                        links = a_tag.find("a", text=True)
                        link_list.append(base_url + links["href"])
                    index_list.insert(0, 0)
                    name_list.insert(0, "Next Page")
                    link_list.insert(0, page_url)
                    index_list.append(len(df_table.index.tolist()) + 1)
                    name_list.append("Previous Page")
                    link_list.append(page_url)
                    data = Musicsources().user_choice(
                        name_list, link_list, index_list, label
                    )
                    url = data[0]
                    name = data[1]
                    index = Musicsources().page_navigation(name, pages, index)
                    web_url = url + str(index) + "/"
                    if name != "Next Page" and name != "Previous Page":
                        break
                # Sending get request to the website.
                driver.get(url)
                # Parsering the response with "BeauitifulSoup".
                soup = BeautifulSoup(driver.page_source, "html.parser")
                # Finding all the mentioned elements in the webpage.
                html_tag = soup.find("a", id="id1")
                url = html_tag["href"]
                dir = os.getcwd()
                # Calling the aria2c module to download.
                args = [
                    "aria2c",
                    "--file-allocation=none",
                    "--seed-time=0",
                    "-d",
                    dir,
                    url,
                ]
                subprocess.call(args)
                Musicsources().retry()
            except SessionNotCreatedException:
                print(
                    "\nIf you are not using android then install from win_linux_requirement.txt file"
                )
            except (
                requests.exceptions.RequestException,
                WebDriverException,
                TimeoutException,
            ):
                print("\nNetwork Error!")
            except TypeError as e:
                pass
            except (IndexError, AttributeError, UnboundLocalError):
                print("\nCould not find any thing :(")
            except KeyboardInterrupt:
                print("\n\nCancelled by user.")


############################################################################
