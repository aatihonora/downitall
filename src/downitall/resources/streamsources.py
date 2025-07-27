"""Stream Sources"""

# Importing necessary modules
import re
import time
import urllib.parse

import requests
from bs4 import BeautifulSoup
from ipytv import playlist
from selenium.common.exceptions import (
    SessionNotCreatedException,
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from downitall.resources.globalfunctions import Globalfunctions, Stream

driver = Globalfunctions().webdriver()[0]
bookcli = Globalfunctions().webdriver()[1]


class Streamsources:
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
                print("\n")
                for index_name, name in zip(index_list, name_list):
                    # Printing name with index for user to choose.
                    print(f"{index_name}. {name}")
                # Calling the user choice function.
                data = Globalfunctions().user_choice(
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
                print("\n")
                for index_name, name in zip(index_list, name_list):
                    # Printing name with index for user to choose.
                    print(f"{index_name}. {name}")
                data = Globalfunctions().user_choice(
                    name_list, link_list, index_list, label
                )
                url = data[0]
                driver.get(url)
                time.sleep(3)
                soup = BeautifulSoup(driver.page_source, "html.parser")
                html_tag = soup.find_all("source")[0]
                url = html_tag["src"]
                Stream().link_check(url)
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
    class Miruro:
        def miruro(self, search_term):
            # Declaring function level variables.
            label = "next_only"
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
                print("\n")
                for index_name, name in zip(index_list, name_list):
                    # Printing name with index for user to choose.
                    print(f"{index_name}. {name}")
                data = Globalfunctions().user_choice(
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

                Stream().link_check(url)
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
    class Hydrahd:
        def hydrahd(self, search_term):
            # Declaring function level variables.
            label = "paged"
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
                    if Globalfunctions().exists(element="pagination"):
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
                    index = Globalfunctions().page_navigation(name, pages, index)
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
                    print("\n")
                    for index_name, name in zip(index_list, name_list):
                        # Printing name with index for user to choose.
                        print(f"{index_name}. {name}")
                    data = Globalfunctions().user_choice(
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
                Stream().link_check(url)
                Globalfunctions().retry()
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
            label = "no_page"
            # Url to access webpage.
            web_url = "https://www.cxtvlive.com/tv/top"
            try:
                # Sending request to the webpage.
                driver.get(web_url)
                time.sleep(5)
                while True:
                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    # Checking weather the element exists.
                    # Finding all the mentioned elements from webpage.
                    html_tag = soup.find_all(
                        "a", class_="m-b-20 btn btn-white btn-block"
                    )
                    html_tag_name = soup.find_all(
                        "h4",
                        class_="resumo p-t-15 p-b-5 no-margin text-center bold",
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
                Stream().link_check(url)
                Globalfunctions().retry()
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
                    print("\n")
                    for index_name, name in zip(index_list, name_list):
                        # Printing name with index for user to choose.
                        print(f"{index_name}. {name}")
                    data = Globalfunctions().user_choice(
                        name_list, link_list, index_list, label
                    )
                    url = data[0]
                    if Stream().link_check(url) == True:
                        break
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
            except TypeError:
                pass
            except (IndexError, AttributeError, UnboundLocalError):
                print("\nCould not find any thing :(")
            except KeyboardInterrupt:
                print("\n\nCancelled by user.")
