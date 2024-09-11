'''Manga Sources'''

#Importing necessary modules
import os
import re
import shutil
import subprocess

import pandas as pd
import questionary
import requests
from bs4 import BeautifulSoup
from cbz_generator import create_cbz_archive as cbz_generator
from selenium import webdriver
from selenium.common.exceptions import (NoSuchElementException,
                                        SessionNotCreatedException,
                                        TimeoutException, WebDriverException)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from term_image.image import from_url
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

class Mangasources:
    '''Manga functions'''
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
    def user_choice(self, name_list, link_list, index_list):
        # Appendind data for next and previous page.
        # Creating two dictionary that take key as index and value as items from "link_list" and "name_list" respectively.
        url_dict = {index_list[i]: link_list[i] for i in range(len(link_list))}
        name_dict = {index_list[i]: name_list[i] for i in range(len(name_list))}
        for key, value in name_dict.items():
            print(f'{key}. {value}')
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
    def confirmation(self, selection, index_list, img_list):
        img_dict = {index_list[i]: img_list[j] for i, j in enumerate(range(len(img_list)), start=1)}
        img = f"{img_dict[selection]}"
        image = from_url(img)
        subprocess.call(["clear"])
        print(f"\n{image}\n\n")
        answer = questionary.select("Is this the manga?", choices=["Yes", "No"]).ask()
        if answer == "Yes":
            subprocess.call(["clear"])
            return True
        else: 
            subprocess.call(["clear"])
            return False
############################################################################
    def download_compress(self, manga_name, chapter_name, img_links_list):
        # Using regex to get the standard naming protocols for easy folder making.
        manga = re.sub('[^a-z,0-9]', '_', manga_name, flags=re.IGNORECASE)
        chapter = re.sub('[^a-z,0-9]', '_', chapter_name, flags=re.IGNORECASE)
        try:
            # Making new directory for manga and inside it a chapter directory and accessing them.
            if not os.path.isdir(manga):
                os.mkdir(manga)
                os.chdir(manga)
                path = os.getcwd()
                if not os.path.isdir(chapter):
                    os.mkdir(chapter)
                    os.chdir(chapter)
                else:
                    os.chdir(chapter)
            elif os.path.isdir(manga):
                os.chdir(manga)
                path = os.getcwd()
                if not os.path.isdir(chapter):
                    os.mkdir(chapter)
                    os.chdir(chapter)
                else:
                    os.chdir(chapter)
            else:
                os.chdir(manga)
                path = os.getcwd()
                os.chdir(chapter)
            # Enumerating the "img_links_list" to get each link with index.
            for i, img in enumerate(img_links_list):
                # Sending request to the image link.
                with requests.get(img, stream = True) as res:
                # Checking header to get the content length, in bytes.
                    total_length = int(res.headers.get("Content-Length"))
                    # Checking if request was valid.
                    if res.status_code == 200:
                        # Naming the image and storing it.
                        image = f'{chapter} Image {i}.jpg' 
                        # Implement progress bar via tqdm.
                        with tqdm.wrapattr(res.raw, "read", total=total_length, desc="")as raw:
                            # Downloading image via shutil.
                            with open(image,'wb') as f:
                                shutil.copyfileobj(raw, f)
                        print('Image sucessfully Downloaded: ',image)
                    else:
                        print('Image Couldn\'t be retrieved')
            # Accessing the manga folder to compress chapter folder into cbz file.
            os.chdir(path)
            # Compressing chapter folder into cbz file using cbz_generator module.
            cbz_generator.create_cbz_archive(chapter, path, f'{manga}_{chapter}')
            print("Download Complete")
        except OSError as e:
            print(e)
############################################################################
    # Defining the function for retrying the user_choice function.
    def retry(self, source, search_term):
        # Using match case argument to see which class called the function.
        answer = questionary.select("Do you want to download another file? ", choices=["Yes", "No"]).ask()
        if answer == "Yes":
            if source == "bato":
                Mangasources().Bato().bato(search_term)
            elif source == "mangasee":
                Mangasources().Mangasee().mangasee(search_term)
            else:
                Mangasources().Comicextra().comicextra(search_term)
############################################################################
    class Bato:
        def bato(self,search_term):
            # Declaring function level variables.
            source = "bato"
            index = 1
            # Making search term better for url through regex.
            term = re.sub("\W", "+", search_term)
            # Url to access webpage.
            web_url = f"https://bato.to/search?word={term}"
            # Url to be used for page navigation.
            page_url = f"https://bato.to/search?word={term}&page="
            # Url to access the base website
            base_url = "https://bato.to"
            try:
                while True:
                    # Sending request to the webpage.
                    driver.get(web_url)
                    # Getting html page with BeautifulSoup module
                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    # Checking weather the element exists.
                    if Mangasources().exists(element = ".pagination.pagination-sm.mb-0"):
                        html_tag = soup.find("ul", class_="pagination pagination-sm mb-0")
                        # Finding the last td tag and getting its text which is the number of last page and converting it into integer.
                        pages = int(re.sub("\W+", "", html_tag.find_all("li")[-2].getText()))
                    else:
                        pass
                    # Finding all the mentioned elements from webpage.
                    html_tag = soup.find_all("a", class_="item-title", href=True)
                    index_list = []
                    name_list = []
                    link_list = []
                    img_list = []
                    # Finding the links and making link list.
                    name_list.append("Next Page")
                    link_list.append(page_url)
                    index_list.append(0)
                    for i, links in enumerate(html_tag, start=1):
                        index_list.append(i)
                        name_list.append(links.text.strip())
                        link_list.append(base_url + links["href"])
                    name_list.append("Previous Page")
                    link_list.append(page_url)
                    index_list.append(i+1)
                    html_tag = soup.find_all("img", class_="rounded")
                    for img in html_tag:
                        img_list.append(img["src"])
                    while True:
                        # Calling the user choice function.
                        data = Mangasources().user_choice(name_list, link_list, index_list)
                        url = data[0]
                        name = data[1]
                        selection = data[2]
                        if name != "Next Page" and name != "Previous Page":
                            answer = Mangasources().confirmation(selection, index_list, img_list)
                            if answer == True:
                                break
                            else:
                                pass
                        else:
                            break
                    index = Mangasources().page_navigation(name, pages, index)
                    web_url = url + str(index)
                    if name != "Next Page" and name != "Previous Page":
                        break
                # Sending request to the webpage.
                driver.get(url)
                # Parsering the response with "BeauitifulSoup".
                soup = BeautifulSoup(driver.page_source, "html.parser")
                # Finding all the mentioned elements in the webpage.
                html_tag = soup.find_all(
                        "a", class_="visited chapt", href=True
                )
                index_list = []
                name_list = []
                link_list = []
                # Finding the links and making link list.
                for i, links in enumerate(html_tag, start=1):
                    index_list.append(i)
                    name_list.append(links.text.strip())
                    link_list.append(base_url + links["href"])
                name_list.reverse()
                link_list.reverse()
                # Using core method as function to get rid of repeating the same lines.
                data = Mangasources().user_choice(name_list, link_list, index_list)
                url = data[0]
                chapter_name = data[1] 
                # Sending request with selenium webdriver.
                driver.get(url)
                # Parsering the response with "BeauitifulSoup".
                soup = BeautifulSoup(
                    driver.page_source, "html.parser"
                )
                # Finding all the mentioned elements from webpage.
                html_tag = soup.find_all(
                    "img", class_="page-img"
                )
                # Creating the list to store image url.
                img_links_list = []
                # Finding all the mentioned elements from img_html_chapter.
                for imgs in html_tag:
                    img_links_list.append(imgs["src"])
                # Calling download_compress method as function.
                Mangasources().download_compress(name, chapter_name, img_links_list)
                Mangasources().retry(source, search_term)
            except SessionNotCreatedException:
                print("If you are not using android then install from win_linux_requirement.txt file")
            except (requests.exceptions.RequestException, WebDriverException, TimeoutException):
                print("Network Error!")
            except TypeError:
                pass
            except KeyboardInterrupt:
                print("Cancelled by user.")
############################################################################
    class Mangasee:
        def mangasee(self, search_term):
            # Declaring function level variables.
            source = "mangasee"
            # Making search term better for url through regex.
            term = re.sub("\W", "+", search_term)
            # Url to access webpage. 
            web_url = f"https://mangasee123.com/search/?sort=v&desc=true&name={term}"
            # Url to access the base website
            base_url = "https://mangasee123.com"
            try:
                # Sending request to the webpage.
                driver.get(web_url)
                while True:
                    # Getting html page with BeautifulSoup module
                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    # Finding all the mentioned elements from webpage.
                    html_tag = soup.find_all("a", class_="SeriesName ng-binding", href=True)
                    index_list = []
                    name_list = []
                    link_list = []
                    img_list = []
                    # Finding the links and making link list.
                    name_list.append("Next Page")
                    link_list.append("")
                    index_list.append(0)
                    for i, links in enumerate(html_tag, start=1):
                        index_list.append(i)
                        name_list.append(links.text.strip())
                        link_list.append(base_url + links["href"])
                    html_tag = soup.find_all("img", class_="img-fluid")
                    for img in html_tag:
                        img_list.append(img["src"])
                    # Calling the user choice function.
                    data = Mangasources().user_choice(name_list, link_list, index_list)
                    url = data[0]
                    name = data[1]
                    selection = data[2]
                    if name != "Next Page":
                        answer = Mangasources().confirmation(selection, index_list, img_list)
                        if answer == True:
                            break
                        else:
                            pass
                    else:
                        if Mangasources().exists(element = ".btn.btn-outline-primary.form-control.top-15.bottom-5.ng-scope") == True:
                            WebDriverWait(driver,1).until(EC.element_to_be_clickable((By.CSS_SELECTOR,".btn.btn-outline-primary.form-control.top-15.bottom-5.ng-scope"))).click()
                # Sending request to the webpage.
                driver.get(url)
                if Mangasources().exists(element = ".list-group-item.ShowAllChapters.ng-scope") == True:
                    WebDriverWait(driver,1).until(EC.element_to_be_clickable((By.CSS_SELECTOR,".list-group-item.ShowAllChapters.ng-scope"))).click()
                # Parsering the response with "BeauitifulSoup".
                soup = BeautifulSoup(driver.page_source, "html.parser")
                # Finding all the mentioned elements in the webpage.
                html_tag = soup.find_all(
                    "a", class_="list-group-item ChapterLink ng-scope", href=True
                    )
                index_list = []
                name_list = []
                link_list = []
                # Finding the links and making link list.
                for i, links in enumerate(html_tag, start=1):
                    index_list.append(i)
                    name_list.append(re.sub("\s+", " ", links.text.strip()))
                    link_list.append(re.sub('-page-1','',(base_url + links["href"])))
                name_list.reverse()
                link_list.reverse()
                # Using core method as function to get rid of repeating the same lines.
                data = Mangasources().user_choice(name_list, link_list, index_list)
                url = data[0]
                chapter_name = data[1] 
                # Sending request with selenium webdriver.
                driver.get(url)
                # Parsering the response with "BeauitifulSoup".
                soup = BeautifulSoup(
                    driver.page_source, "html.parser"
                )
                # Finding all the mentioned elements from webpage.
                html_tag = soup.find_all(
                    "img", class_="img-fluid HasGap"
                )
                # Creating the list to store image url.
                img_links_list = []
                # Finding all the mentioned elements from img_html_chapter.
                for imgs in html_tag:
                    img_links_list.append(imgs["src"])

                # Calling download_compress method as function.
                Mangasources().download_compress(name, chapter_name, img_links_list)
                Mangasources().retry(source, search_term)
            except SessionNotCreatedException:
                print("If you are not using android then install from win_linux_requirement.txt file")
            except (requests.exceptions.RequestException, WebDriverException, TimeoutException):
                print("Network Error!")
            except TypeError:
                pass
            except KeyboardInterrupt:
                print("Cancelled by user.")
############################################################################
    class Comicextra:
        def comicextra(self, search_term):
            # Declaring function level variables.
            source = "comicextra"
            index = 1
            # Making search term better for url through regex.
            term = re.sub("\W", "+", search_term)
            # Url to access webpage.
            web_url = f"https://comixextra.com/search?keyword={term}"
            # Url to be used for page navigation.
            page_url = f"https://comixextra.com/search?keyword={term}&page="
            try:
                while True:
                    # Sending request to the webpage.
                    driver.get(web_url)
                    # Getting html page with BeautifulSoup module
                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    # Checking weather the element exists.
                    html_tag = soup.find("a", href=lambda t: t and "page=" in t)
                    if not html_tag:
                        pages = 1
                    else:
                        html_tag = soup.find_all("div", class_="general-nav")[1]
                        # Finding the last td tag and getting its text which is the number of last page and converting it into integer.
                        pages = int(html_tag.find_all("a")[-2].getText())
                    # Finding all the mentioned elements from webpage.
                    index_list = []
                    name_list = []
                    link_list = []
                    img_list = []
                    # Finding the links and making link list.
                    html_tag = soup.find_all("h3")
                    name_list.append("Next Page")
                    link_list.append(page_url)
                    index_list.append(0)
                    for i, tag in enumerate(html_tag, start=1):
                        for links in tag.find_all("a"):
                            name_list.append(links.text.strip())
                            link_list.append(links["href"])
                            index_list.append(i)
                    name_list.append("Previous Page")
                    link_list.append(page_url)
                    index_list.append(i+1) 
                    html_tag = soup.find_all("a", class_="image")
                    for tag in html_tag:
                        for img in tag.find_all("img", alt=True):
                            img_list.append(img["src"])
                    while True:        
                        # Calling the user choice function.
                        data = Mangasources().user_choice(name_list, link_list, index_list)
                        url = data[0]
                        name = data[1]
                        selection = data[2]
                        if name != "Next Page" and name != "Previous Page":
                            answer = Mangasources().confirmation(selection, index_list, img_list)
                            if answer == True:
                                break
                            else:
                                pass
                        else:
                            break
                    index = Mangasources().page_navigation(name, pages, index)
                    web_url = url + str(index)
                    if name != "Next Page" and name != "Previous Page":
                        break
                # Sending request to the webpage.
                driver.get(url)
                # Parsering the response with "BeauitifulSoup".
                soup = BeautifulSoup(driver.page_source, "html.parser")
                # Finding all the mentioned elements in the webpage.
                table = soup.find(
                        "table", class_="table"
                )
                df = Mangasources().visual_tables(table)
                df_table = df.iloc[:, [0, 1]]
                df_table.index += 1
                index_list = df_table.index.tolist()
                name_list = df[df.columns[0]].values.tolist()
                html_tag = table.find_all("a")
                link_list = []
                # Finding the links and making link list.
                for i, links in enumerate(html_tag, start=1):
                    link_list.append(links["href"])
                # Using core method as function to get rid of repeating the same lines.
                data = Mangasources().user_choice(name_list, link_list, index_list)
                url = data[0]
                chapter_name = data[1] 
                # Sending request with selenium webdriver.
                driver.get(url+"/full")
                # Parsering the response with "BeauitifulSoup".
                soup = BeautifulSoup(
                    driver.page_source, "html.parser"
                )
                # Finding all the mentioned elements from webpage.
                html_tag = soup.find_all(
                    "div", class_="chapter-container"
                )
                # Creating the list to store image url.
                img_links_list = []
                # Finding all the mentioned elements from img_html_chapter.
                for tag in html_tag:
                    for imgs in tag.find_all("img"):
                        img_links_list.append(imgs["src"].strip())
                # Calling download_compress method as function.
                Mangasources().download_compress(name, chapter_name, img_links_list)
                Mangasources().retry(source, search_term)
            except SessionNotCreatedException:
                print("If you are not using android then install from win_linux_requirement.txt file")
            except (requests.exceptions.RequestException, WebDriverException, TimeoutException):
                print("Network Error!")
            except TypeError:
                pass
            except KeyboardInterrupt:
                print("Cancelled by user.")
############################################################################
