# -*- coding: utf-8 -*-
"""
Created on Sat Aug 16 16:27:12 2025

@author: BEST
"""

import csv
import os
from urllib.parse import urlparse

def save_html(content: str, filename: str = "output.html"):
    """
    Save HTML content to a file.
    
    Parameters:
        content (str): HTML string to save.
        filename (str): Name of the file (default: output.html).
    """
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"HTML saved successfully to {filename}")
    except Exception as e:
        print(f"Error while saving HTML: {e}")


def save_csv(data: list[dict], filename: str = "output/output.csv"):
    """
    Save a list of flat dictionaries into a CSV file.
    
    Args:
        data (list[dict]): List of flat dictionaries
            Example: [{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]
        filename (str): Path to the output CSV file (default: 'output/output.csv')
    """
    if not data:
        raise ValueError("The list is empty, nothing to save.")

    # Create directory if it does not exist
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    # Use keys from the first dictionary to keep column order
    fieldnames = list(data[0].keys())

    # Collect additional keys (if other dicts contain extra fields)
    extra_keys = {k for d in data for k in d.keys()} - set(fieldnames)
    fieldnames.extend(extra_keys)

    # Write the CSV file
    with open(filename, mode="w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
        
        
def get_last_path_parts(url: str, n: int = 4):
    """
    Extract the last n parts of the URL path.
    
    Args:
        url (str): The URL to parse
        n (int): Number of last path elements to extract (default: 4)
    
    Returns:
        list: Last n path elements as a list
    """
    parsed = urlparse(url)
    # Split path, remove empty elements
    parts = [p for p in parsed.path.split("/") if p]
    return parts[-n:]


def is_html(txt_response):
    """
    Check if a response is an HTML string.
    
    Args:
        txt_response: Response content
    
    Returns:
        bool: True if txt_response is a string starting with '<!DOCTYPE html>' or '<html',
              False otherwise
    """
    if isinstance(txt_response, str) and (
        txt_response.lstrip().lower().startswith("<!doctype html>") 
        or txt_response.lstrip().lower().startswith("<html")
    ):
        return True
    return False
