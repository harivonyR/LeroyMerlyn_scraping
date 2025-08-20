# -*- coding: utf-8 -*-
"""
Created on Sat Aug 16 16:45:08 2025

@author: BEST
"""

from script.piloterr import website_crawler
from bs4 import BeautifulSoup
from script.util import get_last_path_parts
import time


def get_products(url="https://www.leroymerlin.fr/produits/", retries=4, delay=15):
    """
    Fetch product links with retry mechanism :
        - Attempt scraping until link are fetched,
        - Rise error if 3 attempts fail
    """
    
    for attempt in range(1, retries + 1):
        try:
            html_content = website_crawler(url)
            soup = BeautifulSoup(html_content, "html.parser")

            links = [
                "https://www.leroymerlin.fr" + a.get("href")
                for a in soup.select('a[data-cerberus="ELEM_categoryItem"]')
                if a.get("href")
            ]

            if links:
                print(f"{url} : {len(links)} products found\n")
                return links
            else:
                raise ValueError("[error] : No product links found\n")
        
        except Exception as e:
            if attempt < retries:
                print(f"[Attempt] : {attempt} failed : {e}")
                print(f"[Retrying] : (waiting {delay}s before attempt {attempt+1})")
                time.sleep(delay)
            else:
                raise ValueError(
                    f" [Failed] : attempt failed, fetch product links error after {retries} attempts. Last error: {e}"
                )


# sub_categories_url = "https://www.leroymerlin.fr/produits/terrasse-jardin/salon-et-mobilier-de-jardin/salon-de-jardin/"
def get_pages(sub_categories_url,retries=4, delay=15):
    print("---------------------------------------")
    print(f"scraping pages of : {sub_categories_url}")
    
    for attempt in range(1, retries + 1):
        
        try:
            html_content = website_crawler(sub_categories_url)
            soup = BeautifulSoup(html_content, "html.parser")

            selects = soup.select('select.mc-select.mc-pagination__select.js-selector option')
            
            # 1- check how many options there is in the "pagination field"
            # 2- build link with pagination as get parameters
            options = [f"{sub_categories_url}?p={i+1}" for i in range(len(selects)) if selects]
            
            if options:
                print(f"{sub_categories_url} : {len(options)} pages found\n\n")
                
                return options
            
            else:
                raise ValueError("No product links found")
        
        except Exception as e:
            if attempt < retries:
                print(f"[Attempt] : {attempt} failed : {e}")
                print(f"[Retrying] : (waiting {delay}s before attempt {attempt+1})")
                time.sleep(delay)
                
            else:
                raise ValueError(
                    f" [Attempt] : failed fetch product links after {retries} attempts. Last error: {e}"
                )

# we need safe_get since items can have some missing information
def safe_get(item, selector, attr=None, default=""):
    """
    Manage exception :
    - selector : 
        ("tag", "class") 
        or ("tag", {"class": "...", "data-cerberus": "..."})
    - attr : attribute name (ex: "title") or None for .get_text()
    """
    tag_name, selector_arg = selector

    if isinstance(selector_arg, dict):
        tag = item.find(tag_name, attrs=selector_arg)
    else:  # string or None → géré comme class_
        tag = item.find(tag_name, class_=selector_arg)

    if not tag:
        return default
    if attr:
        return tag.get(attr, default)
    
    return tag.get_text(strip=True)


# page_url = "https://www.leroymerlin.fr/marques/naterial/salon-et-mobilier-de-jardin-naterial/?p=1"
def get_items(page_url,retries=3,delay=10):
    print("------------------")
    print(f"scraping pages of : {page_url}")
    
    for attempt in range(1, retries + 1):
        
        try:
            html_content = website_crawler(page_url)
            soup = BeautifulSoup(html_content, "html.parser")

            items = soup.select('li>article')
            
            # 1- check how many options there is in the "pagination field"
            # 2- build link with pagination as get parameters
            items_list = []
            
            scraping_url = get_last_path_parts(page_url)

            for i in range(len(items)):
                item = items[i]
                data = {
                    "title": safe_get(item, ("a", {"class": "a-designation"}), "title"),
                    "vendor": safe_get(item, ("span", {"class": "a-vendor__name"})),
                    "reviews": safe_get(item, ("span", {"class": "mc-stars-result__text"})),
                    "delivery": safe_get(item, ("span", {"class": "stock-status_label"})),
                    "discount": safe_get(item, ("span", {"class": "a-flag__label"})),
                    "old_price": safe_get(item, ("span", {"class": "m-price__line","data-cerberus":"CROSSED_PRICE"})),
                    "price" : safe_get(item, ("span", {"class": "m-price__line","data-cerberus":"ELEM_PRIX"})),
                    "price_info": safe_get(item, ("div", {"class": "m-price__legals"})),
                    "stock": safe_get(item, ("span", {"class": "stock-status_label"})),
                    "picture": safe_get(item, ("picture", {"data-class": "a-illustration__img"}),"data-iesrc"),
                    "product": scraping_url[1] if len(scraping_url) > 1 else "",
                    "categories": scraping_url[2] if len(scraping_url) > 2 else "",
                    "sub_categories": scraping_url[3] if len(scraping_url) > 3 else ""
                }
                items_list.append(data)
                
            if items_list:
                print(f"[item scraping] : {len(items_list)} items found !\n\n")
                
                return items_list
            
            else:
                raise ValueError("[!] No item found ! ")
        
        except Exception as e:
            if attempt < retries:
                print(f"[Attempt] : {attempt} failed : {e}")
                print(f"[Retrying] : (waiting {delay}s before attempt {attempt+1})")
                time.sleep(delay)
                
            else:
                raise ValueError(
                    f" [Attempt] : failed fetch product links after {retries} attempts. Last error: {e}"
                )

if __name__ == "__main__":
    #product_url = "https://www.leroymerlin.fr/produits/terrasse-jardin/cloture-grillage-occultation/"
    #categories = get_products(product_url)
    
    # debug
    #items_url = "https://www.leroymerlin.fr/marques/naterial/salon-et-mobilier-de-jardin-naterial/?p=1"
    items_url ="https://www.leroymerlin.fr/produits/terrasse-jardin/salon-et-mobilier-de-jardin/decouvrez-nos-styles-exterieurs/"
    items = get_items(items_url)
    