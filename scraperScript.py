import requests
from bs4 import BeautifulSoup
import sqlite3
import datetime
import json

# Step 1: Define the URL
URL = "https://www.willys.se/sortiment/kott-chark-och-fagel"

# Step 2: Connect to SQLite (creates file if if doesn't exist)
conn = sqlite3.connect("willys_offers.db")
cursor = conn.cursor()

# Step 3: Create table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS offers (
        id TEXT PRIMARY KEY,
        name TEXT,
        description TEXT,
        price TEXT,
        scraped_at TEXT
    )
''')

headers = {"User-Agent": "Mozilla/5.0"}
respones = requests.get(URL,headers=headers)
soup = BeautifulSoup(respones.text, "html.parser")

# products = soup.select("[data-testid='product']")

text_only = soup.get_text(separator="\n")
# print(respones)
# print(soup.prettify())

with open("output.html", "w", encoding="utf-8") as f:
    f.write(soup.prettify())

url = "https://www.willys.se/c/kott-chark-och-fagel?page=0&size=10"
response = requests.get(url)
data = response.json()

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

# print(data)
products = data['results']
for prod in products :
    name = prod['name']
    price = prod['potentialPromotions'][0]['price']['formattedValue']
    savings = prod['potentialPromotions'][0]['conditionLabel']
    print(f"Product: {name}, Price: {price}, Savings: {savings}")

# print(products)

conn.commit()
conn.close()