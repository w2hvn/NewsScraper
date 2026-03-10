"""Abstract base class and common utilities for news scrapers.

This module defines the BaseScraper interface that all concrete scraper
implementations must inherit from. It also provides common methods for
fetching HTML content from URLs over HTTP.
"""

import logging
from abc import ABC, abstractmethod
from typing import List, Dict, Optional

import requests
from bs4 import BeautifulSoup

# Set up module level logger
logger = logging.getLogger(__name__)

# Common user-agent headers to mimic a real browser
DEFAULT_HEADERS: Dict[str, str] = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/91.0.4472.124 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}

class BaseScraper(ABC):
    """Abstract base scraper for extracting news data.

    All specific news scrapers should inherit from this class and
    implement the abstract methods.

    Attributes:
        base_url (str): The root URL of the target news site.
    """

    def __init__(self, base_url: str):
        """Initializes the scraper with a base URL.

        Args:
            base_url (str): The root URL for the website to scrape.
        """
        self.base_url: str = base_url

    def fetch_html(self, url: str) -> Optional[str]:
        """Fetches the HTML content of the provided URL.

        Attempts to perform an HTTP GET request to the target URL using
        the default browser headers.

        Args:
            url (str): The target URL to fetch.

        Returns:
            Optional[str]: The HTML content as a string if successful,
            or None if the request failed or returned a non-200 status.
        """
        try:
            response = requests.get(url, headers=DEFAULT_HEADERS, timeout=10)
            if response.status_code == 200:
                return response.text
            else:
                logger.error(f"Failed to fetch HTML. Status code: {response.status_code} for URL: {url}")
                return None
        except requests.RequestException as e:
            logger.error(f"Exception occurred while fetching HTML from {url}: {e}")
            return None

    @abstractmethod
    def parse_article(self, html: str) -> Dict[str, str]:
        """Parses a single article's HTML and returns structured data.

        Args:
            html (str): The raw HTML string of the article page.

        Returns:
            Dict[str, str]: A dictionary containing structured data
            (e.g., 'title', 'content', 'url', 'date').
        """
        pass

    @abstractmethod
    def get_article_links(self) -> List[str]:
        """Extracts article URLs from the main news sections.

        Returns:
            List[str]: A list of absolute URLs for individual articles.
        """
        pass
