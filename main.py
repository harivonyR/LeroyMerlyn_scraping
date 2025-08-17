# -*- coding: utf-8 -*-
"""
Created on Sat Aug 16 16:20:18 2025

@author: harivonyratefiarison
"""

from script.leroymerlin import get_product, get_page


# get products
products_link = get_product()


# get categories
categories_link = get_product(products_link[0])


# loop sub_categories
sub_categories = get_product(categories_link[0])


# get page number link of every page in a subcategorie
pages_link = get_page(sub_categories[0])


# get items from pages_link
