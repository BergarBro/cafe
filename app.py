import time
import tkinter as tk
from tkinter import *
from tkinter import ttk
import random as rd
import multiprocessing

import plotPrices, scraperScript, get_set_funcs, makeBackupDB
from tooltip import ListboxTooltip

def open_popup_scraper():
    popup_scraper = tk.Toplevel(root)
    popup_scraper.title("Scraping Prices")
    popup_scraper.geometry("300x300")
    
    label_scraper_info = tk.Label(popup_scraper, text="Options for Scraping Prices on SvenskCater:")
    label_scraper_info.pack(pady=10)
    
    # Radio buttons for mutually exclusive choices
    option_vars = {}
    options = ["Fetch Products", "Fetch Prices", "Fetch Bread and Breadprices"]
    for opt in options:
        var = tk.BooleanVar(value=True)
        tk.Checkbutton(popup_scraper, text=opt, variable=var).pack(pady=5)
        option_vars[opt] = var

    def on_ok():
        selected = [var.get() for opt, var in option_vars.items()]

        multiproc_scraper = multiprocessing.Process(
            target=scraperScript.run_scraper_script,
            args=(selected, active_database)
            )
        multiproc_scraper.start()
        popup_scraper.destroy()

    def on_cancel():
        print("You canceled the Scraper")
        popup_scraper.destroy()

    frame_select = tk.Frame(popup_scraper)
    frame_select.pack(pady=5)

    button_scraper_ok = tk.Button(frame_select, text="SCRAPE!", command=on_ok)
    button_scraper_ok.pack(side=tk.LEFT, padx=10)

    button_scraper_cancel = tk.Button(frame_select, text="CANCEL", command=on_cancel)
    button_scraper_cancel.pack(side=tk.LEFT, padx=10)

def open_popup_plotter() :
    global categorys, products, listOfListBoxes, scrollbar
    global activeCategory, activeProducts, search_var, search_entry

    def plot_prices() :
        global categorys, activeCategory, activeProducts
        selectedProductsIndex = listOfListBoxes[activeCategory].curselection()
        selectedProducts = []
        for index in selectedProductsIndex :
            selectedProducts.append(activeProducts[index][0])

        plotPrices.makePricePlot(selectedProducts, active_database)

    def change_category(newCategory) :
        global activeCategory, listOfListBoxes, categorys, activeProducts, scrollbar
        listOfListBoxes[activeCategory].pack_forget()
        listOfListBoxes[newCategory].pack(pady=5)
        activeCategory = newCategory
        activeProducts = products[activeCategory]
        # search_entry.delete(0, tk.END)
        # print(listOfListBoxes[activeCategory].size())
        listOfListBoxes[activeCategory].config(yscrollcommand = scrollbar.set)
        scrollbar.config(command = listOfListBoxes[activeCategory].yview)

    def select_all() :
        global activeCategory, listOfListBoxes
        listOfListBoxes[activeCategory].selection_set(0,listOfListBoxes[activeCategory].size())

    def deselect_all() :
        global activeCategory, listOfListBoxes
        listOfListBoxes[activeCategory].selection_clear(0,listOfListBoxes[activeCategory].size())

    def update_search_category_list() :
        global activeProducts, listOfListBoxes, activeProducts, activeCategory
        search_term = search_entry.get().lower()
        # print(search_term)
        listOfListBoxes[activeCategory].delete(0,tk.END)
        activeProducts = []
        for prod in products[activeCategory] :
            if search_term in prod[0].lower() :
                listOfListBoxes[activeCategory].insert(tk.END, prod[0])
                activeProducts.append(prod)

    def on_close():
        print("You canceled the Plotter.")
        popup_plotter.destroy()

    popup_plotter = tk.Toplevel(root)
    popup_plotter.title("Plotting Prices")
    popup_plotter.geometry("500x500")

    label_plotter_info = tk.Label(popup_plotter, text="Choose products to plot the price over time.")
    label_plotter_info.pack(pady=5)

    # button3 = tk.Button(root, text="Pop-Up",command=test)
    # button3.pack(pady=5)

    frame_search = tk.Frame(popup_plotter)
    frame_search.pack(pady=5)  # You can also use padx here

    # Dropdown options  
    products, categorys = get_set_funcs.getProductsAndCategorys(active_database)

    # Selected option variable  
    opt = StringVar(value=categorys[0])  

    # Dropdown menu  
    dropdown_categorys = tk.OptionMenu(frame_search, opt, *categorys, command=change_category)
    dropdown_categorys.pack(side=tk.LEFT, padx=5)

    search_var = tk.StringVar()
    search_entry = tk.Entry(frame_search, textvariable=search_var)
    # search_entry.insert(0, "Search...")
    search_entry.pack(side=tk.LEFT, padx=5)

    # Buttons packed inside the frame side-by-side
    button_select_all = tk.Button(frame_search, text="Select All", command=select_all)
    button_select_all.pack(side=tk.LEFT, padx=5)

    button_deselect_all = tk.Button(frame_search, text="Deselect All", command=deselect_all)
    button_deselect_all.pack(side=tk.LEFT, padx=5)

    listBox_frame = tk.Frame(popup_plotter)
    listBox_frame.pack(pady=5)

    style = ttk.Style(popup_plotter)
    style.theme_use("clam")

    scrollbar = ttk.Scrollbar(listBox_frame) 
    scrollbar.pack(side = RIGHT, fill = BOTH) 

    listOfListBoxes = {}
    for cat in categorys :
        tempListBox = tk.Listbox(listBox_frame, selectmode='multiple', height=14, width=50)
        for item in products[cat] :
            tempListBox.insert(tk.END, item[0])
        listOfListBoxes[cat] = tempListBox

    activeCategory = categorys[0]
    activeProducts = products[activeCategory]
    listOfListBoxes[activeCategory].pack(side=tk.LEFT)

    listOfListBoxes[activeCategory].config(yscrollcommand = scrollbar.set)
    scrollbar.config(command = listOfListBoxes[activeCategory].yview)

    search_var.trace_add("write", lambda *args: update_search_category_list())

    frame_plot = tk.Frame(popup_plotter)
    frame_plot.pack(pady=5)

    button_plot_prices = tk.Button(frame_plot, text="PLOT!",command=plot_prices)
    button_plot_prices.pack(side=tk.LEFT, padx=10)

    button_plotter_cancel = tk.Button(frame_plot, text="CANCEL", command=on_close)
    button_plotter_cancel.pack(side=tk.LEFT, pady=10)

def create_backup() :
    makeBackupDB.create_backup_of_DB(active_database)

def open_popup_ingredient() :
    global categorys, products, list_of_products_tree, scrollbar, search_products_var, search_ingredients_var
    global activeCategory, activeProducts, search_var, entry_search_products, active_ingrediets, ingredients

    def change_category(newCategory) :
        global activeCategory, list_of_products_tree, categorys, activeProducts, scrollbar
        list_of_products_tree[activeCategory].pack_forget()
        list_of_products_tree[newCategory].pack(pady=5)
        activeCategory = newCategory
        activeProducts = products[activeCategory]
        # search_entry.delete(0, tk.END)
        # print(listOfListBoxes[activeCategory].size())
        list_of_products_tree[activeCategory].config(yscrollcommand = scrollbar_products.set)
        scrollbar_products.config(command = list_of_products_tree[activeCategory].yview)

    def update_search_products_list() :
        global activeProducts, list_of_products_tree, activeProducts, activeCategory
        search_term = entry_search_products.get().lower()
        for item in list_of_products_tree[activeCategory].get_children() :
            list_of_products_tree[activeCategory].delete(item)
        activeProducts = []
        for prod in products[activeCategory] :
            if search_term in prod[0].lower() :
                list_of_products_tree[activeCategory].insert("", tk.END, values=prod)
                activeProducts.append(prod)

    def update_search_ingredients_list() :
        global activeProducts, list_of_products_tree, activeProducts, activeCategory
        search_term = entry_search_ingredients.get().lower()
        # print(search_term)
        for item in tree_ingredient.get_children() :
            tree_ingredient.delete(item)
        for ingr in ingredients :
            if search_term in ingr[0].lower() :
                tree_ingredient.insert("", tk.END, values=ingr)

    def add_ingredient() :
        global ingredients, check
        ingredient_name = entry_add_ingredient_name.get()
        if ingredient_name != "" :
            check = True
            if [item[0] for item in ingredients if item[0] == ingredient_name] != [] :
                popup_add_ingredient = tk.Toplevel(popup_ingredient)
                popup_add_ingredient.title("Update Ingredient?")
                popup_add_ingredient.geometry("300x100")
                
                label_remove_ingredient_info = tk.Label(popup_add_ingredient, text=("That ingredient(", ingredient_name, ")already exist, are you sure you want to update it?"))
                label_remove_ingredient_info.pack(pady=10)

                frame_buttons = tk.Frame(popup_add_ingredient)
                frame_buttons.pack(pady=5)

                # button_remove_ok = tk.Button(frame_buttons, text="UPDATE!",    <-- TODO 
                #                             command= lambda : (
                #                                 check = True, 
                #                                 popup_add_ingredient.destroy()))
                # button_remove_ok.pack(side=tk.LEFT, padx=5)

                button_remove_cancel = tk.Button(frame_buttons, text="CANCEL",
                                                command= lambda : (
                                                    popup_add_ingredient.destroy(),
                                                    update_ingredients()))
                button_remove_cancel.pack(side=tk.LEFT, padx=5)
            ingredient_comment = entry_add_ingredient_comment.get()
            get_set_funcs.set_ingredient(active_database, ingredient_name, ingredient_comment)
            update_ingredients()
            entry_add_ingredient_name.delete(0, tk.END)
            entry_add_ingredient_comment.delete(0, tk.END)

    def remove_ingredient() :
        if (tree_ingredient.item(tree_ingredient.selection())["values"]) != "" :
            popup_remove_ingredient = tk.Toplevel(popup_ingredient)
            popup_remove_ingredient.title("Remove Ingredient?")
            popup_remove_ingredient.geometry("300x100")

            ingredient_to_remove = tree_ingredient.item(tree_ingredient.selection())["values"]
            
            label_remove_ingredient_info = tk.Label(popup_remove_ingredient, text=("Are you sure you want to remove ingredient:\n" + ingredient_to_remove[0]))
            label_remove_ingredient_info.pack(pady=10)

            frame_buttons = tk.Frame(popup_remove_ingredient)
            frame_buttons.pack(pady=5)

            button_remove_ok = tk.Button(frame_buttons, text="REMOVE!", 
                                        command= lambda : (
                                            get_set_funcs.remove_ingredient(active_database, ingredient_to_remove[0]),
                                            popup_remove_ingredient.destroy(),
                                            update_ingredients()))
            button_remove_ok.pack(side=tk.LEFT, padx=5)

            button_remove_cancel = tk.Button(frame_buttons, text="CANCEL",
                                            command= lambda : (
                                                popup_remove_ingredient.destroy(),
                                                update_ingredients()))
            button_remove_cancel.pack(side=tk.LEFT, padx=5)

    def on_link() :
        product_name = list_of_products_tree[activeCategory].item(list_of_products_tree[activeCategory].selection())["values"][0]
        ingredient_name = tree_ingredient.item(tree_ingredient.selection())["values"][0]
        get_set_funcs.link_product_ingredient(active_database, product_name, ingredient_name)
        update_products()

    def on_unlink() :
        product_name = list_of_products_tree[activeCategory].item(list_of_products_tree[activeCategory].selection())["values"][0]
        get_set_funcs.unlink_product_ingredient(active_database, product_name)
        update_products()

    def on_close():
        print("You closed the Ingredient Editor.")
        popup_ingredient.destroy()

    def update_ingredients() :
        global ingredients
        ingredients = get_set_funcs.get_ingredients(active_database)
        update_search_ingredients_list()

    def update_products() :
        global products
        products, x = get_set_funcs.getProductsAndCategorys(active_database)
        update_search_products_list()


    popup_ingredient = tk.Toplevel(root)
    popup_ingredient.title("Ingredient Editor")
    popup_ingredient.geometry("1000x500")

    label_ingredient_info = tk.Label(popup_ingredient, text="Choose a product in the left field, " \
    "then choose an ingredient in the right field, then link them together.\n" \
    "If the ingredient does not exist, create a new one.")
    label_ingredient_info.pack(pady=5)

    # button3 = tk.Button(root, text="Pop-Up",command=test)
    # button3.pack(pady=5)

    frame_main = tk.Frame(popup_ingredient)
    frame_main.pack(pady=5)  # You can also use padx here

    frame_products = tk.Frame(frame_main)
    frame_products.pack(side=tk.LEFT, padx=5)

    frame_ingredients = tk.Frame(frame_main)
    frame_ingredients.pack(side=tk.LEFT, padx=5)

    frame_search_products = tk.Frame(frame_products)
    frame_search_products.pack(pady=5)

    # Dropdown options  
    products, categorys = get_set_funcs.getProductsAndCategorys(active_database) # categorys and porducts include an "All Products" item

    # Selected option variable  
    opt = StringVar(value=categorys[0])  

    # Dropdown menu  
    dropdown_categorys = tk.OptionMenu(frame_search_products, opt, *categorys, command=change_category)
    dropdown_categorys.pack(side=tk.LEFT, padx=5)

    search_products_var = tk.StringVar()
    entry_search_products = tk.Entry(frame_search_products, textvariable=search_products_var)
    entry_search_products.pack(side=tk.LEFT, padx=5)

    listBox_frame = tk.Frame(frame_products)
    listBox_frame.pack(pady=5)

    style = ttk.Style(listBox_frame)
    style.theme_use("clam")

    scrollbar_products = ttk.Scrollbar(listBox_frame) 
    scrollbar_products.pack(side = RIGHT, fill = BOTH) 

    list_of_products_tree = {}
    for cat in categorys :
        temp_tree = ttk.Treeview(listBox_frame, columns=("Product Name", "Linked Ingredient"), show="headings")
        temp_tree.heading("Product Name", text="Product Name")
        temp_tree.heading("Linked Ingredient", text="Linked Ingredient")
        # tempListBox = tk.Listbox(listBox_frame, selectmode='multiple', height=14, width=50)
        for item in products[cat] :
            temp_tree.insert("", tk.END, values=item)
        list_of_products_tree[cat] = temp_tree

    activeCategory = categorys[0]
    activeProducts = products[activeCategory]
    list_of_products_tree[activeCategory].pack(side=tk.LEFT)

    list_of_products_tree[activeCategory].config(yscrollcommand = scrollbar_products.set)
    scrollbar_products.config(command = list_of_products_tree[activeCategory].yview)

    search_products_var.trace_add("write", lambda *args: update_search_products_list())


    search_ingredients_var = tk.StringVar()
    entry_search_ingredients = tk.Entry(frame_ingredients, textvariable=search_ingredients_var)
    entry_search_ingredients.pack(pady=5)

    active_ingrediets = []

    frame_tree_ingredient = tk.Frame(frame_ingredients)
    frame_tree_ingredient.pack(pady=5)

    ingredients = get_set_funcs.get_ingredients(active_database)

    tree_ingredient = ttk.Treeview(frame_tree_ingredient, columns=("Ingredient Name", "Ingredient Comment"), show="headings")
    tree_ingredient.heading("Ingredient Name", text="Ingredient Name")
    tree_ingredient.heading("Ingredient Comment", text="Ingredient Comment")
    tree_ingredient.column("Ingredient Name", width=120)

    for ingr in ingredients:
        tree_ingredient.insert("", tk.END, values=ingr)

    scrollbar_ingredient = ttk.Scrollbar(frame_tree_ingredient) 
    scrollbar_ingredient.pack(side = RIGHT, fill = BOTH)

    tree_ingredient.config(yscrollcommand = scrollbar_ingredient.set)
    scrollbar_ingredient.config(command = tree_ingredient.yview)

    tree_ingredient.pack(expand=True)
    tree_ingredient.pack(pady=5)

    search_ingredients_var.trace_add("write", lambda *args: update_search_ingredients_list())

    frame_add_ingredient = tk.Frame(frame_ingredients)
    frame_add_ingredient.pack(pady=5)

    entry_add_ingredient_name = tk.Entry(frame_add_ingredient)
    entry_add_ingredient_name.pack(side=tk.LEFT, padx=5)

    entry_add_ingredient_comment = tk.Entry(frame_add_ingredient)
    entry_add_ingredient_comment.pack(side=tk.LEFT, padx=5)

    frame_add_ingredient_buttons = tk.Frame(frame_ingredients)
    frame_add_ingredient_buttons.pack(pady=5)

    button_add_ingredient = tk.Button(frame_add_ingredient_buttons, text="Add Ingredient", command=add_ingredient)
    button_add_ingredient.pack(side=tk.LEFT, padx=5)

    button_remove_ingredient = tk.Button(frame_add_ingredient_buttons, text="Remove Ingredient", command=remove_ingredient)
    button_remove_ingredient.pack(side=tk.LEFT, padx=5)

    frame_link_buttons = tk.Frame(popup_ingredient)
    frame_link_buttons.pack(pady=5)

    button_link = tk.Button(frame_link_buttons, text="LINK!", command=on_link)
    button_link.pack(side=tk.LEFT, padx=10)

    button_unlink = tk.Button(frame_link_buttons, text="UNLINK!", command=on_unlink)
    button_unlink.pack(side=tk.LEFT, padx=10)

    button_ingredient_cancel = tk.Button(frame_link_buttons, text="CANCEL", command=on_close)
    button_ingredient_cancel.pack(side=tk.LEFT, pady=10)


if __name__ == "__main__" :
    active_database = "hilbertDatabase.db" # Name of active database

    root = tk.Tk()
    root.title("Hilbot 2000")
    root.geometry("600x600")

    label_info_text = "This is a tool to 'help'/replace mackåsnan..."
    label_info = tk.Label(root, text=label_info_text)
    label_info.pack(pady=5)

    button_open_scraper = tk.Button(root, text="Open Scraper",command=open_popup_scraper)
    button_open_scraper.pack(pady=5)

    button_open_plotter = tk.Button(root, text="Open Plotter",command=open_popup_plotter)
    button_open_plotter.pack(pady=5)

    button_open_backup = tk.Button(root, text="Create Backup of Database", command=create_backup)
    button_open_backup.pack(pady=5)

    button_open_ingredient_editor = tk.Button(root, text="Open Ingredient Editor",command=open_popup_ingredient)
    button_open_ingredient_editor.pack(pady=5)

    # button3 = tk.Button(root, text="Pop-Up",command=test)
    # button3.pack(pady=5)



    # tooltip = ListboxTooltip(listOfListBoxes[activeCategory], get_tooltip_text=lambda i: str(i) + "hej")

    # label2 = tk.Label(root, text="Recored Movment")
    # label2.pack(pady=5)

    # label3 = tk.Label(root, text="Nummber of Clicks: " + str(clickCount))
    # label3.pack(pady=0)

    # button2 = tk.Button(root, text="Start",command=startRecored)
    # button2.pack(pady=5)

    # label4 = tk.Label(root, text="Time Between Clicks: (sek)")
    # label4.pack(pady=0)

    # entry1 = tk.Entry(root, textvariable=timeDelay)
    # #entry1.pack(pady=5)


    root.mainloop()