# -*- coding: utf-8 -*-
"""
Created on Sat Aug 16 16:20:18 2025

@author: harivonyratefiarison
"""

import os
from script.leroymerlin import get_products, get_pages, get_items
from script.util import save_csv, get_last_path_parts
# from tqdm import tqdm  # uncomment if you want progress bar

# GET ALL PRODUCT CATEGORIES
products_link = get_products()
items = []

for i in range(len(products_link)):
    # get categories
    categories_link = get_products(products_link[i])

    for j in range(len(categories_link)):
        # get sub_categories
        sub_categories = get_products(categories_link[j])

        for k in range(len(sub_categories)):
            # get page number links of every page in a subcategory
            
            # manage the case where sub_categories doesn't have pagination
            pages_link = get_pages(sub_categories[k])
            
            if len(pages_link) > 0 :
                # LOOP PAGES
                for l in range(len(pages_link)):
                    scraping_url = get_last_path_parts(pages_link[l])
    
                    output_filename = f"output/{scraping_url[0]}_{scraping_url[1]}_{scraping_url[2]}_page{l+1}.csv"
    
                    # continue loop if file already scraped
                    if os.path.exists(output_filename):
                        continue
    
                    # get items from page
                    items_list = get_items(pages_link[l])
                    save_csv(items_list, output_filename)
            
            # scrape items if sub_categories doesn't have pagination
            else :
                continue
