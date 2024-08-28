'''Manga Sources'''

#Importing necessary modules
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
options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options=options)
# Getting the current directory.
bookcli = os.getcwd()

class Mangasources:
    '''Manga functions'''
    def download_compress(self, manga_name, chapter_name, img_links_list):
        # Using regex to get the standard naming protocols for easy folder making.
        manga = re.sub('[^a-z,0-9]', '_', manga_name, flags=re.IGNORECASE)
        chapter = re.sub('[^a-z,0-9]', '_', chapter_name, flags=re.IGNORECASE)
        try:
            # Making new directory for manga and inside it a chapter directory and accessing them.
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
            # Enumerating the "img_links_list" to get each link with index.
            for i, img in enumerate(img_links_list):
                # Sending request to the image link.
                with requests.get(img, stream = True) as res:
                # Checking header to get the content length, in bytes.
                    total_length = int(res.headers.get("Content-Length"))
                    # Checking if request was valid.
                    if res.status_code == 200:
                        # Naming the image and storing it.
                        image = f'{chapter} Image {i}.jpg' 
                        # Implement progress bar via tqdm.
                        with tqdm.wrapattr(res.raw, "read", total=total_length, desc="")as raw:
                            # Downloading image via shutil.
                            with open(image,'wb') as f:
                                shutil.copyfileobj(raw, f)
                        print('Image sucessfully Downloaded: ',image)
                    else:
                        print('Image Couldn\'t be retrieved')
            # Accessing the manga folder to compress chapter folder into cbz file.
            os.chdir(path)
            # Compressing chapter folder into cbz file using cbz_generator module.
            cbz_generator.create_cbz_archive(chapter, path, f'{manga}_{chapter}')
            print("Download Complete")
        except OSError as e:
            print(e)

    def bato(self,search_term):
        # Url to access the searching.
        url = "https://bato.to/search?word=" + search_term
        # Url to access the base website.
        baseurl = "https://bato.to"
        try:
            # Sending request to the webpage.
            response = requests.get(url, timeout=2)
            # Getting html page with BeautifulSoup module.
            soup = BeautifulSoup(response.content, "html.parser")
            # Finding all the "a" elements from webpage.
            a_html = soup.find_all("a", class_="item-title", href=True)
            # Creating three lists for links, names and index, enumerating to get index and element in "a_html".
            # Finally appending the link href to "link_list", link text to "name_list" and i to "index_list".
            link_list = []
            name_list = []
            index_list = []
            for i, links in enumerate(a_html, start=1):
                link_list.append(baseurl + links["href"])
                name_list.append(links.text)
                index_list.append(i)
            # Creating two dictionary that take key as index and value as items from "link_list" and "name_list" respectively.
            url_dict = {index_list[i]: link_list[i] for i in range(len(link_list))}
            name_dict = {index_list[i]: name_list[i] for i in range(len(name_list))}
            # Making UI to get user input from name_list.
            for key, value in name_dict.items():
                print(f'{key}. {value}')
            try:
                # If statement in case no manga was found.
                if not link_list:
                    print(f'No book with title "{search_term}" found')
                else:
                    # Matching the user selection with "urls_dict" dictionary to get its value.
                    manga_selection = int(input("\nSelect the book index number: "))
                    if manga_selection in url_dict:
                        # Getting the manga name and link by matching the index number from dictionaries.
                        manga_link = f"{url_dict[manga_selection]}"
                        manga_name = f"{name_dict[manga_selection]}"
                        print("Fetching, please wait...")
                        # Starting the requests session.
                        session = requests.Session()
                        # Sending get request to the "manga_link" website.
                        manga_response = session.get(manga_link, timeout=2)
                        # Parsering the response with "BeauitifulSoup".
                        manga_soup = BeautifulSoup(manga_response.content, "html.parser")
                        # Finding all the "a" elements in the webpage.
                        a_html_chapter = manga_soup.find_all(
                            "a", class_="visited chapt", href=True
                        )     
                        # Creating three lists for links, names and index, enumerating to get index and element in "a_html".
                        # Finally appending the link href to "chapter_link_list", link text to "chapter_name_list" and i to "chapter_index_list". Srip was used to remove spaces.
                        chapter_name_list = []
                        chapter_link_list = []
                        chapter_index_list = []
                        for i, link in enumerate(a_html_chapter, start=1):
                            chapter_link_list.append(baseurl + link["href"].strip())
                            chapter_name_list.append(link.text.strip())
                            chapter_index_list.append(i)
                        chapter_link_list.reverse()
                        chapter_name_list.reverse()
                        # Creating two dictionary that take key as index and value as items from "chapter_link_list" and "chapter_name_list" respectively.
                        chapter_url_dict = {
                            chapter_index_list[i]: chapter_link_list[i]
                            for i in range(len(chapter_link_list))
                        }
                        chapter_name_dict = {
                            chapter_index_list[i]: chapter_name_list[i]
                            for i in range(len(chapter_name_list))
                        }
                        # Making UI to get user input from chapter_name_list.
                        for key, value in chapter_name_dict.items():
                            print(f'{key}. {value}')
                        # Calling bato_download method as function.
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
        # If statement in case no chapter was found.
            if not chapter_link_list:
                print("No chapter found")
            else:
                # Matching the user selection with "chapter_urls_dict" dictionary to get its value.
                chapter_selection = int(
                input("\n Select the book index number: ")
                )
                if chapter_selection in chapter_url_dict:
                    # Getting the chapter name and link by matching the index number from dictionaries.
                    chapter_link = f"{chapter_url_dict[chapter_selection]}"
                    chapter_name = f"{chapter_name_dict[chapter_selection]}"
                    print("Fetching, please wait...")
                    # Sending request with selenium webdriver.
                    driver.get(chapter_link)
                    # Making driver wait 10 second before it sends error for not finding the page.
                    driver.implicitly_wait(10)
                    # Parsering the response with "BeauitifulSoup".
                    chapter_soup = BeautifulSoup(
                        driver.page_source, "html.parser"
                    )
                    # Finding all the "img" elements from webpage.
                    imgs_html_chapter = chapter_soup.find_all(
                        "img", class_="page-img"
                    )
                    # Closing the selenium webdriver
                    driver. quit()
                    # Creating the list to store image url.
                    img_links_list = []
                    # Finding all the "img" elements from img_html_chapter.
                    for imgs in imgs_html_chapter:
                        img_links_list.append(imgs["src"])
                    # Calling download_compress method as function.
                    self.download_compress(manga_name, chapter_name, img_links_list)
                else:
                    raise ValueError
        except ValueError:
            print("Invalid integer. The number must be in the range.")
        except TimeoutException:
            print("Network Error!")
            sys.exit()

    def mangasee(self, search_term):
        # Url to access the searching.
        url = "https://mangasee123.com/search/?sort=s&desc=false&name=" + search_term   
        # Url to access the base website.
        baseurl = "https://mangasee123.com"
        try:
            # Sending request with selenium webdriver.
            driver.get(url)
            # Making driver wait 10 second before it sends error for not finding the page.
            driver.implicitly_wait(10)
            # Getting html page with BeautifulSoup module.
            soup = BeautifulSoup(driver.page_source, "html.parser")
            # Accessing "a" elements for the webpage.
            a_html_link = soup.find_all("a", class_="SeriesName ng-binding", href=True)
            # Creating three lists for links, names and index, enumerating to get index and "a" elements from "h3" element and 
            # appending the link href to "link_list", link text to "name_list" and i to "index_list".
            link_list = []
            name_list = []
            index_list = []
            for i, links in enumerate(a_html_link, start=1):
                link_list.append(baseurl + links["href"])
                name_list.append(links.text)
                index_list.append(i)
            # Creating two dictionary that take key as index and value as items from "link_list" and "name_list" respectively.
            url_dict = {index_list[i]: link_list[i] for i in range(len(link_list))}
            name_dict = {index_list[i]: name_list[i] for i in range(len(name_list))}
            # Making UI to get user input from name_list:
            for key, value in name_dict.items():
                print(f'{key}. {value}')
            try:
                # If statement in case no manga was found.
                if not link_list:
                    print(f'No book with title "{search_term}" found')
                else:
                    # Matching the user selection with "urls_dict" dictionary to get its value.
                    manga_selection = int(input("\nSelect the book index number: "))
                    if manga_selection in url_dict:
                        # Getting the manga name and link by matching the index number from dictionaries.
                        manga_link = f"{url_dict[manga_selection]}"
                        manga_name = f"{name_dict[manga_selection]}"
                        print("Fetching, please wait...")
                        # Sending request with selenium webdriver.
                        driver.get(manga_link)
                        # Making driver wait 10 second before it sends error for not finding the page.
                        driver.implicitly_wait(10)
                        # Parsering the response with "BeauitifulSoup".
                        manga_soup = BeautifulSoup(driver.page_source, "html.parser")
                        # Finding all the "a" elements in the webpage.
                        a_html_chapter = manga_soup.find_all(
                            "a", class_="list-group-item ChapterLink ng-scope", href=True
                        )
                        # Finding all the "span" elements in the webpage.
                        span_chapter = manga_soup.find_all(
                            "span", class_="ng-binding", attrs={"style": "font-weight:600"})
                        # Creating three lists for links, names and index, enumerating to get index, "a" elements and "span" element and 
                        # appending the chapter_link href to "chapter_link_list", chapter_name to "chapter_name_list" and i to "chapter_index_list".
                        chapter_name_list = []
                        chapter_link_list = []
                        chapter_index_list = []
                        for chapter_links in a_html_chapter:
                            chapter_link_list.append(re.sub('-page-1','',(baseurl + chapter_links["href"]))) 
                        for i, chapter_names in enumerate(span_chapter, start=1):
                            chapter_name_list.append(re.sub('\s+',' ',chapter_names.text))
                            chapter_index_list.append(i)
                        chapter_link_list.reverse()
                        chapter_name_list.reverse()
                        # Creating two dictionary that take key as index and value as items from "chapter_link_list" and "chapter_name_list" respectively.
                        chapter_url_dict = {
                            chapter_index_list[i]: chapter_link_list[i]
                            for i in range(len(chapter_link_list))
                        }
                        chapter_name_dict = {
                            chapter_index_list[i]: chapter_name_list[i]
                            for i in range(len(chapter_name_list))
                        }
                        # Making UI to get user input from chapter_name_list.
                        for key, value in chapter_name_dict.items():
                            print(f'{key}. {value}')
                        # Calling mangasee_download method as a function.
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
        # If statement in case no chapter was found.
            if not chapter_link_list:
                print("No chapter found")
            else:
                # Matching the user selection with "chapter_urls_dict" dictionary to get its value.
                chapter_selection = int(
                input("\n Select the book index number: ")
                )
                if chapter_selection in chapter_url_dict:
                    # Getting the chapter name and link by matching the index number from dictionaries.
                    chapter_link = f"{chapter_url_dict[chapter_selection]}"
                    chapter_name = f"{chapter_name_dict[chapter_selection]}"
                    print("Fetching, please wait...")
                    # Sending request with selenium webdriver.
                    driver.get(chapter_link)
                    # Making driver wait 10 second before it sends error for not finding the page.
                    driver.implicitly_wait(10)
                    # Parsering the response with "BeauitifulSoup".
                    chapter_soup = BeautifulSoup(
                        driver.page_source, "html.parser"
                    )
                    # Finding all the "img" elements from webpage.
                    imgs_html_chapter = chapter_soup.find_all(
                        "img", class_="img-fluid HasGap"
                    )
                    # Closing the selenium webdriver
                    driver. quit()
                    # Creating the list to store image url.
                    img_links_list = []
                    # Finding all the "img" elements from img_html_chapter.
                    for imgs in imgs_html_chapter:
                        img_links_list.append(imgs["src"])
                    # Calling download_compress method as function.
                    self.download_compress(manga_name, chapter_name, img_links_list)
                else:
                    raise ValueError
        except ValueError:
            print("Invalid integer. The number must be in the range.")
        except TimeoutException:
            print("Network Error!")
            sys.exit()
    
    def comicextra(self, search_term):
        # Basic url to access the searching.
        url = "https://comixextra.com/search?keyword=" + search_term   
        try:
            # Sending request with selenium webdriver.
            driver.get(url)
            # Making driver wait 10 second before it sends error for not finding the page.
            driver.implicitly_wait(10)
            # Getting html page with BeautifulSoup module.
            soup = BeautifulSoup(driver.page_source, "html.parser")
            # Accessing "h3" elements in the webpage.
            h3_html = soup.find_all("h3")
            # Creating three lists for links, names and index, enumerating to get index and "a" elements from "h3" element and 
            # appending the link href to "link_list", link text to "name_list" and i to "index_list".
            link_list = []
            name_list = []
            index_list = []
            for i, a_html_link in enumerate(h3_html, start=1):
                for links in a_html_link.find_all("a"):
                    link_list.append(links["href"])
                    name_list.append(links.text)
                    index_list.append(i)
            # Creating two dictionary that take key as index and value as items from "link_list" and "name_list" respectively.
            url_dict = {index_list[i]: link_list[i] for i in range(len(link_list))}
            name_dict = {index_list[i]: name_list[i] for i in range(len(name_list))}
            # Making UI to get user input from name_list:
            for key, value in name_dict.items():
                print(f'{key}. {value}')

            try:
                # If statement in case no manga was found.
                if not link_list:
                    print(f'No book with title "{search_term}" found')
                else:
                    # Matching the user selection with "urls_dict" dictionary to get its value.
                    manga_selection = int(input("\nSelect the book index number: "))
                    if manga_selection in url_dict:
                        # Getting the manga name and link by matching the index number from dictionaries.
                        manga_link = f"{url_dict[manga_selection]}"
                        manga_name = f"{name_dict[manga_selection]}"
                        print("Fetching, please wait...")
                        # Sending request with selenium webdriver.
                        driver.get(manga_link)
                        # Making driver wait 10 second before it sends error for not finding the page.
                        driver.implicitly_wait(10)
                        # Parsering the response with "BeauitifulSoup".
                        manga_soup = BeautifulSoup(driver.page_source, "html.parser")
                        # Getting table element from html page.
                        table_html_chapter = manga_soup.find_all(
                            "table", class_="table"
                        )
                        # Creating three lists for links, names and index, enumerating to get index and "a" elements from "h3" element and 
                        # appending the chapter_data href to "chapter_link_list", chapter_data text to "chapter_name_list" and i to "chapter_index_list".
                        chapter_name_list = []
                        chapter_link_list = []
                        chapter_index_list = []
                        # Finding all the "tr" element from the "table" element.
                        for tr_html_chapter in table_html_chapter:
                            # Finding the chapter_data from "a" tag through tr_html_chapter.
                            for i, chapter_data in enumerate(tr_html_chapter.find_all("a"), start=1):
                                chapter_link_list.append(chapter_data["href"] + "/full") 
                                chapter_name_list.append(re.sub('"','',chapter_data.text))
                                chapter_index_list.append(i)
                        # Creating two dictionary that take key as index and value as items from "chapter_link_list" and "chapter_name_list" respectively.
                        chapter_url_dict = {
                            chapter_index_list[i]: chapter_link_list[i]
                            for i in range(len(chapter_link_list))
                        }
                        chapter_name_dict = {
                            chapter_index_list[i]: chapter_name_list[i]
                            for i in range(len(chapter_name_list))
                        }
                        # Making UI to get user input from name_list.
                        for key, value in chapter_name_dict.items():
                            print(f'{key}. {value}')
                        # Calling comicextra_download method as function.
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
        # If statement in case no chapter was found.
            if not chapter_link_list:
                print("No chapter found")
            else:
                # Matching the user selection with "chapter_urls_dict" dictionary to get its value.
                chapter_selection = int(
                input("\n Select the book index number: ")
                )
                if chapter_selection in chapter_url_dict:
                    # Getting the chapter name and link by matching the index number from dictionaries.
                    chapter_link = f"{chapter_url_dict[chapter_selection]}"
                    chapter_name = f"{chapter_name_dict[chapter_selection]}"
                    print("Fetching, please wait...")
                    # Sending request with selenium webdriver.
                    driver.get(chapter_link)
                    # Making driver wait 10 second before it sends error for not finding the page.
                    driver.implicitly_wait(10)
                    # Parsering the response with "BeauitifulSoup".
                    chapter_soup = BeautifulSoup(
                        driver.page_source, "html.parser"
                    )
                    # Finding all the "div" element in the html page.
                    div_html_chapter = chapter_soup.find_all(
                        "div", class_="chapter-container"
                    )
                    # Closing the selenium webdriver
                    driver. quit()
                    # Creating the list to store image url.
                    img_links_list = []
                    # Finding all the "img" elements from div_html_chapter.
                    for imgs_html_chapter in div_html_chapter:
                        for imgs in imgs_html_chapter.find_all("img"):
                            img_links_list.append(imgs["src"])
                    # Calling download_compress method as function.
                    self.download_compress(manga_name, chapter_name, img_links_list)

                else:
                    raise ValueError
        except ValueError:
            print("Invalid integer. The number must be in the range.")
        except TimeoutException:
            print("Network Error!")
            sys.exit()
