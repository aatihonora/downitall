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
from selenium.common.exceptions import (NoSuchElementException,
                                        SessionNotCreatedException,
                                        TimeoutException)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
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

    def exists(self, element):
        try:
            driver.find_element(By.CSS_SELECTOR,element)
        except NoSuchElementException:
            return False
        return True

    def core(self, html_tag, baseurl, source):
        # Creating three lists "link_list", "name_list" and "index_list".
        link_list = []
        name_list = []
        index_list = []
        # Enumerating links from html_tag taken from sources with i for index.
        for i, links in enumerate(html_tag, start=1):
            # Adding exceptional cases for each sources.
            if source == "mangasee":
                link_list.append(re.sub('-page-1','',(baseurl + links["href"])))
                for span_tag in links.find_all("span", class_="ng-binding", attrs={"style": "font-weight:600"}):
                    for name in span_tag:
                        name_list.append(re.sub('\s+',' ',name.text.strip()))
                index_list.append(i)
            elif source == "comicextra":
                for i, a_html_link in enumerate(html_tag, start=1):
                    for links in a_html_link.find_all("a"):
                        link_list.append(baseurl + links["href"])
                        name_list.append(links.text.strip())
                        index_list.append(i)
            elif source == "comicextra_chapter":
                for tr_html_chapter in html_tag:
                            # Finding the chapter_data from "a" tag through tr_html_chapter.
                    for i, links in enumerate(tr_html_chapter.find_all("a"), start=1):
                        link_list.append(links["href"] + "/full") 
                        name_list.append(re.sub('"','',links.text))
                        index_list.append(i)
            else:
                link_list.append(baseurl + links["href"])
                name_list.append(links.text.strip())
                index_list.append(i)
        if source == "bato" or "mangasee":
            link_list.reverse()
            name_list.reverse()
        # Creating two dictionary that take key as index and value as items from "link_list" and "name_list" respectively.
        url_dict = {index_list[i]: link_list[i] for i in range(len(link_list))}
        name_dict = {index_list[i]: name_list[i] for i in range(len(name_list))}
        # Making UI to get user input from name_list.
        for key, value in name_dict.items():
            print(f'{key}. {value}')
        try:
            # If statement in case no manga/chapter was found.
            if not link_list:
                print(f'Sorry could not found anything :(!')
            else:
                # Matching the user selection with "urls_dict" dictionary to get its value.
                while True:
                    selection = int(input("\nSelect the index number: "))
                    if selection in url_dict:
                        # Getting the name and link by matching the index number from dictionaries.
                        link = f"{url_dict[selection]}"
                        name = f"{name_dict[selection]}"
                        print("Fetching, please wait...")
                        return link, name
                    else:
                        raise ValueError
        except ValueError:
            print("Invalid integer. The number must be in the range.")

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
            html_tag = soup.find_all("a", class_="item-title", href=True)
            # Using core method as function to get rid of repeating the same lines.
            source = ""
            manga_tuple = self.core(html_tag, baseurl, source)
            manga_link = manga_tuple[0]
            manga_name = manga_tuple[1]
            # Starting the requests session.
            session = requests.Session()
            # Sending get request to the "manga_link" website.
            manga_response = session.get(manga_link, timeout=2)
            # Parsering the response with "BeauitifulSoup".
            manga_soup = BeautifulSoup(manga_response.content, "html.parser")
            # Finding all the "a" elements in the webpage.
            html_tag = manga_soup.find_all(
                    "a", class_="visited chapt", href=True
            )
            # Using core method as function to get rid of repeating the same lines.
            source = "bato"
            chapter_tuple = self.core(html_tag, baseurl, source)
            chapter_link = chapter_tuple[0]
            chapter_name = chapter_tuple[1] 
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
            driver.quit()
            # Creating the list to store image url.
            img_links_list = []
            # Finding all the "img" elements from img_html_chapter.
            for imgs in imgs_html_chapter:
                img_links_list.append(imgs["src"])
            # Calling download_compress method as function.
            self.download_compress(manga_name, chapter_name, img_links_list)
        except TimeoutException:
            print("Network Error!")
        except requests.exceptions.RequestException:
            print("Network Error!")
        except TypeError:
            pass
        except SessionNotCreatedException:
            print("If you are not using android then install from win_linux_requirement.txt file")

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
            html_tag = soup.find_all("a", class_="SeriesName ng-binding", href=True)
            # Using core method as function to get rid of repeating the same lines.
            source = ""
            manga_tuple = self.core(html_tag, baseurl, source)
            manga_link = manga_tuple[0]
            manga_name = manga_tuple[1]
            # Sending request with selenium webdriver.
            driver.get(manga_link)
            # Making driver wait 10 second before it sends error for not finding the page. 
            driver.implicitly_wait(10)
            # Using exist method as function to confirm if the clickable element exists, if so then click it.
            if self.exists(element = ".list-group-item.ShowAllChapters.ng-scope") == True:
                WebDriverWait(driver,1).until(EC.element_to_be_clickable((By.CSS_SELECTOR,".list-group-item.ShowAllChapters.ng-scope"))).click()
            # Parsering the response with "BeauitifulSoup".
            manga_soup = BeautifulSoup(driver.page_source, "html.parser")
            # Finding all the "a" elements in the webpage.
            html_tag = manga_soup.find_all(
                "a", class_="list-group-item ChapterLink ng-scope", href=True
                )
            # Using core method as function to get rid of repeating the same lines.
            source = "mangasee"
            chapter_tuple = self.core(html_tag, baseurl, source)
            chapter_link = chapter_tuple[0]
            chapter_name = chapter_tuple[1]
            # Sending request with selenium webdriver.
            driver.get(chapter_link)
            # Making driver wait 10 second before it sends error for not finding the page.
            driver.implicitly_wait(10)
            # Parsering the response with "BeauitifulSoup".
            chapter_soup = BeautifulSoup(
            driver.page_source, "html.parser")
            # Finding all the "img" elements from webpage.
            imgs_html_chapter = chapter_soup.find_all(
                "img", class_="img-fluid HasGap"
            )
            # Closing the selenium webdriver
            driver.quit()
            # Creating the list to store image url.
            img_links_list = []
            # Finding all the "img" elements from img_html_chapter.
            for imgs in imgs_html_chapter:
                img_links_list.append(imgs["src"])
            # Calling download_compress method as function.
            self.download_compress(manga_name, chapter_name, img_links_list)
        except requests.exceptions.RequestException:
            print("Network Error!")
        except TimeoutException:
            print("Network Error!")
        except TypeError:
            pass
        except SessionNotCreatedException:
            print("If you are not using android then install from win_linux_requirement.txt file")
    
    def comicextra(self, search_term):
        # Basic url to access the searching.
        url = "https://comixextra.com/search?keyword=" + search_term  
        baseurl = ""
        try:
            # Sending request with selenium webdriver.
            driver.get(url)
            # Making driver wait 10 second before it sends error for not finding the page.
            driver.implicitly_wait(10)
            # Getting html page with BeautifulSoup module.
            soup = BeautifulSoup(driver.page_source, "html.parser")
            # Accessing "h3" elements in the webpage.
            html_tag = soup.find_all("h3")
            # Using core method as function to get rid of repeating the same lines.
            source = "comicextra"
            manga_tuple = self.core(html_tag, baseurl, source)
            manga_link = manga_tuple[0]
            manga_name = manga_tuple[1]
            # Sending request with selenium webdriver.
            driver.get(manga_link)
            # Making driver wait 10 second before it sends error for not finding the page.
            driver.implicitly_wait(10)
            # Parsering the response with "BeauitifulSoup".
            manga_soup = BeautifulSoup(driver.page_source, "html.parser")
            # Getting table element from html page.
            html_tag = manga_soup.find_all(
                    "table", class_="table"
            )
            # Using core method as function to get rid of repeating the same lines.
            source = "comicextra_chapter"
            chapter_tuple = self.core(html_tag, baseurl, source)
            chapter_link = chapter_tuple[0]
            chapter_name = chapter_tuple[1]
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
            driver.quit()
            # Creating the list to store image url.
            img_links_list = []
            # Finding all the "img" elements from div_html_chapter.
            for imgs_html_chapter in div_html_chapter:
                for imgs in imgs_html_chapter.find_all("img"):
                    img_links_list.append(imgs["src"].strip())
            # Calling download_compress method as function.
            self.download_compress(manga_name, chapter_name, img_links_list)
        except (requests.exceptions.RequestException, TimeoutException):
            print("Network Error!")
        except TypeError:
            pass
        except SessionNotCreatedException:
            print("If you are not using android then install from win_linux_requirement.txt file")
