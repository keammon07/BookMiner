import requests
import pandas as pd
import time

BASE_URL = "https://mp-api.se-ed.com/web-bff/search-product"

HEADERS = {
"User-Agent": "Mozilla/5.0"
}

CATEGORY_ID = "book-dhijad"
LIMIT = 48

all_books = []
skip = 0

while True:

params = {
    "filter.categoryId": CATEGORY_ID,
    "filter.productTypes": "PRODUCT_TYPE_BOOK_PHYSICAL",
    "option.limit": LIMIT,
    "option.skip": skip,
    "sorter": "PRODUCT_SORTER_POPULAR"
}

print(f"Loading page skip={skip}")

try:
    response = requests.get(
        BASE_URL,
        params=params,
        headers=HEADERS,
        timeout=30
    )

    if response.status_code != 200:
        print(
            f"Finished. API returned status "
            f"{response.status_code} at skip={skip}"
        )
        break

    data = response.json()

except Exception as e:
    print("Request Error:", e)
    break

products = data.get("products", [])

if not products:
    print("No more products.")
    break

for item in products:

    try:

        product_data = item.get("physicalProduct", {})
        product = product_data.get("physicalProduct", {})

        variant = (
            product_data
            .get("extendedOrderProduct", {})
            .get("physical", {})
            .get("variants", [{}])[0]
        )

        sku = ""

        if product.get("variants"):
            sku = product["variants"][0].get("sku", "")

        category_name = ""

        if product.get("category"):
            category_name = product["category"].get("name", "")

        def convert_price(value):
            try:
                return int(value) / 1_000_000
            except:
                return None

        all_books.append({
            "id": product.get("id", ""),
            "name": product.get("name", ""),
            "category": category_name,
            "sku": sku,
            "price": convert_price(
                variant.get("price")
            ),
            "sale_price": convert_price(
                variant.get("priceAfterDiscount")
            ),
            "out_of_stock": product_data.get(
                "outOfStock",
                False
            ),
            "cover": product.get("cover", "")
        })

    except Exception as e:
        print("Parse Error:", e)

skip += LIMIT

time.sleep(0.3)

df = pd.DataFrame(all_books)

df.to_csv(
"se_ed_books.csv",
index=False,
encoding="utf-8-sig"
)

print("=" * 50)
print(f"Total books: {len(df)}")
print("Saved: se_ed_books.csv")
print("=" * 50)
