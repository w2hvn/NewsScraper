- **File Name**: app.py
- **Purpose**: Main entry point for the Streamlit web application. Responsible for the overall page layout, title, and orchestrating UI components to display scraped news articles.
- **Dependencies**:
  - `streamlit` as `st`
  - `DatabaseManager` from `src.database.db_manager`
  - `display_article_card` from `src.ui.components`
  - `typing` (e.g., `List`, `Dict`)
- **Variables/Constants**:
  - `PAGE_TITLE: str = "Python News Scraper & Aggregator"`
- **Classes & Methods**:
  - `def main() -> None:`
- **Logic / Workflow**:
  - `main`:
    1. Call `st.set_page_config(page_title=PAGE_TITLE, layout="wide")`.
    2. Display the main title and a brief description.
    3. Initialize the `DatabaseManager()` and ensure the database exists (`init_db()`).
    4. Provide a Sidebar with filters (e.g., a simple slider for the number of articles to fetch) and a refresh button.
    5. Fetch stats using `get_statistics()` and display them using `st.metric` for the KPI layout.
    6. Fetch the latest articles using `get_recent_articles(limit=...)`.
    7. Check if `articles` list is empty. If yes, display an info message: "No articles found. Run the scraper first."
    8. Iterate through the `articles` and pass each article dictionary to `display_article_card(article)` using containers or expanders.
