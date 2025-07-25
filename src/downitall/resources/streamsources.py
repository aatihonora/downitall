"""Stream Sources"""

# Importing necessary modules
import os
import re
import subprocess
import sys
import time
import urllib.parse

import pandas as pd
import questionary
import requests
from bs4 import BeautifulSoup
from ipytv import playlist
from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    SessionNotCreatedException,
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from seleniumwire import webdriver  # <<< This replaces normal selenium.webdriver

# Global variables.
# Selenium Chrome options to lessen the memory usage.
options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--headless=new")
options.add_argument("start-maximized")
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


class Streamsources:
    """Stream functions"""

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
                # subprocess.call(["vlc", url, quality])
                subprocess.call(["mpv", "--really-quiet", "--fs", url])
                return True
            else:
                print("Dead link")
                return False
        except requests.exceptions.RequestException:
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
            search_term = input("Enter the title of the media you want to Stream: ")
            select = questionary.select(
                "Select item",
                choices=[
                    "Anizone",
                    "Miruro",
                    "Yoyomovies",
                    "Cxtvlive",
                    "IPTV",
                    "Exit",
                ],
            ).ask()
            if select == "Anizone":
                Streamsources().Anizone().anizone(search_term)
            elif select == "Miruro":
                Streamsources().Miruro().miruro(search_term)
            elif select == "Yoyomovies":
                Streamsources().Yoyomovies().yoyomovies(search_term)
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
            else:
                pass

    ############################################################################
    ############################################################################
    class Anizone:
        def anizone(self, search_term):
            # Declaring function level variables.
            label = "no_page"
            # Url to access webpage.
            url = f"https://anizone.to/anime?search={search_term}"
            try:
                # Sending request to the webpage.
                driver.get(url)
                # Getting html page with BeautifulSoup module
                time.sleep(5)
                soup = BeautifulSoup(driver.page_source, "html.parser")
                # Checking weather the element exists.
                # Finding all the mentioned elements from webpage.
                html_tag = soup.find_all(
                    "a",
                    class_="text-white inline hocus:text-amber-300 transition-colors duration-300 ease-in-out focus:outline-none focus:ring-0",
                )
                index_list = []
                name_list = []
                link_list = []
                # Finding the links and making link list.
                for i, links in enumerate(html_tag, start=1):
                    index_list.append(i)
                    link_list.append(links["href"])
                    name_list.append(links.get("title"))
                # Calling the user choice function.
                data = Streamsources().user_choice(
                    name_list, link_list, index_list, label
                )
                url = data[0]
                driver.get(url)
                time.sleep(3)
                soup = BeautifulSoup(driver.page_source, "html.parser")
                html_tag = soup.find_all(
                    "a",
                    class_="group block relative drop-shadow-lg overflow-hidden h-[101px] px-5 py-4 bg-slate-900 rounded-lg focus:outline-none",
                )
                html_tag_name = soup.find_all(
                    "h3",
                    class_="group-hocus:text-amber-300 transition-colors duration-300 ease-in-out",
                )
                index_list = []
                name_list = []
                link_list = []
                # Finding the links and making link list.
                for i, links in enumerate(html_tag, start=1):
                    index_list.append(i)
                    link_list.append(links["href"])
                for names in html_tag_name:
                    name_list.append(names.text.strip())
                # Calling the user choice function.
                data = Streamsources().user_choice(
                    name_list, link_list, index_list, label
                )
                url = data[0]
                driver.get(url)
                time.sleep(3)
                soup = BeautifulSoup(driver.page_source, "html.parser")
                html_tag = soup.find_all("source")[0]
                url = html_tag["src"]
                Streamsources().link_check(url)
                Streamsources().retry()
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
    class Miruro:
        def miruro(self, search_term):
            # Declaring function level variables.
            label = "next_only"
            index = 1
            # Url to access webpage.
            web_url = f"https://www.miruro.tv/search?query={search_term}&sort=POPULARITY_DESC&type=ANIME"
            base_url = "https://www.miruro.tv"
            try:
                # Sending request to the webpage.
                driver.get(web_url)
                print("Wait a few moments")
                time.sleep(6)
                while True:
                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    # Checking weather the element exists.
                    # Finding all the mentioned elements from webpage.
                    html_tag = soup.find_all(
                        "a", title=True, href=lambda t: t and "watch" in t
                    )
                    index_list = []
                    name_list = []
                    link_list = []
                    # Finding the links and making link list.
                    index_list.append(0)
                    name_list.append("Next Page")
                    link_list.append("")
                    for i, links in enumerate(html_tag, start=1):
                        index_list.append(i)
                        name_list.append(links["title"].strip())
                        link_list.append(base_url + links["href"])
                    # Calling the user choice function.
                    data = Streamsources().user_choice(
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
                time.sleep(10)
                soup = BeautifulSoup(driver.page_source, "html.parser")
                select_list = []
                select_name = []
                html_tag = soup.find_all("select")[0]
                tag = html_tag.find_all("option")
                for values in tag:
                    select_list.append(values["value"])
                    select_name.append(values.text.strip())
                for i, names in enumerate(select_name, start=1):
                    print(f"{i}. {names}")
                user_input = input("Select an index: ")
                select = Select(driver.find_element(By.TAG_NAME, "select"))
                select.select_by_value(f"{select_list[int(user_input)-1]}")
                time.sleep(5)
                soup = BeautifulSoup(driver.page_source, "html.parser")
                html_tag = soup.find_all("div", id="episodes-list-container")[0]
                html_tag_name = html_tag.find_all("button")
                index_list = []
                name_list = []
                link_list = []
                # Finding the links and making link list.
                label = "no_page"
                for i, names in enumerate(html_tag_name, start=1):
                    index_list.append(i)
                    name_list.append(names["title"].strip())
                    for links in names.find_all("a"):
                        link_list.append(base_url + links["href"])
                # Calling the user choice function.
                data = Streamsources().user_choice(
                    name_list, link_list, index_list, label
                )
                url = data[0]
                driver.get(url)
                time.sleep(5)
                soup = BeautifulSoup(driver.page_source, "html.parser")
                html_tag = soup.find_all("source")[0]
                proxy_url = html_tag["src"]
                # Parse the full URL
                parsed_url = urllib.parse.urlparse(proxy_url)

                # Extract the 'url' query parameter
                query_params = urllib.parse.parse_qs(parsed_url.query)
                encoded_m3u8_url = query_params.get("url", [None])[0]

                # Decode the percent-encoded string
                url = urllib.parse.unquote(encoded_m3u8_url)

                Streamsources().link_check(url)
                Streamsources().retry()
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
    class Hydrahd:
        def hydrahd(self, search_term):
            # Declaring function level variables.
            label = "next_only"
            index = 1
            # Url to access webpage.
            web_url = f"https://hydrahd.sh/index.php?menu=search&query={search_term}"
            base_url = "https://hydrahd.sh"
            page_url = f"https://hydrahd.sh/search/{search_term}/"
            try:
                # Sending request to the webpage.
                while True:
                    driver.get(web_url)
                    time.sleep(3)
                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    # Checking weather the element exists.
                    if Streamsources().exists(element="pagination"):
                        html_tag = soup.find("ul", class_="pagination")
                        # Finding the last td tag and getting its text which is the number of last page and converting it into integer.
                        pages = 6
                    else:
                        pages = 6
                    # Finding all the mentioned elements from webpage.
                    html_tag = soup.find_all("a", class_="hthis")
                    index_list = []
                    name_list = []
                    link_list = []
                    # Finding the links and making link list.
                    name_list.append("Next Page")
                    link_list.append(page_url)
                    index_list.append(0)
                    for i, links in enumerate(html_tag, start=1):
                        index_list.append(i)
                        link_list.append(base_url + links["href"])
                        name_list.append(links["title"].strip())
                    name_list.append("Previous Page")
                    link_list.append(page_url)
                    index_list.append(i + 1)
                    # Calling the user choice function.
                    data = Streamsources().user_choice(
                        name_list, link_list, index_list, label
                    )
                    url = data[0]
                    name = data[1]
                    index = Streamsources().page_navigation(name, pages, index)
                    web_url = url + str(index)
                    if name != "Next Page" and name != "Previous Page":
                        break
                if "watchseries" in url:
                    driver.get(url)
                    time.sleep(2)
                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    html_tag = soup.find_all(
                        "a", class_="dynamic-ep-link visitedep link episodeColorBlack"
                    )
                    index_list = []
                    name_list = []
                    link_list = []
                    # Finding the links and making link list.
                    for i, links in enumerate(html_tag, start=1):
                        index_list.append(i)
                        link_list.append(base_url + links["href"])
                        name_list.append(links["title"])
                    data = Streamsources().user_choice(
                        name_list, link_list, index_list, label
                    )
                    url = data[0]
                    name = data[1]
                driver.get(url)
                time.sleep(4)
                play_button = driver.find_element(By.CLASS_NAME, "video-play-button")
                driver.execute_script("arguments[0].click();", play_button)
                print("Wait a few moments")
                time.sleep(15)
                stream_urls = []
                for request in driver.requests:
                    if request.response:
                        url = request.url
                        if ".m3u8" in url or ".mp4" in url or ".ts" in url:
                            stream_urls.append(url)
                url = stream_urls[0]
                Streamsources().link_check(url)
                Streamsources().retry()
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
    class Cxtvlive:
        def cxtvlive(self):
            # Declaring function level variables.
            label = "next_only"
            index = 1
            # Url to access webpage.
            web_url = f"https://www.cxtvlive.com/tv/country/united-states"
            try:
                # Sending request to the webpage.
                driver.get(web_url)
                time.sleep(3)
                while True:
                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    # Checking weather the element exists.
                    # Finding all the mentioned elements from webpage.
                    html_tag = soup.find_all(
                        "a", class_="m-b-20 btn btn-white btn-block"
                    )
                    html_tag_name = soup.find_all(
                        "h4",
                        class_="resumoDots p-t-15 p-b-5 no-margin text-center bold",
                    )
                    index_list = []
                    name_list = []
                    link_list = []
                    # Finding the links and making link list.
                    index_list.append(0)
                    name_list.append("Next Page")
                    link_list.append("")
                    for i, links in enumerate(html_tag, start=1):
                        index_list.append(i)
                        link_list.append(links["href"])
                    for names in html_tag_name:
                        name_list.append(names.text.strip())
                    # Calling the user choice function.
                    data = Streamsources().user_choice(
                        name_list, link_list, index_list, label
                    )
                    url = data[0]
                    name = data[1]
                    if name == "Next Page":
                        driver.find_element(By.ID, "loadMore").click()
                        time.sleep(2)
                    else:
                        break
                driver.get(url)
                time.sleep(2)
                soup = BeautifulSoup(driver.page_source, "html.parser")
                html_tag = soup.find_all("iframe")[0]
                if not "youtube" in html_tag["src"]:
                    html_tag = soup.find_all("source")[0]
                    url = re.sub("&amp;+", "", html_tag["src"])
                elif not "list" in html_tag["src"] and "youtube" in html_tag["src"]:
                    url = html_tag["src"]
                else:
                    raise IndexError
                Streamsources().link_check(url)
                Streamsources().retry()
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
    class Iptv:
        def iptv(self, choice):
            # Declaring function level variables.
            label = "no_page"
            # Url to access webpage.
            if choice == 1:
                web_url = "https://iptv-org.github.io/iptv/languages/eng.m3u"
            else:
                web_url = "https://raw.githubusercontent.com/FunctionError/PiratesTv/main/combined_playlist.m3u"
            try:
                pl = playlist.loadu(web_url)
                # Let's retrieve the first channel in the list
                index_list = []
                name_list = []
                link_list = []
                for i, channel in enumerate(pl, start=1):
                    index_list.append(i)
                    if (
                        not "[Not 24/7]" in channel.name
                        and not "[Geo-blocked]" in channel.name
                    ):
                        name_list.append(channel.name.strip())
                    if "m3u8" in channel.url or "mpd" in channel.url:
                        link_list.append(channel.url)
                while True:
                    data = Streamsources().user_choice(
                        name_list, link_list, index_list, label
                    )
                    url = data[0]
                    if Streamsources().link_check(url) == True:
                        break
                Streamsources().retry()
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
            except TypeError:
                pass
            except (IndexError, AttributeError, UnboundLocalError):
                print("\nCould not find any thing :(")
            except KeyboardInterrupt:
                print("\n\nCancelled by user.")
