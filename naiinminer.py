import json
import requests
import pandas as pd
from bs4 import BeautifulSoup

URL = "https://www.naiin.com/category?type_book=best_seller&product_type_id=1"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(
    URL,
    headers=HEADERS,
    timeout=30
)

response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

product_list = soup.find("product-list")

if not product_list:
    raise Exception("Cannot find product-list")

items_attr = product_list.get(":items")

if not items_attr:
    raise Exception("Cannot find :items attribute")

products = json.loads(items_attr)

rows = []

for product in products:

    book_id = product.get("ProductID", "")

    rows.append({
        "book_id": book_id,
        "title": product.get("ProductName", ""),
        "today_price": product.get("PriceDiscount", ""),
        "full_price": product.get("PriceFull", ""),
        "author": product.get("AuthorName", ""),
        "publisher": product.get("PublisherName", ""),
        "category": product.get("CategoryText", ""),
        "rating": product.get("AverageRating", ""),
        "rating_count": product.get("TotalRating", ""),
        "rank": product.get("Rank", ""),
        "url": f"https://www.naiin.com/product/detail/{book_id}"
    })

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
