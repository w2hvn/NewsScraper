# AGENTS.md - System-Wide Rules and Guidelines

## 1. Project Overview
This project is a Python News Scraper & Aggregator following a strict 3-tier architecture:
- **Scraping Tier**: Utilizes `requests` and `BeautifulSoup4` to fetch and parse news articles from target websites.
- **Database Tier**: Uses SQLite with `SQLAlchemy` as the ORM to store and manage parsed articles.
- **UI Tier**: A modern, scientific user interface built with `Streamlit` to display the aggregated news.

## 2. AI Agent Directives (How Jules should behave)
- **Read First**: Always read this `AGENTS.md` file before modifying any code.
- **Spec-Driven**: Read the corresponding `[filename].md` specification file before touching or creating a `[filename].py` file.
- **No Hallucinations**: Do not hallucinate functions, classes, or logic. Strictly follow the definitions and signatures outlined in the specification `.md` files.

## 3. Communication & Data Flow
- **Scraper to Database**: The Scraper tier extracts structured data (title, content, url, date, etc.) and passes it to the Database tier using the provided `db_manager` functions for persistence.
- **UI to Database**: The Streamlit UI tier is strictly read-heavy. It retrieves data exclusively by querying the Database tier (SQLite) and does not directly interact with the Scraper tier.
- **Decoupling**: Each tier must remain independent, interacting only through well-defined interfaces/methods documented in the specs.

## 4. Code Style & Conventions
- **PEP-8**: Strict compliance with PEP-8 formatting standards.
- **Type Hinting**: Mandatory for all function signatures and variables where applicable (e.g., `def fetch_html(url: str) -> str:`).
- **Docstrings**: Use Google Style docstrings for all modules, classes, and functions.
- **Error Handling**: Use `try/except` blocks extensively. All errors must be logged appropriately rather than failing silently or crashing the application.
