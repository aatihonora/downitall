'''Stream Sources'''

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
from ipytv import playlist
from selenium import webdriver
from selenium.common.exceptions import (NoSuchElementException,
                                        SessionNotCreatedException,
                                        TimeoutException, WebDriverException)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

# Global variables.
# Selenium Chrome options to lessen the memory usage.
options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--headless=new")
options.add_argument("start-maximized")
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

class Streamsources:
    '''Stream functions'''
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
    def link_check(self, url):
        try:
            res = requests.get(url)
            if res.status_code == 200:
                answer = questionary.select("Select item", choices=["Best", "Worst"]).ask()
                if answer == "Best":
                    quality = "best"
                else: 
                    quality = "worst"
                subprocess.call(["vlc", url, quality])
                return True
            else: 
                print("Dead link")
                return False
        except requests.exceptions.RequestException:
                return False
############################################################################
    # Defining the function for retrying the user_choice function.
    def retry(self):
        # Using match case argument to see which class called the function.
        answer = questionary.select("Do you want to download another file? ", choices=["Yes", "No"]).ask()
        if answer == "Yes":
            # Second question to choose the Website.
            search_term = input("Enter the title of the media you want to Stream: ")
            select = questionary.select("Select item", choices=["Heartive", "Miruro", "Yoyomovies", "Cxtvlive", "IPTV", "Exit"]).ask()
            if select == "Heartive":
                sub_select = questionary.select("Select item", choices=["Search Series", "Search Movies", "Search Live Channels", "Exit"]).ask()
                if sub_select == "Search Series":
                    choice = 1
                    Streamsources().Heartive().heartive(search_term, choice)
                elif sub_select == "Search Movies": 
                    choice = 2
                    Streamsources().Heartive().heartive(search_term, choice)
                elif sub_select == "Search Live Channels":
                    Streamsources().Heartive().heartivetv()
                else:
                    pass
            elif select == "Miruro":
                Streamsources().Miruro().miruro(search_term)
            elif select == "Yoyomovies":
                Streamsources().Yoyomovies().yoyomovies(search_term)
            elif select == "Cxtvlive":
                Streamsources().Cxtvlive().cxtvlive()
            elif select == "IPTV":
                sub_select = questionary.select("Select item", choices=["Global IPTV", "South Asian IPTV", "Exit"]).ask()
                if sub_select == "Global IPTV":
                    choice = 1
                    Streamsources().Iptv().iptv(choice)
                elif sub_select == "South Asian IPTV":
                    choice = 2
                    Streamsources().Iptv().iptv(choice)
                else:
                    pass
            else:
                pass
############################################################################
############################################################################
    class Heartive:
        def heartive(self,search_term, choice):
            # Declaring function level variables.
            label = "no_page"
            if choice == 1:
                search_type = "series"
            else:
                search_type = "movies"
            # Url to access webpage.
            url = f"https://heartive.pages.dev/{search_type}/"
            base_url = "https://heartive.pages.dev"
            try:
                # Sending request to the webpage.
                if choice == 1:
                    driver.get(url)
                    time.sleep(8)
                    elem = driver.find_element(By.TAG_NAME,"input")
                    elem.click()
                    elem.send_keys(search_term)
                    # Getting html page with BeautifulSoup module
                    time.sleep(5)
                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    # Checking weather the element exists.
                    # Finding all the mentioned elements from webpage.
                    html_tag = soup.find_all("a", class_="thumbnail")
                    html_tag_name = soup.find_all("h3")
                    index_list = []
                    name_list = []
                    link_list = []
                    # Finding the links and making link list.
                    for i, links in enumerate(html_tag, start=1):
                        index_list.append(i)
                        link_list.append(links["href"].replace("..", base_url))
                    for names in html_tag_name:
                        name_list.append(names.text.strip())
                    # Calling the user choice function.
                    data = Streamsources().user_choice(name_list, link_list, index_list, label)
                    url = data[0]
                    driver.get(url)
                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    html_tag = soup.find_all("a", class_="thumbnail")
                    html_tag_name = soup.find_all("h3")
                    index_list = []
                    name_list = []
                    link_list = []
                    # Finding the links and making link list.
                    for i, links in enumerate(html_tag, start=1):
                        index_list.append(i)
                        link_list.append(links["href"].replace("..", base_url))
                    for names in html_tag_name:
                        name_list.append(names.text.strip())
                    # Calling the user choice function.
                    data = Streamsources().user_choice(name_list, link_list, index_list, label)
                    url = data[0]
                if choice == 2:
                    driver.get(url)
                    time.sleep(5)
                    elem = driver.find_element(By.TAG_NAME,"input")
                    elem.click()
                    elem.send_keys(search_term)
                    # Getting html page with BeautifulSoup module
                    time.sleep(3)
                else:
                    driver.get(url)
                    time.sleep(5)
                soup = BeautifulSoup(driver.page_source, "html.parser")
                html_tag = soup.find_all("div", class_="videoItem")
                html_tag_name = soup.find_all("h3")
                index_list = []
                name_list = []
                link_list = []
                # Finding the links and making link list.
                for names in html_tag_name:
                    name_list.append(names.text.strip())
                for i, links in enumerate(html_tag, start=1):
                    index_list.append(i)
                    link_list.append(i)
                # Calling the user choice function.
                data = Streamsources().user_choice(name_list, link_list, index_list, label)
                url = int(data[0]) - 1
                driver.find_elements(By.CSS_SELECTOR,".videoItem")[url].click()
                time.sleep(10)
                select = Select(driver.find_element(By.TAG_NAME, "select"))
                answer = questionary.select("Select item", choices=["Vidsrc", "Vidlink"]).ask()
                if answer == "Vidsrc":
                    select.select_by_value('vidsrc.rip')
                else:
                    select.select_by_value('vidlink')
                time.sleep(5)
                soup = BeautifulSoup(driver.page_source, "html.parser")
                html_tag = soup.find_all("iframe")[0]
                url = html_tag["src"]
                driver.get(url)
                time.sleep(5)
                soup = BeautifulSoup(driver.page_source, "html.parser")
                html_tag = soup.find_all("source")[0]
                url = html_tag["src"]
                Streamsources().link_check(url)
                Streamsources().retry()
            except SessionNotCreatedException:
                print("\nIf you are not using android then install from win_linux_requirement.txt file")
            except (requests.exceptions.RequestException, WebDriverException, TimeoutException):
                print("\nNetwork Error!")
            except TypeError as e:
                pass
            except (IndexError, AttributeError, UnboundLocalError):
                print("\nCould not find any thing :(")
            except KeyboardInterrupt:
                print("\n\nCancelled by user.")
############################################################################        
        def heartivetv(self):
            # Declaring function level variables.
            label = "no_page"
            # Url to access webpage.
            web_url = "https://heartive.pages.dev/live/"
            base_url = "https://heartive.pages.dev"
            try:
                # Sending request to the webpage.
                driver.get(web_url)
                time.sleep(5)
                soup = BeautifulSoup(driver.page_source, "html.parser")
                select = Select(driver.find_element(By.TAG_NAME, "select"))
                html_tag = soup.find_all("select", id="country-select")[0]
                tag = html_tag.find_all("option", value=True)
                index_list = []
                name_lists = []
                link_lists = []
                # Finding the links and making link list.
                for i, links in enumerate(tag, start=1):
                    index_list.append(i)
                    name_lists.append(links.text.strip())
                    link_lists.append(links["value"])
                name_list = list(dict.fromkeys(name_lists))
                link_list = list(dict.fromkeys(link_lists))
                # Calling the user choice function.
                data = Streamsources().user_choice(name_list, link_list, index_list, label)
                url = data[0]
                select.select_by_value(url)
                time.sleep(8)
                soup = BeautifulSoup(driver.page_source, "html.parser")
                html_tag = soup.find_all("select", id="stream-select")[0]
                tag = html_tag.find_all("option", value=True)
                index_list = []
                name_list = []
                link_list = []
                # Finding the links and making link list.
                for i, links in enumerate(tag, start=1):
                    index_list.append(i)
                    name_list.append(links.text.strip())
                    link_list.append(links["value"])
                # Calling the user choice function.
                while True:
                    data = Streamsources().user_choice(name_list, link_list, index_list, label)
                    url = data[0]
                    if Streamsources().link_check(url) == True:
                        break
                Streamsources().retry()
            except SessionNotCreatedException:
                print("\nIf you are not using android then install from win_linux_requirement.txt file")
            except (requests.exceptions.RequestException, WebDriverException, TimeoutException):
                print("\nNetwork Error!")
            except TypeError as e:
                pass
            except (IndexError, AttributeError, UnboundLocalError):
                print("\nCould not find any thing :(")
            except KeyboardInterrupt:
                print("\n\nCancelled by user.")
############################################################################
############################################################################
    class Miruro:
        def miruro(self,search_term):
            # Declaring function level variables.
            label = "next_only"
            index = 1
            # Url to access webpage.
            web_url = f"https://www.miruro.tv/search?query={search_term}&sort=POPULARITY_DESC&type=ANIME"
            base_url = "https://www.miruro.tv"
            try:
                # Sending request to the webpage.
                driver.get(web_url)
                time.sleep(6)
                while True:
                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    # Checking weather the element exists.
                    # Finding all the mentioned elements from webpage.
                    html_tag = soup.find_all("a", title=True, href=lambda t: t and "watch" in t)
                    index_list = []
                    name_list = []
                    link_list = []
                    # Finding the links and making link list.
                    index_list.append(0)
                    name_list.append("Next Page")
                    link_list.append("")
                    for i, links in enumerate(html_tag, start=1):
                        index_list.append(i)
                        name_list.append(links["title"].strip())
                        link_list.append(base_url + links["href"])
                    # Calling the user choice function.
                    data = Streamsources().user_choice(name_list, link_list, index_list, label)
                    url = data[0]
                    name = data[1]
                    if name == "Next Page":
                        scroll_amount = 1000
                        driver.execute_script(f"window.scrollBy(0, {scroll_amount})")
                        time.sleep(2)
                    else:
                        break
                driver.get(url)
                time.sleep(10)
                soup = BeautifulSoup(driver.page_source, "html.parser")
                select_list = []
                select_name = []
                html_tag = soup.find_all("select")[0]
                tag = html_tag.find_all("option")
                for values in tag:
                    select_list.append(values["value"])
                    select_name.append(values.text.strip())
                for i, names in enumerate(select_name, start=1):
                    print(f"{i}. {names}")
                user_input = input("Select an index: ")
                select = Select(driver.find_element(By.TAG_NAME, "select")) 
                select.select_by_value(f'{select_list[int(user_input)-1]}')
                time.sleep(5)
                soup = BeautifulSoup(driver.page_source, "html.parser")
                html_tag = soup.find_all("div", id="episodes-list-container")[0]
                html_tag_name = html_tag.find_all("button")
                index_list = []
                name_list = []
                link_list = []
                # Finding the links and making link list.
                label = "no_page"
                for i, names in enumerate(html_tag_name, start=1):
                    index_list.append(i)
                    name_list.append(names["title"].strip())
                    for links in names.find_all("a"):
                        link_list.append(base_url + links["href"])
                # Calling the user choice function.
                data = Streamsources().user_choice(name_list, link_list, index_list, label)
                url = data[0]
                driver.get(url)
                time.sleep(5)
                soup = BeautifulSoup(driver.page_source, "html.parser")
                html_tag = soup.find_all("source")[0]
                url = html_tag["src"]
                Streamsources().link_check(url)
                Streamsources().retry()
            except SessionNotCreatedException:
                print("\nIf you are not using android then install from win_linux_requirement.txt file")
            except (requests.exceptions.RequestException, WebDriverException, TimeoutException):
                print("\nNetwork Error!")
            except TypeError as e:
                pass
            except (IndexError, AttributeError, UnboundLocalError):
                print("\nCould not find any thing :(")
            except KeyboardInterrupt:
                print("\n\nCancelled by user.")
############################################################################
############################################################################
    class Yoyomovies:
        def yoyomovies(self,search_term):
            # Declaring function level variables.
            label = "next_only"
            index = 1
            # Url to access webpage.
            web_url = f"https://yoyomovies.net/?s={search_term}"
            base_url = "https://yoyomovies.net/"
            try:
                # Sending request to the webpage.
                driver.get(web_url)
                time.sleep(6)
                while True:
                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    # Checking weather the element exists.
                    # Finding all the mentioned elements from webpage.
                    html_tag = soup.find_all("div", class_="poster")
                    index_list = []
                    name_list = []
                    link_list = []
                    # Finding the links and making link list.
                    index_list.append(0)
                    name_list.append("Next Page")
                    link_list.append("")
                    for i, tag in enumerate(html_tag, start=1):
                        index_list.append(i)
                        for links in tag.find_all("a"):
                            name_list.append(re.sub("\W+", " ", links["href"].split("net/")[1]).title())
                            link_list.append(links["href"])
                    # Calling the user choice function.
                    data = Streamsources().user_choice(name_list, link_list, index_list, label)
                    url = data[0]
                    name = data[1]
                    if name == "Next Page":
                        scroll_amount = 1000
                        driver.execute_script(f"window.scrollBy(0, {scroll_amount})")
                        time.sleep(2)
                    else:
                        break
                driver.get(url)
                elem = driver.find_element(By.XPATH, f"//ul[@class='servers']/li[4]").click()
                time.sleep(2)
                soup = BeautifulSoup(driver.page_source, "html.parser")
                html_tag = soup.find_all("a", attrs={"class":["dropdown-item season-item", "dropdown-item season-item active"]})
                select_name = []
                if len(html_tag) >= 2:
                    for values in html_tag:
                        select_name.append(values.text.strip())
                    for i, names in enumerate(select_name, start=1):
                        print(f"{i}. {names}")
                    user_input = int(input("Select an index: ")) - 1
                    driver.find_element(By.CLASS_NAME,"btn.dropdown-toggle").click()
                    elem = driver.find_elements(By.CLASS_NAME,"dropdown-item.season-item")[user_input]
                    elem.click()
                    html_tag = soup.find_all("ul", class_="episodes")[0]
                    tag = html_tag.find_all("li")
                    index_list = []
                    name_list = []
                    link_list = []
                    label = "no_page"
                    # Finding the links and making link list.
                    for i, data in enumerate(tag, start=1):
                        index_list.append(i)
                        link_list.append(i)
                        for names in data.find_all("a"):
                            name_list.append(names.text.strip())
                    # Calling the user choice function.
                    data = Streamsources().user_choice(name_list, link_list, index_list, label)
                    url = int(data[0])
                    elem = driver.find_element(By.XPATH, f"//div[@class='body']/ul[@class='episodes']/li[{url}]").click()
                    time.sleep(2)
                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    html_tag = soup.find_all("iframe")[0]
                    if not "vidlink" in html_tag["src"]:
                        url = re.sub("vidsrc", "vidlink", html_tag["src"])
                    else:
                        url = html_tag["src"]
                    if "player_tv" in html_tag["src"]:
                        driver.get(url)
                        time.sleep(8)
                        soup = BeautifulSoup(driver.page_source, "html.parser")
                        html_tag = soup.find_all("iframe")[0]
                        url = re.sub("&amp;+", "", html_tag["src"]).split("/")[1]
                        driver.get(base_url + url)
                        time.sleep(2)
                elif len(html_tag) == 0:
                    pass
                soup = BeautifulSoup(driver.page_source, "html.parser")
                html_tag = soup.find_all("iframe")[0]
                driver.get(html_tag["src"])
                time.sleep(4)
                soup = BeautifulSoup(driver.page_source, "html.parser")
                html_tag = soup.find_all("source")[0]["src"].split(".m3u8")[0]
                url = html_tag + ".m3u8" 
                Streamsources().link_check(url)
                Streamsources().retry()
            except SessionNotCreatedException:
                print("\nIf you are not using android then install from win_linux_requirement.txt file")
            except (requests.exceptions.RequestException, WebDriverException, TimeoutException):
                print("\nNetwork Error!")
            except TypeError as e:
                pass
            except (IndexError, AttributeError, UnboundLocalError):
                print("\nCould not find any thing :(")
            except KeyboardInterrupt:
                print("\n\nCancelled by user.")
############################################################################
############################################################################
    class Cxtvlive:
        def cxtvlive(self):
            # Declaring function level variables.
            label = "next_only"
            index = 1
            # Url to access webpage.
            web_url = f"https://www.cxtvlive.com/tv/country/united-states"
            try:
                # Sending request to the webpage.
                driver.get(web_url)
                time.sleep(3)
                while True:
                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    # Checking weather the element exists.
                    # Finding all the mentioned elements from webpage.
                    html_tag = soup.find_all("a", class_="m-b-20 btn btn-white btn-block")
                    html_tag_name = soup.find_all("h4", class_="resumoDots p-t-15 p-b-5 no-margin text-center bold")
                    index_list = []
                    name_list = []
                    link_list = []
                    # Finding the links and making link list.
                    index_list.append(0)
                    name_list.append("Next Page")
                    link_list.append("")
                    for i, links in enumerate(html_tag, start=1):
                        index_list.append(i)
                        link_list.append(links["href"])
                    for names in html_tag_name:
                        name_list.append(names.text.strip())
                    # Calling the user choice function.
                    data = Streamsources().user_choice(name_list, link_list, index_list, label)
                    url = data[0]
                    name = data[1]
                    if name == "Next Page":
                        driver.find_element(By.ID, "loadMore").click()
                        time.sleep(2)
                    else:
                        break
                driver.get(url)
                time.sleep(2)
                soup = BeautifulSoup(driver.page_source, "html.parser")
                html_tag = soup.find_all("iframe")[0]
                if not "youtube" in html_tag["src"]:
                    html_tag = soup.find_all("source")[0]
                    url = re.sub("&amp;+", "", html_tag["src"])
                elif not "list" in html_tag["src"] and "youtube" in html_tag["src"]:
                    url = html_tag["src"]
                else:
                    raise IndexError
                Streamsources().link_check(url)
                Streamsources().retry()
            except SessionNotCreatedException:
                print("\nIf you are not using android then install from win_linux_requirement.txt file")
            except (requests.exceptions.RequestException, WebDriverException, TimeoutException):
                print("\nNetwork Error!")
            except TypeError as e:
                pass
            except (IndexError, AttributeError, UnboundLocalError):
                print("\nCould not find any thing :(")
            except KeyboardInterrupt:
                print("\n\nCancelled by user.")
############################################################################
############################################################################
    class Iptv:
        def iptv(self, choice):
            # Declaring function level variables.
            label = "no_page"
            # Url to access webpage.
            if choice == 1:
                web_url = "https://iptv-org.github.io/iptv/languages/eng.m3u"
            else:
                web_url = "https://raw.githubusercontent.com/FunctionError/PiratesTv/main/combined_playlist.m3u"
            try:
                pl = playlist.loadu(web_url)
                # Let's retrieve the first channel in the list
                index_list = []
                name_list = []
                link_list = []
                for i, channel in enumerate(pl, start=1):
                    index_list.append(i)
                    if not "[Not 24/7]" in channel.name and not "[Geo-blocked]" in channel.name:
                        name_list.append(channel.name.strip())
                    if "m3u8" in channel.url or "mpd" in channel.url:
                        link_list.append(channel.url)
                while True:
                    data = Streamsources().user_choice(name_list, link_list, index_list, label)
                    url = data[0]
                    if Streamsources().link_check(url) == True:
                        break
                Streamsources().retry()
            except SessionNotCreatedException:
                print("\nIf you are not using android then install from win_linux_requirement.txt file")
            except (requests.exceptions.RequestException, WebDriverException, TimeoutException):
                print("\nNetwork Error!")
            except TypeError:
                pass
            except (IndexError, AttributeError, UnboundLocalError):
                print("\nCould not find any thing :(")
            except KeyboardInterrupt:
                print("\n\nCancelled by user.")
