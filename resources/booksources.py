'''Book Sources'''

#Importing necessary modules
import os
import platform
import re
import shutil
import subprocess
import time
import webbrowser

import pandas as pd
import questionary
import requests
import urllib3.exceptions
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import (NoSuchElementException,
                                        SessionNotCreatedException,
                                        TimeoutException, WebDriverException)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from tqdm.auto import tqdm

# Global variables.
# Selenium Chrome options to lessen the memory usage.
options = webdriver.ChromeOptions()
options.add_experimental_option('prefs',  {
    "download.default_directory": os.getcwd(),
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True
    }
)
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

class Booksources:
    '''Book methods'''
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
    def user_choice(self, name_list, link_list, index_list):
        # Appendind data for next and previous page.
        # Creating two dictionary that take key as index and value as items from "link_list" and "name_list" respectively.
        url_dict = {index_list[i]: link_list[i] for i in range(len(link_list))}
        name_dict = {index_list[i]: name_list[i] for i in range(len(name_list))}
        try:
            # If statement in case no manga/chapter was found.
            if len(link_list) == 2 :
                print(f'Sorry could not found anything :(!')
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
    def download(self, name, url):
        # Reformatting the book name to a standard name and sending a request to server with connection as active.
        book_name = re.sub('[^a-z,0-9.]', '_', name, flags=re.IGNORECASE)
        with requests.get(url, stream = True) as res:
            # Checking header to get the content length, in bytes.
            total_length = int(res.headers.get("Content-Length"))
            # Checking if request was valid.
            if res.status_code == 200:
                # Implement progress bar via tqdm.
                with tqdm.wrapattr(res.raw, "read", total=total_length, desc="")as raw:
                    # Downloading image via shutil.
                    with open(book_name,'wb') as f:
                        shutil.copyfileobj(raw, f)
                print('Book sucessfully Downloaded: ',book_name)
            else:
                print('Book couldn\'t be retrieved')
############################################################################
    # Defining the function for retrying the user_choice function.
    def retry(self, source, search_term, choice):
        # Using match case argument to see which class called the function.
        answer = questionary.select("Do you want to download another file? ", choices=["Yes", "No"]).ask()
        if answer == "Yes":
            if source == "libgen":
                Booksources().Libgen().libgen_search(search_term, choice)
            elif source == "annasarchive":
                Booksources().Annas_Archive().annas_archive_search(search_term, choice)
            else:
                Booksources().Torrent().torrent_search(search_term)
############################################################################
    class Libgen:
        def libgen_search(self, search_term, choice):
            # Declaring function level variables.
            source = "libgen"
            index = 1
            # Making search term better for url through regex.
            term = re.sub("\W", "+", search_term)
            # Checking weather search is for title or author.
            if choice == 1:
                search_type = "t"
            else:
                search_type = "a"
            # Url to access the website.
            web_url = f"https://libgen.li/index.php?req={term}&columns%5B%5D={search_type}&objects%5B%5D=f&topics%5B%5D=l&topics%5B%5D=f&res=50&filesuns=all"
            # Url to be used for page navigation.
            page_url = f"https://libgen.li/index.php?req={term}&columns%5B%5D={search_type}&objects%5B%5D=f&topics%5B%5D=l&topics%5B%5D=f&res=50&filesuns=all&page="
            # Url to access the base website
            base_url = "https://libgen.li/"
            try:
                while True:
                    # Sending request to the webpage.
                    driver.get(web_url)
                    # Getting html page with BeautifulSoup module
                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    # Checking weather the element exists.
                    if Booksources().exists(element = ".paginator.fullsize"):
                        div_tag = soup.find("div", class_="paginator fullsize")
                        # Finding the last td tag and getting its text which is the number of last page and converting it into integer.
                        pages = int(div_tag.find_all("td", colspan=None)[-1].getText())
                    else:
                        pages = 1
                    # Finding all the mentioned elements from webpage.
                    table = soup.find("table", id="tablelibgen")
                    # Calling the table function.
                    df = Booksources().visual_tables(table)
                    # Selecting columns that user can see.
                    df_table = df.iloc[:, [0, 6, 7]]
                    # Making table index start from 1.
                    df_table.index += 1
                    # Converting index column into index list.
                    index_list = df_table.index.tolist()
                    name_list = []
                    # Converting name and extention columns into list and looping them together by using zip.
                    for name, extention in zip(df[df.columns[0]].values.tolist(), df[df.columns[7]].values.tolist()):
                        name_list.append(f"{name}.{extention}")
                    link_list = []
                    # Finding the links and making link list.
                    html_tag = soup.find_all("a", attrs={"data-original-title": "libgen"})
                    for links in html_tag:
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
                    # Calling the user choice function.
                    data = Booksources().user_choice(name_list, link_list, index_list)
                    url = data[0]
                    name = data[1]
                    index = Booksources().page_navigation(name, pages, index)
                    web_url = url + str(index)
                    if name != "Next Page" and name != "Previous Page":
                        break
                # Sending get request to the website.
                driver.get(url)
                # Parsering the response with "BeauitifulSoup".
                soup = BeautifulSoup(driver.page_source, "html.parser")
                # Finding all the mentioned elements in the webpage.
                td_html = soup.find("td", attrs={"align": "center", "valign": "top", "bgcolor": "#A9F5BC"})
                html_tag = td_html.find("a") 
                url = base_url + html_tag["href"]
                Booksources().download(name, url)
                Booksources().retry(source, search_term, choice)
            except SessionNotCreatedException:
                print("If you are not using android then install from win_linux_requirement.txt file")
            except (requests.exceptions.RequestException, WebDriverException, TimeoutException):
                print("Network Error!")
            except (TypeError, urllib3.exceptions.ProtocolError):
                pass
            except AttributeError:
                print(f"No book with title {search_term} found :(")
            except KeyboardInterrupt:
                print("Cancelled by user.")
############################################################################
    class Annas_Archive:
        def annas_archive_search(self,search_term, choice):
            source = "annas_archive"
            index = 1
            # Making search term better for url through regex.
            term = re.sub("\W", "+", search_term)
            # Checking weather search is for title or author.
            if choice == 1:
                search_type = "title"
            else:
                search_type = "author"
            # Url to access the searching.
            web_url = f"https://annas-archive.org/search?index=&page=1&desc=1&termtype_1={search_type}&termval_1={term}&content=book_nonfiction&content=book_fiction&content=book_unknown&sort="
            # Url to be used for page navigation.
            page_url = f"https://annas-archive.org/search?index=&desc=1&termtype_1={search_type}&termval_1={term}&content=book_nonfiction&content=book_fiction&content=book_unknown&sort=&page="
            # Url to access the base website
            base_url = "https://annas-archive.org"
            try:
                while True:
                    # Sending request to the webpage.
                    driver.get(web_url)
                    time.sleep(2)
                    # Scrolling to bottom to get all the elements.
                    elem = driver.find_element(By.TAG_NAME, "html")
                    elem.send_keys(Keys.END)
                    time.sleep(2)
                    # Getting html page with BeautifulSoup module
                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    # Checking weather the element exists.
                    if Booksources().exists(element = ".isolate.inline-flex.-space-x-px.rounded-md.shadow-sm.text-xs"):
                        div_tag = soup.find("nav", class_="isolate inline-flex -space-x-px rounded-md shadow-sm text-xs")
                        pages = int(div_tag.find_all("a", class_="custom-a relative inline-flex items-center px-2 py-2 font-semibold text-gray-900 ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus:z-20 focus:outline-offset-0")[-1].getText())
                    else:
                        pages = 1
                    # Finding all the mentioned elements from webpage.
                    h3_tag = soup.find_all("h3", class_="max-lg:line-clamp-[2] lg:truncate leading-[1.2] lg:leading-[1.35] text-md lg:text-xl font-bold")
                    # Creating index, name and link list and appending the respective items.
                    index_list = []
                    name_list = []
                    link_list = []
                    index_list.append(0)
                    name_list.append("Next Page")
                    link_list.append(page_url)
                    for i, name in enumerate(h3_tag, start=1):
                        name_list.append(name.text.strip())
                        index_list.append(i)
                    div_tag = soup.find_all("div", class_="h-[125] flex flex-col justify-center")
                    for a_tag in div_tag:
                        for links in a_tag.find_all("a"):
                            link_list.append(base_url + links["href"])
                    index_list.append(i+1)
                    name_list.append("Previous Page")
                    link_list.append(page_url)
                    # Iterating using zip as it lets two list loop together
                    for index_name, name in zip(index_list, name_list):
                        # Printing name with index for user to choose.
                        print(f"{index_name}. {name}")
                    data = Booksources().user_choice(name_list, link_list, index_list)
                    url = data[0]
                    name = data[1]
                    index = Booksources().page_navigation(name, pages, index)
                    web_url = url + str(index)
                    if name != "Next Page" and name != "Previous Page":
                        break
                # Sending get request to the website.
                driver.get(url)
                # Parsering the response with "BeauitifulSoup".
                soup = BeautifulSoup(driver.page_source, "html.parser")
                # Finding all the mentioned elements in the webpage.
                html_tag = soup.find_all("ul", class_="list-inside mb-4 ml-1")[1]
                link = html_tag.find_all("a")[-1]
                url = base_url + link["href"]
                platforms = platform.system()
                if platforms == "Linux":
                    subprocess.Popen(["am", "start", "-n", "com.android.chrome/com.google.android.apps.chrome.Main", url])
                else:
                    webbrowser.open(url, new=2)
                Booksources().retry(source, search_term, choice)
            except SessionNotCreatedException:
                print("If you are not using android then install from win_linux_requirement.txt file")
            except (requests.exceptions.RequestException, WebDriverException, TimeoutException):
                print("Network Error!")
            except TypeError:
                pass
            except FileNotFoundError:
                pass
            except KeyboardInterrupt:
                print("Cancelled by user.")
############################################################################
    class Torrent:
        def torrent_search(self, search_term):
            source = "1337x"
            index = 1
            term = re.sub("\W", "+", search_term)
            # Url to access the searching.
            web_url = f"https://1337x.to/sort-category-search/{term}/Other/seeders/desc/1/"
            page_url = f"https://1337x.to/sort-category-search/{term}/Other/seeders/desc/"
            # Url to access the base website
            base_url = "https://1337x.to"
            try:
                while True:
                    # Sending request to the webpage.
                    driver.get(web_url)
                    # Getting html page with BeautifulSoup module
                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    if Booksources().exists(element = ".pagination"):
                        div_tag = soup.find("div", class_="pagination")
                        if div_tag.find("li", class_="last"):
                            li_tag = div_tag.find("li", class_="last")
                            pages = int(li_tag.find("a")["href"].split("desc/")[1].strip("/"))
                        else:
                            pages = 1
                    else:
                        pages = 1
                    # Finding all the mentioned elements from webpage.
                    table = soup.find("table", class_="table-list table table-responsive table-striped")
                    df = Booksources().visual_tables(table)
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
                    book_tuple = Booksources().user_choice(name_list, link_list, index_list)
                    url = book_tuple[0]
                    name = book_tuple[1]
                    index = Booksources().page_navigation(name, pages, index)
                    web_url = url + str(index) + "/"
                    if name != "Next Page" and name != "Previous Page":
                        break
                # Sending get request to the website.
                driver.get(url)
                # Parsering the response with "BeauitifulSoup".
                book_soup = BeautifulSoup(driver.page_source, "html.parser")
                # Finding all the mentioned elements in the webpage.
                html_tag = book_soup.find("a", id="id1")
                url = html_tag["href"]
                dir = os.getcwd()
                # Calling the aria2c module to download.
                args = ["aria2c", "--file-allocation=none", "--seed-time=0", "-d", dir, url]
                subprocess.call(args)
            except SessionNotCreatedException:
                print("If you are not using android then install from win_linux_requirement.txt file")
            except (requests.exceptions.RequestException, WebDriverException, TimeoutException):
                print("Network Error!")
            except TypeError:
                pass
            except KeyboardInterrupt:
                print("Cancelled by user.")
############################################################################
