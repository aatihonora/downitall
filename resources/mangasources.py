'''Manga Sources'''

import os
import re
import shutil
import sys

import requests
from bs4 import BeautifulSoup
from cbz_generator import create_cbz_archive as cbz_generator
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from tqdm.auto import tqdm

# Global variables.
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
options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options=options)
bookcli = os.getcwd()

class Mangasources:
    '''Manga functions'''
    def download_compress(self, manga_name, chapter_name, img_links_list):
        manga = re.sub('[^a-z,0-9]', '_', manga_name, flags=re.IGNORECASE)
        chapter = re.sub('[^a-z,0-9]', '_', chapter_name, flags=re.IGNORECASE)
        try:
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
            for i, img in enumerate(img_links_list):
                with requests.get(img, stream = True) as res:
                # check header to get content length, in bytes
                    total_length = int(res.headers.get("Content-Length"))
                    if res.status_code == 200:
                        image = f'{chapter} Image {i}.jpg' 
                    # implement progress bar via tqdm
                        with tqdm.wrapattr(res.raw, "read", total=total_length, desc="")as raw:
                            with open(image,'wb') as f:
                                shutil.copyfileobj(raw, f)
                        print('Image sucessfully Downloaded: ',image)
                    else:
                        print('Image Couldn\'t be retrieved')
            os.chdir(path)
            cbz_generator.create_cbz_archive(chapter, path, f'{manga}_{chapter}')
            print("Download Complete")
        except OSError as e:
            print(e)


    def comicextra(self, search_term):
        url = "https://comixextra.com/search?keyword=" + search_term   
        try:
            driver.get(url)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            h3_html = soup.find_all("h3")
            link_list = []
            name_list = []
            for a_html_link in h3_html:
                for links in a_html_link.find_all("a"):
                    link_list.append(links["href"])
                    name_list.append(links.text)
            index_list = []
            for i in range(1, 100):
                index_list.append(i)

            url_dict = {index_list[i]: link_list[i] for i in range(len(link_list))}
            name_dict = {index_list[i]: name_list[i] for i in range(len(name_list))}

            index = 1
            for i in name_list:
                print(str(index) + ". " + str(i))
                index += 1

            try:
                # If statement in case no book was found.
                if not link_list:
                    print(f'No book with title "{search_term}" found')
                else:
                    # Matching the user selection with "urls_dict" dictionary to get its value.
                    manga_selection = int(input("\nSelect the book index number: "))
                    if manga_selection in url_dict:
                        # Getting the book name and link by matching the index number from dictionaries.
                        manga_link = f"{url_dict[manga_selection]}"
                        manga_name = f"{name_dict[manga_selection]}"
                        print("Fetching, please wait...")
                        # Starting the requests session.
                        driver.get(manga_link)
                        driver.implicitly_wait(10)
                        # Parsering the response with "BeauitifulSoup".
                        manga_soup = BeautifulSoup(driver.page_source, "html.parser")
                        # Finding the chapters link from "a" tag through a_html_chapter.
                        table_html_chapter = manga_soup.find_all(
                            "table", class_="table"
                        )
                        chapter_name_list = []
                        chapter_link_list = []
                        for tr_html_chapter in table_html_chapter:
                            for chapter_data in tr_html_chapter.find_all("a"):
                                chapter_link_list.append(chapter_data["href"] + "/full") 
                                chapter_name_list.append(re.sub('"','',chapter_data.text))
                        chapter_index_list = []
                        for i in range(1, 2000):
                            chapter_index_list.append(i)
                        chapter_url_dict = {
                            chapter_index_list[i]: chapter_link_list[i]
                            for i in range(len(chapter_link_list))
                        }
                        chapter_name_dict = {
                            chapter_index_list[i]: chapter_name_list[i]
                            for i in range(len(chapter_name_list))
                        }
                        index = 1
                        for i in chapter_name_list:
                            print(str(index) + ". " + str(i))
                            index += 1
                        self.comicextra_download(manga_name, chapter_url_dict, chapter_name_dict, chapter_link_list)
                    else:
                        raise ValueError
            except ValueError:
                print("Invalid integer. The number must be in the range.")
        except requests.exceptions.RequestException:
            print("Network Error!")
            sys.exit()
        except TimeoutException:
            print("Network Error!")
            sys.exit()

    def comicextra_download(self, manga_name, chapter_url_dict, chapter_name_dict, chapter_link_list):
        try:
        # If statement in case no book was found.
            if not chapter_link_list:
                print("No chapter found")
            else:
                # Matching the user selection with "urls_dict" dictionary to get its value.
                chapter_selection = int(
                input("\n Select the book index number: ")
                )
                if chapter_selection in chapter_url_dict:
                    # Getting the book name and link by matching the index number from dictionaries.
                    chapter_link = f"{chapter_url_dict[chapter_selection]}"
                    chapter_name = f"{chapter_name_dict[chapter_selection]}"
                    print("Fetching, please wait...")
                    # Sending get request to the "book_link" website.
                    driver.get(chapter_link)
                    driver.implicitly_wait(10)
                    # Parsering the response with "BeauitifulSoup".
                    chapter_soup = BeautifulSoup(
                        driver.page_source, "html.parser"
                    )
                    # Finding the chapters link from "a" tag through a_html_chapter.
                    div_html_chapter = chapter_soup.find_all(
                        "div", class_="chapter-container"
                    )
                    driver. quit()
                    img_links_list = []
                    for imgs_html_chapter in div_html_chapter:
                        for imgs in imgs_html_chapter.find_all("img"):
                            img_links_list.append(imgs["src"])
                    print(img_links_list)
                    self.download_compress(manga_name, chapter_name, img_links_list)

                else:
                    raise ValueError
        except ValueError:
            print("Invalid integer. The number must be in the range.")
        except TimeoutException:
            print("Network Error!")
            sys.exit()

    def bato(self,search_term):
        url = "https://bato.to/search?word=" + search_term
        baseurl = "https://bato.to"
        try:
            response = requests.get(url, timeout=2)
            isoup = BeautifulSoup(response.content, "html.parser")
            a_html = isoup.find_all("a", class_="item-title", href=True)

            link_list = []
            name_list = []
            for links in a_html:
                link_list.append(baseurl + links["href"])
                name_list.append(links.text)
            index_list = []
            for i in range(1, 100):
                index_list.append(i)

            url_dict = {index_list[i]: link_list[i] for i in range(len(link_list))}
            name_dict = {index_list[i]: name_list[i] for i in range(len(name_list))}

            index = 1
            for i in name_list:
                print(str(index) + ". " + str(i))
                index += 1

            try:
                # If statement in case no book was found.
                if not link_list:
                    print(f'No book with title "{search_term}" found')
                else:
                    # Matching the user selection with "urls_dict" dictionary to get its value.
                    manga_selection = int(input("\nSelect the book index number: "))
                    if manga_selection in url_dict:
                        # Getting the book name and link by matching the index number from dictionaries.
                        manga_link = f"{url_dict[manga_selection]}"
                        manga_name = f"{name_dict[manga_selection]}"
                        print("Fetching, please wait...")
                        # Starting the requests session.
                        session = requests.Session()
                        # Sending get request to the "book_link" website.
                        manga_response = session.get(manga_link, timeout=2)
                        # Parsering the response with "BeauitifulSoup".
                        manga_soup = BeautifulSoup(manga_response.content, "html.parser")
                        # Finding the chapters link from "a" tag through a_html_chapter.
                        a_html_chapter = manga_soup.find_all(
                            "a", class_="visited chapt", href=True
                        )
                        # Storing "chapters link" link in variable.
                        chapter_name_list = []
                        chapter_link_list = []
                        for chapter_data in a_html_chapter:
                            chapter_link_list.append(baseurl + chapter_data["href"].strip())
                            chapter_name_list.append(chapter_data.text.strip())
                        chapter_link_list.reverse()
                        chapter_name_list.reverse()
                        chapter_index_list = []
                        for i in range(1, 2000):
                            chapter_index_list.append(i)
                        chapter_url_dict = {
                            chapter_index_list[i]: chapter_link_list[i]
                            for i in range(len(chapter_link_list))
                        }
                        chapter_name_dict = {
                            chapter_index_list[i]: chapter_name_list[i]
                            for i in range(len(chapter_name_list))
                        }
                        index = 1
                        for i in chapter_name_list:
                            print(str(index) + ". " + str(i))
                            index += 1
                        self.bato_download(manga_name, chapter_url_dict, chapter_name_dict, chapter_link_list)
                    else:
                        raise ValueError
            except ValueError:
                print("Invalid integer. The number must be in the range.")
        except requests.exceptions.RequestException:
            print("Network Error!")
            sys.exit()
        except TimeoutException:
            print("Network Error!")
            sys.exit()

    def bato_download(self, manga_name, chapter_url_dict, chapter_name_dict, chapter_link_list):
        try:
        # If statement in case no book was found.
            if not chapter_link_list:
                print("No chapter found")
            else:
                # Matching the user selection with "urls_dict" dictionary to get its value.
                chapter_selection = int(
                input("\n Select the book index number: ")
                )
                if chapter_selection in chapter_url_dict:
                    # Getting the book name and link by matching the index number from dictionaries.
                    chapter_link = f"{chapter_url_dict[chapter_selection]}"
                    chapter_name = f"{chapter_name_dict[chapter_selection]}"
                    print("Fetching, please wait...")
                    # Sending get request to the "book_link" website.
                    driver.get(chapter_link)
                    driver.implicitly_wait(10)
                    # Parsering the response with "BeauitifulSoup".
                    chapter_soup = BeautifulSoup(
                        driver.page_source, "html.parser"
                    )
                    # Finding the chapters link from "a" tag through a_html_chapter.
                    imgs_html_chapter = chapter_soup.find_all(
                        "img", class_="page-img"
                    )
                    driver. quit()
                    img_links_list = []
                    for imgs in imgs_html_chapter:
                        img_links_list.append(imgs["src"])
                    self.download_compress(manga_name, chapter_name, img_links_list)
                else:
                    raise ValueError
        except ValueError:
            print("Invalid integer. The number must be in the range.")
        except TimeoutException:
            print("Network Error!")
            sys.exit()

    def mangasee(self, search_term):
        url = "https://mangasee123.com/search/?sort=s&desc=false&name=" + search_term   
        baseurl = "https://mangasee123.com"
        try:
            driver.get(url)
            driver.implicitly_wait(10)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            a_html_link = soup.find_all("a", class_="SeriesName ng-binding", href=True)
            link_list = []
            name_list = []
            for links in a_html_link:
                link_list.append(baseurl + links["href"])
                name_list.append(links.text)
            index_list = []
            for i in range(1, 100):
                index_list.append(i)

            url_dict = {index_list[i]: link_list[i] for i in range(len(link_list))}
            name_dict = {index_list[i]: name_list[i] for i in range(len(name_list))}

            index = 1
            for i in name_list:
                print(str(index) + ". " + str(i))
                index += 1

            try:
                # If statement in case no book was found.
                if not link_list:
                    print(f'No book with title "{search_term}" found')
                else:
                    # Matching the user selection with "urls_dict" dictionary to get its value.
                    manga_selection = int(input("\nSelect the book index number: "))
                    if manga_selection in url_dict:
                        # Getting the book name and link by matching the index number from dictionaries.
                        manga_link = f"{url_dict[manga_selection]}"
                        manga_name = f"{name_dict[manga_selection]}"
                        print("Fetching, please wait...")
                        # Starting the requests session.
                        driver.get(manga_link)
                        driver.implicitly_wait(10)
                        # Parsering the response with "BeauitifulSoup".
                        manga_soup = BeautifulSoup(driver.page_source, "html.parser")
                        # Finding the chapters link from "a" tag through a_html_chapter.
                        a_html_chapter = manga_soup.find_all(
                            "a", class_="list-group-item ChapterLink ng-scope", href=True
                        )
                        span_chapter = manga_soup.find_all(
                            "span", class_="ng-binding", attrs={"style": "font-weight:600"}
                        )
                        # Storing "chapters link" link in variable.
                        chapter_name_list = []
                        chapter_link_list = []
                        for chapter_links in a_html_chapter:
                            chapter_link_list.append(re.sub('-page-1','',(baseurl + chapter_links["href"]))) 
                        for chapter_names in span_chapter:
                            chapter_name_list.append(re.sub('\s+',' ',chapter_names.text))
                        chapter_link_list.reverse()
                        chapter_name_list.reverse()
                        chapter_index_list = []
                        for i in range(1, 2000):
                            chapter_index_list.append(i)
                        chapter_url_dict = {
                            chapter_index_list[i]: chapter_link_list[i]
                            for i in range(len(chapter_link_list))
                        }
                        chapter_name_dict = {
                            chapter_index_list[i]: chapter_name_list[i]
                            for i in range(len(chapter_name_list))
                        }
                        print(chapter_link_list)
                        index = 1
                        for i in chapter_name_list:
                            print(str(index) + ". " + str(i))
                            index += 1
                        self.mangasee_download(manga_name, chapter_url_dict, chapter_name_dict, chapter_link_list)
                    else:
                        raise ValueError
            except ValueError:
                print("Invalid integer. The number must be in the range.")
        except requests.exceptions.RequestException:
            print("Network Error!")
            sys.exit()
        except TimeoutException:
            print("Network Error!")
            sys.exit()

    def mangasee_download(self, manga_name, chapter_url_dict, chapter_name_dict, chapter_link_list):
        try:
        # If statement in case no book was found.
            if not chapter_link_list:
                print("No chapter found")
            else:
                # Matching the user selection with "urls_dict" dictionary to get its value.
                chapter_selection = int(
                input("\n Select the book index number: ")
                )
                if chapter_selection in chapter_url_dict:
                    # Getting the book name and link by matching the index number from dictionaries.
                    chapter_link = f"{chapter_url_dict[chapter_selection]}"
                    chapter_name = f"{chapter_name_dict[chapter_selection]}"
                    print("Fetching, please wait...")
                    # Sending get request to the "book_link" website.
                    driver.get(chapter_link)
                    driver.implicitly_wait(10)
                    # Parsering the response with "BeauitifulSoup".
                    chapter_soup = BeautifulSoup(
                        driver.page_source, "html.parser"
                    )
                    # Finding the chapters link from "a" tag through a_html_chapter.
                    imgs_html_chapter = chapter_soup.find_all(
                        "img", class_="img-fluid HasGap"
                    )
                    driver. quit()
                    img_links_list = []
                    for imgs in imgs_html_chapter:
                        img_links_list.append(imgs["src"])
                    self.download_compress(manga_name, chapter_name, img_links_list)
                else:
                    raise ValueError
        except ValueError:
            print("Invalid integer. The number must be in the range.")
        except TimeoutException:
            print("Network Error!")
            sys.exit()
