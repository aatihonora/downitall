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
                    anna_archive()
                case '4':
                    choice()
                case '5':
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
                    choice()
                case '5':
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
                    choice()
                case '5':
                    exit()
                case _:
                    print('\nInvalid value')
        case '4':
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
    

## Function 3: Corresponds to "singlelogin.rs" website and uses pydantic and requests to extract the books and download them.
def anna_archive():
    pass

## Creating the "extract_episode_data" function, which takes row and returns dict and making a dict variable "model_data" to store the data for each row of the table, also making "row_data" variable to store table data as td.
## Enumerating the row_data taken from table data as "td" with index "i", each iteration of "i" being an element of table.
# def extract_episode_data(row: Tag) -> dict:
#     model_data = {}
#     row_data = row.select('td')
#     for i, td in enumerate(row_data):
#         if i==2:
#             link = td.find('a')
#             model_data['url'] = base_url + link.attrs['href'] + "/"
#             model_data['title'] = link.text
# 
#     return model_data

## Space for functions end here

## Declaring global variables that will be used.
## Sending request to the webpage to get the response stored in "response" variable.
## Getting the html file from the response in the form of text and then storing it in the variable "soup" for parsing it with BeautifulSoup.

login_url = 'https://singlelogin.rs/' 
redirect_url = 'https://z-library.rs/'
payload = {

}
with requests.session() as session:
    session.post(login_url, data=payload)
    response = session.get(login_url)
    soup = BeautifulSoup(response.content, "html.parser")
    f = open("file.txt", "a")
    f.write(soup.prettify())
    f.close()

## Specifying the particular table and storing it in variable "rows" and creating a list "episodes" with pydantic class "Episode" which takes function "extract_episode_data" as argument while "extract_episode_data" function takes row as argument that is acquired by looping rows.
# rows = soup.select('tbody > tr')
# episodes = [Episode(**extract_episode_data(row)) for row in rows]

#search_term = input("Enter the title: ")
#resultepisodes = [eachepisode for eachepisode in episodes if search_term.lower() in eachepisode.title.lower() ]

# Converting list "resultepisodes" into a string type and stored as "results" and seperating url through regex and storing it in an array called "pageurl"
#results = str(resultepisodes)
#pageurl = re.findall("http[s]*\S+/", results)
#print(f"\nEpisode with the term {search_term}: ")
#for i in pageurl:
    #print(i)
