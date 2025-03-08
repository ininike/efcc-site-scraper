# EFCC Scraper

This script is designed to scrape search results from the EFCC (Economic and Financial Crimes Commission) website using `aiohttp` and `BeautifulSoup`. It performs a search based on a given keyword, extracts relevant information from the search results, and retrieves full article details including images and excerpts.

## Requirements

- Python 3.6+
- aiohttp
- asyncio
- BeautifulSoup4

## Installation

1. Clone the repository or download the `efcc-scraper.py` file.

2. Install the required Python packages using pip:

    ```bash
    pip install aiohttp asyncio beautifulsoup4
    ```

## Usage

1. Ensure that you have Python installed on your system.

2. Run the [efcc-scraper.py](https://github.com/ininike/efcc-site-scraper/blob/main/efcc-scraper.py) script:

    ```bash
    python efcc-scraper.py
    ```

3. The script will perform a search on the EFCC website based on the keyword provided in the search method and print the extracted results.
