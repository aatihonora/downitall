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

## Creating the "extract_episode_data" function, which takes row and returns dict and making a dict variable "model_data" to store the data for each row of the table, also making "row_data" variable to store table data as td.

# def extract_episode_data(row: Tag) -> dict:
#     model_data = {}
#     row_data = row.select('td')

## Enumerating the row_data taken from table data as "td" with index "i", each iteration of "i" being an element of table.

#     for i, td in enumerate(row_data):
#         if i==2:
#             link = td.find('a')
#             model_data['url'] = base_url + link.attrs['href'] + "/"
#             model_data['title'] = link.text
# 
#     return model_data


## Space for functions end here


## Declaring global variables that will be used.
  
url = 'https://singlelogin.rs

## Sending request to the webpage to get the response stored in "response" variable.

response = requests.get(url)

## Getting the html file from the response in the form of text and then storing it in the variable "soup" for parsing it with BeautifulSoup.

soup = BeautifulSoup(response.text, 'html.parser')

## Specifying the particular table and storing it in variable "rows" and creating a list "episodes" with pydantic class "Episode" which takes function "extract_episode_data" as argument while "extract_episode_data" function takes row as argument that is acquired by looping rows.

# rows = soup.select('tbody > tr')
# episodes = [Episode(**extract_episode_data(row)) for row in rows]

## Taking input from user as int in  "website_selection" variable and checking if it is in the range if so moving to the selected portion.

try:
    website_selection = int(input("Select the website: \n1. Libgen\n2. Zlib\n\nChoose: "))
    if website_selection < 1 or website_selection  > 2:
        raise ValueError
    else:
        search_term = input("Enter the title: ")
except ValueError:
    print("\nInvalid integer. The number must be in the range of 1-10.")

## Creating modules and directing user to them.

## Module 1: Corresponds to "libgen.is" website and uses libgen_api package to find and download the books.

if website_selection == 1:
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

## Module 2: Corresponds to "singlelogin.rs" website and uses pydantic and requests to extract the books and download them.

elif website_selection == 2:
    pass
    

#search_term = input("Enter the title: ")
#resultepisodes = [eachepisode for eachepisode in episodes if search_term.lower() in eachepisode.title.lower() ]

# Converting list "resultepisodes" into a string type and stored as "results" and seperating url through regex and storing it in an array called "pageurl"

#results = str(resultepisodes)
#pageurl = re.findall("http[s]*\S+/", results)

#print(f"\nEpisode with the term {search_term}: ")
#for i in pageurl:
    #print(i)
