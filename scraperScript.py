from playwright.sync_api import sync_playwright
import sqlite3
import datetime

import importBread

def main() :
    run_scraper_script([True, False, True])

def run_scraper_script(optionsList, active_database) :
    urlList = [ # List of Important URL:s
        "https://shop.svenskcater.se/", # Main website
        "https://shop.svenskcater.se/webbshop/starta-bestaellningen/?f=120361&d=131%20Malm%C3%B6",  # Name: Ej Mat
        "https://shop.svenskcater.se/webbshop/starta-bestaellningen/?f=120364&d=131%20Malm%C3%B6",  # Name: Frukt och Grönt
        "https://shop.svenskcater.se/webbshop/starta-bestaellningen/?f=120366&d=131%20Malm%C3%B6",  # Name: Frys
        "https://shop.svenskcater.se/webbshop/starta-bestaellningen/?f=121064&d=131%20Malm%C3%B6",  # Name: Glass
        "https://shop.svenskcater.se/webbshop/starta-bestaellningen/?f=120362&d=131%20Malm%C3%B6",  # Name: Kakor
        "https://shop.svenskcater.se/webbshop/starta-bestaellningen/?f=120368&d=131%20Malm%C3%B6",  # Name: Kolonial
        "https://shop.svenskcater.se/webbshop/starta-bestaellningen/?f=116002&d=131%20Malm%C3%B6",  # Name: Kryddor
        "https://shop.svenskcater.se/webbshop/starta-bestaellningen/?f=116001&d=131%20Malm%C3%B6",  # Name: Kyl
        "https://shop.svenskcater.se/webbshop/starta-bestaellningen/?f=120365&d=131%20Malm%C3%B6",  # Name: Läsk och Dryck
        "https://shop.svenskcater.se/webbshop/starta-bestaellningen/?f=120367&d=131%20Malm%C3%B6"   # Name: Skåp
    ]

    urlCategory = [ # List of Names of the URL:s above
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

    delayButton = 1000  # Time to wait between button-clicks
    # delay = 4000        # Time to wait between jumps to websites
    delayLogin = 30000  # Time to wait after loging in, first time

    # optionsList[0]  = True # executeProductsScrape
    # optionsList[1]  = True # executePriceScrape
    # optionsList[2]  = True # executeImportBread

    # active_database = "hilbertDatabase.db" # Name of active database

    # Step 2: Connect to SQLite (creates file if if doesn't exist)
    error = False
    total_items_scraped = 0
    try :
        with sqlite3.connect(active_database) as conn :
            cursor = conn.cursor()

            if optionsList[0] or optionsList[1] :
                with sync_playwright() as p:
                    browser = p.chromium.launch(headless=False)  # False to see the browser
                    page = browser.new_page()

                    # Navigate to the login page
                    page.goto(urlList[0])

                    # page.wait_for_timeout(delayButton)
                    page.wait_for_selector('#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowallSelection')
                    page.click('#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowallSelection')

                    # page.wait_for_timeout(delayButton)
                    page.wait_for_selector('button:has-text("Jag är 20 år eller äldre.")')
                    page.click('button:has-text("Jag är 20 år eller äldre.")')

                    # page.wait_for_timeout(delayButton)
                    page.wait_for_selector('input[name="user"]')
                    page.fill('input[name="user"]', "K38189")

                    # page.pause()

                    # page.wait_for_timeout(delayLogin)
                    page.wait_for_selector('text="STARTA DIN BESTÄLLNING"', timeout=120000)
                    i = 0
                    for url, categoryName in zip(urlList[1:],urlCategory[1:]) :
                        page.goto(url, wait_until="networkidle")
                        # page.wait_for_timeout(delay)

                        product_wrapper = []
                        while product_wrapper == [] :
                            product_wrapper = page.query_selector_all(".shop-gallery-item-wrapper")
                            if product_wrapper == [] :
                                print("Error fetching products from: ", categoryName)
                                print("Trying fetching again!")
                                page.wait_for_timeout(500)
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

                            if optionsList[0] :
                                cursor.execute('''
                                    INSERT OR REPLACE INTO products (product_id, product_name, product_brand, category_name)
                                    VALUES (?, ?, ?, ?)
                                ''', (productId, name, brandName, categoryName))

                            if optionsList[1] :
                                cursor.execute('''
                                    INSERT INTO price_offers (product_id, offer_price, offer_unit, offer_timestamp)
                                    VALUES (?, ?, ?, ?)
                                ''', (productId, price, unit, timestamp))
                            total_items_scraped += 1
                            # print(f"{i:<4} {productId:<10} {name:<30} {brandName:<20} {price:<10} {unit:<10} {timestamp:<10}")


                        # print("-" * 30)

                    # print(i)
                    browser.close()
    except sqlite3.Error as e :
        print("Something went wrong then inserting information into the database.")
        print("Error:", e)
        print("Canceling the scraping of products and prices.")
        print("")
        error = True

    if optionsList[2] :
        importBread.importBread(active_database)
    if not error :
        print("Total Items Scraped from Svensk Cater: ", total_items_scraped)
        print("Done Scrapeing!")

# main()