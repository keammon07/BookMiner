import requests
import pandas as pd
import time

SHOP_ID = 119383836
LIMIT = 30

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Accept-Language": "th-TH,th;q=0.9,en;q=0.8",
    "Referer": "https://shopee.co.th/se_ed_officialshop",
    "Origin": "https://shopee.co.th",
}

session = requests.Session()

all_products = []
offset = 0

while True:
    url = (
        "https://shopee.co.th/api/v4/search/search_items"
        f"?by=pop"
        f"&limit={LIMIT}"
        f"&match_id={SHOP_ID}"
        f"&newest={offset}"
        f"&order=desc"
        f"&page_type=shop"
        f"&scenario=PAGE_OTHERSHOP"
        f"&version=2"
    )

    print(f"Loading offset {offset}")

    r = session.get(url, headers=headers, timeout=30)

    print("STATUS:", r.status_code)

    if r.status_code != 200:
        print(r.text[:500])
        break

    data = r.json()
    items = data.get("items", [])

    if not items:
        print("No more items")
        break

    for row in items:
        item = row.get("item_basic", {})

        all_products.append({
            "shop_id": item.get("shopid"),
            "item_id": item.get("itemid"),
            "ชื่อสินค้า": item.get("name"),
            "ราคาเต็ม": item.get("price_before_discount", 0) / 100000,
            "ราคาลด": item.get("price", 0) / 100000,
            "ยอดขาย": item.get("historical_sold", 0),
        })

    offset += LIMIT
    time.sleep(1)

df = pd.DataFrame(all_products)
df.to_excel("SEED_test.xlsx", index=False)

print("Total products:", len(df))
print("Done")
