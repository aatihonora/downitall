'''Anime Sources'''

#Importing necessary modules
import os
import re
import subprocess
import time

import aria2p
import gdown
import requests
import wget
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import (NoSuchElementException,
                                        SessionNotCreatedException,
                                        TimeoutException, WebDriverException)
from selenium.webdriver.common.by import By

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
# initializing default aria server.
aria2 = aria2p.API(
    aria2p.Client(
        host="http://localhost",
        port=6800,
        secret=""
    )
)
# Getting the current directory.
bookcli = os.getcwd()

class Animesources:
    '''Anime functions'''

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
        # Adding exceptional cases for each sources.
        if source == "nyaa":
            for i, a_html in enumerate(html_tag, start=1):
                for links in a_html.find_all("a", title=True, class_=None, href=True):
                    link_list.append(baseurl + links["href"])
                    name_list.append(links["title"].strip())
                    index_list.append(i)
        elif source == "kayoanime":
            for a_html in html_tag:
                for i, links in enumerate(a_html.find_all("a", class_="post-thumb", href=True), start=1):
                    link_list.append(links["href"])
                    name_list.append(links["aria-label"].strip())
                    index_list.append(i)
        else:
            for i, links in enumerate(html_tag, start=1):
                link_list.append(baseurl + links["href"])
                name_list.append(links.text.strip())
                index_list.append(i)
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
    def download(self, anime_name, url):
        # Making the folder and opening it
        anime = re.sub('[^a-z,0-9]', '_', anime_name, flags=re.IGNORECASE)
        if not os.path.isdir(anime):
            os.mkdir(anime)
            os.chdir(anime)
        else:
            os.chdir(anime)
        # Downloading the file with wget as it is fast and has its own progress bar.
        anime = wget.download(url)

    def kayoanime(self,search_term):
        # Url to access the searching.
        url = "https://kayoanime.com/?s=" + search_term
        baseurl = ""
        # Url to access the base website.
        try:
            # Sending request to the webpage.
            driver.get(url)
            # Getting html page with BeautifulSoup module
            soup = BeautifulSoup(driver.page_source, "html.parser")
            # Finding all the "a" elements from webpage.
            html_tag = soup.find_all("ul", class_="posts-items")
            # Using core method as function to get rid of repeating the same lines.
            source = "kayoanime"
            anime_tuple = self.core(html_tag, baseurl, source)
            anime_link = anime_tuple[0]
            # Sending get request to the "manga_link" website.
            driver.get(anime_link)
            # Parsering the response with "BeauitifulSoup".
            anime_soup = BeautifulSoup(driver.page_source, "html.parser")
            # Finding all the "a" elements in the webpage.
            html_tag = anime_soup.find("a", target="_blank")
            url = html_tag["href"].split("?")[0]
            gdown.download_folder(url)
        except (requests.exceptions.RequestException, WebDriverException, TimeoutException):
            print("Network Error!")
        except TypeError:
            pass
        except RuntimeError:
            print("Google file is either private or unavilable")
        except SessionNotCreatedException:
            print("If you are not using android then install from win_linux_requirement.txt file")

    def tokyoinsider(self, search_term):
        # Url to access the searching.
        url = "https://www.tokyoinsider.com/anime/search?k=" + search_term
        # Url to access the base website.
        baseurl = "https://www.tokyoinsider.com"
        try:
            # Sending request to the webpage.
            driver.get(url)
            # Getting html page with BeautifulSoup module
            soup = BeautifulSoup(driver.page_source, "html.parser")
            # Finding all the "a" elements from webpage.
            html_tag = soup.find_all("a", attrs={"style":"font: bold 14px verdana;"})
            # Using core method as function to get rid of repeating the same lines.
            source = ""
            anime_tuple = self.core(html_tag, baseurl, source)
            anime_link = anime_tuple[0]
            anime_name = anime_tuple[1]
            # Sending get request to the "manga_link" website.
            driver.get(anime_link)
            # Parsering the response with "BeauitifulSoup".
            anime_soup = BeautifulSoup(driver.page_source, "html.parser")
            # Finding all the "a" elements in the webpage.
            html_tag = anime_soup.find_all(
                    "a", class_="download-link"
            )
            # Using core method as function to get rid of repeating the same lines.
            source = ""
            episode_tuple = self.core(html_tag, baseurl, source)
            episode_link = episode_tuple[0]
            # Sending request with selenium webdriver.
            driver.get(episode_link)
            # Parsering the response with "BeauitifulSoup".
            episode_soup = BeautifulSoup(
                driver.page_source, "html.parser"
            )
            driver.quit()
            # Getting the working download link from html webpage.
            html = episode_soup.find("div", id="inner_page")
            link = html.find("a")
            url = link.find_next("a")['href']
            self.download(anime_name, url)
            print("\nDownload Complete.")
        except (requests.exceptions.RequestException, WebDriverException, TimeoutException):
            print("Network Error!")
        except TypeError:
            pass
        except SessionNotCreatedException:
            print("If you are not using android then install from win_linux_requirement.txt file")

    def nyaa(self, search_term):
        # Url to access the searching.
        url = f'https://nyaa.si/?q={search_term}&f=0&c=1_2&s=seeders&o=desc'
        # Url to access the base website.
        baseurl = "https://nyaa.si"
        try:
            # Sending request to the webpage.
            driver.get(url)
            # Getting html page with BeautifulSoup module
            soup = BeautifulSoup(driver.page_source, "html.parser")
            # Finding all the "a" elements from webpage.
            html_tag = soup.find_all("td", colspan="2")
            # Using core method as function to get rid of repeating the same lines.
            source = "nyaa"
            anime_tuple = self.core(html_tag, baseurl, source)
            anime_link = anime_tuple[0]
            # Sending get request to the "manga_link" website.
            driver.get(anime_link)
            # Parsering the response with "BeauitifulSoup".
            anime_soup = BeautifulSoup(driver.page_source, "html.parser")
            # Finding all the "a" elements in the webpage.
            html_tag = anime_soup.find(
                    "a", class_="card-footer-item"
            )
            driver.quit()
            # Getting the download link and uaing aria2p module to download magnet link.
            download_link = html_tag['href']
            aria2.add_magnet(download_link)
            # Calling the aria2p gui to see download progress.
            subprocess.call(["aria2p"])
        except (requests.exceptions.RequestException, WebDriverException, TimeoutException):
            print("Network Error! or Aria2c is not on, use aria2c --enable-rpc command")
        except TypeError:
            pass
        except SessionNotCreatedException:
            print("If you are not using android then install from win_linux_requirement.txt file")
