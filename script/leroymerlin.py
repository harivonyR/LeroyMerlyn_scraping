# -*- coding: utf-8 -*-
"""
Created on Sat Aug 16 16:45:08 2025

@author: BEST
"""

from script.piloterr import website_crawler
from bs4 import BeautifulSoup
import time


def get_product(url="https://www.leroymerlin.fr/produits/", retries=3, delay=10):
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
                print(f"{url} : {len(links)} products found")
                return links
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


# sub_categories_url = "https://www.leroymerlin.fr/produits/terrasse-jardin/salon-et-mobilier-de-jardin/salon-de-jardin/"
def get_page(sub_categories_url,retries=3,delay=10):
    print("------------------")
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
    
    

if __name__ == "__main__":
    product_url = "https://www.leroymerlin.fr/produits/terrasse-jardin/cloture-grillage-occultation/"
    categories = get_product(product_url)
    