"""Manga Sources"""

# Importing necessary modules
import os
import re
import shutil
import subprocess
import sys
import time

import pandas as pd
import questionary
import requests
from bs4 import BeautifulSoup
from cbz_generator import create_cbz_archive as cbz_generator
from selenium import webdriver
from selenium.common.exceptions import (NoSuchElementException,
                                        SessionNotCreatedException,
                                        TimeoutException, WebDriverException)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from term_image.image import from_url
from tqdm.auto import tqdm

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


############################################################################
############################################################################
class Mangasources:
    """Manga functions"""

    ############################################################################
    def directory(self):
        if not os.path.isdir("Manga"):
            os.mkdir("Manga")
            os.chdir("Manga")
        else:
            os.chdir("Manga")

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
            data = Mangasources().download_directory(manga_name, chapter_name)
            path = data[0]
            manga = data[1]
            chapter = data[2]
            Mangasources().download(img_links_list, manga, chapter, path)
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
            data = Mangasources().download_directory(name, chapter_name)
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
                Mangasources().download(img_links_list, manga, chapter, path)
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
    # Defining the function for retrying the user_choice function.
    def retry(self):
        # Using match case argument to see which class called the function.
        answer = questionary.select(
            "Do you want to download another file? ", choices=["Yes", "No"]
        ).ask()
        if answer == "Yes":
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
                elif select == "Batch Download":
                    Mangasources().Weebcentral().weebcentral_batch(search_term)
                else:
                    pass
            elif select == "Nyaa":
                Mangasources().Nyaa().nyaa_search(search_term)
            elif select == "Rawotaku":
                Mangasources().Rawotaku().rawotaku(search_term)
            elif select == "Readallcomics":
                Mangasources().Readallcomics().readallcomics(search_term)
            else:
                pass

    ############################################################################
    ############################################################################
    class Bato:
        def bato_search(self, search_term):
            Mangasources().directory()
            # Declaring function level variables.
            source = "bato"
            label = "paged"
            index = 1
            # Making search term better for url through regex.
            term = re.sub("\W", "+", search_term)
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
                    if Mangasources().exists(element=".pagination.pagination-sm.mb-0"):
                        html_tag = soup.find(
                            "ul", class_="pagination pagination-sm mb-0"
                        )
                        # Finding the last td tag and getting its text which is the number of last page and converting it into integer.
                        pages = int(
                            re.sub("\W+", "", html_tag.find_all("li")[-2].getText())
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
                        data = Mangasources().user_choice(
                            name_list, link_list, index_list, label
                        )
                        url = data[0]
                        name = data[1]
                        selection = data[2]
                        if name != "Next Page" and name != "Previous Page":
                            answer = Mangasources().confirmation(
                                selection, index_list, img_list
                            )
                            if answer == True:
                                break
                            else:
                                pass
                        else:
                            break
                    index = Mangasources().page_navigation(name, pages, index)
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
                data = Mangasources().user_choice(
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
                Mangasources().download_compress(name, chapter_name, img_links_list)
                Mangasources().retry()
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
            Mangasources().directory()
            # Declaring function level variables.
            source = "mangasee"
            label = "next_only"
            # Making search term better for url through regex.
            term = re.sub("\W", "+", search_term)
            # Url to access webpage.
            web_url = f"https://weebcentral.com/search?text={term}&sort=Best+Match&order=Descending&official=Any&anime=Any&adult=Any&display_mode=Full+Display"
            # Url to access the base website
            base_url = "https://mangasee123.com"
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
                    data = Mangasources().user_choice(
                        name_list, link_list, index_list, label
                    )
                    url = data[0]
                    name = data[1]
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
                    print("no")
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
                data = Mangasources().user_choice(
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
                Mangasources().download_compress(name, chapter_name, img_links_list)
                Mangasources().retry()
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
            Mangasources().directory()
            # Declaring function level variables.
            source = "mangasee"
            label = "next_only"
            # Making search term better for url through regex.
            term = re.sub("\W", "+", search_term)
            # Url to access webpage.
            web_url = f"https://weebcentral.com/search?text={term}&sort=Best+Match&order=Descending&official=Any&anime=Any&adult=Any&display_mode=Full+Display"
            # Url to access the base website
            base_url = "https://mangasee123.com"
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
                    print("\n")
                    for i, name in zip(index_list, name_list):
                        print(f"{i}. {name}")
                    # Calling the user choice function.
                    data = Mangasources().user_choice(
                        name_list, link_list, index_list, label
                    )
                    url = data[0]
                    name = data[1]
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
                    print("no")
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
                Mangasources().batch_download(name_list, link_list, name)
                Mangasources().retry()
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
            Mangasources().directory()
            label = "paged"
            index = 1
            term = re.sub("\W", "+", search_term)
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
                    if Mangasources().exists(element=".pagination"):
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
                    df = Mangasources().visual_tables(table)
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
                    data = Mangasources().user_choice(
                        name_list, link_list, index_list, label
                    )
                    url = data[0]
                    name = data[1]
                    index = Mangasources().page_navigation(name, pages, index)
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
                Mangasources().retry()
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
            Mangasources().directory()
            # Declaring function level variables.
            label = "no_page"
            index = 1
            # Making search term better for url through regex.
            term = re.sub("\W", "+", search_term)
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
                    data = Mangasources().user_choice(
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
                data = Mangasources().user_choice(
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
                Mangasources().download_compress(name, chapter_name, img_links_list)
                Mangasources().retry()
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
            Mangasources().directory()
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
                    data = Mangasources().user_choice(
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
                data = Mangasources().user_choice(
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
                Mangasources().download_compress(name, chapter_name, img_links_list)
                Mangasources().retry()
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
