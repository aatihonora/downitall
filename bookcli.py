"""Bookcli"""

# Importing packages required for the program.
import sys

from resources import Animesources, Booksources, Mangasources

# Global variables.
books = Booksources()
manga = Mangasources()
anime = Animesources()
# Space for functions start from here


def file_open(soup):
    """Function for opening file and appending soup."""
    with open("file.txt", "a", encoding="utf-8") as f:
        f.write(soup.prettify())
        f.close()


def retry():
    """Function for restarting."""
    match input(
        "\nDo you want to search another book:\n1. Yes\n2. No"
        "\nType the index number: "
    ):
        case "1":
            choice()
            clear()
        case "2":
            clear()
            sys.exit()
        case _:
            print("\nInvalid value")
            retry()


def clear():
    """Function for terminal clear."""
    print("\033c")


def choice():
    """Function to start the core app."""
    match input(
        "\nSelect the category: \n1. Books\n2. Manga\n3. Anime"
        "\n4. Exit\n\nEnter index number: "
    ):
        case "1":
            search_term = input("\nEnter the title of the book: ")
            match input(
                "\nSelect the website: \n1. Libgen\n2. Anna's Archive"
                "\n3. Zlibrary\n4. Restart\n5. Exit"
                "\n\nEnter index number: "
            ):
                case "1":
                    books.libgen(search_term)
                case "2":
                    books.anna_archive(search_term)
                case "3":
                    books.zlibrary(search_term)
                case "4":
                    clear()
                    choice()
                case "5":
                    clear()
                    sys.exit()
                case _:
                    print("\nInvalid value")

        case "2":
            search_term = input("\nEnter the title of the manga: ")
            match input(
                "\nSelect the website: \n1. Bato\n2. Mangasee"
                "\n3. ComicExtra\n4. Restart\n5. Exit"
                "\n\nEnter index number: "
            ):
                case "1":
                    manga.bato(search_term)
                case "2":
                    manga.mangasee(search_term)
                case "3":
                    manga.comicextra(search_term)
                case "4":
                    clear()
                    choice()
                case "5":
                    clear()
                    sys.exit()
                case _:
                    print("\nInvalid value")
        case "3":
            search_term = input("\nEnter the title of the anime: ")
            match input(
                "\nSelect the website: \n1. TokyoInsider\n2. Nyaa"
                "\n3. Kayoanime\n4. Restart\n5. Exit"
                "\n\nEnter index number: "
            ):
                case "1":
                    anime.tokyoinsider(search_term)
                case "2":
                    anime.nyaa(search_term)
                case "3":
                    anime.kayoanime(search_term)
                case "4":
                    clear()
                    choice()
                case "5":
                    clear()
                    sys.exit()
                case _:
                    print("\nInvalid value")
        case "4":
            clear()
            sys.exit()
        case _:
            print("\nInvalid value")

choice()
#
## Space for functions ends here
#search_term = input("Manga title: ")
#URL = "https://bato.to/search?word=" + search_term
#BASEURL = "https://bato.to"
#try:
#    response = requests.get(URL, timeout=2)
#    isoup = BeautifulSoup(response.content, "html.parser")
#    a_html = isoup.find_all("a", class_="item-title", href=True)
#    span_html = isoup.find_all("span", class_="highlight-text")
#
#    link_list = []
#    name_list = []
#    for links in a_html:
#        link_list.append(BASEURL + links["href"])
#        name_list.append(links.text)
#    index_list = []
#    for i in range(1, 100):
#        index_list.append(i)
#
#    url_dict = {index_list[i]: link_list[i] for i in range(len(link_list))}
#    name_dict = {index_list[i]: name_list[i] for i in range(len(name_list))}
#
#    index = 1
#    for i in name_list:
#        print(str(index) + ". " + str(i))
#        index += 1
#
#    try:
#        # If statement in case no book was found.
#        if not link_list:
#            print(f'No book with title "{search_term}" found')
#        else:
#            # Matching the user selection with "urls_dict" dictionary to get its value.
#            manga_selection = int(input("\nSelect the book index number: "))
#            if manga_selection in url_dict:
#                # Getting the book name and link by matching the index number from dictionaries.
#                manga_link = f"{url_dict[manga_selection]}"
#                manga_name = f"{name_dict[manga_selection]}"
#                print("Fetching, please wait...")
#                # Starting the requests session.
#                session = requests.Session()
#                # Sending get request to the "book_link" website.
#                manga_response = session.get(manga_link, timeout=2)
#                # Parsering the response with "BeauitifulSoup".
#                manga_soup = BeautifulSoup(manga_response.content, "html.parser")
#                # Finding the chapters link from "a" tag through a_html_chapter.
#                a_html_chapter = manga_soup.find_all(
#                    "a", class_="visited chapt", href=True
#                )
#                # Storing "chapters link" link in variable.
#                chapter_name_list = []
#                chapter_link_list = []
#                for chapter_data in a_html_chapter:
#                    chapter_link_list.append(BASEURL + chapter_data["href"].strip())
#                    chapter_name_list.append(chapter_data.text.strip())
#                chapter_link_list.reverse()
#                chapter_name_list.reverse()
#                chapter_index_list = []
#                for i in range(1, 2000):
#                    chapter_index_list.append(i)
#                chapter_url_dict = {
#                    chapter_index_list[i]: chapter_link_list[i]
#                    for i in range(len(chapter_link_list))
#                }
#                chapter_name_dict = {
#                    chapter_index_list[i]: chapter_name_list[i]
#                    for i in range(len(chapter_name_list))
#                }
#                index = 1
#                for i in chapter_name_list:
#                    print(str(index) + ". " + str(i))
#                    index += 1
#                try:
#                    # If statement in case no book was found.
#                    if not chapter_link_list:
#                        print("No chapter found")
#                    else:
#                        # Matching the user selection with "urls_dict" dictionary to get its value.
#                        chapter_selection = int(
#                            input("\n Select the book index number: ")
#                        )
#                        if chapter_selection in chapter_url_dict:
#                            # Getting the book name and link by matching the index number from dictionaries.
#                            chapter_link = f"{chapter_url_dict[chapter_selection]}"
#                            chapter_name = f"{chapter_name_dict[chapter_selection]}"
#                            print("Fetching, please wait...")
#                            # Sending get request to the "book_link" website.
#                            chapter_response = driver.get(chapter_link)
#                            # Parsering the response with "BeauitifulSoup".
#                            chapter_soup = BeautifulSoup(
#                                driver.page_source, "html.parser"
#                            )
#                            # Finding the chapters link from "a" tag through a_html_chapter.
#                            imgs_html_chapter = chapter_soup.find_all(
#                                "img", class_="page-img"
#                            )
#                            driver. quit()
#                            img_links_list = []
#                            for imgs in imgs_html_chapter:
#                                img_links_list.append(imgs["src"])
#                            manga = re.sub('[^a-z,0-9]', '_', manga_name, flags=re.IGNORECASE)
#                            chapter = re.sub('[^a-z,0-9]', '_', chapter_name, flags=re.IGNORECASE)
#                            os.mkdir(manga)
#                            os.chdir(manga)
#                            for i, img in enumerate(img_links_list):
#                                res = requests.get(img, stream = True)
#                                if res.status_code == 200:
#                                    image = f'{chapter} Image {i}.jpg'
#                                    with open(image,'wb') as f:
#                                        shutil.copyfileobj(res.raw, f)
#                                    print('Image sucessfully Downloaded: ',image)
#                                else:
#                                    print('Image Couldn\'t be retrieved')
#                            os.chdir(bookcli)
#                            cbz_generator.create_cbz_archive(manga, bookcli, f'{manga}_{chapter}')
#                            print("Download Complete")
#                            shutil.rmtree(manga)
#                        else:
#                            raise ValueError
#                except ValueError:
#                    print("Invalid integer. The number must be in the range.")
#            else:
#                raise ValueError
#    except ValueError:
#        print("Invalid integer. The number must be in the range.")
#except requests.exceptions.RequestException:
#    print("Network Error!")
#    sys.exit()
