"""VNExpress specific news scraper implementation.

This module implements the VNExpressScraper class, inheriting from BaseScraper,
to parse article URLs and extract structured data (title, content, date) from
VNExpress news pages using BeautifulSoup4.
"""

import logging
from typing import List, Dict, Optional

from bs4 import BeautifulSoup

from .base_scraper import BaseScraper

logger = logging.getLogger(__name__)

VNEXPRESS_BASE_URL: str = "https://vnexpress.net/"

class VNExpressScraper(BaseScraper):
    """Scraper implementation for VNExpress news.

    Inherits from BaseScraper and overrides abstract methods
    for fetching links and parsing articles specifically for VNExpress.
    """

    def __init__(self):
        """Initializes the VNExpressScraper with its specific base URL."""
        super().__init__(VNEXPRESS_BASE_URL)

    def get_article_links(self) -> List[str]:
        """Extracts unique absolute URLs to articles from the main page.

        Fetches HTML from the base URL, parses it to find anchor tags,
        and extracts absolute href attributes.

        Returns:
            List[str]: A list of unique URLs. Returns an empty list on failure.
        """
        html: Optional[str] = self.fetch_html(self.base_url)
        if not html:
            logger.error(f"Failed to fetch content from base URL: {self.base_url}")
            return []

        links: List[str] = []
        try:
            soup = BeautifulSoup(html, "html.parser")

            # Find all anchor tags within possible news sections
            a_tags = soup.find_all("a", href=True)
            for a in a_tags:
                href: str = a["href"].strip()
                # Filter for absolute vnexpress URLs pointing to html articles
                if href.startswith(VNEXPRESS_BASE_URL) and href.endswith(".html"):
                    if href not in links:
                        links.append(href)

        except Exception as e:
            logger.error(f"Error while parsing article links from {self.base_url}: {e}")

        return links

    def parse_article(self, html: str) -> Dict[str, str]:
        """Parses the raw HTML of an article and extracts its content.

        Searches the HTML for title, content, and publication date using
        the specific DOM structure of VNExpress.

        Args:
            html (str): The raw HTML string of the article.

        Returns:
            Dict[str, str]: Extracted structured data containing
            keys for 'url', 'title', 'content', and 'date'.
        """
        article_data: Dict[str, str] = {
            "url": "",  # This must be populated externally or updated by the caller.
            "title": "",
            "content": "",
            "date": ""
        }

        if not html:
            logger.error("No HTML provided to parse_article.")
            return article_data

        try:
            soup = BeautifulSoup(html, "html.parser")

            # Extract Title: Typically an h1 tag with class 'title-detail'
            title_tag = soup.find("h1", class_="title-detail")
            if title_tag:
                article_data["title"] = title_tag.get_text(strip=True)

            # Extract Content: Typically p tags with class 'Normal'
            content_tags = soup.find_all("p", class_="Normal")
            if content_tags:
                paragraphs = [p.get_text(strip=True) for p in content_tags]
                article_data["content"] = "\n".join(paragraphs).strip()

            # Extract Date: Typically a span or div with class 'date'
            date_tag = soup.find("span", class_="date")
            if date_tag:
                article_data["date"] = date_tag.get_text(strip=True)
            else:
                # Try finding alternative date elements if needed
                header_date = soup.find(class_="header-content")
                if header_date and header_date.find(class_="date"):
                    article_data["date"] = header_date.find(class_="date").get_text(strip=True)

        except Exception as e:
            logger.error(f"Error while parsing article HTML: {e}")

        return article_data
