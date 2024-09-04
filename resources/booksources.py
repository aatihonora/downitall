'''Book Sources'''

#Importing necessary modules
import os
import re
import shutil
import subprocess
import time

import requests
import urllib3.exceptions
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
        if source == "libgen":
            extension_list = []
            for i, a_html in enumerate(html_tag, start=1):
                for links in a_html.find_all("a", id=True, href=True):
                    link_list.append(baseurl + links["href"].split(".")[1].strip())
                    name_list.append(links.next_element.text)
                    index_list.append(i)
            for td_html in html_tag:
                for extension in td_html.find_all("td", nowrap=True)[2]:
                    extension_list.append(extension.text)
        elif source == "annasarchive":
            for i, links in enumerate(html_tag, start=1):
                link_list.append(baseurl + links["href"])
                for name in links.find("h3"):
                    name_list.append(name.text.strip())
                index_list.append(i)
        elif source == "glodls":
            for i, html_td in enumerate(html_tag, start=1):
                for links in html_td.find_all("a", title=True, href=True):
                    link_list.append(baseurl + links["href"])
                    name_list.append(links.text.strip())
                index_list.append(i)
        elif source == "annasarchive_chapter":
            for i, links in enumerate(html_tag, start=1):
                if "/fast" in links["href"].split("_")[0] or "/slow" in links["href"].split("_")[0]:
                    link_list.append(baseurl + links["href"])
                    name_list.append(links.text.strip())
                    index_list.append(i)
                else:
                    link_list.append(links["href"])
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
        if source == "libgen":
            extension_dict = {index_list[i]: extension_list[i] for i in range(len(extension_list))}

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
                    if source == "libgen":
                        name = f"{name_dict[selection]}.{extension_dict[selection]}"
                    print("Fetching, please wait...")
                    return link, name

                else:
                    raise ValueError
        except ValueError:
            print("Invalid integer. The number must be in the range.")
    def download(self, book_name, url):
        # Making the folder and opening it
        name = re.sub('[^a-z,0-9.]', '_', book_name, flags=re.IGNORECASE)
        with requests.get(url, stream = True) as res:
            # Checking header to get the content length, in bytes.
            total_length = int(res.headers.get("Content-Length"))
            # Checking if request was valid.
            if res.status_code == 200:
                # Implement progress bar via tqdm.
                with tqdm.wrapattr(res.raw, "read", total=total_length, desc="")as raw:
                    # Downloading image via shutil.
                    with open(name,'wb') as f:
                        shutil.copyfileobj(raw, f)
                print('Book sucessfully Downloaded: ',name)
            else:
                print('Book couldn\'t be retrieved')

    def libgen(self,search_term):
        # Url to access the searching.
        url = f"https://libgen.is/search.php?req={search_term}&open=0&res=50&view=simple&phrase=1&column=title"
        # Url to access the base website
        baseurl = "https://libgen.li/ads."
        # Url to access the downloaf website
        downloadurl = "https://libgen.li/"
        try:
            # Sending request to the webpage.
            driver.get(url)
            # Getting html page with BeautifulSoup module
            soup = BeautifulSoup(driver.page_source, "html.parser")
            # Finding all the mentioned elements from webpage.
            html_tag = soup.find_all("tr", attrs={"valign": "top", "bgcolor": "#C6DEFF"})
            # Using core method as function to get rid of repeating the same lines.
            source = "libgen"
            book_tuple = self.core(html_tag, baseurl, source)
            book_link = book_tuple[0]
            book_name = book_tuple[1]
            # Sending get request to the website.
            driver.get(book_link)
            # Parsering the response with "BeauitifulSoup".
            book_soup = BeautifulSoup(driver.page_source, "html.parser")
            # Finding all the mentioned elements in the webpage.
            td_html = book_soup.find("td", attrs={"align": "center", "valign": "top", "bgcolor": "#A9F5BC"})
            html_tag = td_html.find("a") 
            url = downloadurl + html_tag["href"]
            self.download(book_name, url)
        except SessionNotCreatedException:
            print("If you are not using android then install from win_linux_requirement.txt file")
        except (requests.exceptions.RequestException, WebDriverException, TimeoutException):
            print("Network Error!")
        except (TypeError, urllib3.exceptions.ProtocolError):
            print("Bad file.")

    def anna_archive(self,search_term):
        # Url to access the searching.
        url = f"https://annas-archive.org/search?index=&page=1&q={search_term}&desc=1&termtype_1=title&termval_1=&content=book_nonfiction&content=book_fiction&content=book_unknown&ext=pdf&ext=epub&sort=&lang=en"
        # Url to access the base website
        baseurl = "https://annas-archive.org"
        try:
            # Sending request to the webpage.
            driver.get(url)
            # Getting html page with BeautifulSoup module
            soup = BeautifulSoup(driver.page_source, "html.parser")
            # Finding all the mentioned elements from webpage.
            html_tag = soup.find_all("a", class_="js-vim-focus custom-a flex items-center relative left-[-10px] w-[calc(100%+20px)] px-2.5 outline-offset-[-2px] outline-2 rounded-[3px] hover:bg-black/6.7 focus:outline")
            # Using core method as function to get rid of repeating the same lines.
            source = "annasarchive"
            book_tuple = self.core(html_tag, baseurl, source)
            book_link = book_tuple[0]
            book_name = book_tuple[1]
            # Sending get request to the website.
            driver.get(book_link)
            # Parsering the response with "BeauitifulSoup".
            book_soup = BeautifulSoup(driver.page_source, "html.parser")
            # Finding all the mentioned elements in the webpage.
            html_tag = book_soup.find_all("a", class_="js-download-link")
            source = "annasarchive_chapter"
            book_tuple = self.core(html_tag, baseurl, source)
            book_link = book_tuple[0] 
            print(f"{book_name}\n{book_link}")
            subprocess.call(["am", "start", "-a", "android.intent.action.VIEW", "-d", book_link])
        except SessionNotCreatedException:
            print("If you are not using android then install from win_linux_requirement.txt file")
        except (requests.exceptions.RequestException, WebDriverException, TimeoutException):
            print("Network Error!")
        except TypeError:
            pass
        except FileNotFoundError:
            pass

    def glodls(self,search_term):
        # Url to access the searching.
        url = f"https://glodls.to/search_results.php?search={search_term}&cat=74&incldead=0&inclexternal=0&lang=0&sort=seeders&order=desc"
        # Url to access the base website
        baseurl = "https://glodls.to"
        try:
            # Sending request to the webpage.
            driver.get(url)
            time.sleep(1)
            # Getting html page with BeautifulSoup module
            soup = BeautifulSoup(driver.page_source, "html.parser")
            # Finding all the mentioned elements from webpage.
            html_tag = soup.find_all("td", class_="ttable_col2")
            # Using core method as function to get rid of repeating the same lines.
            source = "glodls"
            book_tuple = self.core(html_tag, baseurl, source)
            book_link = book_tuple[0]
            # Sending get request to the website.
            driver.get(book_link)
            # Parsering the response with "BeauitifulSoup".
            book_soup = BeautifulSoup(driver.page_source, "html.parser")
            # Finding all the mentioned elements in the webpage.
            html_td = book_soup.find("td", attrs={"align": "center", "valign": "middle", "width": "204"}) 
            html_tag = html_td.find("a")
            url = baseurl + "/" + html_tag["href"]
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
