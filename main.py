# -*- coding: utf-8 -*-
"""
Created on Sat Aug 16 16:20:18 2025

@author: harivonyratefiarison
"""

from script.leroymerlin import get_products, get_pages, get_items
from script.util import save_csv, get_last_path_parts
#from tqd import tqdm

# GET ALL PRODUCT CATEGORIES
products_link = get_products()
items = []

for i in range(len(products_link)):
# get categories
    categories_link = get_products(products_link[i])

    for j in range(len(categories_link)):
    # loop sub_categories
        sub_categories = get_products(categories_link[j])
        
        for k in range(len(sub_categories)):
        # get page number link of every page in a subcategorie
            pages_link = get_pages(sub_categories[k])
            
            # LOOP PAGES
            for l in range(len(pages_link)):
                # get items from pages_link
                items_list = get_items(pages_link[l])
                file_name = get_last_path_parts(pages_link[l])
                
                save_csv(items_list,f"output/{file_name[0]}_{file_name[1]}_{file_name[2]}_page{l}.csv")
