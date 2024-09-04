'''TV Sources'''

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

class Tvsources:
    '''TV Sources'''

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
        if source == "1337x":
            for i, a_html in enumerate(html_tag, start=1):
                for links in a_html.find_all("a", href=True):
                    link_list.append(baseurl + links["href"])
                    name_list.append(links.text.strip())
                    index_list.append(i)
        elif source == "lime":
            for i, tr_html in enumerate(html_tag, start=1):
                for a_html in tr_html.find_all("div", class_="tt-name"):
                    for links in a_html.find_all("a", rel=True):
                        print(links)
                        link_list.append(baseurl + links["href"])
                    for links in a_html.find_all("a", rel=None):
                        name_list.append(links.text.strip())
                index_list.append(i)
        else:
            for i, links in enumerate(html_tag, start=1):
                link_list.append(baseurl + links["href"])
                name_list.append(links.text.strip())
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
    def download(self, name, anime_name, url):
        # Making the folder and opening it
        if not os.path.isdir(anime_name):
            os.mkdir(anime_name)
            os.chdir(anime_name)
        else:
            os.chdir(anime_name)
        # Downloading the file with wget as it is fast and has its own progress bar.
        args = ['wget', '-O', name, url]
        subprocess.call(args)
        print("Download Complete.")

    def vadapav(self,search_term):
        # Url to access the searching.
        url = "https://vadapav.mov/s/" + search_term
        # Url to access the base website.
        baseurl = "https://vadapav.mov"
        try:
            # Sending request to the webpage.
            driver.get(url)
            # Getting html page with BeautifulSoup module
            soup = BeautifulSoup(driver.page_source, "html.parser")
            # Finding all the mentioned elements from webpage.
            html_tag = soup.find_all("a", class_="directory-entry wrap")
            # Using core method as function to get rid of repeating the same lines.
            source = ""
            series_tuple = self.core(html_tag, baseurl, source)
            series_link = series_tuple[0]
            series_name = series_tuple[1]
            # Sending request to the webpage.
            driver.get(series_link)
            # Getting html page with BeautifulSoup module
            soup = BeautifulSoup(driver.page_source, "html.parser")
            # Finding all the mentioned elements from webpage.
            html_tag = soup.find_all("a", class_="directory-entry wrap") 
            if not len(html_tag) == 1:
                driver.get(series_link)
                # Getting html page with BeautifulSoup module
                series_soup = BeautifulSoup(driver.page_source, "html.parser")
                # Finding all the mentioned elements from webpage.
                html_tag = series_soup.find_all("a", class_="directory-entry wrap")[1:]
                # Using core method as function to get rid of repeating the same lines.
                source = ""
                season_tuple = self.core(html_tag, baseurl, source)
                link = season_tuple[0]
            else:
                link = series_link
                print(link)
            # Sending get request to the website.
            driver.get(link)
            # Parsering the response with "BeauitifulSoup".
            soup = BeautifulSoup(driver.page_source, "html.parser")
            # Finding all the mentioned elements in the webpage.
            html_tag = soup.find_all("a", class_="file-entry wrap")
            # Using core method as function to get rid of repeating the same lines.
            source = ""
            episode_tuple = self.core(html_tag, baseurl, source)
            url = episode_tuple[0]
            name = episode_tuple[1]
            self.download(name, series_name, url)  
        except SessionNotCreatedException:
            print("If you are not using android then install from win_linux_requirement.txt file")
        except (requests.exceptions.RequestException, WebDriverException, TimeoutException):
            print("Network Error!")
        except TypeError:
            pass

    def lime(self, search_term):
        # Url to access the searching.
        url = f"https://www.limetorrents.lol/search/all/{search_term}/seeds/1/"
        # Url to access the base website.
        baseurl = ""
        try:
            # Sending request to the webpage.
            driver.get(url)
            # Getting html page with BeautifulSoup module
            soup = BeautifulSoup(driver.page_source, "html.parser")
            # Finding all the mmentioned elements from webpage.
            html_tag = soup.find_all("tbody")[1]
            # Using core method as function to get rid of repeating the same lines.
            source = "lime"
            series_tuple = self.core(html_tag, baseurl, source)
            url = series_tuple[0]
            dir = os.getcwd()
            # Using the aria2c module to download.
            args = ["aria2c", "--file-allocation=none", "--seed-time=0", "-d", dir, url]
            subprocess.call(args)
        except SessionNotCreatedException:
            print("If you are not using android then install from win_linux_requirement.txt file")
        except (requests.exceptions.RequestException, WebDriverException, TimeoutException):
            print("Network Error!")
        except TypeError:
            pass

    def torrent(self, search_term):
        # Url to access the searching.
        url = f'https://1337x.to/sort-search/{search_term}/seeders/desc/1/'
        # Url to access the base website.
        baseurl = "https://1337x.to"
        try:
            # Sending request to the webpage.
            driver.get(url)
            # Getting html page with BeautifulSoup module
            soup = BeautifulSoup(driver.page_source, "html.parser")
            # Finding all the mentioned elements from webpage.
            html_tag = soup.find_all("td", class_="coll-1 name")
            # Using core method as function to get rid of repeating the same lines.
            source = "1337x"
            series_tuple = self.core(html_tag, baseurl, source)
            series_link = series_tuple[0]
            # Sending get request to the website.
            driver.get(series_link)
            # Parsering the response with "BeauitifulSoup".
            series_soup = BeautifulSoup(driver.page_source, "html.parser")
            # Finding all the mentioned elements in the webpage.
            html_tag = series_soup.find(
                    "a", id="id1"
            )
            # Using aria2c module to download.
            url = html_tag['href']
            dir = os.getcwd()
            args = ["aria2c", "--file-allocation=none", "--seed-time=0", "-d", dir, url]
            subprocess.call(args)
        except SessionNotCreatedException:
            print("If you are not using android then install from win_linux_requirement.txt file")
        except (requests.exceptions.RequestException, WebDriverException, TimeoutException):
            print("Network Error!")
        except TypeError:
            pass
