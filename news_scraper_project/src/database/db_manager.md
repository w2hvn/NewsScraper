- **File Name**: db_manager.py
- **Purpose**: Provides CRUD (Create, Read, Update, Delete) operations and session management for interacting with the SQLite database.
- **Dependencies**:
  - `create_engine`, `sessionmaker`, `Session` from `sqlalchemy`
  - `Article`, `Base` from `.models`
  - `typing` (e.g., `List`, `Dict`, `Optional`)
  - `os` (for file paths)
- **Variables/Constants**:
  - `DB_URL: str = "sqlite:///news.db"` (Default SQLite connection string)
- **Classes & Methods**:
  - `class DatabaseManager:`
    - `def __init__(self, db_url: str = DB_URL):`
    - `def init_db(self):` (Creates tables)
    - `def get_session(self) -> Session:`
    - `def save_article(self, article_data: Dict[str, str]) -> bool:`
    - `def get_all_articles(self, limit: int = 50) -> List[Dict]:`
- **Logic / Workflow**:
  - `__init__`: Set up `self.engine = create_engine(db_url)` and `self.SessionLocal = sessionmaker(bind=self.engine)`.
  - `init_db`: Call `Base.metadata.create_all(self.engine)` to ensure the `articles` table is created.
  - `save_article`:
    1. Open a new session (`with self.get_session() as session:`).
    2. Check if an article with `article_data['url']` already exists to prevent duplicate entries.
    3. If it does not exist, create an `Article` object, `add()` to session, and `commit()`.
    4. Return `True` on success, `False` on failure or duplicate.
    5. Log any database exceptions.
  - `get_all_articles`:
    1. Query the database for the most recent `Article` entries ordered by `scraped_at` descending, up to `limit`.
    2. Convert `Article` ORM objects to a list of dictionaries.
    3. Return the list.
