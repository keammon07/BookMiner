import json
import requests
import pandas as pd
from bs4 import BeautifulSoup
import time

HEADERS = {
"User-Agent": "Mozilla/5.0"
}

def get_book_extra(book_url):
try:
html = requests.get(
book_url,
headers=HEADERS,
timeout=30
).text

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    isbn = ""
    release_date = ""

    isbn_tag = soup.find(
        "meta",
        {"property": "book:isbn"}
    )

    if isbn_tag:
        isbn = isbn_tag.get(
            "content",
            ""
        )

    release_tag = soup.find(
        "meta",
        {"property": "book:release_date"}
    )

    if release_tag:
        release_date = release_tag.get(
            "content",
            ""
        )

    return isbn, release_date

except Exception:
    return "", ""

all_products = []

for page in range(1, 11):

url = (
    "https://www.naiin.com/category"
    "?type_book=best_seller"
    "&product_type_id=1"
    f"&pageNo={page}"
)

print(f"Loading page {page}")

try:

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=30
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    product_list = soup.find(
        "product-list"
    )

    if not product_list:
        print(
            f"No products on page {page}"
        )
        continue

    items_attr = product_list.get(
        ":items"
    )

    if not items_attr:
        continue

    products = json.loads(
        items_attr
    )

    for product in products:

        product["_page_no"] = page

        all_products.append(
            product
        )

    print(
        f"Found {len(products)} books"
    )

    time.sleep(1)

except Exception as e:

    print(
        f"Page {page} error:",
        e
    )

print(
f"Total products found: {len(all_products)}"
)

rows = []

for product in all_products:

book_id = product.get(
    "ProductID",
    ""
)

book_url = (
    f"https://www.naiin.com/"
    f"product/detail/{book_id}"
)

isbn, release_date = get_book_extra(
    book_url
)

rows.append({
    "book_id": book_id,
    "title": product.get(
        "ProductName",
        ""
    ),
    "page_no": product.get(
        "_page_no",
        ""
    ),
    "today_price": product.get(
        "PriceDiscount",
        ""
    ),
    "full_price": product.get(
        "PriceFull",
        ""
    ),
    "author": product.get(
        "AuthorName",
        ""
    ),
    "publisher": product.get(
        "PublisherName",
        ""
    ),
    "category": product.get(
        "CategoryText",
        ""
    ),
    "rating": product.get(
        "AverageRating",
        ""
    ),
    "rating_count": product.get(
        "TotalRating",
        ""
    ),
    "rank": product.get(
        "Rank",
        ""
    ),
    "isbn": isbn,
    "release_date": release_date,
    "url": book_url
})

time.sleep(0.2)

df = pd.DataFrame(rows)

df.to_csv(
"naiin_books.csv",
index=False,
encoding="utf-8-sig"
)

print("=" * 50)
print(f"Total books: {len(df)}")
print("Saved: naiin_books.csv")
print("=" * 50)
