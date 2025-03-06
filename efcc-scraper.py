import aiohttp
import asyncio
from bs4 import BeautifulSoup
import re

DOMAIN = "https://www.efcc.gov.ng"

class EFCCScraper:
    def __init__(self):
        pass
        
    def search(self, keyword: str) -> list:
        """run search in an event loop"""
        results = asyncio.run(self._search(keyword))
        return results
       
    async def _search(self, keyword) -> list:
        """Search EFCC site based on a keyword"""
        async with aiohttp.ClientSession() as session:
            html = await self._get_results(keyword, session)
            if html:
                results = self._extract_content(html)
                tasks = [self._async_task(result, session) for result in results]
                results = await asyncio.gather(*tasks)
                return results
            return []

    async def _get_results(self, keyword, session) -> str | None:
        """Search for the results of the first page"""
        url = f"{DOMAIN}/efcc/other-pages/smart-search?q={keyword}&limit=100"
        try:
            async with session.get(url) as response:
                html = await response.text()
                return html
        except Exception as e:
            print("Error:", e)
            return None
        
    async def _async_task(self, result, session) -> dict:
        """Get the full article details from the link"""
        link = result['link']
        article = await self._get_article(link, session)
        if article:
            data = self._extract_images_and_excerpt(article)
            result.update(data)
        return result
        
    async def _get_article(self, link, session) -> str | None:
        """Get the full article from the link"""
        try:
            async with session.get(link) as response:
                html = await response.text()
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
                "link": result.select_one(".result-url").text.strip()
            }
            for result in soup.select(".result-item")
        ]
        return results

    def _clean_string(self, text: str) -> str:
        """Clean the string to remove redundant data"""
        parts = text.split(':')
        return parts[1].lstrip()
    
    def _extract_images_and_excerpt(self, html) -> dict:
        """Extract images and excerpt from the full article"""
        soup = BeautifulSoup(html, 'html.parser')
        images = self._get_img_src(soup.select_one(".ja-masthead").get("style"))
        excerpt = self._format_body(soup.select(".com-content-article__body p"))
        return {"images": images, "excerpt": excerpt}
    
    def _format_body(self, body) -> str:
        """Format the body of the article"""
        truncated_body = body[:3]
        return ' '.join([p.text.strip() for p in truncated_body])
    
    def _get_img_src(self, link) -> str:
        """Getting the link from the style attribute"""
        if link is None:
            return None
        pattern = r"url\('([^']+)'\)"
        match = re.search(pattern, link)
        if match:
            return DOMAIN + match.group(1)
