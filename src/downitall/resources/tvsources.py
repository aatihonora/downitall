"""TV Sources"""

# Importing necessary modules
import os
import re
import subprocess
import time

import requests
from bs4 import BeautifulSoup
from downitall.resources.globalfunctions import Globalfunctions
from selenium.common.exceptions import (
    NoSuchElementException,
    SessionNotCreatedException,
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver.common.by import By

driver = Globalfunctions().webdriver()[0]
bookcli = Globalfunctions().webdriver()[1]


class Tvsources:
    ############################################################################
    ############################################################################
    class Vadapav:
        def vadapav_search(self):
            Globalfunctions().directory(name="TV Movies")
            label = "no_page"
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
                    data = Globalfunctions().user_choice(
                        name_list, link_list, index_list, label
                    )
                    url = data[0]
                    name = data[1]
                    if "mkv" in url:
                        break
                # Downloading the file with wget as it is fast and has its own progress bar.
                args = ["wget", "-O", name, url]
                subprocess.call(args)
                print("\nDownload Complete.")
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
        def vadapav_batch(self):
            Globalfunctions().directory(name="TV Movies")
            label = "no_page"
            save = 0
            # Url to access the searching.
            url = "https://vadapav.mov/s/"
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
                    data = Globalfunctions().user_choice(
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
        def torrent_search(self, search_term, choice):
            Globalfunctions().directory(name="TV Movies")
            label = "paged"
            index = 1
            term = re.sub(r"\W", "+", search_term)
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
    ############################################################################
    class Documentary:
        def documentary(self):
            Globalfunctions().directory(name="TV Movies")
            label = "no_page"
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
                data = Globalfunctions().user_choice(
                    name_list, link_list, index_list, label
                )
                web_url = data[0]
                page_url = f"{web_url}/page/"
                while True:
                    label = "paged"
                    driver.get(web_url)
                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    if Globalfunctions().exists(element=".numeric-nav"):
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
                html_tag = soup.find("meta", attrs={"itemprop": "embedUrl"})
                if "https://www.dailymotion" in html_tag["content"].split(".com")[0]:
                    url = html_tag["content"].replace("/embed", "")
                else:
                    url = html_tag["content"]
                args = ["yt-dlp", url]
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
    class Vegamovies:
        def vegamovies(self, search_term):
            Globalfunctions().directory(name="TV Movies")
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
                    data = Globalfunctions().user_choice(
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
    class Asian_Dramas:
        def asian_dramas(self):
            Globalfunctions().directory(name="TV Movies")
            label = "no_page"
            # Url to access the searching.
            url = "https://dramasuki.pages.dev/#DramaSuki/"
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
                    data = Globalfunctions().user_choice(
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
                        data = Globalfunctions().user_choice(
                            name_list, link_list, index_list, label
                        )
                        url = data[0]
                        name = data[1]
                        if "mkv" in name:
                            break
                args = ["wget", "-O", name, url]
                subprocess.call(args)
                print("\nDownload Complete.")
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
