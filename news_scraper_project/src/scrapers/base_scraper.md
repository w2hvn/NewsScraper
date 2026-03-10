- **File Name**: base_scraper.py
- **Purpose**: Defines the abstract base class and common utility functions for all individual news scrapers.
- **Dependencies**:
  - `requests`
  - `BeautifulSoup` from `bs4`
  - `ABC`, `abstractmethod` from `abc`
  - `typing` (e.g., `List`, `Dict`, `Optional`)
- **Variables/Constants**:
  - `DEFAULT_HEADERS: Dict[str, str]` (Common user-agent headers to mimic a real browser)
- **Classes & Methods**:
  - `class BaseScraper(ABC):`
    - `def __init__(self, base_url: str):`
    - `def fetch_html(self, url: str) -> Optional[str]:`
    - `@abstractmethod def parse_article(self, html: str) -> Dict[str, str]:`
    - `@abstractmethod def get_article_links(self) -> List[str]:`
- **Logic / Workflow**:
  - `fetch_html`:
    1. Try to make a GET request to `url` using `DEFAULT_HEADERS`.
    2. Check for HTTP status code. If 200, return `response.text`.
    3. If there is an exception or status code is not 200, log the error and return `None`.
