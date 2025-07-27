"""Music Sources"""

# Importing necessary modules
import os
import re
import subprocess
import time

import requests
from bs4 import BeautifulSoup
from downitall.resources.globalfunctions import Globalfunctions, Music
from selenium.common.exceptions import (SessionNotCreatedException,
                                        TimeoutException, WebDriverException)
from ytmusicapi import YTMusic

driver = Globalfunctions().webdriver()[0]
bookcli = Globalfunctions().webdriver()[1]


class Musicsources:

    ############################################################################
    ############################################################################
    class Podcastindex:
        def podcastindex(self, search_term):
            Globalfunctions().directory(name="Music")
            # Declaring function level variables.
            label = "next_only"
            # Making search term better for url through regex.
            term = re.sub(r"\W", "+", search_term)
            # Url to access webpage.
            web_url = f"https://podcastindex.org/search?q={term}&type=all"
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
                    print("\n")
                    for index_name, name in zip(index_list, name_list):
                        # Printing name with index for user to choose.
                        print(f"{index_name}. {name}")
                    # Calling the user choice function.
                    data = Globalfunctions().user_choice(
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
                    print("\n")
                    for index_name, name in zip(index_list, name_list):
                        # Printing name with index for user to choose.
                        print(f"{index_name}. {name}")
                    # Calling the user choice function.
                    data = Globalfunctions().user_choice(
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
                Music().download(name, url)
                Globalfunctions().retry()
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
            Globalfunctions().directory(name="Music")
            # Declaring function level variables.
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
                print("\n")
                for index_name, name in zip(index_list, name_list):
                    # Printing name with index for user to choose.
                    print(f"{index_name}. {name}")
                # Calling the user choice function.
                data = Globalfunctions().user_choice(
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
                Music().download(name, url)
                Globalfunctions().retry()
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
            Globalfunctions().directory(name="Music")
            # Declaring function level variables.
            label = "next_only"
            # Making search term better for url through regex.
            term = re.sub(r"\W", "+", search_term)
            # Url to access webpage.
            web_url = f"https://player.fm/search/{term}"
            # Url to access the base website
            base_url = "https://player.fm"
            try:
                # Sending request to the webpage.
                driver.get(web_url)
                while True:
                    index_list = []
                    name_list = []
                    link_list = []
                    # Finding the links and making link list.
                    index_list.append(0)
                    name_list.append("Next Page")
                    link_list.append("")
                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    # Finding all the mentioned elements from webpage.
                    html_tag = soup.find_all(["h3", "h2"], class_="title")
                    for i, links in enumerate(html_tag, start=1):
                        link = links.find("a")
                        index_list.append(i)
                        name_list.append(link.text.strip())
                        link_list.append(base_url + link["href"].strip())
                    print("\n")
                    for index_name, name in zip(index_list, name_list):
                        # Printing name with index for user to choose.
                        print(f"{index_name}. {name}")
                    # Calling the user choice function.
                    data = Globalfunctions().user_choice(
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
                    print("\n")
                    for index_name, name in zip(index_list, name_list):
                        # Printing name with index for user to choose.
                        print(f"{index_name}. {name}")
                    data = Globalfunctions().user_choice(
                        name_list, link_list, index_list, label
                    )
                    url = data[0]
                    name = data[1]
                    if name == "Next Page":
                        scroll_amount = 1000
                        driver.execute_script(f"window.scrollBy(0, {scroll_amount})")
                        time.sleep(2)
                    else:
                        name = re.sub(r"\W", "_", data[1]) + ".mp3"
                        break
                Music().download(name, url)
                Globalfunctions().retry()
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
            ytmusic = YTMusic()
            Globalfunctions().directory(name="Music")
            try:
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
                print("\n")
                for index_name, name in zip(index_list, name_list):
                    # Printing name with index for user to choose.
                    print(f"{index_name}. {name}")
                data = Globalfunctions().user_choice(
                    name_list, link_list, index_list, label
                )
                url = data[0]
                name = data[1]
                new_name = re.sub("[^a-z,0-9]", "_", name, flags=re.IGNORECASE)
                subprocess.call(
                    ["yt-dlp", "-x", "--audio-format", "mp3", "-o", new_name, url]
                )
                Globalfunctions().retry()
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
            Globalfunctions().directory(name="Music")
            label = "paged"
            index = 1
            term = re.sub(r"\W", "+", search_term)
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
                    if Globalfunctions().exists(element=".pagination"):
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
                    df = Globalfunctions().visual_tables(table)
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
                    print("\n")
                    for index_name, name in zip(index_list, name_list):
                        # Printing name with index for user to choose.
                        print(f"{index_name}. {name}")
                    data = Globalfunctions().user_choice(
                        name_list, link_list, index_list, label
                    )
                    url = data[0]
                    name = data[1]
                    index = Globalfunctions().page_navigation(name, pages, index)
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
                Globalfunctions().retry()
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
