- **File Name**: app.py
- **Purpose**: Main entry point for the Streamlit web application. Responsible for the overall page layout, title, and orchestrating UI components to display scraped news articles.
- **Dependencies**:
  - `streamlit` as `st`
  - `DatabaseManager` from `../database/db_manager`
  - `display_article_card` from `.components`
  - `typing` (e.g., `List`, `Dict`)
- **Variables/Constants**:
  - `PAGE_TITLE: str = "Python News Scraper & Aggregator"`
- **Classes & Methods**:
  - `def main() -> None:`
- **Logic / Workflow**:
  - `main`:
    1. Call `st.set_page_config(page_title=PAGE_TITLE, layout="wide")`.
    2. Display the main title and a brief description.
    3. Initialize the `DatabaseManager()` and ensure the database exists.
    4. Provide a refresh button or use auto-refresh to fetch the latest articles (`get_all_articles(limit=50)`).
    5. Check if `articles` list is empty. If yes, display an info message: "No articles found. Run the scraper first."
    6. Iterate through the `articles` and pass each article dictionary to `display_article_card(article)`.
    7. Optionally add a sidebar with filters (e.g., by date or source).
