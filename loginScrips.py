from playwright.sync_api import sync_playwright
import sqlite3
import datetime


urlList = [ # List of Important URL:s
    "https://shop.svenskcater.se/", # Main website
    "https://shop.svenskcater.se/webbshop/starta-bestaellningen/?f=120361&d=131%20Malm%C3%B6", # Name: Ej Mat
    "https://shop.svenskcater.se/webbshop/starta-bestaellningen/?f=120364&d=131%20Malm%C3%B6", # Name: Frukt och Grönt
    "https://shop.svenskcater.se/webbshop/starta-bestaellningen/?f=120366&d=131%20Malm%C3%B6", # Name: Frys
    "https://shop.svenskcater.se/webbshop/starta-bestaellningen/?f=121064&d=131%20Malm%C3%B6", # Name: Glass
    "https://shop.svenskcater.se/webbshop/starta-bestaellningen/?f=120362&d=131%20Malm%C3%B6", # Name: Kakor
    "https://shop.svenskcater.se/webbshop/starta-bestaellningen/?f=120368&d=131%20Malm%C3%B6", # Name: Kolonial
    "https://shop.svenskcater.se/webbshop/starta-bestaellningen/?f=116002&d=131%20Malm%C3%B6", # Name: Kryddor
    "https://shop.svenskcater.se/webbshop/starta-bestaellningen/?f=116001&d=131%20Malm%C3%B6", # Name: Kyl
    "https://shop.svenskcater.se/webbshop/starta-bestaellningen/?f=120365&d=131%20Malm%C3%B6", # Name: Läsk och Dryck
    "https://shop.svenskcater.se/webbshop/starta-bestaellningen/?f=120367&d=131%20Malm%C3%B6"  # Name: Skåp
]

urlName = [ # List of Names of the URL:s above
    "Main Site",
    "Ej Mat",
    "Frukt och Grönt",
    "Frys",
    "Glass",
    "Kakor",
    "Kolonial",
    "Kryddor",
    "Kyl",
    "Läsk och Dryck",
    "Skåp"
]

delayButton = 1000   # Time to wait between button-clicks
delay = 5000        # Time to wait between jumps to websites
delayLogin = 30000  # Time to wait after loging in, first time



# Step 2: Connect to SQLite (creates file if if doesn't exist)
conn = sqlite3.connect("hilbertDatabase.db")
cursor = conn.cursor()

# Step 3: Create table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INT PRIMARY KEY,
        name TEXT NOT NULL,
        brand TEXT
    )
''')

cursor.execute('''       
    CREATE TABLE IF NOT EXISTS prices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        productId INT NOT NULL,
        price DECIMAL(10,2) NOT NULL,
        unit TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (productId) REFERENCES products(id) ON DELETE CASCADE
    )
''')


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # False to see the browser
    page = browser.new_page()

    # Navigate to the login page
    page.goto(urlList[0])

    page.wait_for_timeout(delayButton)

    page.click('#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowallSelection')

    page.wait_for_timeout(delayButton)

    page.click('button:has-text("Jag är 20 år eller äldre.")')

    page.wait_for_timeout(delayButton)

    page.fill('input[name="user"]', "K38189")

    # page.pause()

    page.wait_for_timeout(delayLogin)

    for url, name in zip(urlList[1:],urlName[1:]) :
        page.goto(url)
        page.wait_for_timeout(delay)

        # print("-" * 10 + " " + name + " " + "-" * 10) 
        product_wrapper = page.query_selector_all(".shop-gallery-item-wrapper")
        for product in product_wrapper:
            productId = int(product.query_selector(".productId").text_content())
            name = product.query_selector("strong a").text_content()
            brandInfo = product.query_selector_all(".brand")
            if len(brandInfo) >= 5 :
                brandName = brandInfo[0].text_content()
                priceText = brandInfo[4].text_content()[10:]
            unitLocation = priceText.find("kr")
            price = float(priceText[:unitLocation].replace(",","."))
            unit = priceText[unitLocation:]
            timestamp = datetime.datetime.now().isoformat()

            cursor.execute('''
                INSERT OR REPLACE INTO products (id, name, brand)
                VALUES (?, ?, ?)
            ''', (productId, name, brandName))

            cursor.execute('''
                INSERT OR REPLACE INTO prices (productId, price, unit, timestamp)
                VALUES (?, ?, ?, ?)
            ''', (productId, price, unit, timestamp))

            # print(f"{productId:<10} {name:<30} {brandName:<20} {price:<10} {unit:<10} {timestamp:<10}")

        # print("-" * 30)

    

    browser.close()

conn.commit()
conn.close()

print("Done")