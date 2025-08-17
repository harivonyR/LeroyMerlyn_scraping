# -*- coding: utf-8 -*-
"""
Created on Sat Aug 16 16:20:18 2025

@author: harivonyratefiarison
"""

from script.leroymerlin import get_products, get_pages, get_items


# get products
products_link = get_products()


# get categories
categories_link = get_products(products_link[0])


# loop sub_categories
sub_categories = get_products(categories_link[0])


# get page number link of every page in a subcategorie
pages_link = get_pages(sub_categories[0])


# get items from pages_link
items_list = get_items(pages_link[0])
