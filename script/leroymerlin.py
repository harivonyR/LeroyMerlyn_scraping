# -*- coding: utf-8 -*-
"""
Created on Sat Aug 16 16:45:08 2025

@author: BEST
"""

from script.piloterr import website_unlocker #website_crawler,
from bs4 import BeautifulSoup
from script.util import get_last_path_parts, write_log, safe_get #is_html
import time


def get_products(url="https://www.leroymerlin.fr/produits/", retries=4, delay=15):
    for attempt in range(1, retries + 1):
        try:
            html_content = website_unlocker(url)
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
                raise ValueError("No product link found\n")
        
        except Exception as e:
            # retry until attemps limit reached
            if attempt < retries:
                print(f"[Attempt] : {attempt} failed : {e}")
                print(f"[Retrying] : (waiting {delay}s before attempt {attempt+1})")
                time.sleep(delay)
            
            # if attempt fail : return empty array, write error in log
            else:
                print(f"[Failed] : error after {retries} attempts. Last error: {e}")
                # écrire dans log pour analyse après scraping
                write_log(url, e, log_file="logs/error_log.txt")
                return []



# sub_categories_url = "https://www.leroymerlin.fr/produits/terrasse-jardin/salon-et-mobilier-de-jardin/salon-de-jardin/"
def get_pages(sub_categories_url, retries=4, delay=15):
    """
    Scrape pagination links for a given subcategory URL.
    
    Returns:
        list: A list of page URLs if pagination exists.
        []  : If HTML response is fetched but no pagination found.
    
    Raises:
        ValueError: If no response is received within the given retries.
    """
    
    print("---------------------------------------")
    print(f"Scraping pages of: {sub_categories_url}")
    
    for attempt in range(1, retries + 1):     
        try:
            
            #html_content = website_crawler(sub_categories_url)
            html_content = website_unlocker(sub_categories_url)
            
            soup = BeautifulSoup(html_content, "html.parser")
            selects = soup.select('select.mc-select.mc-pagination__select.js-selector option')
            
            # Build links with pagination if options exist
            options = [f"{sub_categories_url}?p={i+1}" for i in range(len(selects))] if selects else []
            
            if options:
                print(f"{sub_categories_url} : {len(options)} pages found\n")
                return options
            
            # No pagination found but response was valid
            print('> reponse html but no pagination found !')
            return []
        
        except Exception as e:

            if attempt < retries:
                print(f"[Attempt {attempt}] failed: {e}")
                print(f"[Retrying] in {delay}s (attempt {attempt+1}/{retries})")
                time.sleep(delay)
                
            else:
                print(f"[Failed] Could not fetch product links after {retries} attempts. Last error: {e}")
                return []




# page_url = "https://www.leroymerlin.fr/marques/naterial/salon-et-mobilier-de-jardin-naterial/?p=1"
def get_items(page_url,retries=3,delay=10):
    print("------------------")
    print(f"scraping pages of : {page_url}")
    
    for attempt in range(1, retries + 1):
        
        try:
            #html_content = website_crawler(page_url)
            html_content = website_unlocker(page_url)
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
                    "href":"https://www.leroymerlin.fr"+safe_get(item, ("a", {"class": "a-designation"}), "href"),
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
            # Skip current item and continue
            print(f"[!] Skipping url {page_url} due to error: {e}")
            continue

if __name__ == "__main__":
    product_url = "https://www.leroymerlin.fr/produits/terrasse-jardin/cloture-grillage-occultation/cloture-electrique/"
    categories = get_products(product_url)
    
    #items_url = "https://www.leroymerlin.fr/marques/naterial/salon-et-mobilier-de-jardin-naterial/?p=1"
    
    # scraping fail over 4 attempts
    #items_url ="https://www.leroymerlin.fr/produits/terrasse-jardin/salon-et-mobilier-de-jardin/decouvrez-nos-styles-exterieurs/"
    #items = get_items(items_url)
    
    # try scrape pagination where link don't have
    #sub_categories = "https://www.leroymerlin.fr/produits/terrasse-jardin/salon-et-mobilier-de-jardin/decouvrez-nos-styles-exterieurs/"
    #pages = get_pages(sub_categories)
    
    # try get pages on bot detection test :
    # sometimes test apprear randomly, html response find but no pagination
    #bot_url = "https://www.leroymerlin.fr/produits/terrasse-jardin/salon-et-mobilier-de-jardin/fauteuil-de-jardin/?p=2"
    #bot_pages = get_pages(bot_url)
    
    