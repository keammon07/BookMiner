import requests
from bs4 import BeautifulSoup

def get_book_extra(book_url):
    """
    Return: ISBN, ReleaseDate
    """
    try:
        html = requests.get(
            book_url,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=30
        ).text

        soup = BeautifulSoup(html, "html.parser")

        isbn = ""
        release_date = ""

        isbn_tag = soup.find("meta", {"property": "book:isbn"})
        if isbn_tag:
            isbn = isbn_tag.get("content", "")

        release_tag = soup.find("meta", {"property": "book:release_date"})
        if release_tag:
            release_date = release_tag.get("content", "")

        return isbn, release_date

    except Exception:
        return "", ""

# ตัวอย่างการเรียกใช้
# isbn, release_date = get_book_extra(
#     "https://www.naiin.com/product/detail/705612"
# )
# print(isbn, release_date)
