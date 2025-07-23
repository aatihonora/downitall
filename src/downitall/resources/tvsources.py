"""TV Sources"""

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
from pandas.core.arrays.datetimelike import DatetimeLikeArrayMixin
from selenium import webdriver
from selenium.common.exceptions import (NoSuchElementException,
                                        SessionNotCreatedException,
                                        TimeoutException, WebDriverException)
from selenium.webdriver.common.by import By
from seleniumwire import webdriver

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


class Tvsources:
    """TV Sources"""

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
            driver.find_element(By.XPATH, element)
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
                row_data.append(cell_info[:30])
            data.append(row_data)
        # Creating a pandas dataframe
        df = pd.DataFrame(data)
        return df

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

    def download(self):
        if not os.path.isdir("TV/Movies"):
            os.mkdir("TV/Movies")
            os.chdir("TV/Movies")
        else:
            os.chdir("TV/Movies")

    ############################################################################
    # Defining the function for retrying the user_choice function.
    def retry(self):
        # Using match case argument to see which class called the function.
        answer = questionary.select(
            "Do you want to download another file? ", choices=["Yes", "No"]
        ).ask()
        if answer == "Yes":
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
            else:
                pass

    ############################################################################
    ############################################################################
    class Vadapav:
        def vadapav_search(self, search_term):
            source = "vadapav"
            label = "no_page"
            choice = 0
            # Url to access the searching.
            url = "https://vadapav.mov/"
            # Url to access the base website.
            base_url = "https://vadapav.mov"
            try:
                while True:
                    # Sending request to the webpage.
                    driver.get(url)
                    # Getting html page with BeautifulSoup module
                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    # Finding all the mentioned elements from webpage.
                    html_tag = soup.find_all(
                        "a", {"class": ["directory-entry wrap", "file-entry wrap"]}
                    )
                    print(html_tag)
                    index_list = []
                    name_list = []
                    link_list = []
                    for i, links in enumerate(html_tag, start=1):
                        index_list.append(i)
                        name_list.append(links.text.strip())
                        link_list.append(base_url + links["href"])
                    print("\n")
                    for i, name in zip(index_list, name_list):
                        print(f"{i}. {name}")
                    data = Tvsources().user_choice(
                        name_list, link_list, index_list, label
                    )
                    url = data[0]
                    name = data[1]
                    if "mkv" in url:
                        break
                # Downloading the file with wget as it is fast and has its own progress bar.
                Tvsources().download()
                args = ["wget", "-O", name, url]
                subprocess.call(args)
                print("\nDownload Complete.")
                Tvsources().retry()
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
        def vadapav_batch(self, search_term):
            source = "vadapav"
            label = "no_page"
            save = 0
            # Url to access the searching.
            url = "https://vadapav.mov/s/" + search_term
            # Url to access the base website.
            base_url = "https://vadapav.mov"
            try:
                while True:
                    # Sending request to the webpage.
                    driver.get(url)
                    # Getting html page with BeautifulSoup module
                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    # Finding all the mentioned elements from webpage.
                    html_tag = soup.find_all("a", {"class": "directory-entry wrap"})
                    index_list = []
                    name_list = []
                    link_list = []
                    for i, links in enumerate(html_tag, start=1):
                        index_list.append(i)
                        name_list.append(links.text.strip())
                        link_list.append(base_url + links["href"])
                    if save == 1:
                        name_list.pop(0)
                        link_list.pop(0)
                    for i, name in zip(index_list, name_list):
                        print(f"{i}. {name}")
                    if not link_list:
                        break
                    data = Tvsources().user_choice(
                        name_list, link_list, index_list, label
                    )
                    url = data[0]
                    name = data[1]
                    if save == 0:
                        tv_name = name
                    save += 1
                # Sending request to the webpage.
                driver.get(url)
                # Getting html page with BeautifulSoup module
                soup = BeautifulSoup(driver.page_source, "html.parser")
                # Finding all the mentioned elements from webpage.
                html_tag = soup.find_all("a", {"class": "file-entry wrap"})
                link_list = []
                name_list = []
                for links in html_tag:
                    link_list.append(base_url + links["href"])
                    name_list.append(links.text.strip())
                total_links = len(link_list)
                if not os.path.isdir(tv_name):
                    os.mkdir(tv_name)
                    os.chdir(tv_name)
                else:
                    os.chdir(tv_name)
                if os.path.isfile(f".{tv_name}.txt"):
                    file = open(f".{tv_name}.txt", "r+")
                    data = file.read()
                    start = len(data)
                else:
                    open(f".{tv_name}.txt", "x")
                    file = open(f".{tv_name}.txt", "r+")
                    start = 0
                Tvsources().download()
                for ep_name in name_list[start:]:
                    for url in link_list[start:]:
                        args = ["wget", "-O", ep_name, url]
                        subprocess.call(args)
                        link_list.pop(0)
                        new_total_links = len(link_list)
                        file.write(str(total_links - new_total_links))
                        data = file.read()
                        start = len(data)
                        break
                print("\nDownload Complete.")
                Tvsources().retry()
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
        def torrent_search(self, search_term, choice):
            source = "1337x"
            label = "paged"
            index = 1
            term = re.sub("\W", "+", search_term)
            if choice == 1:
                search_type = "Movies"
            elif choice == 2:
                search_type = "TV"
            else:
                search_type = "Documentaries"
            # Url to access the searching.
            web_url = f"https://1337x.to/sort-category-search/{term}/{search_type}/seeders/desc/1/"
            page_url = f"https://1337x.to/sort-category-search/{term}/{search_type}/seeders/desc/"
            # Url to access the base website
            base_url = "https://1337x.to"
            try:
                while True:
                    # Sending request to the webpage.
                    driver.get(web_url)
                    # Getting html page with BeautifulSoup module
                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    if Tvsources().exists(element=".pagination"):
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
                    df = Tvsources().visual_tables(table)
                    df_table = df.iloc[:, [0, 1]]
                    df_table.index += 1
                    index_list = df_table.index.tolist()
                    name_list = df[df.columns[0]].values.tolist()
                    link_list = []
                    td_tag = table.find_all("td", class_="coll-1 name")
                    for a_tag in td_tag:
                        links = a_tag.find("a", text=True)
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
                    data = Tvsources().user_choice(
                        name_list, link_list, index_list, label
                    )
                    url = data[0]
                    name = data[1]
                    index = Tvsources().page_navigation(name, pages, index)
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
                Tvsources().download()
                subprocess.call(args)
                Tvsources().retry()
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
    class Documentary:
        def documentary(self):
            source = "documentary"
            label = "no_page"
            choice = 0
            search_term = ""
            index = 1
            # Url to access the searching.
            web_url = "https://documentaryheaven.com/watch-online/"
            # Url to access the base website
            base_url = "https://documentaryheaven.com"

            try:
                # Sending request to the webpage.
                driver.get(web_url)
                # Getting html page with BeautifulSoup module
                soup = BeautifulSoup(driver.page_source, "html.parser")
                # Finding all the mentioned elements from webpage.
                html_tag = soup.find_all("a", class_="browse-all")
                index_list = []
                name_list = []
                link_list = []
                for i, links in enumerate(html_tag, start=1):
                    index_list.append(i)
                    name_list.append(links.text.replace("Browse ", ""))
                    link_list.append(base_url + links["href"])
                print("\n")
                for i, name in zip(index_list, name_list):
                    print(f"{i}. {name}")
                data = Tvsources().user_choice(name_list, link_list, index_list, label)
                web_url = data[0]
                page_url = f"{web_url}/page/"
                while True:
                    label = "paged"
                    driver.get(web_url)
                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    if Tvsources().exists(element=".numeric-nav"):
                        html_tag = soup.find("div", class_="numeric-nav")
                        tag = html_tag.find_all("li", class_=None)[-1]
                        pages = int(tag.find("a").text.strip())
                    else:
                        pages = 1
                    html_tag = soup.find_all("h2")
                    index_list = []
                    name_list = []
                    link_list = []
                    index_list.append(0)
                    name_list.append("Next Page")
                    link_list.append(page_url)
                    for i, links in enumerate(html_tag, start=1):
                        index_list.append(i)
                        name_list.append(links.text)
                        tag = links.find_all("a")
                        for link in tag:
                            link_list.append(link["href"])
                    index_list.append(i + 1)
                    name_list.append("Previous Page")
                    link_list.append(page_url)
                    print("\n")
                    for i, name in zip(index_list, name_list):
                        print(f"{i}. {name}")
                    data = Tvsources().user_choice(
                        name_list, link_list, index_list, label
                    )
                    url = data[0]
                    name = data[1]
                    index = Tvsources().page_navigation(name, pages, index)
                    web_url = url + str(index) + "/"
                    if name != "Next Page" and name != "Previous Page":
                        break
                # Sending get request to the website.
                driver.get(url)
                # Parsering the response with "BeauitifulSoup".
                soup = BeautifulSoup(driver.page_source, "html.parser")
                # Finding all the mentioned elements in the webpage.
                html_tag = soup.find("meta", attrs={"itemprop": "embedUrl"})
                if "https://www.dailymotion" in html_tag["content"].split(".com")[0]:
                    url = html_tag["content"].replace("/embed", "")
                else:
                    url = html_tag["content"]
                Tvsources().download()
                args = ["yt-dlp", url]
                subprocess.call(args)
                Tvsources().retry()
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
    class Vegamovies:
        def vegamovies(self, search_term):
            source = "vegamovies"
            label = "no_page"
            # Url to access the searching.
            web_url = f"https://vegamovies.com.lv/search.php?query={search_term}"
            base_url = "https://vegamovies.com.lv"
            try:
                while True:
                    # Sending request to the webpage.
                    driver.get(web_url)
                    # Getting html page with BeautifulSoup module
                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    # Finding all the mentioned elements from webpage.
                    html_tag = soup.find_all("p", class_="font-medium text-gray-800")
                    index_list = []
                    name_list = []
                    link_list = []
                    for i, tag in enumerate(html_tag, start=1):
                        index_list.append(i)
                        for links in tag.find_all("a"):
                            name_list.append(links.text.strip())
                            link_list.append(base_url + links["href"])
                    for i, name in zip(index_list, name_list):
                        print(f"{i}. {name}")
                    data = Tvsources().user_choice(
                        name_list, link_list, index_list, label
                    )
                    url = data[0]
                    name = data[1]
                    if name != "Next Page" and name != "Previous Page":
                        break
                driver.get(url)
                time.sleep(2)
                soup = BeautifulSoup(driver.page_source, "html.parser")
                try:
                    if driver.find_element(By.CSS_SELECTOR, "a.bg-blue-600"):
                        url = (
                            soup.find(
                                "a",
                                class_="rounded-m bg-blue-600 text-white text-[13px] font-bold px-5 py-2 rounded hover:bg-blue-500 hover:bg-blue-700",
                            )["href"]
                            + "?download=main"
                        )
                except NoSuchElementException:
                    url = (
                        soup.find(
                            "a",
                            class_="rounded-m bg-pink-600 text-white text-[13px] font-bold px-5 py-2 rounded hover:bg-pink-500 hover:bg-pink-700",
                        )["href"]
                        + "?download=main"
                    )

                # Downloading the file with wget as it is fast and has its own progress bar.
                args = ["wget", "-O", name, url]
                subprocess.call(args)
                print("\nDownload Complete.")
                Tvsources().retry()
            except SessionNotCreatedException:
                print(
                    "\nIf you are not using android then install from win_linux_requirement.txt file"
                )
            except requests.exceptions.RequestException as e:
                print(e)
            except WebDriverException as e:
                print(e)
            except TypeError as e:
                pass
            except (IndexError, AttributeError, UnboundLocalError):
                print("\nCould not find any thing :(")
            except KeyboardInterrupt:
                print("\n\nCancelled by user.")

    ############################################################################
    ############################################################################
    class Asian_Dramas:
        def asian_dramas(self):
            label = "next_only"
            # Url to access the searching.
            url = f"https://dramasuki.pages.dev/#DramaSuki/"
            try:
                driver.get(url)
                while True:
                    # Sending request to the webpage.
                    driver.get(url)
                    # Getting html page with BeautifulSoup module
                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    # Finding all the mentioned elements from webpage.
                    html_tag = soup.find_all("a", class_="folder_link")
                    span = soup.find("span", class_="file mkv")
                    index_list = []
                    name_list = []
                    link_list = []
                    for i, links in enumerate(html_tag, start=1):
                        index_list.append(i)
                        name_list.append(links.get_text().strip())
                        link_list.append(links.get_text().strip())
                    print("\n")
                    for i, name in zip(index_list, name_list):
                        print(f"{i}. {name}")
                    data = Tvsources().user_choice(
                        name_list, link_list, index_list, label
                    )
                    name = data[1]
                    xpath_expr = f"//a[contains(normalize-space(text()), '{name}')]"
                    element = driver.find_element(By.XPATH, xpath_expr)
                    element.click()
                    time.sleep(2)
                    if span:
                        # Downloading the file with wget as it is fast and has its own progress bar.
                        soup = BeautifulSoup(driver.page_source, "html.parser")
                        # Finding all the mentioned elements from webpage.
                        html_tag = soup.find_all("a", string=lambda t: t and "mkv" in t)
                        index_list = []
                        name_list = []
                        link_list = []
                        for i, links in enumerate(html_tag, start=1):
                            index_list.append(i)
                            name_list.append(links.get_text().strip())
                            link_list.append(links["href"])
                        print("\n")
                        for i, name in zip(index_list, name_list):
                            print(f"{i}. {name}")
                        data = Tvsources().user_choice(name_list, link_list, index_list, label)
                        url = data[0]
                        name = data[1]
                        if "mkv" in name:
                            break
                args = ["wget", "-O", name, url]
                subprocess.call(args)
                print("\nDownload Complete.")
                Tvsources().retry()
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
