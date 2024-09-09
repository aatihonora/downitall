'''Anime Sources'''

#Importing necessary modules
import os
import re
import subprocess

import gdown
import pandas as pd
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

class Animesources:
    '''Anime functions'''
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
                clean_cell = re.sub("\s+", " ", cell_info)
                row_data.append(clean_cell[:30])
            data.append(row_data)
        # Creating a pandas dataframe
        df = pd.DataFrame(data)
        pd.set_option('display.max_rows', None)
        return df
############################################################################
    # Defining the function for player to choose the index.
    def user_choice(self, name_list, link_list, index_list, page_url):
        # Appendind data for next and previous page.
        name_list.append("Next Page")
        link_list.append(page_url)
        index_list.append(0)
        name_list.append("Previous Page")
        link_list.append(page_url)
        index = len(index_list)
        index_list.append(index)
        # Creating two dictionary that take key as index and value as items from "link_list" and "name_list" respectively.
        url_dict = {index_list[i]: link_list[i] for i in range(len(link_list))}
        name_dict = {index_list[i]: name_list[i] for i in range(len(name_list))}
        try:
            # If statement in case no manga/chapter was found.
            if not link_list:
                print(f'Sorry could not found anything :(!')
            else:
                # Matching the user selection with "urls_dict" dictionary to get its value.
                selection = int(input(f"\n0 for Next Page | {index} for Previous Page\n\nSelect the index number: "))
                if selection in url_dict:
                    # Getting the name and link by matching the index number from dictionaries.
                    link = f"{url_dict[selection]}"
                    name = f"{name_dict[selection]}"
                    print("Fetching, please wait...")
                    subprocess.call(["clear"])
                    return link, name
                else:
                    raise ValueError
        except ValueError:
            print("Invalid integer. The number must be in the range.")
############################################################################
    def no_page(self, name_list, link_list, index_list):
        url_dict = {index_list[i]: link_list[i] for i in range(len(link_list))}
        name_dict = {index_list[i]: name_list[i] for i in range(len(name_list))}
        # Making UI to get user input from name_list.
        for key, value in enumerate(name_list, start=1):
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
                    subprocess.call(["clear"])
                    return link, name
                else:
                    raise ValueError
        except ValueError:
            print("Invalid integer. The number must be in the range.")
############################################################################
    def download(self, anime_name, url):
        # Making the folder and opening it
        anime = re.sub('[^a-z,0-9]', '_', anime_name, flags=re.IGNORECASE)
        if not os.path.isdir(anime):
            os.mkdir(anime)
            os.chdir(anime)
        else:
            os.chdir(anime)
        # Downloading the file with wget as it is fast and has its own progress bar.
        args = ['wget', url]
        subprocess.call(args)
        print("Download Complete.")
############################################################################
    # Defining the function for retrying the user_choice function.
    def retry(self, source, search_term, choice):
        # Using match case argument to see which class called the function.
        match input("\n1. Continue \n2. Exit\n\nEnter the index: "):
            case "1":
                if source == "kayoanime":
                    Animesources().Kayoanime().kayoanime_search(search_term, choice)
                if source == "tokyoinsider":
                    Animesources().Tokyoinsider().tokyoinsider_search(search_term, choice)
                else:
                    Animesources().Nyaa().nyaa_search(search_term)
            case "2":
                pass
            case _:
                pass
############################################################################
    class Kayoanime:
        def kayoanime_search(self,search_term, choice):
            source = "kayoanime"
            if choice == 1:
                search_type = "?s="
            elif choice == 2:
                search_type = "series/"
            else:
                search_type = "ongoing-animes/"
            # Url to access the searching.
            if choice == 1:
                web_url = f"https://kayoanime.com/{search_type}{search_term}"
            else:
                web_url = f"https://kayoanime.com/{search_type}"
            page_url = web_url
            try:
                # Sending request to the webpage.
                driver.get(web_url)
                # Getting html page with BeautifulSoup module
                soup = BeautifulSoup(driver.page_source, "html.parser")
                # Finding all the mentioned elements from webpage.
                html_tag = soup.find_all("a", class_="post-thumb", attrs={"aria-label" : True})
                index_list = []
                name_list = []
                link_list = []
                for i, links in enumerate(html_tag, start=1):
                    index_list.append(i)
                    name_list.append(links["aria-label"].strip())
                    link_list.append(links["href"])
                data = Animesources().no_page(name_list, link_list, index_list)
                url = data[0]
                # Sending get request to the "manga_link" website.
                driver.get(url)
                # Parsering the response with "BeauitifulSoup".
                soup = BeautifulSoup(driver.page_source, "html.parser")
                # Finding all the "a" elements in the webpage.
                html_tag = soup.find("a", target="_blank")
                url = html_tag["href"].split("?")[0]
                gdown.download_folder(url)
                Animesources().retry(source, search_term, choice)
            except SessionNotCreatedException:
                print("If you are not using android then install from win_linux_requirement.txt file")
            except (requests.exceptions.RequestException, WebDriverException, TimeoutException):
                print("Network Error!")
            except TypeError:
                pass
            except (RuntimeError, gdown.exceptions.FileURLRetrievalError, gdown.exceptions.FolderContentsMaximumLimitError, PermissionError):
                print("Google file is either private or unavilable")

    class Tokyoinsider:
        def tokyoinsider_search(self, search_term, choice):
            # Declaring function level variables.
            source = "tokyoinsider"
            index = 1
            # Making search term better for url through regex.
            term = re.sub("\W", "+", search_term)
            # Checking weather search if for title or author/
            if choice == 1:
                search_type = "&s=completed"
            else:
                search_type = "&s=airing"
            # Url to access the website.
            web_url = f"https://www.tokyoinsider.com/anime/search?k={term}{search_type}"
            # Url to be used for page navigation.
            page_url = web_url + "&start="
            # Url to access the base website
            base_url = "https://www.tokyoinsider.com"
            try:
                while True:
                    # Sending request to the webpage.
                    print(web_url)
                    driver.get(web_url)
                    # Getting html page with BeautifulSoup module
                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    # Checking weather the element exists.
                    if Animesources().exists(element = ".pager"):
                        div_tag = soup.find("div", class_="pager")
                        # Finding the last td tag and getting its text which is the number of last page and converting it into integer.
                        pages = int(div_tag.find_all("a", class_=None)[-1].getText())
                    else:
                        pages = 1
                    # Finding all the mentioned elements from webpage.
                    table = soup.find("table", attrs={"width" : "100%", "border" : "0", "cellspacing" : "0", "cellpadding" : "3"})
                    # Calling the table function.
                    df = Animesources().visual_tables(table)
                    # Selecting columns that user can see.
                    df_table = df.iloc[:, [1]]
                    # Making table index start from 1.
                    df_table.index += 1
                    print(df_table)
                    # Converting index column into index list.
                    index_list = df_table.index.tolist()
                    name_list = df[df.columns[1]].values.tolist()
                    link_list = []
                    # Finding the links and making link list.
                    html_tag = soup.find_all("a", title=True, attrs={"style" : "display: block"})
                    for links in html_tag:
                        link_list.append(base_url + links["href"])
                    # Calling the user choice function.
                    data = Animesources().user_choice(name_list, link_list, index_list, page_url)
                    url = data[0]
                    name = data[1]
                    index = Animesources().page_navigation(name, pages, index)
                    if pages == 1:
                        web_url = url + "0"
                    else:
                        web_url = url + str(index*20)
                    if name != "Next Page" and name != "Previous Page":
                        # Sending get request to the "manga_link" website.
                        driver.get(url)
                        # Parsering the response with "BeauitifulSoup".
                        soup = BeautifulSoup(driver.page_source, "html.parser")
                        # Finding all the "a" elements in the webpage.
                        html_tag = soup.find_all(
                                "a", class_="download-link"
                        )
                        index_list = []
                        name_list = []
                        link_list = []
                        for i, links in enumerate(html_tag, start=1):
                            index_list.append(i)
                            name_list.append(links.text.strip())
                            link_list.append(base_url + links["href"])
                        name_list.reverse()
                        link_list.reverse()
                        # Using core method as function to get rid of repeating the same lines.
                        data = Animesources().no_page(name_list, link_list, index_list)
                        url = data[0]
                        # Sending request with selenium webdriver.
                        driver.get(url)
                        # Parsering the response with "BeauitifulSoup".
                        soup = BeautifulSoup(
                            driver.page_source, "html.parser"
                        )
                        # Getting the working download link from html webpage.
                        html_tag = soup.find_all("a", href=lambda t: t and "media" in t)
                        index_list = []
                        name_list = []
                        link_list = []
                        for i, links in enumerate(html_tag, start=1):
                            index_list.append(i)
                            name_list.append(links.text.strip())
                            link_list.append(links["href"]) 
                        name_list.reverse()
                        link_list.reverse()
                        data = Animesources().no_page(name_list, link_list, index_list)
                        url = data[0]
                        Animesources().download(name, url)
                        print("\nDownload Complete.")
                        break
            except SessionNotCreatedException:
                print("If you are not using android then install from win_linux_requirement.txt file")
            except (requests.exceptions.RequestException, WebDriverException, TimeoutException):
                print("Network Error!")
            except TypeError:
                pass

    class Nyaa:
        def nyaa_search(self, search_term):
            source = "nyaa"
            index = 1
            term = re.sub("\W", "+", search_term)
            # Url to access the searching.
            web_url = f"https://nyaa.si/?q={term}&f=0&c=1_2&s=seeders&o=desc"
            page_url = f"https://nyaa.si/?q={term}&f=0&c=1_2&s=seeders&o=desc&p="
            # Url to access the base website
            base_url = "https://nyaa.si"
            try:
                while True:
                    # Sending request to the webpage.
                    driver.get(web_url)
                    # Getting html page with BeautifulSoup module
                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    if Animesources().exists(element = ".pagination"):
                        html_tag = soup.find("ul", class_="pagination")
                        pages = int(html_tag.find_all("li", class_=None)[-1].getText().strip())
                    else:
                        pages = 1
                    # Finding all the mentioned elements from webpage.
                    table = soup.find("table", class_="table table-bordered table-hover table-striped torrent-list")
                    df = Animesources().visual_tables(table)
                    df_table = df.iloc[:, [1, 3]]
                    df_table.index += 1
                    print(df_table)
                    index_list = df_table.index.tolist()
                    name_list = df[df.columns[1]].values.tolist()
                    link_list = []
                    td_tag = soup.find_all("td", colspan="2")
                    for a_html in td_tag:
                        for links in a_html.find_all("a", title=True, class_=None, href=True):
                            link_list.append(base_url + links["href"])
                    data = Animesources().user_choice(name_list, link_list, index_list, page_url)
                    url = data[0]
                    name = data[1]
                    index = Animesources().page_navigation(name, pages, index)
                    web_url = url + str(index)
                    if name != "Next Page" and name != "Previous Page":
                        break
                driver.get(url)
                # Parsering the response with "BeauitifulSoup".
                soup = BeautifulSoup(driver.page_source, "html.parser")
                # Finding all the "a" elements in the webpage.
                html_tag = soup.find(
                        "a", class_="card-footer-item"
                )
                driver.quit()
                dir = os.getcwd()
                url = html_tag["href"]
                args = ["aria2c", "--file-allocation=none", "--seed-time=0", "-d", dir, url]
                subprocess.call(args)
                Animesources().retry(source, search_term, choice="")
            except SessionNotCreatedException:
                print("If you are not using android then install from win_linux_requirement.txt file")
            except (requests.exceptions.RequestException, WebDriverException, TimeoutException):
                print("Network Error!")
            except TypeError:
                pass
