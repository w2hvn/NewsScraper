- **File Name**: main_scheduler.py
- **Purpose**: The main orchestration script that initializes the database, runs the specified scrapers at set intervals (or as a one-off job), and handles saving the scraped data using the `schedule` library.
- **Dependencies**:
  - `time`, `logging`, `schedule`
  - `DatabaseManager` from `src.database.db_manager`
  - `VNExpressScraper` from `src.scrapers.vnexpress`
  - `typing` (e.g., `List`, `Dict`)
- **Variables/Constants**:
  - `SCRAPE_INTERVAL_MINUTES: int = 30` (Default interval for scraping)
- **Classes & Methods**:
  - `def setup_logging() -> None:`
  - `def run_scrapers(db: DatabaseManager) -> None:`
  - `def main(continuous: bool = False) -> None:`
- **Logic / Workflow**:
  - `setup_logging`: Configure the root logger with `INFO` level, defining format string (e.g., `%(asctime)s - %(name)s - %(levelname)s - %(message)s`).
  - `run_scrapers`:
    1. Initialize `VNExpressScraper()`.
    2. Get links `scraper.get_article_links()`.
    3. Loop through links. For each link, fetch HTML using `scraper.fetch_html()`.
    4. Parse `article_data = scraper.parse_article(html)`.
    5. Add `url` to `article_data` manually if needed.
    6. Build a list of valid articles.
    7. Save to database using the batch method `db.save_articles(articles_data_list)`.
    8. Log progress and sleep briefly (`time.sleep(1)`) between requests to avoid rate limits.
  - `main`:
    1. Call `setup_logging()`.
    2. Initialize `DatabaseManager()`, run `init_db()`.
    3. If `continuous` is true, use `schedule.every(SCRAPE_INTERVAL_MINUTES).minutes.do(run_scrapers, db)`. Call `run_scrapers(db)` once immediately. Loop `while True: schedule.run_pending(); time.sleep(1)`.
    4. If false, run `run_scrapers(db)` once and exit.
