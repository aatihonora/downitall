'''TV Sources'''

#Importing necessary modules
import os
import re
import subprocess
import time

import pandas as pd
import questionary
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import (NoSuchElementException,
                                        SessionNotCreatedException,
                                        TimeoutException, WebDriverException)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

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
            driver.find_element(By.CSS_SELECTOR,element)
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
        for row in tbody.find_all('tr'):
            row_data = []
            for cell in row.find_all('td'):
                cell_info = cell.text.strip()
                row_data.append(cell_info[:30])
            data.append(row_data)
        # Creating a pandas dataframe
        df = pd.DataFrame(data)
        return df
############################################################################
    # Defining the function for player to choose the index.
    def user_choice(self, name_list, link_list, index_list, source):
        # Appendind data for next and previous page.
        # Creating two dictionary that take key as index and value as items from "link_list" and "name_list" respectively.
        url_dict = {index_list[i]: link_list[i] for i in range(len(link_list))}
        name_dict = {index_list[i]: name_list[i] for i in range(len(name_list))}
        try:
            # If statement in case no manga/chapter was found.
            if source == "vadapav" and not name_list:
                print("Could not find any thing :(")
            elif source != "vadapav" and name_list == 2:
                print("Could not find any thing :(")
            else:
                # Matching the user selection with "urls_dict" dictionary to get its value.
                selection = int(input("\n\nSelect the index number: "))
                if selection in url_dict:
                    # Getting the name and link by matching the index number from dictionaries.
                    link = f"{url_dict[selection]}"
                    name = f"{name_dict[selection]}"
                    print("Fetching, please wait...")
                    subprocess.call(["clear"])
                    return [link, name, selection]
                else:
                    raise ValueError
        except ValueError:
            print("Invalid integer. The number must be in the range.") 
############################################################################
    # Defining the function for retrying the user_choice function.
    def retry(self, source, search_term, choice):
        # Using match case argument to see which class called the function.
        answer = questionary.select("Do you want to download another file? ", choices=["Yes", "No"]).ask()
        if answer == "Yes":
            if source == "vadapav":
                Tvsources().Vadapav().vadapav(search_term)
            elif source == "1337x":
                Tvsources().Torrent().torrent_search(search_term, choice)
            else:
                Tvsources().Documentary().documentary()
############################################################################
    class Vadapav:
        def vadapav(self,search_term):
            source = "vadapav"
            # Url to access the searching.
            url = "https://vadapav.mov/s/" + search_term
            # Url to access the base website.
            base_url = "https://vadapav.mov"
            try:
                while True:
                    # Sending request to the webpage.
                    driver.get(url)
                    # Getting html page with BeautifulSoup module
                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    # Finding all the mentioned elements from webpage.
                    html_tag = soup.find_all("a", {"class": ["directory-entry wrap", "file-entry wrap"]})
                    index_list = []
                    name_list = []
                    link_list = []
                    for i, links in enumerate(html_tag, start=1):
                        index_list.append(i)
                        name_list.append(links.text.strip())
                        link_list.append(base_url + links["href"]) 
                    for i, name in zip(index_list, name_list):
                        print(f"{i}. {name}")
                    data = Tvsources().user_choice(name_list, link_list, index_list, source)
                    url = data[0]
                    name = data[1]
                    if "/f/" in url:
                        break
                # Downloading the file with wget as it is fast and has its own progress bar.
                args = ['wget', '-O', name, url]
                subprocess.call(args)
                print("Download Complete.")
            except SessionNotCreatedException:
                print("If you are not using android then install from win_linux_requirement.txt file")
            except (requests.exceptions.RequestException, WebDriverException, TimeoutException):
                print("Network Error!")
            except TypeError:
                pass
############################################################################
    class Torrent:
        def torrent_search(self, search_term, choice):
            source = "1337x"
            index = 1
            term = re.sub("\W", "+", search_term)
            if choice == 1:
                search_type = "Movies"
            else:
                search_type = "TV"
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
                    if Tvsources().exists(element = ".pagination"):
                        html_tag = soup.find("div", class_="pagination")
                        if html_tag.find("li", class_="last"):
                            tag = html_tag.find("li", class_="last")
                            pages = int(tag.find("a")["href"].split("desc/")[1].strip("/"))
                        else:
                            pages = 1
                    else:
                        pages = 1
                    # Finding all the mentioned elements from webpage.
                    table = soup.find("table", class_="table-list table table-responsive table-striped")
                    df = Tvsources().visual_tables(table)
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
                    index_list.append(len(df_table.index.tolist())+1)
                    name_list.append("Previous Page")
                    link_list.append(page_url)
                    print("0. Next Page")
                    print(df_table)
                    print(f"{len(df_table.index.tolist())+1}. Previous Page")
                    data = Tvsources().user_choice(name_list, link_list, index_list, source)
                    url = data[0]
                    name = data[1]
                    index = Tvsources().page_navigation(name, pages, index)
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
                args = ["aria2c", "--file-allocation=none", "--seed-time=0", "-d", dir, url]
                subprocess.call(args)
                Tvsources().retry(source, search_term, choice)
            except SessionNotCreatedException:
                print("If you are not using android then install from win_linux_requirement.txt file")
            except (requests.exceptions.RequestException, WebDriverException, TimeoutException):
                print("Network Error!")
            except TypeError:
                pass
            except AttributeError:
                print("Could not find any thing :(")
            except KeyboardInterrupt:
                print("Cancelled by user.")
############################################################################
    class Documentary:
        def documentary(self):
            source = "documentary"
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
                for i, name in zip(index_list, name_list):
                    print(f"{i}. {name}")
                data = Tvsources().user_choice(name_list, link_list, index_list, source)
                web_url = data[0]
                page_url = f"{web_url}/page/"
                while True:
                    driver.get(web_url) 
                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    if Tvsources().exists(element = ".numeric-nav"):
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
                    index_list.append(i+1)
                    name_list.append("Previous Page")
                    link_list.append(page_url)
                    for i, name in zip(index_list, name_list):
                        print(f"{i}. {name}")
                    data = Tvsources().user_choice(name_list, link_list, index_list, source)
                    url = data[0]
                    name = data[1]
                    index = Tvsources().page_navigation(name, pages, index)
                    web_url = url + str(index) + "/"
                    if name != "Next Page" and name != "Previous Page":
                        break
                # Sending get request to the website.
                driver.get(url)
                # Parsering the response with "BeauitifulSoup".
                soup = BeautifulSoup(driver.page_source, "html.parser")
                # Finding all the mentioned elements in the webpage.
                html_tag = soup.find("meta", attrs={"itemprop" : "embedUrl"})
                if "https://www.dailymotion" in html_tag["content"].split(".com")[0]:
                    url = html_tag["content"].replace("/embed", "")
                else:
                    url = html_tag["content"]
                args = ["yt-dlp", url]
                subprocess.call(args)
            except SessionNotCreatedException:
                print("If you are not using android then install from win_linux_requirement.txt file")
            except (requests.exceptions.RequestException, WebDriverException, TimeoutException):
                print("Network Error!")
            except TypeError:
                pass
            except AttributeError:
                print("Could not find any thing :(")
            except KeyboardInterrupt:
                print("Cancelled by user.")
############################################################################
