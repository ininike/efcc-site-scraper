from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

DOMAIN = "https://www.efcc.gov.ng"

class EFCCScraper:
    def __init__(self):
        """Initialize the Selenium WebDriver options"""
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_argument("--window-size=1920x1080")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
        self.service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service, options=self.chrome_options)
    
    @staticmethod    
    async def search(self, keyword: str) -> list:
        """Search EFCC site based on a keyword"""
        html = self._get_results(keyword)
        if html:
            results = self._extract_content(html)
            return results
        return []

    def _get_results(self, keyword) -> str | None:
        """Search for the results of the first page"""
        url = f"{DOMAIN}/efcc/other-pages/smart-search?q={keyword}&limit=100"
        try:
            self.driver.get(url)
            time.sleep(5)
            html = self.driver.page_source
            return html
        except Exception as e:
            print("Error:", e)
            return None

    def _extract_content(self, html) -> list:
        """Extract search results"""
        soup = BeautifulSoup(html, 'html.parser')
        results = [
            {
                "type": self._clean_string(result.select_one(".badge:first-of-type").text.strip()),
                "title": result.select_one(".result-title").text.strip(),
                "author": self._clean_string(result.select_one(".badge:nth-of-type(2)").text.strip()),
                "category": self._clean_string(result.select_one(".badge:nth-of-type(3)").text.strip()),
                "date": result.select_one(".result-date").text.strip(),
                "description": result.select_one(".result-text").text.strip(),
                "link": result.select_one(".result-url").text.strip()
            }
            for result in soup.select(".result-item")
        ]
        return results

    def _clean_string(self, text: str) -> str:
        """Clean the string to remove redundant data"""
        parts = text.split(':')
        return parts[1].lstrip()

    def __del__(self):
        """Ensure the WebDriver is properly closed when the object is deleted"""
        self.driver.quit()