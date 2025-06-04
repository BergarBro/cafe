import time
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import font
import random as rd
import multiprocessing

import plotPrices, scraperScript, get_set_funcs, makeBackupDB
from tooltip import ListboxTooltip

### Global Helper Functions ###
def make_treeview_with_search(current_frame, heading_names, heading_width = [], tree_names = ["0"]) :
    if heading_width == [] :
        heading_width = [-1] * len(heading_names)

    frame_search = tk.Frame(current_frame)
    frame_search.pack(pady=5)
    
    label_search = tk.Label(frame_search, text="Search:")
    label_search.pack(side="left")

    search_var = tk.StringVar()
    entry_search = ttk.Entry(frame_search, textvariable=search_var)
    entry_search.pack(side="left")

    frame_tree = tk.Frame(current_frame)
    frame_tree.pack(pady=5)

    tree_frames = {}
    trees = {}
    for j in range(len(tree_names)) :
        temp_frame = tk.Frame(frame_tree)
        temp_tree = ttk.Treeview(temp_frame, columns=heading_names, show="headings", selectmode="browse")

        for i in range(len(heading_names)) :
            temp_tree.heading(heading_names[i], text=heading_names[i])
            if heading_width[i] > 0 :
                temp_tree.column(heading_names[i], width=heading_width[i])

        scrollbar = ttk.Scrollbar(temp_frame) 
        scrollbar.pack(side = RIGHT, fill = BOTH)

        temp_tree.config(yscrollcommand = scrollbar.set)
        scrollbar.config(command = temp_tree.yview)

        temp_tree.pack(expand=True)

        tree_frames[tree_names[j]] = temp_frame
        trees[tree_names[j]] = temp_tree

    tree_frames[tree_names[0]].pack()

    return (frame_search, label_search, search_var, trees, tree_frames)

def update_search_in_tree(tree, search_var, list_of_items, index_of_items = []) :
    search_term = search_var.get().lower()
    # print(search_term)
    for i in tree.get_children() :
        tree.delete(i)

    if index_of_items == [] :
        index_of_items = range(len(list_of_items[0]))

    for item in list_of_items :
        if search_term in item[0].lower() :
            tree.insert("", tk.END, values=tuple(item[i] for i in index_of_items))

def make_entry_with_label(current_frame, label_text) :
    frame = ttk.Frame(current_frame)

    label = tk.Label(frame, text=label_text)
    label.pack(side="left")
    
    str_var = tk.StringVar()
    entry = ttk.Entry(frame, textvariable=str_var)
    entry.pack(side="left")

    return (frame, str_var)

def make_popup_window(current_fame, title_text, info_text) :
    def on_ok() :
        window.destroy()

    window = tk.Toplevel(current_fame)
    window.title(title_text)
    window.geometry("300x100")

    label_info = tk.Label(window, text=info_text)
    label_info.pack(pady=5)

    ok_button = ttk.Button(window, text="OK", command=on_ok)
    ok_button.pack(pady=5)
    


### Button Functions ###
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

    button_scraper_ok = ttk.Button(frame_select, text="SCRAPE!", command=on_ok)
    button_scraper_ok.pack(side=tk.LEFT, padx=10)

    button_scraper_cancel = ttk.Button(frame_select, text="CANCEL", command=on_cancel)
    button_scraper_cancel.pack(side=tk.LEFT, padx=10)

def open_popup_plotter() :
    global categorys, products, listOfListBoxes, scrollbar
    global active_category, active_products, search_var

    def plot_prices() :
        global categorys, active_category, active_products
        selectedProductsIndex = listOfListBoxes[active_category].curselection()
        selectedProducts = []
        for index in selectedProductsIndex :
            selectedProducts.append(active_products[index][0])

        plotPrices.makePricePlot(selectedProducts, active_database)

    def change_category(newCategory) :
        global active_category, listOfListBoxes, categorys, active_products, scrollbar
        listOfListBoxes[active_category].pack_forget()
        listOfListBoxes[newCategory].pack(pady=5)
        active_category = newCategory
        active_products = products[active_category]
        # search_entry.delete(0, tk.END)
        # print(listOfListBoxes[active_category].size())
        listOfListBoxes[active_category].config(yscrollcommand = scrollbar.set)
        scrollbar.config(command = listOfListBoxes[active_category].yview)

    def select_all() :
        global active_category, listOfListBoxes
        listOfListBoxes[active_category].selection_set(0,listOfListBoxes[active_category].size())

    def deselect_all() :
        global active_category, listOfListBoxes
        listOfListBoxes[active_category].selection_clear(0,listOfListBoxes[active_category].size())

    def update_search_category_list() :
        global active_products, listOfListBoxes, active_products, active_category
        search_term = search_var.get().lower()
        # print(search_term)
        listOfListBoxes[active_category].delete(0,tk.END)
        active_products = []
        for prod in products[active_category] :
            if search_term in prod[0].lower() :
                listOfListBoxes[active_category].insert(tk.END, prod[0])
                active_products.append(prod)

    def on_close():
        print("You canceled the Plotter.")
        popup_plotter.destroy()

    popup_plotter = tk.Toplevel(root)
    popup_plotter.title("Plotting Prices")
    popup_plotter.geometry("500x500")

    label_plotter_info = tk.Label(popup_plotter, text="Choose products to plot the price over time.")
    label_plotter_info.pack(pady=5)

    # button3 = ttk.Button(root, text="Pop-Up",command=test)
    # button3.pack(pady=5)

    frame_search = tk.Frame(popup_plotter)
    frame_search.pack(pady=5)

    # Dropdown options  
    products, categorys = get_set_funcs.getProductsAndCategorys(active_database)

    # Selected option variable  
    opt = StringVar()  

    # Dropdown menu  
    dropdown_categorys = ttk.OptionMenu(frame_search, opt, categorys[0], *categorys, command=change_category)
    dropdown_categorys.pack(side=tk.LEFT, padx=5)

    frame_entry, search_var = make_entry_with_label(current_frame=frame_search, label_text="Search:")
    frame_entry.pack(side="left")

    # Buttons packed inside the frame side-by-side
    button_select_all = ttk.Button(frame_search, text="Select All", command=select_all)
    button_select_all.pack(side=tk.LEFT, padx=10)

    button_deselect_all = ttk.Button(frame_search, text="Deselect All", command=deselect_all)
    button_deselect_all.pack(side=tk.LEFT, padx=5)

    listBox_frame = tk.Frame(popup_plotter)
    listBox_frame.pack(pady=5)

    # style = ttk.Style(popup_plotter)
    # style.theme_use("clam")

    scrollbar = ttk.Scrollbar(listBox_frame) 
    scrollbar.pack(side = RIGHT, fill = BOTH) 

    listOfListBoxes = {}
    for cat in categorys :
        tempListBox = tk.Listbox(listBox_frame, selectmode='multiple', height=14, width=50)
        for item in products[cat] :
            tempListBox.insert(tk.END, item[0])
        listOfListBoxes[cat] = tempListBox

    active_category = categorys[0]
    active_products = products[active_category]
    listOfListBoxes[active_category].pack(side=tk.LEFT)

    listOfListBoxes[active_category].config(yscrollcommand = scrollbar.set)
    scrollbar.config(command = listOfListBoxes[active_category].yview)

    search_var.trace_add("write", lambda *args: update_search_category_list())

    frame_plot = tk.Frame(popup_plotter)
    frame_plot.pack(pady=5)

    button_plot_prices = ttk.Button(frame_plot, text="PLOT!",command=plot_prices)
    button_plot_prices.pack(side=tk.LEFT, padx=10)

    button_plotter_cancel = ttk.Button(frame_plot, text="CANCEL", command=on_close)
    button_plotter_cancel.pack(side=tk.LEFT, pady=10)

def create_backup() :
    def on_ok():
        makeBackupDB.create_backup_of_DB(active_database)
        popup_backup.destroy()

    def on_cancel():
        print("You canceled the Backup:er")
        popup_backup.destroy()

    popup_backup = tk.Toplevel(root)
    popup_backup.title("Create Backup?")
    popup_backup.geometry("300x100")
    
    label_backup_info = tk.Label(popup_backup, text="Do you want to make a backup of the database?")
    label_backup_info.pack(pady=10)

    frame_select = tk.Frame(popup_backup)
    frame_select.pack(pady=5)

    button_create_backup = ttk.Button(frame_select, text="CREATE BACKUP!", command=on_ok)
    button_create_backup.pack(side=tk.LEFT, padx=10)

    button_cancel = ttk.Button(frame_select, text="CANCEL", command=on_cancel)
    button_cancel.pack(side=tk.LEFT, padx=10)

def open_popup_ingredient() :
    global categorys, products, product_tress, scrollbar, search_products_var, search_ingredients_var, product_frames
    global active_category, search_var, ingredients, tree_ingredient

    def change_category(newCategory) :
        global active_category, product_tress, categorys, scrollbar, product_frames
        product_frames[active_category].pack_forget()
        product_frames[newCategory].pack()
        active_category = newCategory
        update_products()

    def add_ingredient() :
        global ingredients

        def add_new_ingredient(ingredient_name) :
            ingredient_comment = ingredient_comment_var.get()
            get_set_funcs.add_ingredient(active_database, ingredient_name, ingredient_comment)
            update_ingredients()
            ingredient_name_var.set("")
            ingredient_comment_var.set("")

        ingredient_name = ingredient_name_var.get().upper()
        if ingredient_name != "" :
            if [item[0] for item in ingredients if item[0].lower() == ingredient_name.lower()] != [] :
                popup_add_ingredient = tk.Toplevel(popup_ingredient)
                popup_add_ingredient.title("Update Ingredient?")
                popup_add_ingredient.geometry("300x100")

                frame_add_ingredient_info = tk.Frame(popup_add_ingredient)
                
                tk.Label(frame_add_ingredient_info, text="Ingredient ").pack(side="left")
                tk.Label(frame_add_ingredient_info, text=ingredient_name, font=bold_font).pack(side="left")
                tk.Label(frame_add_ingredient_info, text=" already exists."). pack(side="left")
                frame_add_ingredient_info.pack()
                tk.Label(popup_add_ingredient, text="Are you sure you want to update it?").pack(pady=5)

                frame_buttons = tk.Frame(popup_add_ingredient)
                frame_buttons.pack(pady=5)

                button_remove_ok = ttk.Button(frame_buttons, text="UPDATE!",
                                            command= lambda : (
                                                add_new_ingredient(ingredient_name),
                                                popup_add_ingredient.destroy()))
                button_remove_ok.pack(side=tk.LEFT, padx=5)

                button_remove_cancel = ttk.Button(frame_buttons, text="CANCEL",
                                                command= lambda : popup_add_ingredient.destroy())
                button_remove_cancel.pack(side=tk.LEFT, padx=5)
            else :
                add_new_ingredient(ingredient_name)

    def remove_ingredient() :
        if (tree_ingredient.item(tree_ingredient.selection())["values"]) != "" :
            popup_remove_ingredient = tk.Toplevel(popup_ingredient)
            popup_remove_ingredient.title("Remove Ingredient?")
            popup_remove_ingredient.geometry("300x100")

            ingredient_to_remove = tree_ingredient.item(tree_ingredient.selection())["values"]
            
            label_remove_ingredient_info1 = tk.Label(popup_remove_ingredient, text="Are you sure you want to remove Ingredient:")
            label_remove_ingredient_info1.pack()
            label_remove_ingredient_info2 = tk.Label(popup_remove_ingredient, text=ingredient_to_remove[0], font=bold_font)
            label_remove_ingredient_info2.pack(pady=5)

            frame_buttons = tk.Frame(popup_remove_ingredient)
            frame_buttons.pack(pady=5)

            button_remove_ok = ttk.Button(frame_buttons, text="REMOVE!", 
                                        command= lambda : (
                                            get_set_funcs.remove_ingredient(active_database, ingredient_to_remove[0]),
                                            popup_remove_ingredient.destroy(),
                                            update_ingredients()))
            button_remove_ok.pack(side=tk.LEFT, padx=5)

            button_remove_cancel = ttk.Button(frame_buttons, text="CANCEL",
                                            command= lambda : (
                                                popup_remove_ingredient.destroy(),
                                                update_ingredients()))
            button_remove_cancel.pack(side=tk.LEFT, padx=5)

    def on_link() :
        if (tree_ingredient.item(tree_ingredient.selection())["values"]) != "" and (product_tress[active_category].item(product_tress[active_category].selection())["values"]) != "" :
            product_name = product_tress[active_category].item(product_tress[active_category].selection())["values"][0]
            ingredient_name = tree_ingredient.item(tree_ingredient.selection())["values"][0]
            get_set_funcs.link_product_ingredient(active_database, product_name, ingredient_name)
            update_products()

    def on_unlink() :
        if product_tress[active_category].item(product_tress[active_category].selection())["values"] != "" :
            product_name = product_tress[active_category].item(product_tress[active_category].selection())["values"][0]
            get_set_funcs.unlink_product_ingredient(active_database, product_name)
            update_products()

    def on_close():
        print("You closed the Ingredient Editor.")
        popup_ingredient.destroy()

    def update_ingredients() :
        global ingredients, tree_ingredient, search_ingredients_var
        ingredients = get_set_funcs.get_ingredients(active_database)
        print(ingredients)
        update_search_in_tree(tree= tree_ingredient, search_var= search_ingredients_var, list_of_items= ingredients)

    def update_products() :
        global products
        products, x = get_set_funcs.getProductsAndCategorys(active_database)
        update_search_in_tree(tree= product_tress[active_category], search_var= search_products_var, list_of_items= products[active_category])


    popup_ingredient = tk.Toplevel(root)
    popup_ingredient.title("Ingredient Editor")
    popup_ingredient.geometry("1000x500")

    label_ingredient_info = tk.Label(popup_ingredient, text="Choose a product in the left field, " \
    "then choose an ingredient in the right field, then link them together.\n" \
    "If the ingredient does not exist, create a new one.")
    label_ingredient_info.pack(pady=5)

    # button3 = ttk.Button(root, text="Pop-Up",command=test)
    # button3.pack(pady=5)

    frame_main = tk.Frame(popup_ingredient)
    frame_main.pack(pady=5)  # You can also use padx here

    frame_products = tk.Frame(frame_main)
    frame_products.pack(side=tk.LEFT, padx=20)

    frame_ingredients = tk.Frame(frame_main)
    frame_ingredients.pack(side=tk.LEFT)

    frame_search_products = tk.Frame(frame_products)
    frame_search_products.pack(pady=5)

    # Dropdown options  
    products, categorys = get_set_funcs.getProductsAndCategorys(active_database) # categorys and products include an "All Products" category

    search_frame, search_label, search_products_var, product_tress, product_frames = make_treeview_with_search(current_frame= frame_products, 
                                                                                                               heading_names= ("Product Name", "Linked Ingredient"), 
                                                                                                               tree_names= categorys)

    opt = StringVar() 
    dropdown_categorys = ttk.OptionMenu(search_frame, opt, categorys[0], *categorys, command=change_category)
    dropdown_categorys.pack(before=search_label, side=tk.LEFT, padx=20)

    for cat in categorys :
        for item in products[cat] :
            product_tress[cat].insert("", tk.END, values=item)

    active_category = categorys[0]

    search_products_var.trace_add("write", lambda *args: update_search_in_tree(tree= product_tress[active_category],
                                                                               search_var= search_products_var, 
                                                                               list_of_items= products[active_category]))

    frame, label, search_ingredients_var, trees, tree_frames = make_treeview_with_search(current_frame= frame_ingredients, 
                                                                                      heading_names= ("Ingredient Name", "Ingredient Comment"), 
                                                                                      heading_width= (120, -1))
    tree_ingredient = trees["0"]

    update_ingredients()

    search_ingredients_var.trace_add("write", lambda *args: update_search_in_tree(tree= tree_ingredient, 
                                                                                  search_var= search_ingredients_var, 
                                                                                  list_of_items= ingredients))

    frame_add_ingredient = tk.Frame(frame_ingredients)
    frame_add_ingredient.pack(pady=5)

    frame_name, ingredient_name_var = make_entry_with_label(current_frame=frame_add_ingredient, label_text="Name:")
    frame_name.pack(side="left")

    frame_comment, ingredient_comment_var = make_entry_with_label(current_frame=frame_add_ingredient, label_text="    Comment:")
    frame_comment.pack(side="left")

    frame_add_ingredient_buttons = tk.Frame(frame_ingredients)
    frame_add_ingredient_buttons.pack(pady=5)

    button_add_ingredient = ttk.Button(frame_add_ingredient_buttons, text="Add Ingredient", command=add_ingredient)
    button_add_ingredient.pack(side=tk.LEFT, padx=5)

    button_remove_ingredient = ttk.Button(frame_add_ingredient_buttons, text="Remove Ingredient", command=remove_ingredient)
    button_remove_ingredient.pack(side=tk.LEFT, padx=5)

    frame_link_buttons = tk.Frame(popup_ingredient)
    frame_link_buttons.pack(pady=5)

    button_link = ttk.Button(frame_link_buttons, text="LINK!", command=on_link)
    button_link.pack(side=tk.LEFT, padx=10)

    button_unlink = ttk.Button(frame_link_buttons, text="UNLINK!", command=on_unlink)
    button_unlink.pack(side=tk.LEFT, padx=10)

    button_ingredient_cancel = ttk.Button(frame_link_buttons, text="CANCEL", command=on_close)
    button_ingredient_cancel.pack(side=tk.LEFT, pady=10)

def open_popup_recipe() :
    global frame_sandwich, frame_mixture, search_mixture_var, mixtures, tree_mixture, mixture_name_var

    def create_new_mixture() :
        global mixtures, tree_mixture

        name_of_new_mixture = "NEW MIXTURE"
        nbr_of_sandwiches = 0

        get_set_funcs.add_mixture(active_database, name_of_new_mixture, nbr_of_sandwiches)
        update_mixture_tree()
        for i in tree_mixture.get_children() :
            if tree_mixture.item(i, "values")[0] == name_of_new_mixture :
                tree_mixture.selection_set(i)
                tree_mixture.see(i)
                break
        select_mixture(event=EventType)

    def remove_mixture() :
        if (tree_mixture.item(tree_mixture.selection())["values"]) != "" :
            popup_remove_mixture = tk.Toplevel(popup_recipe)
            popup_remove_mixture.title("Remove Mixture?")
            popup_remove_mixture.geometry("300x100")

            mixture_to_remove = tree_mixture.item(tree_mixture.selection(),"values")[0]
            
            label_remove_mixture_info1 = tk.Label(popup_remove_mixture, text="Are you sure you want to remove Mixture:")
            label_remove_mixture_info1.pack()
            label_remove_mixture_info2 = tk.Label(popup_remove_mixture, text=mixture_to_remove, font=bold_font)
            label_remove_mixture_info2.pack(pady=5)

            frame_buttons = tk.Frame(popup_remove_mixture)
            frame_buttons.pack(pady=5)

            button_remove_ok = ttk.Button(frame_buttons, text="REMOVE!", 
                                        command= lambda : (
                                            get_set_funcs.remove_mixture(active_database, mixture_to_remove),
                                            popup_remove_mixture.destroy(),
                                            update_mixture_tree(),
                                            mixture_name_var.set(""),
                                            mixture_nbr_sand_var.set("")))
            button_remove_ok.pack(side=tk.LEFT, padx=5)

            button_remove_cancel = ttk.Button(frame_buttons, text="CANCEL",
                                            command= lambda : (
                                                popup_remove_mixture.destroy(),
                                                update_mixture_tree()))
            button_remove_cancel.pack(side=tk.LEFT, padx=5)

    # def on_close():
    #     print("You closed the Ingredient Editor.")
    #     popup_ingredient.destroy()

    def update_mixture_tree() :
        global mixtures, tree_mixture
        mixtures = get_set_funcs.get_mixtures(active_database)
        # print(mixtures)
        tree_mixture.selection_remove(tree_mixture.selection())
        update_search_in_tree(tree=tree_mixture, search_var=search_mixture_var, list_of_items= mixtures, index_of_items=[0,1])

    def update_mixture() :
        global tree_mixture
        if tree_mixture.item(tree_mixture.selection(), "values") != "" :
            mixture_name_old = tree_mixture.item(tree_mixture.selection(), "values")[0]
            mixture_name_new = mixture_name_var.get().upper()
            if not mixture_nbr_sand_var.get().isnumeric() :
                make_popup_window(current_fame=popup_recipe, title_text="Not A Nummber!", info_text="Number of Sandwiches has to be a nummber!")
                mixture_nbr_sand_var.set("")
            else :
                mixture_nbr_sand = int(mixture_nbr_sand_var.get())
                mixture_instructions = mixture_instructions_var.get()
                get_set_funcs.update_mixture(active_database, mixture_name_old, mixture_name_new, mixture_nbr_sand, mixture_instructions)
                update_mixture_tree()


    def select_mixture(event) :
        global tree_mixture
        selected_mixture = tree_mixture.item(tree_mixture.selection(), "values")
        # print(temp)
        if selected_mixture != [] :
            mixture_name = selected_mixture[0]
            for mix in mixtures :
                if mix[0] == mixture_name :
                    mixture_name_var.set(mix[0])
                    mixture_nbr_sand_var.set(mix[1])
                    mixture_instructions_var.set(mix[2])

    def update_ingredients(current_ingredients) :
        update_search_in_tree(tree=tree_ingredient_list, search_var=ingredient_search_var, list_of_items=current_ingredients, index_of_items=[0])


    popup_recipe = tk.Toplevel(root)
    popup_recipe.title("Recipe Editor")
    popup_recipe.geometry("1000x500")

    label_ingredient_info = tk.Label(popup_recipe, text="Make Recipe...")
    label_ingredient_info.pack(pady=5)

    frame_select = tk.Frame(popup_recipe)
    frame_select.pack(pady=5)

    intVar = tk.IntVar()
    intVar.set(1)

    radio_mixture = tk.Radiobutton(frame_select, text = "Make Mixture Recipe", variable = intVar, value=1, 
                                    command= lambda : (
                                        frame_sandwich.pack_forget(),
                                        frame_mixture.pack()
                                    ))
    radio_mixture.pack(side=tk.LEFT, padx=10)

    radio_sandwich = tk.Radiobutton(frame_select, text = "Make Sandwich Recipe", variable = intVar, value=2,
                                    command= lambda : (
                                        frame_mixture.pack_forget(),
                                        frame_sandwich.pack()
                                    ))
    radio_sandwich.pack(side=tk.LEFT, padx=10)

    frame_mixture = tk.Frame(popup_recipe)
    frame_mixture.pack()

    frame_sandwich = tk.Frame(popup_recipe)

    frame_mixture_select = tk.Frame(frame_mixture)
    frame_mixture_select.pack(side=tk.LEFT, padx=20)


    frame, label, search_mixture_var, trees, tree_frames = make_treeview_with_search(current_frame=frame_mixture_select, 
                                                                              heading_names= ("Mixture Name","Nummber of Sandwiches") , 
                                                                              heading_width= (150,150))
    tree_mixture = trees["0"]

    update_mixture_tree()

    search_mixture_var.trace_add("write", lambda *args: update_search_in_tree(tree=tree_mixture, 
                                                                              search_var=search_mixture_var, 
                                                                              list_of_items= mixtures))

    frame_add_mixture = tk.Frame(frame_mixture_select)
    frame_add_mixture.pack(pady=5)

    button_add_mixture = ttk.Button(frame_add_mixture, text="Create New Mixture", command=create_new_mixture)
    button_add_mixture.pack(side=tk.LEFT, padx=10)

    button_remove_mixture = ttk.Button(frame_add_mixture, text="Remove Mixture", command=remove_mixture)
    button_remove_mixture.pack(side=tk.LEFT, padx=5)


    frame_mixture_ingredients = tk.Frame(frame_mixture)
    frame_mixture_ingredients.pack(side=tk.LEFT, padx=20)

    frame_mixture_name, mixture_name_var = make_entry_with_label(current_frame=frame_mixture_ingredients, label_text="Name:")
    frame_mixture_name.pack(pady=5)

    frame_mixture_nbr_sand, mixture_nbr_sand_var = make_entry_with_label(current_frame=frame_mixture_ingredients, label_text="Number of Sandwiches(st):")
    frame_mixture_nbr_sand.pack(pady=5)

    frame_mixture_instructions, mixture_instructions_var = make_entry_with_label(current_frame=frame_mixture_ingredients, label_text="Instructions:")
    frame_mixture_instructions.pack(pady=5)

    search_frame, label, ingredient_search_var, trees, tree_frames = make_treeview_with_search(current_frame=frame_mixture_ingredients, 
                                                                              heading_names= ("Ingredient List", "Amount", "Unit") , 
                                                                              heading_width= (250,100,50))
    search_frame.pack_forget()
    tree_ingredient_list = trees["0"]

    ingredients = get_set_funcs.get_ingredients(active_database)
    update_ingredients(ingredients)

    tree_mixture.bind("<ButtonRelease-1>", select_mixture)

    button_update_mixture = ttk.Button(frame_mixture_ingredients, text="Update Mixture", command=update_mixture)
    button_update_mixture.pack(pady=5)

    # frame_products = tk.Frame(frame_main)
    # frame_products.pack(side=tk.LEFT, padx=20)

    # frame_ingredients = tk.Frame(frame_main)
    # frame_ingredients.pack(side=tk.LEFT)

    # frame_search_products = tk.Frame(frame_products)
    # frame_search_products.pack(pady=5)
    
    # frame_search_ingredients = tk.Frame(frame_ingredients)
    # frame_search_ingredients.pack(pady=5)

    # # Dropdown options  
    # products, categorys = get_set_funcs.getProductsAndCategorys(active_database) # categorys and products include an "All Products" category

    # # Selected option variable  
    # opt = StringVar()  

    # # Dropdown menu  
    # dropdown_categorys = ttk.OptionMenu(frame_search_products, opt, categorys[0], *categorys, command=change_category)
    # dropdown_categorys.pack(side=tk.LEFT, padx=20)

    # label_search_products = tk.Label(frame_search_products, text="Search:")
    # label_search_products.pack(side=tk.LEFT)

    # search_products_var = tk.StringVar()
    # entry_search_products = ttk.Entry(frame_search_products, textvariable=search_products_var)
    # entry_search_products.pack(side=tk.LEFT)

    # listBox_frame = tk.Frame(frame_products)
    # listBox_frame.pack(pady=5)

    # # style = ttk.Style(listBox_frame)
    # # style.theme_use("clam")

    # scrollbar_products = ttk.Scrollbar(listBox_frame) 
    # scrollbar_products.pack(side = RIGHT, fill = BOTH) 

    # list_of_products_tree = {}
    # for cat in categorys :
    #     temp_tree = ttk.Treeview(listBox_frame, columns=("Product Name", "Linked Ingredient"), show="headings")
    #     temp_tree.heading("Product Name", text="Product Name")
    #     temp_tree.heading("Linked Ingredient", text="Linked Ingredient")
    #     # tempListBox = tk.Listbox(listBox_frame, selectmode='multiple', height=14, width=50)
    #     for item in products[cat] :
    #         temp_tree.insert("", tk.END, values=item)
    #     list_of_products_tree[cat] = temp_tree

    # active_category = categorys[0]
    # active_products = products[active_category]
    # list_of_products_tree[active_category].pack(side=tk.LEFT)

    # list_of_products_tree[active_category].config(yscrollcommand = scrollbar_products.set)
    # scrollbar_products.config(command = list_of_products_tree[active_category].yview)

    # search_products_var.trace_add("write", lambda *args: update_search_products_list())

    # label_search_ingredients = tk.Label(frame_search_ingredients, text="Search:")
    # label_search_ingredients.pack(side=tk.LEFT)

    # search_ingredients_var = tk.StringVar()
    # entry_search_ingredients = ttk.Entry(frame_search_ingredients, textvariable=search_ingredients_var)
    # entry_search_ingredients.pack(side=tk.LEFT)

    # active_ingrediets = []

    # frame_tree_ingredient = tk.Frame(frame_ingredients)
    # frame_tree_ingredient.pack(pady=5)

    # ingredients = get_set_funcs.get_ingredients(active_database)

    # tree_ingredient = ttk.Treeview(frame_tree_ingredient, columns=("Ingredient Name", "Ingredient Comment"), show="headings")
    # tree_ingredient.heading("Ingredient Name", text="Ingredient Name")
    # tree_ingredient.heading("Ingredient Comment", text="Ingredient Comment")
    # tree_ingredient.column("Ingredient Name", width=120)

    # for ingr in ingredients:
    #     tree_ingredient.insert("", tk.END, values=ingr)

    # scrollbar_ingredient = ttk.Scrollbar(frame_tree_ingredient) 
    # scrollbar_ingredient.pack(side = RIGHT, fill = BOTH)

    # tree_ingredient.config(yscrollcommand = scrollbar_ingredient.set)
    # scrollbar_ingredient.config(command = tree_ingredient.yview)

    # tree_ingredient.pack(expand=True)
    # tree_ingredient.pack(pady=5)

    # search_ingredients_var.trace_add("write", lambda *args: update_search_ingredients_list())

    # frame_add_ingredient = tk.Frame(frame_ingredients)
    # frame_add_ingredient.pack(pady=5)

    # label_name_ingredients = tk.Label(frame_add_ingredient, text="Name:")
    # label_name_ingredients.pack(side=tk.LEFT)

    # entry_add_ingredient_name = ttk.Entry(frame_add_ingredient)
    # entry_add_ingredient_name.pack(side=tk.LEFT)

    # label_comment_ingredients = tk.Label(frame_add_ingredient, text="    Comment:")
    # label_comment_ingredients.pack(side=tk.LEFT)

    # entry_add_ingredient_comment = ttk.Entry(frame_add_ingredient)
    # entry_add_ingredient_comment.pack(side=tk.LEFT)

    # frame_add_ingredient_buttons = tk.Frame(frame_ingredients)
    # frame_add_ingredient_buttons.pack(pady=5)

    # button_add_ingredient = ttk.Button(frame_add_ingredient_buttons, text="Add Ingredient", command=add_ingredient)
    # button_add_ingredient.pack(side=tk.LEFT, padx=5)

    # button_remove_ingredient = ttk.Button(frame_add_ingredient_buttons, text="Remove Ingredient", command=remove_ingredient)
    # button_remove_ingredient.pack(side=tk.LEFT, padx=5)

    # frame_link_buttons = tk.Frame(popup_ingredient)
    # frame_link_buttons.pack(pady=5)

    # button_link = ttk.Button(frame_link_buttons, text="LINK!", command=on_link)
    # button_link.pack(side=tk.LEFT, padx=10)

    # button_unlink = ttk.Button(frame_link_buttons, text="UNLINK!", command=on_unlink)
    # button_unlink.pack(side=tk.LEFT, padx=10)

    # button_ingredient_cancel = ttk.Button(frame_link_buttons, text="CANCEL", command=on_close)
    # button_ingredient_cancel.pack(side=tk.LEFT, pady=10)



if __name__ == "__main__" :
    active_database = "hilbertDatabase.db" # Name of active database
    bold_font = ("Segoe UI", 10, "bold")
    bigger_font = ("Segoe UI", 12)

    root = tk.Tk()
    root.title("Hilbot 2000")
    root.geometry("600x600")

    style = ttk.Style(root)
    style.theme_use("clam")

    label_info = tk.Label(root, text="This is a tool to help/replace mackåsnan...", font=bigger_font)
    label_info.pack(pady=5)

    button_open_scraper = ttk.Button(root, text="Open Scraper",command=open_popup_scraper)
    button_open_scraper.pack(pady=5)

    button_open_plotter = ttk.Button(root, text="Open Plotter",command=open_popup_plotter)
    button_open_plotter.pack(pady=5)

    button_open_backup = ttk.Button(root, text="Create Backup of Database", command=create_backup)
    button_open_backup.pack(pady=5)

    button_open_ingredient_editor = ttk.Button(root, text="Open Ingredient Editor",command=open_popup_ingredient)
    button_open_ingredient_editor.pack(pady=5)

    button_open_recipe_editor = ttk.Button(root, text="Open Recipe Editor",command=open_popup_recipe)
    button_open_recipe_editor.pack(pady=5)

    # button3 = ttk.Button(root, text="Pop-Up",command=test)
    # button3.pack(pady=5)



    # tooltip = ListboxTooltip(listOfListBoxes[active_category], get_tooltip_text=lambda i: str(i) + "hej")

    # label2 = tk.Label(root, text="Recored Movment")
    # label2.pack(pady=5)

    # label3 = tk.Label(root, text="Nummber of Clicks: " + str(clickCount))
    # label3.pack(pady=0)

    # button2 = ttk.Button(root, text="Start",command=startRecored)
    # button2.pack(pady=5)

    # label4 = tk.Label(root, text="Time Between Clicks: (sek)")
    # label4.pack(pady=0)

    # entry1 = ttk.Entry(root, textvariable=timeDelay)
    # #entry1.pack(pady=5)


    root.mainloop()