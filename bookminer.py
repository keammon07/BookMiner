```python
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

    response = requests.get(
        BASE_URL,
        params=params,
        headers=HEADERS,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    products = data.get("products", [])

    if not products:
        print("No more products")
        break

    for item in products:

        try:
            product_data = item["physicalProduct"]
            product = product_data["physicalProduct"]

            variant = (
                product_data
                .get("extendedOrderProduct", {})
                .get("physical", {})
                .get("variants", [{}])[0]
            )

            all_books.append({
                "id": product.get("id", ""),
                "name": product.get("name", ""),
                "category": product.get("category", {}).get("name", ""),
                "sku": product.get("variants", [{}])[0].get("sku", ""),
                "price": int(variant.get("price", 0)) / 1000000,
                "sale_price": int(variant.get("priceAfterDiscount", 0)) / 1000000,
                "out_of_stock": product_data.get("outOfStock", False),
                "cover": product.get("cover", "")
            })

        except Exception as e:
            print("ERROR:", e)

    skip += LIMIT
    time.sleep(0.5)

df = pd.DataFrame(all_books)

df.to_csv(
    "se_ed_books.csv",
    index=False,
    encoding="utf-8-sig"
)

print(f"Done! {len(df)} books saved.")
```
