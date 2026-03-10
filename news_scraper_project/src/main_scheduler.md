- **File Name**: main_scheduler.py
- **Purpose**: The main orchestration script that initializes the database, runs the specified scrapers at set intervals (or as a one-off job), and handles saving the scraped data.
- **Dependencies**:
  - `time`, `logging`
  - `DatabaseManager` from `database.db_manager`
  - `VNExpressScraper` from `scrapers.vnexpress`
  - `typing` (e.g., `List`)
- **Variables/Constants**:
  - `SCRAPE_INTERVAL_SECONDS: int = 3600` (Default interval for scraping)
- **Classes & Methods**:
  - `def setup_logging() -> None:`
  - `def run_scrapers(db: DatabaseManager) -> None:`
  - `def main(continuous: bool = False) -> None:`
- **Logic / Workflow**:
  - `setup_logging`: Configure the root logger with `INFO` level, defining format string (e.g., `%(asctime)s - %(name)s - %(levelname)s - %(message)s`).
  - `run_scrapers`:
    1. Initialize `VNExpressScraper()`.
    2. Get links `scraper.get_article_links()`.
    3. Loop through links. For each:
       - Fetch and parse `article_data = scraper.parse_article(html)`.
       - Save to database `db.save_article(article_data)`.
       - Log progress and sleep briefly (`time.sleep(1)`) to avoid rate limits.
  - `main`:
    1. Call `setup_logging()`.
    2. Initialize `DatabaseManager()`, run `init_db()`.
    3. If `continuous` is true, loop `while True:`, `run_scrapers(db)`, then `time.sleep(SCRAPE_INTERVAL_SECONDS)`.
    4. If false, run `run_scrapers(db)` once and exit.
