import pandas as pd
from datetime import datetime

today = datetime.now().strftime("%Y-%m-%d")

data = [
    {
        "วันที่ดึงข้อมูล": today,
        "ร้าน": "TEST",
        "item_id": 123,
        "model_id": 456,
        "ชื่อสินค้า": "ทดสอบ",
        "ราคาเต็ม": 100,
        "ราคาลด": 80,
        "%ลด": 20,
        "ยอดขาย": 1000,
        "ลิงก์สินค้า": "https://example.com"
    }
]

df = pd.DataFrame(data)

with pd.ExcelWriter("BookPrice.xlsx", engine="openpyxl") as writer:
    df.to_excel(writer, sheet_name="AllProducts", index=False)

print("BookPrice.xlsx created")
