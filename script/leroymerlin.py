# -*- coding: utf-8 -*-
"""
Created on Sat Aug 16 16:45:08 2025

@author: BEST
"""

from script.piloterr import website_crawler
from bs4 import BeautifulSoup


def get_product():
    product = "https://www.leroymerlin.fr/produits/"
    #document.querySelectorAll('a[data-cerberus="ELEM_categoryItem"]')
    
    html_content = website_crawler(product)
    
    soup = BeautifulSoup(html_content, "html.parser")

    links = ["https://www.leroymerlin.fr"+a.get("href") for a in soup.select('a[data-cerberus="ELEM_categoryItem"]') if a.get("href")]
    
    return links

def get_category(product_url):

    html_content = website_crawler(product_url)
    
    soup = BeautifulSoup(html_content, "html.parser")

    links = ["https://www.leroymerlin.fr"+a.get("href") for a in soup.select('a[data-cerberus="ELEM_categoryItem"]') if a.get("href")]
    
    return links


if __name__ == "__main__":
    product_url = "https://www.leroymerlin.fr/produits/terrasse-jardin/cloture-grillage-occultation/"
    categories = get_category(product_url)
    