'''Manga Sources'''

#Importing necessary modules
import os
import re
import shutil
import subprocess

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import (NoSuchElementException,
                                        SessionNotCreatedException,
                                        TimeoutException, WebDriverException)
from selenium.webdriver.common.by import By
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

class Schoolsources:
    '''Manga functions'''

    def exists(self, element):
        try:
            driver.find_element(By.CSS_SELECTOR,element)
        except NoSuchElementException:
            return False
        return True

    def core(self, html_tag, baseurl, source, pageurl):
        # Creating three lists "link_list", "name_list" and "index_list".
        link_list = []
        name_list = []
        index_list = []
        # Enumerating links from html_tag taken from sources with i for index.
        if source == "sundari":
            for i, a_html in enumerate(html_tag, start=1):
                for links in a_html.find_all("a"):
                    name = re.sub("\W+", " ", links["href"].split("xyz")[1]).title()
                    link_list.append(baseurl + links["href"])
                    name_list.append(name.strip())
                    index_list.append(i)
        elif source == "desi":
            link_list.append(pageurl)
            name_list.append("Next Page")
            index_list.append(0)
            for i, links in enumerate(html_tag, start=1):
                name = re.sub("[^a-z]", " ", links["href"].split("in")[1]).title()
                link_list.append(baseurl + links["href"])
                name_list.append(name.strip())
                index_list.append(i)
        elif source == "hotpic":
            link_list.append(pageurl)
            name_list.append("Next Page")
            index_list.append(0)
            for i, links in enumerate(html_tag, start=1):
                # Adding exceptional cases for each sources.
                link_list.append(baseurl + links["href"])
                name_list.append(links["title"].strip())
                index_list.append(i)
        elif source == "xcxco":
            link_list.append(pageurl)
            name_list.append("Previous Page")
            index_list.append(0)
            for i, links in enumerate(html_tag, start=1):
                # Adding exceptional cases for each sources.
                name = re.sub("[^a-z]", " ", links["href"].split("-")[1]).title()
                link_list.append(baseurl + links["href"])
                name_list.append(name.strip())
                index_list.append(i)
            link_list.append(pageurl)
            name_list.append("Next Page")
            index_list.append(i)
        else:
            for i, links in enumerate(html_tag, start=1):
                # Adding exceptional cases for each sources.
                link_list.append(baseurl + links["href"])
                name_list.append(links["title"].strip())
                index_list.append(i)
        # Creating two dictionary that take key as indx and value as items from "link_list" and "name_list" respectively.
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

    def directory(self, method_dir):
        dir = ".NSFW"
        if not os.path.isdir(dir):
            os.mkdir(dir)
            os.chdir(dir)
        else:
            os.chdir(dir)
        if not os.path.isdir(method_dir):
            os.mkdir(method_dir)
            os.chdir(method_dir)
        else:
            os.chdir(method_dir)

    def download(self, url, name):
        with requests.get(url, stream = True) as res:
            # Checking header to get the content length, in bytes.
            total_length = int(res.headers.get("Content-Length"))
            # Checking if request was valid.
            if res.status_code == 200:
                # Implement progress bar via tqdm.
                with tqdm.wrapattr(res.raw, "read", toal=total_length, desc="")as raw:
                    # Downloading image via shutil.
                    with open(name,'wb') as f:
                         shutil.copyfileobj(raw, f)
                print('Video sucessfully Downloaded: ',name)
            else:
                print('Video Couldn\'t be retrieved')

    def r34(self,search_term):
        # Url to access the searching.
        url = f"https://r-34.xyz/tag/{search_term}?type=image&sort=top_rated"
        # Url to access the base website.
        baseurl = ""
        try:
            # Sending request to the webpage.
            driver.get(url)
            # Getting html page with BeautifulSoup module.
            soup = BeautifulSoup(driver.page_source, "html.parser")
            # Finding all the "a" elements from webpage.
            html_tag = soup.find_all("img", class_="img")
            self.directory(method_dir="R-34")
            for links in html_tag:
                url = links["src"]
                subprocess.call(["wget", url])
        except SessionNotCreatedException:
            print("If you are not using android then install from win_linux_requirement.txt file")
        except (requests.exceptions.RequestException, WebDriverException, TimeoutException):
            print("Network Error!")
        except TypeError:
            pass

    def hotpic(self):
        # Basic url to access the searching.
        url = "https://hotpic.cc/nsfw"
        baseurl = "https://hotpic.cc"
        pageurl = "https://hotpic.cc/nsfw/"
        try:
            # Sending request with selenium webdriver.
            driver.get(url)
            # Making driver wait 10 second before it sends error for not finding the page.
            driver.implicitly_wait(10)
            # Getting html page with BeautifulSoup module.
            soup = BeautifulSoup(driver.page_source, "html.parser")
            # Accessing "h3" elements in the webpage.
            div_tag = soup.find("div", class_="row g-2 adpop")
            html_tag = div_tag.find_all("a", attrs={"data-zoom": "false", "data-autofit": "false", "data-preload": "true", "data-download": "true", "data-controls": "false"})
            # Using core method as function to get rid of repeating the same lines.
            source = "hotpic"
            manga_tuple = self.core(html_tag, baseurl, source, pageurl)
            manga_link = manga_tuple[0]
            manga_name = manga_tuple[1]
            index = 1
            while True:
                if manga_name == "Next Page":
                    index += 1
                    # Sending request with selenium webdriver.
                    driver.get(manga_link + str(index))
                    # Getting html page with BeautifulSoup module.
                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    # Accessing "h3" elements in the webpage.
                    html_tag = soup.find_all("a", attrs={"data-zoom": "false", "data-autofit": "false", "data-preload": "true", "data-download": "true", "data-controls": "false"})
                    # Using core method as function to get rid of repeating the same lines.
                    source = "hotpic"
                    manga_tuple = self.core(html_tag, baseurl, source, pageurl)
                    manga_link = manga_tuple[0]
                    manga_name = manga_tuple[1]
                    if manga_name != "Next Page":
                        break
                else: 
                    break
            # Sending request with selenium webdriver.
            driver.get(manga_link)
            # Making driver wait 10 second before it sends error for not finding the page.
            driver.implicitly_wait(10)
            # Parsering the response with "BeauitifulSoup".
            manga_soup = BeautifulSoup(driver.page_source, "html.parser")
            # Getting table element from html page.
            self.directory(method_dir="HotPic")
            html_tag = manga_soup.find_all("a", class_="spotlight")
            for links in html_tag:
                url = links["href"]
                subprocess.call(["wget", url])
        except SessionNotCreatedException:
            print("If you are not using android then install from win_linux_requirement.txt file")
        except (requests.exceptions.RequestException, WebDriverException, TimeoutException):
            print("Network Error!")

    def sundari(self, search_term):
        # Basic url to access the searching.
        url = "https://sundarikanya.xyz/?s=" + search_term
        baseurl = ""
        try:
            # Sending request with selenium webdriver.
            driver.get(url)
            # Getting html page with BeautifulSoup module.
            soup = BeautifulSoup(driver.page_source, "html.parser")
            # Accessing "h3" elements in the webpage.
            html_tag = soup.find_all("div", class_="post-thumb-img-content post-thumb")
            # Using core method as function to get rid of repeating the same lines.
            source = "sundari"
            manga_tuple = self.core(html_tag, baseurl, source, pageurl="")
            manga_link = manga_tuple[0]
            # Sending request with selenium webdriver.
            driver.get(manga_link)
            # Making driver wait 10 second before it sends error for not finding the page.
            driver.implicitly_wait(10)
            # Parsering the response with "BeauitifulSoup".
            manga_soup = BeautifulSoup(driver.page_source, "html.parser")
            # Getting table element from html page.
            self.directory(method_dir="Sundari")
            html_tag = manga_soup.find("source")
            url = html_tag["src"]
            subprocess.call(["wget", url])
        except SessionNotCreatedException:
            print("If you are not using android then install from win_linux_requirement.txt file")
        except (requests.exceptions.RequestException, WebDriverException, TimeoutException):
            print("Network Error!")

    def desi(self):
        # Basic url to access the searching.
        url = "https://desifakes.in/"
        baseurl = ""
        pageurl = "https://desifakes.in/page/"
        try:
            # Sending request with selenium webdriver.
            driver.get(url)
            # Getting html page with BeautifulSoup module.
            soup = BeautifulSoup(driver.page_source, "html.parser")
            # Accessing "h3" elements in the webpage.
            html_tag = soup.find_all("a", rel="bookmark")
            # Using core method as function to get rid of repeating the same lines.
            source = "desi"
            manga_tuple = self.core(html_tag, baseurl, source, pageurl)
            manga_link = manga_tuple[0]
            manga_name = manga_tuple[1]
            index = 1
            while True:
                if manga_name == "Next Page":
                    index += 1
                    # Sending request with selenium webdriver.
                    driver.get(manga_link + str(index))
                    # Getting html page with BeautifulSoup module.
                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    # Accessing "h3" elements in the webpage.
                    html_tag = soup.find_all("a", rel="bookmark")
                    # Using core method as function to get rid of repeating the same lines.
                    source = "desi"
                    manga_tuple = self.core(html_tag, baseurl, source, pageurl)
                    manga_link = manga_tuple[0]
                    manga_name = manga_tuple[1]
                    if manga_name != "Next Page":
                        break
                else:
                    break
            driver.get(manga_link)
            # Making driver wait 10 second before it sends error for not finding the page.
            driver.implicitly_wait(10)
            # Parsering the response with "BeauitifulSoup".
            manga_soup = BeautifulSoup(driver.page_source, "html.parser")                    # Getting table element from html page.
            self.directory(method_dir="DesiFakes")
            a_tag = manga_soup.find_all("a", attrs={"data-elementor-open-lightbox": "yes"})
            img_tag = manga_soup.find_all("img", border="0")
            if not a_tag:
                for i, html_tag in enumerate(img_tag, start=1):
                    url = html_tag["src"]
                    name = manga_name + " " + str(i) + ".jpg"
                    subprocess.call(["wget", "-O", name, url])
            else: 
                for i, html_tag in enumerate(a_tag, start=1):
                    url = html_tag["href"]
                    name = manga_link + " " + str(i) + ".jpg"
                    subprocess.call(["wget", "-O", name, url])
        except SessionNotCreatedException:
            print("If you are not using android then install from win_linux_requirement.txt file")
        except (requests.exceptions.RequestException, WebDriverException, TimeoutException):
            print("Network Error!")
        except TypeError:
            print("Invalid Value")

    def xcxco(self, search_term):
        # Basic url to access the searching.
        url = "https://xcxco.com/new/" + search_term
        baseurl = ""
        pageurl = f"https://xcxco.com/new/{search_term}?p="
        try:
            # Sending request with selenium webdriver.
            driver.get(url)
            # Making driver wait 10 second before it sends error for not finding the page.
            driver.implicitly_wait(10)
            # Getting html page with BeautifulSoup module.
            soup = BeautifulSoup(driver.page_source, "html.parser")
            # Accessing "h3" elements in the webpage.
            html_tag = soup.find_all("a", class_="nuyrfe")
            # Using core method as function to get rid of repeating the same lines.
            source = "xcxco"
            manga_tuple = self.core(html_tag, baseurl, source, pageurl)
            manga_link = manga_tuple[0]
            manga_name = manga_tuple[1]
            # Sending request with selenium webdriver.
            driver.get(manga_link)
            # Making driver wait 10 second before it sends error for not finding the page.
            driver.implicitly_wait(10)
            # Parsering the response with "BeauitifulSoup".
            manga_soup = BeautifulSoup(driver.page_source, "html.parser")
            # Getting table element from html page.
            self.directory(method_dir="Xcxco")
            html_tag = manga_soup.find_all("source", type="video/mp4")
            for links in html_tag:
                url = links["src"]
                subprocess.call(["wget", url])
        except SessionNotCreatedException:
            print("If you are not using android then install from win_linux_requirement.txt file")
        except (requests.exceptions.RequestException, WebDriverException, TimeoutException):
            print("Network Error!")
