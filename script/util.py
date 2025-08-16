# -*- coding: utf-8 -*-
"""
Created on Sat Aug 16 16:27:12 2025

@author: BEST
"""

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
