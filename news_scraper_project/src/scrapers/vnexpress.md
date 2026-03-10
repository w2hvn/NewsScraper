- **File Name**: vnexpress.py
- **Purpose**: A specific scraper implementation to fetch and parse news articles from VNExpress.
- **Dependencies**:
  - `BaseScraper` from `.base_scraper`
  - `BeautifulSoup` from `bs4`
  - `typing` (e.g., `List`, `Dict`)
- **Variables/Constants**:
  - `VNEXPRESS_BASE_URL: str = "https://vnexpress.net/"`
- **Classes & Methods**:
  - `class VNExpressScraper(BaseScraper):`
    - `def __init__(self):` (Initializes with `VNEXPRESS_BASE_URL`)
    - `def get_article_links(self) -> List[str]:`
    - `def parse_article(self, html: str) -> Dict[str, str]:`
- **Logic / Workflow**:
  - `get_article_links`:
    1. Call `fetch_html` on the `base_url`.
    2. Parse the HTML using BeautifulSoup.
    3. Find all anchor (`<a>`) tags within the main news sections.
    4. Extract `href` attributes, filter out non-article links, and return a list of unique absolute URLs.
  - `parse_article`:
    1. Parse the given `html` using BeautifulSoup.
    2. Extract the `title` (e.g., `h1` tag with class `title-detail`).
    3. Extract the `content` (e.g., `p` tags with class `Normal`).
    4. Extract the `date` (e.g., span or div tag for publication date).
    5. Ensure all fields are properly cleaned and stripped of extra whitespaces.
    6. Return a dictionary with keys: `url`, `title`, `content`, `date`.
