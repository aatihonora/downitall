'''Anime Sources'''

#Importing necessary modules
import os
import re
import subprocess

import requests
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
# Getting the current directory.
bookcli = os.getcwd()

class Musicsources:
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
        if source == "bombmusic": 
            for i, a_html in enumerate(html_tag, start=1):
                for links in a_html.find_all("a", class_="link", attrs={"no-data-pjax": ""}):
                    link_list.append(baseurl + links["href"])
                for links in a_html.find("a", class_="trackLink"):
                    name_list.append(links.text)
                index_list.append(i)
        elif source == "pagalnew":
            for i, a_html in enumerate(html_tag, start=1):
                div = a_html.find("div")
                links = div.find("a")
                link_list.append(baseurl + links["href"])
                name_list.append(links.text.strip())
                index_list.append(i)
        elif source == "pagalnew_track":
            for i, links in enumerate(html_tag, start=1):
                link_list.append(baseurl + links["href"])
                name_list.append(links.text.strip())
                index_list.append(i)
        else:
            for i, links in enumerate(html_tag, start=1):
                link_list.append(baseurl + links["href"])
                name_list.append(re.sub("»", "", links["title"].split("«")[1]))
                index_list.append(i)
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
    def download(self, name, url):
        # Making the folder and opening it
        folder = "Music"
        if not os.path.isdir(folder):
            os.mkdir(folder)
            os.chdir(folder)
        else:
            os.chdir(folder)
        # Downloading the file with wget as it is fast and has its own progress bar.
        args = ['wget', '-O', name, url]
        subprocess.call(args)
        print("Download Complete.")

    def lightaudio(self,search_term):
        # Url to access the searching.
        url = "https://web.ligaudio.ru/mp3/" + search_term
        baseurl = "https:"
        # Url to access the base website.
        try:
            # Sending request to the webpage.
            driver.get(url)
            # Getting html page with BeautifulSoup module
            soup = BeautifulSoup(driver.page_source, "html.parser")
            # Finding all the mentioned elements from webpage.
            html_tag = soup.find_all("a", class_="down")
            # Using core method as function to get rid of repeating the same lines.
            source = ""
            track_tuple = self.core(html_tag, baseurl, source)
            url = track_tuple[0]
            name = track_tuple[1] + ".mp3"
            self.download(name, url)
        except SessionNotCreatedException:
            print("If you are not using android then install from win_linux_requirement.txt file")
        except (requests.exceptions.RequestException, WebDriverException, TimeoutException):
            print("Network Error!")
        except TypeError:
            pass

    def bombmusic(self,search_term):
        # Url to access the searching.
        url = f"https://bomb-music.ru/tracks/{search_term}/"
        baseurl = "https:"
        # Url to access the base website.
        try:
            # Sending request to the webpage.
            driver.get(url)
            # Getting html page with BeautifulSoup module
            soup = BeautifulSoup(driver.page_source, "html.parser")
            # Finding all the mentioned elements from webpage.
            html_tag = soup.find_all("div", class_="themeWhiteTrackBoxResult")
            # Using core method as function to get rid of repeating the same lines.
            source = "bombmusic"
            track_tuple = self.core(html_tag, baseurl, source)
            url = track_tuple[0]
            name = track_tuple[1] + ".mp3"
            self.download(name, url)
        except SessionNotCreatedException:
            print("If you are not using android then install from win_linux_requirement.txt file")
        except (requests.exceptions.RequestException, WebDriverException, TimeoutException):
            print("Network Error!")
        except TypeError:
            pass

    def pagalnew(self,search_term):
        # Url to access the searching.
        url = "https://pagalnew.com/search.php?find=" + search_term
        baseurl = "https://pagalnew.com"
        # Url to access the base website.
        try:
            # Sending request to the webpage.
            driver.get(url)
            # Getting html page with BeautifulSoup module
            soup = BeautifulSoup(driver.page_source, "html.parser")
            # Finding all the mentioned elements from webpage.
            html_tag = soup.find_all("div", class_="main_page_category_music_txt")
            # Using core method as function to get rid of repeating the same lines.
            source = "pagalnew"
            track_tuple = self.core(html_tag, baseurl, source)
            link = track_tuple[0]
            name = track_tuple[1] + ".mp3"
            # Sending request to the webpage.
            driver.get(link)
            # Getting html page with BeautifulSoup module
            soup = BeautifulSoup(driver.page_source, "html.parser")
            # Finding all the mentioned elements from webpage.
            html = soup.find("a", class_="dbutton", text=lambda t: t and "320" in t)
            url = baseurl + html["href"]
            self.download(name, url)
        except SessionNotCreatedException:
            print("If you are not using android then install from win_linux_requirement.txt file")
        except (requests.exceptions.RequestException, WebDriverException, TimeoutException):
            print("Network Error!")
        except TypeError:
            pass
