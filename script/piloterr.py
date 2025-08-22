# -*- coding: utf-8 -*-
"""
Created on Sat Aug 16 16:24:28 2025

@author: BEST
"""


from credential import x_api_key
import requests
from script.util import save_html

def website_crawler(site_url):
    url = "https://piloterr.com/api/v2/website/crawler"
    
    headers = {"x-api-key": x_api_key}
    querystring = {"query":site_url}
    
    response = requests.request("GET", url, headers=headers,params=querystring)
    
    # decode double escape "\\" and inline "\n" 
    clean_html = response.text.encode('utf-8').decode('unicode_escape')
    
    # decode special character 
    clean_html = clean_html.encode('latin-1').decode('utf-8')
   
    return clean_html


def website_rendering(site_url, wait_in_seconds=5, scroll=0):
    """
    Render a website using Piloterr API.
    Supports optional scroll to bottom.
    """
    url = "https://piloterr.com/api/v2/website/rendering"
    querystring = {"query": site_url, "wait_in_seconds": str(wait_in_seconds)}
    headers = {"x-api-key": x_api_key}  # Assure-toi que x_api_key est défini globalement

    # we don't need to scroll
    if scroll == 0:
        response = requests.get(url, headers=headers, params=querystring)
    
    # with scrolling
    else:
        
        smooth_scroll = [
            {
                "type": "scroll",
                "x": 0,
                "y": 2000,         # scrolling height : 2000 pixels down
                "duration": 3,     # scrolling duration
                "wait_time_s": 4   # wait time in second (s) before the next instruction
            }
        ]

        instruction = {
            "query": site_url,
            "wait_in_seconds": str(wait_in_seconds),
            "browser_instructions": smooth_scroll*scroll
        }

        response = requests.post(url, headers=headers, json=instruction)
    
    # decode double escape "\\" and inline "\n" 
    clean_html = response.text.encode('utf-8').decode('unicode_escape')
    
    # decode special character 
    clean_html = clean_html.encode('latin-1').decode('utf-8')
    
    return clean_html

    
if __name__ == "__main__":
    # redering OK
    LeroyMerlin = "https://www.leroymerlin.fr/produits/terrasse-jardin/cloture-grillage-occultation/"

    response = website_crawler(site_url=LeroyMerlin)
    
    
    #print(response)
    #save_html(response,r"sample/rendering_home.html")
    
    print("test ends !")
