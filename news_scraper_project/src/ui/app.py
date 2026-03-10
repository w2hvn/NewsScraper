"""Main entry point for the Streamlit web application.

This module orchestrates the UI components to build a dashboard
for visualizing scraped news articles. It acts as the UI Tier,
fetching data from the Database Tier and displaying it securely.
"""

import logging
from typing import List, Dict

import streamlit as st

from src.database.db_manager import DatabaseManager
from src.ui.components import display_article_card

# Setup basic logging for the UI
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PAGE_TITLE: str = "Python News Scraper & Aggregator"

def main() -> None:
    """Initializes and runs the Streamlit application.

    Configures the page, sets up the sidebar with filters, fetches
    the latest articles and statistics from the database, and displays
    the information using Streamlit components.
    """
    # 1. Page Configuration
    st.set_page_config(page_title=PAGE_TITLE, layout="wide")

    # 2. Display Main Title
    st.title("📰 " + PAGE_TITLE)
    st.markdown("A modern dashboard for viewing aggregated news scraped from top sources.")

    # 3. Initialize Database Manager
    db = DatabaseManager()
    db.init_db()

    # 4. Sidebar Configuration
    st.sidebar.header("Filters & Controls")

    # Slider to control how many articles to display
    limit: int = st.sidebar.slider(
        "Number of Articles to Fetch",
        min_value=10,
        max_value=200,
        value=50,
        step=10
    )

    # Refresh Button
    if st.sidebar.button("🔄 Refresh Data"):
        st.sidebar.success("Fetching latest articles...")
        # Since this is a simple app, triggering Streamlit re-run
        # is enough to call `get_recent_articles` again.

    # 5. Dashboard KPI Section
    stats: Dict[str, int] = db.get_statistics()
    total_articles: int = stats.get("total_articles", 0)

    st.subheader("Database Statistics")
    # Display the KPI using st.metric
    col1, _ = st.columns([1, 3])
    with col1:
        st.metric(label="Total Scraped Articles", value=total_articles)

    st.divider()

    # 6. Fetch and Display Recent Articles
    st.subheader("Recent News")
    articles: List[Dict[str, str]] = db.get_recent_articles(limit=limit)

    # 7. Check for Empty State
    if not articles:
        st.info("No articles found in the database. Run the scraper first.")
        return

    # 8. Iterate and Display Article Cards using the component
    for article in articles:
        display_article_card(article)

if __name__ == "__main__":
    main()
