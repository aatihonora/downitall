"""Anime Sources"""

# Importing necessary modules
import os
import re
import subprocess
import time

import gdown
import requests
from bs4 import BeautifulSoup
from downitall.resources.globalfunctions import Anime, Globalfunctions
from selenium.common.exceptions import (SessionNotCreatedException,
                                        TimeoutException, WebDriverException)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from xdcc_dl.entities import IrcServer, XDCCPack
from xdcc_dl.xdcc import download_packs

driver = Globalfunctions().webdriver()[0]
bookcli = Globalfunctions().webdriver()[1]


class Animesources:
    ########################################################################################################
    ########################################################################################################
    class Kayoanime:
        def kayoanime_search(self, search_term):
            Globalfunctions().directory(name="Anime")
            label = "next_only"
            web_url = f"https://kayoanime.com/?s={search_term}"
            try:
                # Sending request to the webpage.
                driver.get(web_url)
                # Getting html page with BeautifulSoup module
                while True:
                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    # Finding all the mentioned elements from webpage.
                    html_tag = soup.find("div", class_="container-wrapper").find_all(
                        "a", class_="post-thumb", attrs={"aria-label": True}
                    )
                    # Creating lists and appending next page.
                    index_list = []
                    name_list = []
                    link_list = []
                    index_list.append(0)
                    name_list.append("Next Page")
                    link_list.append("")
                    for i, links in enumerate(html_tag, start=1):
                        index_list.append(i)
                        name_list.append(links["aria-label"].strip())
                        link_list.append(links["href"])
                    # Printing the index anf name for user to choose from.
                    print("\n")
                    for i, names in zip(index_list, name_list):
                        print(f"{i}. {names}")
                    # Calling user_choice function to get list called data and use the user selected options.
                    data = Globalfunctions().user_choice(
                        name_list, link_list, index_list, label
                    )
                    url = data[0]
                    name = data[1]
                    if name == "Next Page":
                        # Calling exists function to check if an element exists.
                        if (
                            Globalfunctions().exists(
                                element=".container-wrapper.show-more-button.load-more-button.infinite-scroll-archives"
                            )
                            == True
                        ):
                            WebDriverWait(driver, 1).until(
                                EC.element_to_be_clickable(
                                    (
                                        By.CSS_SELECTOR,
                                        ".container-wrapper.show-more-button.load-more-button.infinite-scroll-archives",
                                    )
                                )
                            ).click()
                        # Finding the last element on the page by TAG to scroll to the bottom of the page.
                        elem = driver.find_element(By.TAG_NAME, "html")
                        elem.send_keys(Keys.END)
                        time.sleep(2)
                    else:
                        break
                # Sending get request to the "manga_link" website.
                driver.get(url)
                # Parsering the response with "BeauitifulSoup".
                soup = BeautifulSoup(driver.page_source, "html.parser")
                # Finding all the mentioned elements in the webpage.
                html_tag = soup.find("a", target="_blank")
                # Getting the url by spliting the string by ? and getting the first part.
                url = html_tag["href"].split("?")[0]
                # Downloading google folders using gdown libraries.
                gdown.download_folder(url)
                # Calling retry function to start this entire method again.
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
            except (
                RuntimeError,
                gdown.exceptions.FileURLRetrievalError,
                gdown.exceptions.FolderContentsMaximumLimitError,
                PermissionError,
            ):
                print("\nGoogle file is either private or unavilable")
            except KeyboardInterrupt:
                print("\n\nCancelled by user.")

    ############################################################################
    class Tokyoinsider:
        def tokyoinsider_search(self, search_term, choice):
            # Declaring function level variables.
            Globalfunctions().directory(name="Anime")
            label = "paged"
            index = 1
            # Making search term better for url through regex.
            term = re.sub(r"\W", "+", search_term)
            # Checking weather search if for title or author/
            if choice == 1:
                search_type = "&s=completed"
            else:
                search_type = "&s=airing"
            # Url to access the website.
            web_url = f"https://www.tokyoinsider.com/anime/search?k={term}{search_type}"
            # Url to be used for page navigation.
            page_url = web_url + "&start="
            # Url to access the base website
            base_url = "https://www.tokyoinsider.com"
            try:
                while True:
                    # Sending request to the webpage.
                    driver.get(web_url)
                    # Getting html page with BeautifulSoup module
                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    # Checking weather the element exists.
                    if Globalfunctions().exists(element=".pager"):
                        html_tag = soup.find("div", class_="pager")
                        # Finding the last td tag and getting its text which is the number of last page and converting it into integer.
                        pages = int(html_tag.find_all("a", class_=None)[-1].getText())
                    else:
                        pages = 1
                    # Finding all the mentioned elements from webpage.
                    table = soup.find(
                        "table",
                        attrs={
                            "width": "100%",
                            "border": "0",
                            "cellspacing": "0",
                            "cellpadding": "3",
                        },
                    )
                    # Calling the table function.
                    df = Globalfunctions().visual_tables(table)
                    # Selecting columns that user can see.
                    df_table = df.iloc[:, [1]]
                    # Making table index start from 1.
                    df_table.index += 1
                    # Converting index column into index list.
                    link_list = []
                    index_list = df_table.index.tolist()
                    name_list = df[df.columns[1]].values.tolist()
                    # Finding the links and making link list.
                    html_tag = soup.find_all(
                        "a", title=True, attrs={"style": "display: block"}
                    )
                    for links in html_tag:
                        link_list.append(base_url + links["href"])
                    # Appending next page on 0 index and previous page on last index i+1.
                    index_list.append(0)
                    name_list.append("Next Page")
                    link_list.append(page_url)
                    index_list.append(len(df_table.index.tolist()) + 1)
                    name_list.append("Previous Page")
                    link_list.append(page_url)
                    # Printing the index and name for user to choose from.
                    print("\n0. Next Page")
                    print(df_table)
                    print(f"{len(df_table.index.tolist())+1}. Previous Page")
                    # Calling the user choice function.
                    data = Globalfunctions().user_choice(
                        name_list, link_list, index_list, label
                    )
                    url = data[0]
                    name = data[1]
                    # Calling the page_navigation function to get new index number for pages.
                    index = Globalfunctions().page_navigation(name, pages, index)
                    if pages == 1:
                        web_url = url + "0"
                    else:
                        # This website uses item numbers instead of pages so here multiplication 20 is necessary.
                        web_url = url + str((index - 1) * 20)
                    if name != "Next Page" and name != "Previous Page":
                        # Sending get request to the website.
                        label = "no_page"
                        driver.get(url)
                        # Parsering the response with "BeauitifulSoup".
                        soup = BeautifulSoup(driver.page_source, "html.parser")
                        # Finding all the mentioned elements in the webpage.
                        html_tag = soup.find_all("a", class_="download-link")
                        # Making lists and appending to them the data.
                        index_list = []
                        name_list = []
                        link_list = []
                        for i, links in enumerate(html_tag, start=1):
                            index_list.append(i)
                            name_list.append(links.text.strip())
                            link_list.append(base_url + links["href"])
                        # Reversing the name and link list to have better organized data.
                        name_list.reverse()
                        link_list.reverse()
                        # Printing the index and name for user to choose from.
                        print("\n")
                        for i, names in zip(index_list, name_list):
                            print(f"{i}. {names}")
                        # Calling the user choice function.
                        data = Globalfunctions().user_choice(
                            name_list, link_list, index_list, label
                        )
                        url = data[0]
                        # Sending request with selenium webdriver.
                        label = "no_page"
                        driver.get(url)
                        # Parsering the response with "BeauitifulSoup".
                        soup = BeautifulSoup(driver.page_source, "html.parser")
                        # Getting the working download link from html webpage.
                        html_tag = soup.find_all("a", href=lambda t: t and "media" in t)
                        index_list = []
                        name_list = []
                        link_list = []
                        for i, links in enumerate(html_tag, start=1):
                            index_list.append(i)
                            name_list.append(links.text.strip())
                            link_list.append(links["href"])
                        name_list.reverse()
                        link_list.reverse()
                        print("\n")
                        for i, names in zip(index_list, name_list):
                            print(f"{i}. {names}")
                        data = Globalfunctions().user_choice(
                            name_list, link_list, index_list, label
                        )
                        url = data[0]
                        Anime().download(name, url)
                        Globalfunctions().retry()
                        break
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
        def tokyoinsider_batch(self, search_term, choice):
            # Declaring function level variables.
            Globalfunctions().directory(name="Anime")
            label = "paged"
            index = 1
            # Making search term better for url through regex.
            term = re.sub(r"\W", "+", search_term)
            # Checking the filter used.
            if choice == 1:
                search_type = "&s=completed"
            else:
                search_type = "&s=airing"
            # Url to access the website.
            web_url = f"https://www.tokyoinsider.com/anime/search?k={term}{search_type}"
            # Url to be used for page navigation.
            page_url = web_url + "&start="
            # Url to access the base website
            base_url = "https://www.tokyoinsider.com"
            try:
                while True:
                    # Sending request to the webpage.
                    driver.get(web_url)
                    # Getting html page with BeautifulSoup module
                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    # Checking weather the element exists.
                    if Globalfunctions().exists(element=".pager"):
                        html_tag = soup.find("div", class_="pager")
                        # Finding the last td tag and getting its text which is the number of last page and converting it into integer.
                        pages = int(html_tag.find_all("a", class_=None)[-1].getText())
                    else:
                        pages = 1
                    # Finding all the mentioned elements from webpage.
                    table = soup.find(
                        "table",
                        attrs={
                            "width": "100%",
                            "border": "0",
                            "cellspacing": "0",
                            "cellpadding": "3",
                        },
                    )
                    # Calling the table function.
                    df = Globalfunctions().visual_tables(table)
                    # Selecting columns that user can see.
                    df_table = df.iloc[:, [1]]
                    # Making table index start from 1.
                    df_table.index += 1
                    # Converting index column into index list.
                    link_list = []
                    index_list = df_table.index.tolist()
                    name_list = df[df.columns[1]].values.tolist()
                    # Finding the links and making link list.
                    html_tag = soup.find_all(
                        "a", title=True, attrs={"style": "display: block"}
                    )
                    for links in html_tag:
                        link_list.append(base_url + links["href"])
                    index_list.append(0)
                    name_list.append("Next Page")
                    link_list.append(page_url)
                    index_list.append(len(df_table.index.tolist()) + 1)
                    name_list.append("Previous Page")
                    link_list.append(page_url)
                    print("\n0. Next Page")
                    print(df_table)
                    print(f"{len(df_table.index.tolist())+1}. Previous Page")
                    # Calling the user choice function.
                    data = Globalfunctions().user_choice(
                        name_list, link_list, index_list, label
                    )
                    url = data[0]
                    name = data[1]
                    index = Globalfunctions().page_navigation(name, pages, index)
                    if pages == 1:
                        web_url = url + "0"
                    else:
                        web_url = url + str((index - 1) * 20)
                    if name != "Next Page" and name != "Previous Page":
                        label = "no_page"
                        driver.get(url)
                        # Parsering the response with "BeauitifulSoup".
                        soup = BeautifulSoup(driver.page_source, "html.parser")
                        # Finding all the mentioned elements in the webpage.
                        html_tag = soup.find_all("a", class_="download-link")
                        # Making lists and appending to them the data.
                        index_list = []
                        name_list = []
                        link_list = []
                        for i, links in enumerate(html_tag, start=1):
                            index_list.append(i)
                            name_list.append(links.text.strip())
                            link_list.append(base_url + links["href"])
                        # Reversing the name and link list to have better organized data.
                        name_list.reverse()
                        link_list.reverse()
                        # Printing the index and name for user to choose from.
                        print("\n")
                        for i, names in zip(index_list, name_list):
                            print(f"{i}. {names}")
                        # Calling the user choice function.
                        data = Anime().xdcc_choice(link_list, index_list, label)
                        start = int(data[2]) - 1
                        end = int(data[3])
                        anime = re.sub("[^a-z,0-9]", "_", name, flags=re.IGNORECASE)
                        if not os.path.isdir(anime):
                            os.mkdir(anime)
                            os.chdir(anime)
                        else:
                            os.chdir(anime)
                        for url in link_list[start:end]:
                            driver.get(url)
                            soup = BeautifulSoup(driver.page_source, "html.parser")
                            # Getting the working download link from html webpage.
                            html_tag = soup.find_all(
                                "a", href=lambda t: t and "media" in t
                            )[0]
                            url = html_tag["href"]
                            # Downloading the file with wget as it is fast and has its own progress bar.
                            args = ["wget", url]
                            subprocess.call(args)
                            print("\nDownload Complete.")
                        Globalfunctions().retry()
                        break
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
    class Nyaa:
        def nyaa_search(self, search_term):
            Globalfunctions().directory(name="Anime")
            label = "paged"
            index = 1
            term = re.sub(r"\W", "+", search_term)
            # Url to access the searching.
            web_url = f"https://nyaa.si/?q={term}&f=0&c=1_2&s=seeders&o=desc"
            page_url = f"https://nyaa.si/?q={term}&f=0&c=1_2&s=seeders&o=desc&p="
            # Url to access the base website
            base_url = "https://nyaa.si"
            try:
                while True:
                    # Sending request to the webpage.
                    driver.get(web_url)
                    # Getting html page with BeautifulSoup module
                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    if Globalfunctions().exists(element=".pagination"):
                        html_tag = soup.find("ul", class_="pagination")
                        pages = int(
                            html_tag.find_all("li", class_=None)[-1].getText().strip()
                        )
                    else:
                        pages = 1
                    # Finding all the mentioned elements from webpage.
                    table = soup.find(
                        "table",
                        class_="table table-bordered table-hover table-striped torrent-list",
                    )
                    df = Globalfunctions().visual_tables(table)
                    df_table = df.iloc[:, [1, 3]]
                    df_table.index += 1
                    index_list = df_table.index.tolist()
                    name_list = df[df.columns[1]].values.tolist()
                    link_list = []
                    td_tag = soup.find_all("td", colspan="2")
                    for a_html in td_tag:
                        for links in a_html.find_all(
                            "a", title=True, class_=None, href=True
                        ):
                            link_list.append(base_url + links["href"])
                    index_list.append(0)
                    name_list.append("Next Page")
                    link_list.append(page_url)
                    index_list.append(len(df_table.index.tolist()) + 1)
                    name_list.append("Previous Page")
                    link_list.append(page_url)
                    print("\n0. Next Page")
                    print(df_table)
                    print(f"{len(df_table.index.tolist())+1}. Previous Page")
                    data = Globalfunctions().user_choice(
                        name_list, link_list, index_list, label
                    )
                    url = data[0]
                    name = data[1]
                    index = Globalfunctions().page_navigation(name, pages, index)
                    web_url = url + str(index)
                    if name != "Next Page" and name != "Previous Page":
                        break
                driver.get(url)
                # Parsering the response with "BeauitifulSoup".
                soup = BeautifulSoup(driver.page_source, "html.parser")
                # Finding all the "a" elements in the webpage.
                html_tag = soup.find("a", class_="card-footer-item")
                driver.quit()
                dir = os.getcwd()
                url = html_tag["href"]
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
    ############################################################################
    class Nibl:
        def nibl_search(self, search_term):
            Globalfunctions().directory(name="Anime")
            label = "no_page"
            term = re.sub(r"\W", "+", search_term)
            # Url to access the searching.
            web_url = f"https://nibl.co.uk/search?query={term}"
            # Url to access the base website
            try:
                # Sending request to the webpage.
                driver.get(web_url)
                # Getting html page with BeautifulSoup module
                soup = BeautifulSoup(driver.page_source, "html.parser")
                # Finding all the mentioned elements from webpage.
                table = soup.find(
                    "table",
                    class_="border-collapse table-auto w-full whitespace-no-wrap bg-white table-striped relative shadow dark:bg-gray-800",
                )
                df = Globalfunctions().visual_tables(table)
                df_table = df.iloc[:, [0, 3, 2]]
                df_table.index += 1
                index_list = df_table.index.tolist()
                name_list = df[df.columns[3]].values.tolist()
                link_list = []
                html_tag = soup.find_all(
                    "button",
                    class_="copy-data py-1 px-2 bg-gray-300 hover:bg-gray-200 dark:bg-gray-900 dark:hover:bg-gray-800",
                )
                for links in html_tag:
                    link_list.append(
                        links["data-botname"] + " " + links["data-botpack"]
                    )
                print(df_table)
                data = Globalfunctions().user_choice(
                    name_list, link_list, index_list, label
                )
                bot = data[0].split(" ")[0]
                pack = int(data[0].split(" ")[1])
                manual = XDCCPack(IrcServer("irc.rizon.net"), f"{bot}", pack)
                # Start download
                download_packs([manual])
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
        def nibl_batch(self, search_term):
            Globalfunctions().directory(name="Anime")
            label = "no_page"
            term = re.sub(r"\W", "+", search_term)
            # Url to access the searching.
            web_url = f"https://nibl.co.uk/search?query={term}"
            # Url to access the base website
            try:
                # Sending request to the webpage.
                driver.get(web_url)
                # Getting html page with BeautifulSoup module
                soup = BeautifulSoup(driver.page_source, "html.parser")
                # Finding all the mentioned elements from webpage.
                table = soup.find(
                    "table",
                    class_="border-collapse table-auto w-full whitespace-no-wrap bg-white table-striped relative shadow dark:bg-gray-800",
                )
                df = Globalfunctions().visual_tables(table)
                df_table = df.iloc[:, [0, 3, 2]]
                df_table.index += 1
                index_list = df_table.index.tolist()
                link_list = []
                html_tag = soup.find_all(
                    "button",
                    class_="copy-data py-1 px-2 bg-gray-300 hover:bg-gray-200 dark:bg-gray-900 dark:hover:bg-gray-800",
                )
                for links in html_tag:
                    link_list.append(
                        links["data-botname"] + " " + links["data-botpack"]
                    )
                print(df_table)
                data = Anime().xdcc_choice(link_list, index_list, label)
                start_bot = data[0].split(" ")[0]
                end_bot = data[1].split(" ")[0]
                start_pack = int(data[0].split(" ")[1])
                end_pack = int(data[1].split(" ")[1])
                while True:
                    if start_bot == end_bot:
                        manual = XDCCPack(
                            IrcServer("irc.rizon.net"), f"{start_bot}", start_pack
                        )
                        from_message = XDCCPack.from_xdcc_message(
                            f"/msg {start_bot} xdcc send #{start_pack + 1}-{end_pack}",
                            os.getcwd(),
                        )
                        combined = [manual] + from_message
                        # Start download
                        download_packs(combined)
                        Globalfunctions().retry()
                    else:
                        print("Make sure to choose from single bot")
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
    class Animk:
        def animk_search(self, search_term):
            Globalfunctions().directory(name="Anime")
            label = "no_page"
            # Url to access the searching.
            web_url = f"https://xdcc.animk.info/?search={search_term}"
            # Url to access the base website
            try:
                # Sending request to the webpage.
                driver.get(web_url)
                time.sleep(4)
                # Getting html page with BeautifulSoup module
                soup = BeautifulSoup(driver.page_source, "html.parser")
                # Finding all the mentioned elements from webpage.
                table = soup.find("table", id="listtable")
                df = Globalfunctions().visual_tables(table)
                df_table = df.iloc[:, [0, 3, 2]]
                df_table.index += 1
                index_list = df_table.index.tolist()
                name_list = df[df.columns[3]].values.tolist()
                df["combined_column"] = (
                    df[df.columns[0]] + " " + df[df.columns[1]].astype(str)
                )
                link_list = df["combined_column"].values.tolist()
                print(df_table)
                data = Globalfunctions().user_choice(
                    name_list, link_list, index_list, label
                )
                bot = data[0].split(" ")[0]
                pack = int(data[0].split(" ")[1])
                manual = XDCCPack(IrcServer("irc.rizon.net"), f"{bot}", pack)
                # Start download
                download_packs([manual])
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
        def animk_batch(self, search_term):
            Globalfunctions().directory()
            label = "no_page"
            # Url to access the searching.
            web_url = f"https://xdcc.animk.info/?search={search_term}"
            # Url to access the base website
            try:
                # Sending request to the webpage.
                driver.get(web_url)
                time.sleep(6)
                # Getting html page with BeautifulSoup module
                soup = BeautifulSoup(driver.page_source, "html.parser")
                # Finding all the mentioned elements from webpage.
                table = soup.find("table", id="listtable")
                df = Globalfunctions().visual_tables(table)
                df_table = df.iloc[:, [0, 3, 2]]
                df_table.index += 1
                index_list = df_table.index.tolist()
                df["combined_column"] = (
                    df[df.columns[0]] + " " + df[df.columns[1]].astype(str)
                )
                link_list = df["combined_column"].values.tolist()
                print(df_table)
                data = Anime().xdcc_choice(link_list, index_list, label)
                start_bot = data[0].split(" ")[0]
                end_bot = data[1].split(" ")[0]
                start_pack = int(data[0].split(" ")[1])
                end_pack = int(data[1].split(" ")[1])
                while True:
                    if start_bot == end_bot:
                        manual = XDCCPack(
                            IrcServer("irc.rizon.net"), f"{start_bot}", start_pack
                        )
                        from_message = XDCCPack.from_xdcc_message(
                            f"/msg {start_bot} xdcc send #{start_pack + 1}-{end_pack}",
                            os.getcwd(),
                        )
                        combined = [manual] + from_message
                        # Start download
                        download_packs(combined)
                        Globalfunctions().retry()
                    else:
                        print("Make sure to choose from single bot")
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
