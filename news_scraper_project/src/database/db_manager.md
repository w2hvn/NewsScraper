- **File Name**: db_manager.py
- **Purpose**: Provides CRUD (Create, Read, Update, Delete) operations and session management for interacting with the SQLite database.
- **Dependencies**:
  - `create_engine`, `sessionmaker`, `Session`, `func` from `sqlalchemy`
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
    - `def save_articles(self, articles_data: List[Dict[str, str]]) -> int:`
    - `def get_recent_articles(self, limit: int = 50) -> List[Dict]:`
    - `def get_statistics(self) -> Dict[str, int]:`
- **Logic / Workflow**:
  - `__init__`: Set up `self.engine = create_engine(db_url)` and `self.SessionLocal = sessionmaker(bind=self.engine)`.
  - `init_db`: Call `Base.metadata.create_all(self.engine)` to ensure the `articles` table is created.
  - `save_articles`:
    1. Open a new session (`with self.get_session() as session:`).
    2. Iterate over the `articles_data` list.
    3. Check if an article with `article_data['url']` already exists to prevent duplicate entries.
    4. If it does not exist, create an `Article` object, and `add()` to session.
    5. `commit()` the session after all inserts. Return the number of successful inserts.
    6. Log any database exceptions.
  - `get_recent_articles`:
    1. Query the database for the most recent `Article` entries ordered by `scraped_at` descending, up to `limit`.
    2. Convert `Article` ORM objects to a list of dictionaries.
    3. Return the list.
  - `get_statistics`:
    1. Query the total count of articles in the database.
    2. Return a dictionary containing the total count (e.g., `{"total_articles": count}`).
