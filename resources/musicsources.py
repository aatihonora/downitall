'''Music Sources'''

#Importing necessary modules
import os
import re
import subprocess
import sys
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
    '''Music functions'''
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
        print("\n")
        for key, value in name_dict.items():
            print(f'{key}. {value}')
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
    def download(self, name, url):
        # Making the folder and opening it
        folder = "Music"
        if not os.path.isdir(folder):
            os.mkdir(folder)
            os.chdir(folder)
        else:
            os.chdir(folder)
        # Downloading the file with wget as it is fast and has its own progress bar.
        args = ['wget', '-O', name, f"{url}"]
        subprocess.call(args)
        print("\nDownload Complete.")
############################################################################
    # Defining the function for retrying the user_choice function.
    def retry(self, source, search_term):
        # Using match case argument to see which class called the function.
        answer = questionary.select("Do you want to download another file? ", choices=["Yes", "No"]).ask()
        if answer == "Yes":
            if source == "lightaudio":
                Musicsources().Light_audio().lightaudio(search_term)
            elif source == "bombmusic":
                Musicsources().Bomb_music().bombmusic(search_term)
            else:
                Musicsources().Player_fm().player(search_term)
############################################################################
    class Light_audio:
        def lightaudio(self,search_term):
            # Declaring function level variables.
            source = "lightaudio"
            label = "paged"
            index = 1
            # Making search term better for url through regex.
            term = re.sub("\W", "+", search_term)
            # Url to access webpage.
            web_url = f"https://lightaudio.ru/mp3/{term}"
            # Url to be used for page navigation.
            page_url = f"https://lightaudio.ru/mp3/{term}/"
            # Url to access the base website
            base_url = "https:"
            try:
                while True:
                    # Sending request to the webpage.
                    driver.get(web_url)
                    # Getting html page with BeautifulSoup module
                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    # Checking weather the element exists.
                    if Musicsources().exists(element = ".pagination"):
                        html_tag = soup.find("div", class_="pagination")
                        # Finding the last td tag and getting its text which is the number of last page and converting it into integer.
                        pages = int(re.sub("\W+", "", html_tag.find_all("a")[-1].getText()))
                    else:
                        pages = 1
                    # Finding all the mentioned elements from webpage.
                    html_tag = soup.find_all("a", class_="down")
                    index_list = []
                    name_list = []
                    link_list = []
                    # Finding the links and making link list.
                    name_list.append("Next Page")
                    link_list.append(page_url)
                    index_list.append(0)
                    for i, links in enumerate(html_tag, start=1):
                        index_list.append(i)
                        name_list.append(links["title"].split("«")[1].replace("»", "").strip())
                        link_list.append(base_url + links["href"].split("?d")[0])
                    name_list.append("Previous Page")
                    link_list.append(page_url)
                    index_list.append(i+1)
                    # Calling the user choice function.
                    data = Musicsources().user_choice(name_list, link_list, index_list, label)
                    url = data[0]
                    name = data[1]
                    index = Musicsources().page_navigation(name, pages, index)
                    web_url = url + str(index)
                    if name != "Next Page" and name != "Previous Page":
                        break
                name = data[1] + ".mp3"
                Musicsources().download(name, url)
                Musicsources().retry(source, search_term)
            except SessionNotCreatedException:
                print("\nIf you are not using android then install from win_linux_requirement.txt file")
            except (requests.exceptions.RequestException, WebDriverException, TimeoutException):
                print("\nNetwork Error!")
            except TypeError as e:
                print("\n", e)
            except (IndexError, AttributeError, UnboundLocalError):
                print("\nCould not find any thing :(")
            except KeyboardInterrupt:
                print("\n\nCancelled by user.")
############################################################################
    class Bomb_music:
        def bombmusic(self,search_term):
            # Declaring function level variables.
            source = "bombmusic"
            label = "no_page"
            # Making search term better for url through regex.
            term = re.sub("\W", "+", search_term)
            # Url to access webpage.
            web_url = f"https://bomb-music.ru/tracks/{term}/"
            # Url to access the base website
            base_url = "https:"
            try:
                # Sending request to the webpage.
                driver.get(web_url)
                # Getting html page with BeautifulSoup module
                soup = BeautifulSoup(driver.page_source, "html.parser")
                # Finding all the mentioned elements from webpage.
                html_tag = soup.find_all("a", class_="link", onclick=True)
                html_tag_name = soup.find_all("a", class_="trackLink")
                index_list = []
                name_list = []
                link_list = []
                # Finding the links and making link list.
                for i, links in enumerate(html_tag, start=1):
                    index_list.append(i)
                    link_list.append(base_url + links["href"])
                for names in html_tag_name:
                    name_list.append(names.text.strip())
                # Calling the user choice function.
                data = Musicsources().user_choice(name_list, link_list, index_list, label)
                url = data[0]
                name = data[1] + ".mp3"
                Musicsources().download(name, url)
                Musicsources().retry(source, search_term)
            except SessionNotCreatedException:
                print("\nIf you are not using android then install from win_linux_requirement.txt file")
            except (requests.exceptions.RequestException, WebDriverException, TimeoutException):
                print("\nNetwork Error!")
            except TypeError as e:
                print("\n", e)
            except (IndexError, AttributeError, UnboundLocalError):
                print("\nCould not find any thing :(")
            except KeyboardInterrupt:
                print("\n\nCancelled by user.")
############################################################################
    class Player_fm:
        def player(self,search_term):
            # Declaring function level variables.
            source = "player_fm"
            label = "next_only"
            # Making search term better for url through regex.
            term = re.sub("\W", "+", search_term)
            # Url to access webpage.
            web_url = f"https://player.fm/search/{term}"
            # Url to access the base website
            base_url = "https://player.fm"
            try:
                # Sending request to the webpage.
                driver.get(web_url)
                index_list = []
                name_list = []
                link_list = []
                # Finding the links and making link list.
                index_list.append(0)
                name_list.append("Next Page")
                link_list.append("")
                while True:
                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    # Finding all the mentioned elements from webpage.
                    html_tag = soup.find_all(["h3", "h2"], class_="title")
                    for i, links in enumerate(html_tag, start=1):
                        link = links.find("a")
                        index_list.append(i)
                        name_list.append(link.text.strip())
                        link_list.append(base_url + link["href"].strip())
                    # Calling the user choice function.
                    data = Musicsources().user_choice(name_list, link_list, index_list, label)
                    url = data[0]
                    name = data[1]
                    if name == "Next Page":
                        scroll_amount = 1000
                        driver.execute_script(f"window.scrollBy(0, {scroll_amount})")
                        time.sleep(2)
                    else:
                        break
                driver.get(url)
                index_list = []
                name_list = []
                link_list = []
                index_list.append(0)
                name_list.append("Next Page")
                link_list.append("")
                while True:
                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    html_tag = soup.find_all("main")[3]
                    html_tag_name = html_tag.find_all("h3", class_="title") 
                    html_tag_link = html_tag.find_all("a", class_="normal action playable round-button info-right")
                    for i, tag in enumerate(html_tag_name, start=1):
                        for names in tag.find_all("a"):
                            index_list.append(i)
                            name_list.append(names.text.strip())
                    for links in html_tag_link:
                        link_list.append(links["href"])
                    data = Musicsources().user_choice(name_list, link_list, index_list, label)
                    url = data[0]
                    name = data[1] 
                    if name == "Next Page":
                        scroll_amount = 1000
                        driver.execute_script(f"window.scrollBy(0, {scroll_amount})")
                        time.sleep(2)
                    else:
                        name = re.sub("\W", "_", data[1]) + ".mp3"
                        break
                Musicsources().download(name, url)
                Musicsources().retry(source, search_term)
            except SessionNotCreatedException:
                print("\nIf you are not using android then install from win_linux_requirement.txt file")
            except (requests.exceptions.RequestException, WebDriverException, TimeoutException):
                print("\nNetwork Error!")
            except TypeError as e:
                print("\n", e)
            except (IndexError, AttributeError, UnboundLocalError):
                print("\nCould not find any thing :(")
            except KeyboardInterrupt:
                print("\n\nCancelled by user.")
############################################################################
