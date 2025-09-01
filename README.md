# Leroy Merlin Scraper

This project is a web scraping pipeline that extracts product data from Leroy Merlin’s website.  
It uses a modular approach with dedicated functions to fetch product categories, subcategories, pages, and individual items, then saves the results in CSV format.

---

## Features

- Scrape product categories, subcategories, and paginated pages
- Extract items from each page using custom parsing functions
- Save results as structured CSV files inside the `output/` folder
- Skip already-scraped pages to avoid duplicates

---

## Requirements

This project works with **Python 3.8+**.  
External dependencies must be installed with `pip`:

```bash
pip install requests beautifulsoup4
```

---

## Project Structure

```
├── main.py                  # Entry point
├── script/
│   ├── leroymerlin.py        # get_products, get_pages, get_items
│   ├── util.py               # save_csv, get_last_path_parts
├── credential.example.py     # Example API credential file
├── output/                  # Scraped CSV files (auto-generated)
└── README.md
```

---

## Installation & Usage

### 1. Clone the repository
```bash
git clone https://github.com/harivonyR/LeroyMerlyn_scraping
```

### 2. Open the project folder
```bash
cd LeroyMerlyn_scraping
```

### 3. Create your credential file
Copy the example file:
```bash
copy credential.example.py credential.py
```

Open `credential.py` and paste your **PILOTERR API KEY**:
```python
x_api_key = "paste your API key here !"
```

### 4. Install dependencies
```bash
pip install requests beautifulsoup4
```

### 5. Run the scraper
```bash
python main.py
```

---

## Notes

- The scraper automatically skips files that already exist in `output/`.  
- If a subcategory has no pagination, the scraper moves on.  
