from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # False to see the browser
    page = browser.new_page()

    # Navigate to the login page
    page.goto("https://shop.svenskcater.se/")

    page.wait_for_timeout(1000)

    page.click('#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowallSelection')

    page.wait_for_timeout(1000)

    page.click('button:has-text("Jag är 20 år eller äldre.")')

    page.wait_for_timeout(1000)

    page.fill('input[name="user"]', "K38189")

    # page.pause()

    page.wait_for_timeout(30000)

    page.goto("https://shop.svenskcater.se/webbshop/starta-bestaellningen/?f=120362&d=131%20Malm%C3%B6")

    # page.pause()

    page.wait_for_timeout(3000)

    # <div data-v-199eb9a6="" column="xs-12 m-6 l-6 xl-4" class="shop-gallery-item-wrapper"><div data-v-43ac3b2b="" data-v-199eb9a6="" class="ui-card shop-table-product shop-product-thumb shop-search-product gallery-item"><div data-v-43ac3b2b="" class="shop-product-imageload"></div> <div data-v-43ac3b2b="" class="ui-card-image-full"><div data-v-43ac3b2b="" class="productId">46850</div> <!----> <div data-v-43ac3b2b="" class="shop-product-thumb-imageWrapper"><img data-v-43ac3b2b="" src="https://vcd.svenskcater.se/TradeItemImage.aspx?type=web&amp;itemno=46850&amp;filename=07310770111312" class="product-image"></div></div> <div data-v-43ac3b2b="" class="ui-card-content"><div data-v-43ac3b2b="" class="content shop-product-thumb-row"><span data-v-43ac3b2b="" class="shop-item-stock-status"><span class="shop-item-stock-status-wrapper"><svg viewBox="0 0 64 64" class="shop-item-stock-status-svg"><circle r="25%" cx="50%" cy="50%" class="circle-base"></circle> <circle r="25%" cx="50%" cy="50%" class="circle-base product-stock-status-available" style="stroke-dasharray: 11.11, 101;"></circle> <circle r="43%" cx="50%" cy="50%" fill="#fff"></circle></svg> <div class="shop-item-stock-status-text"><div>11</div> <div>HINK</div></div></span> <!----></span> <strong data-v-43ac3b2b=""><a data-v-43ac3b2b="">Aprikosmarmelad 2,3kg</a></strong> <span data-v-43ac3b2b="" class="brand">ÖNOS</span> <span data-v-43ac3b2b="" class="brand">Produktgrupp: Sylt, gele &amp; marmelad         </span> <span data-v-43ac3b2b="" class="brand shop-product-country"></span> <span data-v-43ac3b2b="" class="brand">Lev. Artikelnr.: 454011131</span> <span data-v-43ac3b2b="" class="brand">jmf.pris: 70,24 kr / Kg</span> <!----></div> <div data-v-43ac3b2b="" class="shop-product-table-icons shop-product-thumb-row"><div data-v-4002c3ed="" data-v-43ac3b2b="" class="shop-item-icons"><span data-v-4002c3ed="" title="Kolonial" class="appicon appicon-colonial"></span> <!----> <!----> <!----> <!----> <!----> <!----> <!----> <!----> <!----> <!----> <!----> <!----> <!----> <!----> <!----> <!----> <!----> <!----> <!----> <!----> <!----> <!----> <!----> <!----> <!----> <!----> <!----> <!----> <!----> <!----> <!----> <!----> <!----> <a data-v-4002c3ed="" class="icon-info show-foodinfo tooltip"><span data-v-4002c3ed=""><img data-v-4002c3ed="" src="https://vcd.svenskcater.se/TradeItemImage.aspx?type=web&amp;itemno=46850&amp;filename=07310770111312"></span></a> <!----> <!----> <!----> <!----> <!----></div></div> <div data-v-43ac3b2b="" class="highlight-markings"><div class="highlight-markings-wrapper"></div></div></div> <div data-v-43ac3b2b="" class="shop-product-loggedin-content"><div data-v-43ac3b2b="" class="ui-card-devider"></div> <!----> <div data-v-43ac3b2b="" class="ui-card-content"><div data-v-43ac3b2b="" class="shop-product-thumb-row"><table data-v-43ac3b2b="" class="shop-gallery-item-table"><thead data-v-43ac3b2b=""><tr data-v-43ac3b2b=""><td data-v-43ac3b2b="" class="unit-col"><span data-v-43ac3b2b="" class="notice price-weight-notice">Enhet</span></td> <td data-v-43ac3b2b="" align="right"><span data-v-43ac3b2b="" class="notice price-weight-notice">Pris</span></td></tr></thead> <tbody data-v-43ac3b2b=""><tr data-v-43ac3b2b=""><td data-v-43ac3b2b="" class="unit-col unit-col-one"><span data-v-43ac3b2b="" class="single-unit">HINK (2,3 kg)</span></td> <td data-v-43ac3b2b="" align="right"><div data-v-62377e55="" data-v-43ac3b2b="" class="item-surcharge-wrapper" style="display: none;"><div data-v-62377e55="" title="Inkluderar en avgift för delad förpackning. Köp minst 0 för att undvika avgiften." class="icon-report-problem"></div> <div data-v-62377e55="" class="item-surcharge-warning" style="display: none;">Inkluderar en avgift för delad förpackning. Köp minst 0 för att undvika avgiften.</div></div> <span data-v-43ac3b2b="" class="price-container">161,55 kr</span> <!----></td></tr></tbody></table> <!----></div></div> <div data-v-43ac3b2b="" class="ui-card-devider"></div> <div data-v-43ac3b2b="" class="ui-card-content"><div data-v-43ac3b2b="" class="shop-product-thumb-row shop-product-thumb-footerrow favorites"><div data-v-e4ae22d0="" data-v-43ac3b2b=""><a data-v-e4ae22d0="" class="shop-product-addToFavorites shop-product-addToFavorites-active"><span data-v-e4ae22d0="" class="shop-favorite-list-icon"><span data-v-e4ae22d0="" class="icon-list"></span> <span data-v-e4ae22d0="" class="shop-favorite-checkmarkWrapper"><span data-v-e4ae22d0="" class="icon-checkmark"></span></span></span></a> <!----> <!----></div> <!----> <div data-v-2dd421ab="" data-v-43ac3b2b=""><a data-v-2dd421ab="" class="shop-product-addToBasket ui-button"><span data-v-2dd421ab="" title="" class="shop-favorite-list-icon"><span data-v-2dd421ab="" class="mdi mdi-cart right-5"></span></span> <span data-v-2dd421ab="">Köp</span></a></div> <div data-v-43ac3b2b="" class="shop-product-thumb-quantity-wrapper"><div data-v-468acb0e="" data-v-43ac3b2b="" class="input-wrapper input-number-unit" placeholder="Antal"><input data-v-468acb0e="" tabindex="3" type="text" placeholder="Antal" class="quantity shop-product-thumb-quantity"> <span data-v-468acb0e="">HINK</span></div> <div data-v-43ac3b2b="" class="suggestion-tooltip-wrapper"><!----></div> <!----></div> <div data-v-43ac3b2b="" class="clear"></div></div></div></div></div></div>

    product_wrapper = page.query_selector_all(".shop-gallery-item-wrapper")
    for prod in product_wrapper:
        name = prod.query_selector("strong a")
        brandInfo = prod.query_selector_all(".brand")
        if len(brandInfo) >= 5 :
            relPrice = brandInfo[4]
        
        print("Name:", name.text_content())
        print("Relative Price:", relPrice.text_content())
        # for info in brandInfo :
        #     print(info.text_content())
    print("-" * 30)

    page.goto("https://shop.svenskcater.se/webbshop/starta-bestaellningen/?f=120366&d=131%20Malm%C3%B6")

    page.wait_for_timeout(3000)

    # <div data-v-199eb9a6="" column="xs-12 m-6 l-6 xl-4" class="shop-gallery-item-wrapper"><div data-v-43ac3b2b="" data-v-199eb9a6="" class="ui-card shop-table-product shop-product-thumb shop-search-product gallery-item"><div data-v-43ac3b2b="" class="shop-product-imageload"></div> <div data-v-43ac3b2b="" class="ui-card-image-full"><div data-v-43ac3b2b="" class="productId">46850</div> <!----> <div data-v-43ac3b2b="" class="shop-product-thumb-imageWrapper"><img data-v-43ac3b2b="" src="https://vcd.svenskcater.se/TradeItemImage.aspx?type=web&amp;itemno=46850&amp;filename=07310770111312" class="product-image"></div></div> <div data-v-43ac3b2b="" class="ui-card-content"><div data-v-43ac3b2b="" class="content shop-product-thumb-row"><span data-v-43ac3b2b="" class="shop-item-stock-status"><span class="shop-item-stock-status-wrapper"><svg viewBox="0 0 64 64" class="shop-item-stock-status-svg"><circle r="25%" cx="50%" cy="50%" class="circle-base"></circle> <circle r="25%" cx="50%" cy="50%" class="circle-base product-stock-status-available" style="stroke-dasharray: 11.11, 101;"></circle> <circle r="43%" cx="50%" cy="50%" fill="#fff"></circle></svg> <div class="shop-item-stock-status-text"><div>11</div> <div>HINK</div></div></span> <!----></span> <strong data-v-43ac3b2b=""><a data-v-43ac3b2b="">Aprikosmarmelad 2,3kg</a></strong> <span data-v-43ac3b2b="" class="brand">ÖNOS</span> <span data-v-43ac3b2b="" class="brand">Produktgrupp: Sylt, gele &amp; marmelad         </span> <span data-v-43ac3b2b="" class="brand shop-product-country"></span> <span data-v-43ac3b2b="" class="brand">Lev. Artikelnr.: 454011131</span> <span data-v-43ac3b2b="" class="brand">jmf.pris: 70,24 kr / Kg</span> <!----></div> <div data-v-43ac3b2b="" class="shop-product-table-icons shop-product-thumb-row"><div data-v-4002c3ed="" data-v-43ac3b2b="" class="shop-item-icons"><span data-v-4002c3ed="" title="Kolonial" class="appicon appicon-colonial"></span> <!----> <!----> <!----> <!----> <!----> <!----> <!----> <!----> <!----> <!----> <!----> <!----> <!----> <!----> <!----> <!----> <!----> <!----> <!----> <!----> <!----> <!----> <!----> <!----> <!----> <!----> <!----> <!----> <!----> <!----> <!----> <!----> <!----> <a data-v-4002c3ed="" class="icon-info show-foodinfo tooltip"><span data-v-4002c3ed=""><img data-v-4002c3ed="" src="https://vcd.svenskcater.se/TradeItemImage.aspx?type=web&amp;itemno=46850&amp;filename=07310770111312"></span></a> <!----> <!----> <!----> <!----> <!----></div></div> <div data-v-43ac3b2b="" class="highlight-markings"><div class="highlight-markings-wrapper"></div></div></div> <div data-v-43ac3b2b="" class="shop-product-loggedin-content"><div data-v-43ac3b2b="" class="ui-card-devider"></div> <!----> <div data-v-43ac3b2b="" class="ui-card-content"><div data-v-43ac3b2b="" class="shop-product-thumb-row"><table data-v-43ac3b2b="" class="shop-gallery-item-table"><thead data-v-43ac3b2b=""><tr data-v-43ac3b2b=""><td data-v-43ac3b2b="" class="unit-col"><span data-v-43ac3b2b="" class="notice price-weight-notice">Enhet</span></td> <td data-v-43ac3b2b="" align="right"><span data-v-43ac3b2b="" class="notice price-weight-notice">Pris</span></td></tr></thead> <tbody data-v-43ac3b2b=""><tr data-v-43ac3b2b=""><td data-v-43ac3b2b="" class="unit-col unit-col-one"><span data-v-43ac3b2b="" class="single-unit">HINK (2,3 kg)</span></td> <td data-v-43ac3b2b="" align="right"><div data-v-62377e55="" data-v-43ac3b2b="" class="item-surcharge-wrapper" style="display: none;"><div data-v-62377e55="" title="Inkluderar en avgift för delad förpackning. Köp minst 0 för att undvika avgiften." class="icon-report-problem"></div> <div data-v-62377e55="" class="item-surcharge-warning" style="display: none;">Inkluderar en avgift för delad förpackning. Köp minst 0 för att undvika avgiften.</div></div> <span data-v-43ac3b2b="" class="price-container">161,55 kr</span> <!----></td></tr></tbody></table> <!----></div></div> <div data-v-43ac3b2b="" class="ui-card-devider"></div> <div data-v-43ac3b2b="" class="ui-card-content"><div data-v-43ac3b2b="" class="shop-product-thumb-row shop-product-thumb-footerrow favorites"><div data-v-e4ae22d0="" data-v-43ac3b2b=""><a data-v-e4ae22d0="" class="shop-product-addToFavorites shop-product-addToFavorites-active"><span data-v-e4ae22d0="" class="shop-favorite-list-icon"><span data-v-e4ae22d0="" class="icon-list"></span> <span data-v-e4ae22d0="" class="shop-favorite-checkmarkWrapper"><span data-v-e4ae22d0="" class="icon-checkmark"></span></span></span></a> <!----> <!----></div> <!----> <div data-v-2dd421ab="" data-v-43ac3b2b=""><a data-v-2dd421ab="" class="shop-product-addToBasket ui-button"><span data-v-2dd421ab="" title="" class="shop-favorite-list-icon"><span data-v-2dd421ab="" class="mdi mdi-cart right-5"></span></span> <span data-v-2dd421ab="">Köp</span></a></div> <div data-v-43ac3b2b="" class="shop-product-thumb-quantity-wrapper"><div data-v-468acb0e="" data-v-43ac3b2b="" class="input-wrapper input-number-unit" placeholder="Antal"><input data-v-468acb0e="" tabindex="3" type="text" placeholder="Antal" class="quantity shop-product-thumb-quantity"> <span data-v-468acb0e="">HINK</span></div> <div data-v-43ac3b2b="" class="suggestion-tooltip-wrapper"><!----></div> <!----></div> <div data-v-43ac3b2b="" class="clear"></div></div></div></div></div></div>

    product_wrapper = page.query_selector_all(".shop-gallery-item-wrapper")
    for prod in product_wrapper:
        name = prod.query_selector("strong a")
        brandInfo = prod.query_selector_all(".brand")
        if len(brandInfo) >= 5 :
            relPrice = brandInfo[4]
        
        print("Name:", name.text_content())
        print("Relative Price:", relPrice.text_content())
        # for info in brandInfo :
        #     print(info.text_content())
    print("-" * 30)
    
    # Fill out the login form
    # page.fill("input[name='j_username']", "199807130555")
    # page.fill("input[name='j_password']", "Tesla123")

    # Submit the form
    

    # page.click("button[type='submit']")

    # Wait for successful login (modify selector to match post-login state)

    # page.wait_for_timeout(3000)

    # print(page.content())

    # page.wait_for_selector("text='Mina vanligaste varor'")  # Example, use the actual element

    # Scrape information after logging in
    # content = page.text_content(".name")
    # products = page.query_selector_all('div[itemprop="name"].sc-57d5cc93-6.iKFOfw')
    # for product in products:
    #     print(product.text_content())


    browser.close()
