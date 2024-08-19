## The part of the code that is commented was part of the base program that will be modified to be used with zlib.
## The code is in single '#' while comments are in '##'


## Importing packages required for the program.
import requests
import re
from bs4 import BeautifulSoup, Tag
# from pydantic import BaseModel, AnyHttpUrl
from datetime import date 
from libgen_api import LibgenSearch


## Space for classes start from here

## Episode class uses BaseModel from pydantic to form an automatic model based on given values.
# class Episode(BaseModel):
#     title:  str
#     url:  AnyHttpUrl

## Space for classes end here

## Space for functions start from here

def clear():
    print("\033c")
    

def choice():
    match input('\nSelect the category: \n1. Books\n2. Manga\n3. Anime\n4. Exit\n\nEnter index number: '):
        case '1':
            search_term = input('\nEnter the title of the book: ')
            match input('\nSelect the website: \n1. Libgen\n2. Zlibrary\n3. Anna\'s Archive\n4. Restart\n5. Exit\n\nEnter index number: '):
                case '1':
                    libgen(search_term)
                case '2':
                    zlibrary()
                case '3':
                    anna_archive(search_term)
                case '4':
                    clear()
                    choice()
                case '5':
                    clear()
                    exit()
                case _:
                    print('\nInvalid value')

        case '2':
            match input('\nSelect the website: \n1. MangaSee\n2. Comick\n3. Bato\n4. Restart\n5. Exit\n\nEnter index number: '):
                case '1':
                    pass
                case '2':
                    pass
                case '3':
                    pass
                case '4':
                    clear()
                    choice()
                case '5':
                    clear()
                    exit()
                case _:
                    print('\nInvalid value')
        case '3':
            match input('\nSelect the website: \n1. Anime1\n2. Anime2\n3. Anime3\n4. Restart\n5. Exit\n\nEnter index number: '):
                case '1':
                    pass
                case '2':
                    pass
                case '3':
                    pass
                case '4':
                    clear()
                    choice()
                case '5':
                    clear()
                    exit()
                case _:
                    print('\nInvalid value')
        case '4':
            clear()
            exit()                    
        case _:
            print('\nInvalid value')


## Function 1: Corresponds to "libgen.is" website and uses libgen_api package to find and download the books.
def libgen(search_term):
    libgen_search = LibgenSearch()
    results = libgen_search.search_title(search_term)
    index_int = 1
    for result in results:
        index = str(index_int)
        print(index + " " + result["Title"])
        index_int += 1
    try:
        book_selection = int(input("Select the book by typing the index number: "))
        if book_selection < 1 or book_selection > index_int-1:
            raise ValueError
        else:
            item_to_download = results[book_selection-1]
            download_links = libgen_search.resolve_download_links(item_to_download)
            print(download_links)
    except ValueError:
        print("Invalid integer. The number must be in the range.")

## Function 2: Corresponds to "singlelogin.rs" website and uses pydantic and requests to extract the books and download them.
def zlibrary():
    pass
    # Useful stuff
    #https://singlelogin.rs/rpc.php
    #https://z-library.rs/
    
    # login_url = 'https://singlelogin.rs/rpc.php' 
    # redirect_url = 'https://z-library.rs/'
    # payload = {   
    # }
    # response = requests.post(login_url, data=payload)
    # print(response.text)
    # soup = BeautifulSoup(response.content, "html.parser")
    

## Function 3: Corresponds to "annads-archive.org" website and uses requests to extract the books and download them.
## Defining the fuction that takes argument 'search_term'.
def anna_archive(search_term):
    url = 'https://annas-archive.org/search?q=' + search_term
    book_url = 'https://annas-archive.org'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
## Finding the specific piece of html body that corresponds with book names and url.
    div_html = soup.find_all('div', class_ = 'h-[125] flex flex-col justify-center')
    h3_html = soup.find_all('h3', class_ = 'max-lg:line-clamp-[2] lg:truncate leading-[1.2] lg:leading-[1.35] text-md lg:text-xl font-bold')
## Creating an empty list "link_list" and iterating each link found in "div" html class and appending them into the list.
    link_list = []
    for links in div_html:
        for each_link in links.find_all('a', href=True):
            link_list.append(book_url + each_link['href'])
## Creating an empty list "name_list" and iterating each name found in "h3" html class and appending them into the list.
    name_list = []
    for names in h3_html:
        for name in names:
            name_list.append(name.string)
## Creating an empty list "index_list" and iterating "i" in the range of 1 to 12 for indexing dictionary and appending them into the list.
    index_list = []
    for i in range(1,12):
        index_list.append(i)
## Creating a dictionary that takes length from "link_list" witk key as index and value as url. i.e  {'1': 'url'}.
    model_data = {index_list[i]: link_list[i] for i in range(len(link_list))}
## Printing the names of the books with imdex for user to select.
    index_int = 1
    for title in name_list:
        index = str(index_int)
        print(index + " " + title)
        index_int += 1
## Matching the user selection with library to get its value. Sending another get request to acquire download links for selected book.
    try:
        book_selection = int(input("\nSelect the book by typing the index number: "))
        if book_selection in model_data:
            book_link = f'{model_data[book_selection]}'
            book_response = requests.get(book_link)
            book_soup = BeautifulSoup(book_response.content, "html.parser")
## Finding the specific piece of html body that corresponds with download url.
            ul_html = book_soup.find_all('ul', class_ = 'list-inside mb-4 ml-1')
## Iterating each link found in "ul" html class and printing it.
            for links in ul_html:
                for each_link in links.find_all('a', class_ = 'js-download-link', href=True):
                    print(book_url + each_link['href'])
            print('\n\nThe links will lead to cloudflare human verifaction, if it fails to redirect just paste the link and try again')
                       
        else:
            raise ValueError
    except ValueError:
        print("Invalid integer. The number must be in the range.")
        
## Space for functions end here

##Under Progress
# login_url = 'https://singlelogin.rs/' 
# redirect_url = 'https://z-library.rs/'
# payload = {
# 
# }
# with requests.session() as session:
#     session.post(login_url, data=payload)
#     response = session.get(login_url)
#     soup = BeautifulSoup(response.content, "html.parser")
#     f = open("file.txt", "a")
#     f.write(soup.prettify())
#     f.close()
##Under Progress

choice()
