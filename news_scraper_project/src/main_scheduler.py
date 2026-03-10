"""Main orchestration script for the news scraper application.

This module initializes the database, orchestrates the scraper to fetch data
from specified sources, and saves the structured data to the database. It
utilizes the 'schedule' library to automate the process periodically.
"""

import logging
import time
from typing import List, Dict, Optional

import schedule

from src.database.db_manager import DatabaseManager
from src.scrapers.vnexpress import VNExpressScraper

SCRAPE_INTERVAL_MINUTES: int = 30

def setup_logging() -> None:
    """Configures the root logger with a standard format and INFO level."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

def run_scrapers(db: DatabaseManager) -> None:
    """Executes the scraping process and saves results to the database.

    Initializes the VNExpress scraper, fetches article links, parses the HTML
    content of each link, and performs a bulk insert of the structured data
    using the DatabaseManager.

    Args:
        db (DatabaseManager): The active database manager instance.
    """
    logger = logging.getLogger(__name__)
    logger.info("Starting scheduled scraper execution...")

    scraper = VNExpressScraper()

    try:
        links: List[str] = scraper.get_article_links()
        logger.info(f"Found {len(links)} article links to process.")

        articles_data_list: List[Dict[str, str]] = []

        for link in links:
            try:
                # Add a brief delay to avoid rate limits
                time.sleep(1)

                html: Optional[str] = scraper.fetch_html(link)
                if not html:
                    logger.warning(f"Skipping link due to fetch failure: {link}")
                    continue

                article_data: Dict[str, str] = scraper.parse_article(html)

                # The parse_article method leaves url empty, so we must populate it
                article_data["url"] = link

                # Only append if we successfully parsed the basic data
                if article_data.get("title") and article_data.get("content"):
                    articles_data_list.append(article_data)
                else:
                    logger.warning(f"Failed to extract title or content from: {link}")

            except Exception as e:
                logger.error(f"Error processing link {link}: {e}")

        # Bulk save all successfully processed articles
        if articles_data_list:
            inserted_count = db.save_articles(articles_data_list)
            logger.info(f"Execution complete. Inserted {inserted_count} new articles.")
        else:
            logger.info("Execution complete. No new valid articles were processed.")

    except Exception as e:
        logger.error(f"Critical error during scraper execution: {e}")

def main(continuous: bool = False) -> None:
    """Entry point for the application scheduler.

    Initializes logging and the database. Depending on the `continuous` flag,
    it either runs the scraping process once and exits, or enters a scheduling
    loop using the 'schedule' library.

    Args:
        continuous (bool, optional): If True, run continuously based on the schedule.
            Defaults to False.
    """
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Initializing Python News Scraper & Aggregator Scheduler")

    try:
        # Initialize Database Tier
        db = DatabaseManager()
        db.init_db()

        if continuous:
            logger.info(f"Configuring continuous scraping every {SCRAPE_INTERVAL_MINUTES} minutes.")

            # Run once immediately on startup
            run_scrapers(db)

            # Schedule periodic execution
            schedule.every(SCRAPE_INTERVAL_MINUTES).minutes.do(run_scrapers, db)

            # Keep the script running
            while True:
                schedule.run_pending()
                time.sleep(1)
        else:
            logger.info("Running scraper in single-execution mode.")
            run_scrapers(db)

    except Exception as e:
        logger.error(f"Failed to start the application scheduler: {e}")

if __name__ == "__main__":
    # Change to True if you want the script to run as a daemon process
    main(continuous=False)
