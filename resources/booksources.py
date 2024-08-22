"""Class for Book sources"""

import sys

import requests
from bs4 import BeautifulSoup


class Booksources:
    """Class and the objects for book scraping"""

    # Method 1: Corresponds to "Libgen.is" website and uses requests to
    # extract the books and sends download links.

    # Defining the method that takes argument 'search_term'.
    def libgen(self, search_term):
        """Function for scraping Libgen."""
        # All the necessary urls for scraping.
        url = "https://libgen.is/search.php?req=" + search_term
        book_url = "https://libgen.is/"
        booksdl_url = "https://cdn3.booksdl.org/"
        libgen_url = "https://libgen.li/"
        # try and except to catch errors produced by requests.
        try:
            # Sending get request to the "libgen.is" website
            response = requests.get(url, timeout=2)
            # Parsering the response with "BeauitifulSoup".
            soup = BeautifulSoup(response.content, "html.parser")
            # Finding the specific piece of html body that corresponds with book ids, names
            # and urls.
            tr_html = soup.find_all("tr", attrs={"bgcolor": "#C6DEFF"})
            id_list = []
            # Iterating every "td" tag in "tr" tag.
            for td_html in tr_html:
                # Iterating every "id" property in first "td" tag or [0].
                for each_id in td_html.find_all("td")[0]:
                    # Appending all of the ids found into "id_list".
                    id_list.append(each_id.text)
            # Creating empty lists "link_list" "name_list".
            link_list = []
            name_list = []
            # Iterating each id in "id_list" as i.
            for i in id_list:
                # Iterating every "td_html" tag in "tr_html" tag.
                for td_html in tr_html:
                    # Iterating every "a href" tag in td_html.
                    for each_element in td_html.find_all(
                        "a", attrs={"id": i}, href=True
                    ):
                        # Appending all of the urls found into "link_list"
                        # with addition of book_url.
                        link_list.append(book_url + each_element["href"])
                        # Getting the name from the next element to "each_element" variable in html.
                        names = each_element.next_element
                        # Appending all of the names found into "name_list".
                        name_list.append(names)
            # Creating an empty "index_link" and iterating as well as appending numbers 1 to 30.
            index_list = []
            for i in range(1, 30):
                index_list.append(i)
            # Creating dictionaries that takes length from "name_list"
            # and "link_list" respectively witk key from "index_list" and value
            # from "name_list" and "link_list" respectively.
            names_dict = {index_list[i]: name_list[i] for i in range(len(name_list))}
            urls_dict = {index_list[i]: link_list[i] for i in range(len(link_list))}
            # Printing the names of the books with imdex for user to select.
            index_int = 1

            for title in name_list:
                index = str(index_int)
                print(index + " " + title)
                index_int += 1
            # Try and except to catch "ValueError".
            try:
                # If statement in case no book was found.
                if not link_list:
                    print(f'No book with title "{search_term}" found')
                # Matching the user selection with "urls_dict" dictionary to get its value.
                book_selection = int(input("\nSelect the book index number: "))
                if book_selection in urls_dict:
                    # Getting the book name and link by matching the index number from dictionaries.
                    book_link = f"{urls_dict[book_selection]}"
                    book_name = f"{names_dict[book_selection]}"
                    print("Fetching, please wait...")
                    # Starting the requests session.
                    session = requests.Session()
                    # Sending get request to the "book_link" website.
                    book_response = session.get(book_link, timeout=2)
                    # Parsering the response with "BeauitifulSoup".
                    book_soup = BeautifulSoup(book_response.content, "html.parser")
                    # Finding the libgen.li link from "a" tag through a_html_book.
                    a_html_book = book_soup.find(
                        "a", attrs={"title": "Libgen.li"}, href=True
                    )
                    # Storing "libgen.li" link in variable.
                    download_link = a_html_book["href"]
                    # Sending get request to the "download_link" website.
                    download_response = session.get(download_link, timeout=2)
                    # Parsering the response with "BeauitifulSoup".
                    download_soup = BeautifulSoup(
                        download_response.content, "html.parser"
                    )
                    # Finding the "a" tag from "td" tag.
                    td_html_download = download_soup.find(
                        "td", attrs={"bgcolor": "#A9F5BC"}
                    )
                    # Finding the adfree direct download link from "a" tag.
                    a_html_download = td_html_download.find("a", href=True)
                    # Storing link and adding main website link with it.
                    booksdl_link = f'{booksdl_url}{a_html_download["href"]}'
                    libgen_link = f'{libgen_url}{a_html_download["href"]}'
                    print(f"\nName: {book_name}\n{booksdl_link}\n{libgen_link}")
                else:
                    raise ValueError
            except ValueError:
                print("Invalid integer. The number must be in the range.")
        except requests.exceptions.RequestException:
            print("Network Error!")
            sys.exit()

    # Method 2: Corresponds to "Annas-archive.org" website and uses requests to
    # extract the books and sends download links.

    # Defining the method that takes argument 'search_term'.
    def anna_archive(self, search_term):
        """Function for scraping Anna's Archive."""
        # All the necessary urls for scraping.
        url = "https://annas-archive.org/search?q=" + search_term
        book_url = "https://annas-archive.org"
        # try and except to catch errors produced by requests.
        try:
            # Sending get request to the "annas-archive.org" website
            response = requests.get(url, timeout=2)
            # Parsering the response with "BeauitifulSoup".
            soup = BeautifulSoup(response.content, "html.parser")
            # Finding the specific piece of html body that corresponds with
            # book links and names in "div" and "h3" tags respectively.
            div_html = soup.find_all(
                "div", class_="h-[125] flex flex-col justify-center"
            )
            h3_html = soup.find_all(
                "h3",
                class_="max-lg:line-clamp-[2] lg:truncate leading-"
                "[1.2] lg:leading-[1.35] text-md lg:text-xl font-"
                "bold",
            )
            # Creating an empty list "link_list" and iterating each link found in "div"
            # tag and appending them into the list.
            link_list = []
            for links in div_html:
                for each_link in links.find_all("a", href=True):
                    link_list.append(book_url + each_link["href"])
            # Creating an empty list "name_list" and iterating each name found
            # in "h3" tag and appending them into the list.
            name_list = []
            for names in h3_html:
                for name in names:
                    name_list.append(name.string)
            # Creating an empty "index_link" and iterating as well as appending numbers 1 to 30.
            index_list = []
            for i in range(1, 30):
                index_list.append(i)
            # Creating dictionaries that takes length from "name_list"
            # and "link_list" respectively witk key from "index_list" and value
            # from "name_list" and "link_list" respectively.
            names_dict = {index_list[i]: name_list[i] for i in range(len(name_list))}
            urls_dict = {index_list[i]: link_list[i] for i in range(len(link_list))}
            # Printing the names of the books with imdex for user to select.
            index_int = 1
            for title in name_list:
                index = str(index_int)
                print(index + " " + title)
                index_int += 1
            # Try and except to catch "ValueError".
            try:
                # If statement in case no book was found.
                if not link_list:
                    print(f'No book with title "{search_term}" found')
                # Matching the user selection with "urls_dict" dictionary to get its value.
                book_selection = int(input("\nSelect the book index number: "))
                if book_selection in urls_dict:
                    # Getting the book name and link by matching the index number from dictionaries.
                    book_link = f"{urls_dict[book_selection]}"
                    book_name = f"{names_dict[book_selection]}"
                    print("Fetching, please wait...")
                    # Sending get request to the "book_link" website
                    book_response = requests.get(book_link, timeout=2)
                    # Parsering the response with "BeauitifulSoup".
                    book_soup = BeautifulSoup(book_response.content, "html.parser")
                    # Finding the specific piece of html body that corresponds with
                    # download url in "ul" tag.
                    ul_html = book_soup.find("ul", class_="list-inside mb-4 ml-1")
                    # Printing the name of the book.
                    print(f"\nName: {book_name}\n")
                    # Iterating each link found in "ul" tag and printing it.
                    for each_link in ul_html.find_all(
                        "a", class_="js-download-link", href=True
                    ):
                        print(f'{book_url}{each_link["href"]}')
                    print(
                        "\n\nThe links will lead to cloudflare human verifaction "
                        "if it fails to redirect just paste the link and try again"
                    )
                else:
                    raise ValueError
            except ValueError:
                print("Invalid integer. The number must be in the range.")
        except requests.exceptions.RequestException:
            print("Network Error!")
            sys.exit()

    # Method 3: Corresponds to "Z-library.rs" website and uses requests to
    # extract the books and sends download links.

    # Defining the method that takes argument 'search_term'.
    def zlibrary(self, search_term):
        """Function for scraping Zlibrary."""

        # Under Progress
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
        # Under Progress
