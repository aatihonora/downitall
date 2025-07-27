"""Manga Sources"""

# Importing necessary modules
import os
import re
import subprocess
import time

import requests
from bs4 import BeautifulSoup
from downitall.resources.globalfunctions import Globalfunctions, Manga
from selenium.common.exceptions import (
    NoSuchElementException,
    SessionNotCreatedException,
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver.common.by import By

driver = Globalfunctions().webdriver()[0]
bookcli = Globalfunctions().webdriver()[1]


class Mangasources:
    ############################################################################
    ############################################################################
    class Bato:
        def bato_search(self, search_term):
            Globalfunctions().directory(name="Manga")
            # Declaring function level variables.
            label = "paged"
            index = 1
            # Making search term better for url through regex.
            term = re.sub(r"\W", "+", search_term)
            # Url to access webpage.
            web_url = f"https://bato.to/search?word={term}"
            # Url to be used for page navigation.
            page_url = f"https://bato.to/search?word={term}&page="
            # Url to access the base website
            base_url = "https://bato.to"
            try:
                while True:
                    # Sending request to the webpage.
                    driver.get(web_url)
                    # Getting html page with BeautifulSoup module
                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    # Checking weather the element exists.
                    if Globalfunctions().exists(
                        element=".pagination.pagination-sm.mb-0"
                    ):
                        html_tag = soup.find(
                            "ul", class_="pagination pagination-sm mb-0"
                        )
                        # Finding the last td tag and getting its text which is the number of last page and converting it into integer.
                        pages = int(
                            re.sub(r"\W+", "", html_tag.find_all("li")[-2].getText())
                        )
                    else:
                        pass
                    # Finding all the mentioned elements from webpage.
                    html_tag = soup.find_all("a", class_="item-title", href=True)
                    index_list = []
                    name_list = []
                    link_list = []
                    img_list = []
                    # Finding the links and making link list.
                    name_list.append("Next Page")
                    link_list.append(page_url)
                    index_list.append(0)
                    for i, links in enumerate(html_tag, start=1):
                        index_list.append(i)
                        name_list.append(links.text.strip())
                        link_list.append(base_url + links["href"])
                    name_list.append("Previous Page")
                    link_list.append(page_url)
                    index_list.append(i + 1)
                    html_tag = soup.find_all("img", class_="rounded")
                    for img in html_tag:
                        img_list.append(img["src"])
                    while True:
                        print("\n")
                        for i, name in zip(index_list, name_list):
                            print(f"{i}. {name}")
                        # Calling the user choice function.
                        data = Globalfunctions().user_choice(
                            name_list, link_list, index_list, label
                        )
                        url = data[0]
                        name = data[1]
                        selection = data[2]
                        if name != "Next Page" and name != "Previous Page":
                            answer = Globalfunctions().confirmation(
                                selection, index_list, img_list
                            )
                            if answer == True:
                                break
                            else:
                                pass
                        else:
                            break
                    index = Globalfunctions().page_navigation(name, pages, index)
                    web_url = url + str(index)
                    if name != "Next Page" and name != "Previous Page":
                        break
                # Sending request to the webpage.
                label = "no_page"
                driver.get(url)
                # Parsering the response with "BeauitifulSoup".
                soup = BeautifulSoup(driver.page_source, "html.parser")
                # Finding all the mentioned elements in the webpage.
                html_tag = soup.find_all("a", class_="visited chapt", href=True)
                index_list = []
                name_list = []
                link_list = []
                # Finding the links and making link list.
                for i, links in enumerate(html_tag, start=1):
                    index_list.append(i)
                    name_list.append(links.text.strip())
                    link_list.append(base_url + links["href"])
                name_list.reverse()
                link_list.reverse()
                print("\n")
                for i, namess in zip(index_list, name_list):
                    print(f"{i}. {namess}")
                # Using core method as function to get rid of repeating the same lines.
                data = Globalfunctions().user_choice(
                    name_list, link_list, index_list, label
                )
                url = data[0]
                chapter_name = data[1]
                # Sending request with selenium webdriver.
                driver.get(url)
                # Parsering the response with "BeauitifulSoup".
                soup = BeautifulSoup(driver.page_source, "html.parser")
                # Finding all the mentioned elements from webpage.
                html_tag = soup.find_all("img", class_="page-img")
                # Creating the list to store image url.
                img_links_list = []
                # Finding all the mentioned elements from img_html_chapter.
                for imgs in html_tag:
                    img_links_list.append(imgs["src"])
                # Calling download_compress method as function.
                Manga().download_compress(name, chapter_name, img_links_list)
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
    class Weebcentral:
        def weebcentral(self, search_term):
            Globalfunctions().directory(name="Manga")
            # Declaring function level variables.
            label = "next_only"
            # Making search term better for url through regex.
            term = re.sub(r"\W", "+", search_term)
            # Url to access webpage.
            web_url = f"https://weebcentral.com/search?text={term}&sort=Best+Match&order=Descending&official=Any&anime=Any&adult=Any&display_mode=Full+Display"
            # Url to access the base website
            try:
                # Sending request to the webpage.
                driver.get(web_url)
                time.sleep(2)
                while True:
                    # Getting html page with BeautifulSoup module
                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    # Finding all the mentioned elements from webpage.
                    html_tag = soup.find_all("a", class_="line-clamp-1 link link-hover")
                    index_list = []
                    name_list = []
                    link_list = []
                    img_list = []
                    # Finding the links and making link list.
                    name_list.append("Next Page")
                    link_list.append("")
                    index_list.append(0)
                    for i, links in enumerate(html_tag, start=1):
                        index_list.append(i)
                        name_list.append(links.text.strip())
                        link_list.append(links["href"])
                    html_tag = soup.find_all(
                        "img", {"width": "400", "height": "600", "decoding": "async"}
                    )
                    for img in html_tag:
                        img_list.append(img["src"])
                    print("\n")
                    for i, name in zip(index_list, name_list):
                        print(f"{i}. {name}")
                    # Calling the user choice function.
                    data = Globalfunctions().user_choice(
                        name_list, link_list, index_list, label
                    )
                    url = data[0]
                    name = data[1]
                    if name == "Next Page":
                        try:
                            driver.find_element(
                                By.XPATH,
                                '//button[contains(@class, "btn") and contains(@class, "bg-base-300")]',
                            ).click()
                            time.sleep(3)
                        except NoSuchElementException:
                            pass
                    else:
                        break
                # Sending request to the webpage.
                label = "no_page"
                driver.get(url)
                time.sleep(5)
                try:
                    driver.find_element(
                        By.XPATH,
                        "//button[@class='hover:bg-base-300 p-2' and @hx-target='#chapter-list']",
                    ).click()
                except NoSuchElementException:
                    pass
                time.sleep(2)
                # Parsering the response with "BeauitifulSoup".
                soup = BeautifulSoup(driver.page_source, "html.parser")
                # Finding all the mentioned elements in the webpage.
                html_tag = soup.find_all(
                    "a",
                    class_="hover:bg-base-300 flex-1 flex items-center p-2",
                    href=True,
                )
                html_tag_name = soup.find_all(
                    lambda tag: tag.name == "span"
                    and tag.has_attr("class")
                    and tag["class"] == []
                )
                index_list = []
                name_list = []
                link_list = []
                # Finding the links and making link list.
                for i, links in enumerate(html_tag, start=1):
                    index_list.append(i)
                    link_list.append(links["href"])
                for names in html_tag_name:
                    name_list.append(names.text)
                name_list.reverse()
                link_list.reverse()
                print("\n")
                for i, names in zip(index_list, name_list):
                    print(f"{i}. {names}")
                # Using core method as function to get rid of repeating the same lines.
                data = Globalfunctions().user_choice(
                    name_list, link_list, index_list, label
                )
                url = data[0]
                chapter_name = data[1]
                # Sending request with selenium webdriver.
                driver.get(url)
                time.sleep(5)
                # Parsering the response with "BeauitifulSoup".
                soup = BeautifulSoup(driver.page_source, "html.parser")
                # Finding all the mentioned elements from webpage.
                html_tag = soup.find_all("img", class_="maw-w-full mx-auto")
                # Creating the list to store image url.
                img_links_list = []
                # Finding all the mentioned elements from img_html_chapter.
                for imgs in html_tag:
                    img_links_list.append(imgs["src"])
                # Calling download_compress method as function.
                Manga().download_compress(name, chapter_name, img_links_list)
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
        def weebcentral_batch(self, search_term):
            Globalfunctions().directory(name="Manga")
            # Declaring function level variables.
            label = "next_only"
            # Making search term better for url through regex.
            term = re.sub(r"\W", "+", search_term)
            # Url to access webpage.
            web_url = f"https://weebcentral.com/search?text={term}&sort=Best+Match&order=Descending&official=Any&anime=Any&adult=Any&display_mode=Full+Display"
            # Url to access the base website
            try:
                # Sending request to the webpage.
                driver.get(web_url)
                time.sleep(2)
                while True:
                    # Getting html page with BeautifulSoup module
                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    # Finding all the mentioned elements from webpage.
                    html_tag = soup.find_all("a", class_="line-clamp-1 link link-hover")
                    index_list = []
                    name_list = []
                    link_list = []
                    # Finding the links and making link list.
                    name_list.append("Next Page")
                    link_list.append("")
                    index_list.append(0)
                    for i, links in enumerate(html_tag, start=1):
                        index_list.append(i)
                        name_list.append(links.text.strip())
                        link_list.append(links["href"])
                    print("\n")
                    for i, name in zip(index_list, name_list):
                        print(f"{i}. {name}")
                    # Calling the user choice function.
                    data = Globalfunctions().user_choice(
                        name_list, link_list, index_list, label
                    )
                    url = data[0]
                    name = data[1]
                    if name == "Next Page":
                        try:
                            driver.find_element(
                                By.XPATH,
                                '//button[contains(@class, "btn") and contains(@class, "bg-base-300")]',
                            ).click()
                            time.sleep(3)
                        except NoSuchElementException:
                            pass
                    else:
                        break
                # Sending request to the webpage.
                label = "no_page"
                driver.get(url)
                time.sleep(5)
                try:
                    driver.find_element(
                        By.XPATH,
                        "//button[@class='hover:bg-base-300 p-2' and @hx-target='#chapter-list']",
                    ).click()
                except NoSuchElementException:
                    pass
                time.sleep(2)
                # Parsering the response with "BeauitifulSoup".
                soup = BeautifulSoup(driver.page_source, "html.parser")
                # Finding all the mentioned elements in the webpage.
                html_tag = soup.find_all(
                    "a",
                    class_="hover:bg-base-300 flex-1 flex items-center p-2",
                    href=True,
                )
                html_tag_name = soup.find_all(
                    lambda tag: tag.name == "span"
                    and tag.has_attr("class")
                    and tag["class"] == []
                )
                name_list = []
                link_list = []
                # Finding the links and making link list.
                for links in html_tag:
                    link_list.append(links["href"])
                for names in html_tag_name:
                    name_list.append(names.text)
                name_list.reverse()
                link_list.reverse()
                Manga.batch_download(name_list, link_list, name)
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
    class Nyaa:
        def nyaa_search(self, search_term):
            Globalfunctions().directory(name="Manga")
            label = "paged"
            index = 1
            term = re.sub(r"\W", "+", search_term)
            # Url to access the searching.
            web_url = f"https://nyaa.si/?q={term}&f=0&c=3_1&s=seeders&o=desc"
            page_url = f"https://nyaa.si/?q={term}&f=0&c=3_1&s=seeders&o=desc&p="
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
    class Rawotaku:
        def rawotaku(self, search_term):
            Globalfunctions().directory(name="Manga")
            # Declaring function level variables.
            label = "no_page"
            # Making search term better for url through regex.
            term = re.sub(r"\W", "+", search_term)
            # Url to access webpage.
            web_url = f"https://rawotaku.com/?q={term}"
            # Url to be used for page navigation.
            try:
                while True:
                    # Sending request to the webpage.
                    driver.get(web_url)
                    time.sleep(5)
                    # Getting html page with BeautifulSoup module
                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    # Checking weather the element exists.
                    index_list = []
                    name_list = []
                    link_list = []
                    # Finding the links and making link list.
                    html_tag = soup.find_all("a", class_="manga-poster")
                    html_tag_name = soup.find_all(
                        "img", class_="manga-poster-img lazyloaded"
                    )
                    for i, links in enumerate(html_tag, start=1):
                        index_list.append(i)
                        link_list.append(links["href"])
                    for names in html_tag_name:
                        name_list.append(names["alt"].strip())
                    # Calling the user choice function.
                    print("\n")
                    for i, name in zip(index_list, name_list):
                        print(f"{i}. {name}")
                    data = Globalfunctions().user_choice(
                        name_list, link_list, index_list, label
                    )
                    url = data[0]
                    name = data[1]
                    break
                driver.get(url)
                time.sleep(5)
                # Getting html page with BeautifulSoup module
                soup = BeautifulSoup(driver.page_source, "html.parser")
                # Checking weather the element exists.
                index_list = []
                name_list = []
                link_list = []
                # Finding the links and making link list.
                html_tag = soup.find_all("a", class_="item-link")
                for i, links in enumerate(html_tag, start=1):
                    index_list.append(i)
                    link_list.append(links["href"])
                    name_list.append(links["title"].strip())
                link_list.reverse()
                name_list.reverse()
                # Calling the user choice function.
                print("\n")
                for i, namess in zip(index_list, name_list):
                    print(f"{i}. {namess}")
                data = Globalfunctions().user_choice(
                    name_list, link_list, index_list, label
                )
                url = data[0]
                chapter_name = data[1]
                driver.get(url)
                last_height = driver.execute_script("return document.body.scrollHeight")
                current_position = 0

                while current_position < last_height:
                    current_position += 300
                    driver.execute_script(f"window.scrollTo(0, {current_position});")
                    time.sleep(0.2)
                    last_height = driver.execute_script(
                        "return document.body.scrollHeight"
                    )

                # Parsering the response with "BeauitifulSoup".
                soup = BeautifulSoup(driver.page_source, "html.parser")
                # Finding all the mentioned elements from webpage.
                html_tag = soup.find_all("img", class_="image-vertical lazyloaded")
                # Creating the list to store image url.
                img_links_list = []
                # Finding all the mentioned elements from img_html_chapter.
                for imgs in html_tag:
                    img_links_list.append(imgs["data-src"])
                # Calling download_compress method as function.
                Manga().download_compress(name, chapter_name, img_links_list)
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
    class Readallcomics:
        def readallcomics(self, search_term):
            Globalfunctions().directory(name="Manga")
            # Declaring function level variables.
            label = "no_page"
            # Url to access webpage.
            web_url = f"https://readallcomics.com/?story={search_term}&s=&type=comic"
            try:
                # Sending request to the webpage.
                driver.get(web_url)
                while True:
                    time.sleep(5)
                    # Getting html page with BeautifulSoup module
                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    # Finding all the mentioned elements from webpage.
                    html_tag = soup.find_all("a", href=True, title=True)
                    index_list = []
                    name_list = []
                    link_list = []
                    # Finding the links and making link list.
                    for i, links in enumerate(html_tag, start=1):
                        index_list.append(i)
                        name_list.append(links["title"])
                        link_list.append(links["href"])
                    print("\n")
                    for i, name in zip(index_list, name_list):
                        print(f"{i}. {name}")
                    # Calling the user choice function.
                    data = Globalfunctions().user_choice(
                        name_list, link_list, index_list, label
                    )
                    url = data[0]
                    name = data[1]
                    break
                # Sending request to the webpage.
                driver.get(url)
                soup = BeautifulSoup(driver.page_source, "html.parser")
                # Finding all the mentioned elements from webpage.
                html_tag = soup.find_all("a", href=True, title=True)
                index_list = []
                name_list = []
                link_list = []
                # Finding the links and making link list.
                for i, links in enumerate(html_tag, start=1):
                    index_list.append(i)
                    name_list.append(links["title"])
                    link_list.append(links["href"])
                link_list.reverse()
                name_list.reverse()
                print("\n")
                for i, namess in zip(index_list, name_list):
                    print(f"{i}. {namess}")
                # Calling the user choice function.
                data = Globalfunctions().user_choice(
                    name_list, link_list, index_list, label
                )
                url = data[0]
                chapter_name = data[1]
                driver.get(url)
                print("Waiting for pages to load...")
                last_height = driver.execute_script("return document.body.scrollHeight")
                for y in range(0, last_height, 300):
                    driver.execute_script(f"window.scrollTo(0, {y});")
                    time.sleep(0.2)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                soup = BeautifulSoup(driver.page_source, "html.parser")
                html_tag = soup.find_all(
                    "img", class_="bgimglazy-load", attrs={"decoding": "async"}
                )
                # Creating the list to store image url.
                img_links_list = []
                # Finding all the mentioned elements from img_html_chapter.
                for imgs in html_tag:
                    img_links_list.append(imgs["src"])
                # Calling download_compress method as function.
                Manga().download_compress(name, chapter_name, img_links_list)
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
