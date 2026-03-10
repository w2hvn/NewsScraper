"""Database manager for handling CRUD operations and session management.

This module provides the DatabaseManager class, which acts as the bridge
between the scraping tier and the database tier. It handles the secure
bulk insertion of data into the SQLite database, checks for duplicate URLs,
retrieval of recent articles, and provides database statistics.
"""

import logging
import os
from typing import List, Dict, Optional
from contextlib import contextmanager

from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError

from .models import Article, Base

logger = logging.getLogger(__name__)

DB_URL: str = "sqlite:///news.db"

class DatabaseManager:
    """Manages database connections, sessions, and CRUD operations.

    Handles interactions with the SQLite database using SQLAlchemy, ensuring
    duplicate URLs are not inserted and abstracting database logic away from
    the rest of the application.
    """

    def __init__(self, db_url: str = DB_URL):
        """Initializes the database engine and session factory.

        Args:
            db_url (str, optional): The SQLAlchemy connection string. Defaults to DB_URL.
        """
        self.engine = create_engine(db_url, echo=False)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def init_db(self) -> None:
        """Creates the database tables if they do not already exist."""
        try:
            Base.metadata.create_all(self.engine)
            logger.info("Database tables initialized successfully.")
        except SQLAlchemyError as e:
            logger.error(f"Error initializing database tables: {e}")

    @contextmanager
    def get_session(self):
        """Provides a transactional scope around a series of operations.

        Yields:
            Session: A SQLAlchemy database session object.
        """
        session: Session = self.SessionLocal()
        try:
            yield session
        except Exception as e:
            logger.error(f"Session error: {e}")
            session.rollback()
            raise
        finally:
            session.close()

    def save_articles(self, articles_data: List[Dict[str, str]]) -> int:
        """Saves a list of articles to the database if they don't already exist.

        Checks the database for an existing article with the same URL.
        If it doesn't exist, it adds the new article to the database.

        Args:
            articles_data (List[Dict[str, str]]): A list of dictionaries containing
                article data (url, title, content, date).

        Returns:
            int: The number of newly saved articles.
        """
        inserted_count: int = 0
        if not articles_data:
            return inserted_count

        try:
            with self.get_session() as session:
                for article_data in articles_data:
                    if not article_data.get("url"):
                        logger.error("Skipping article without a URL.")
                        continue

                    # Check for existing article by URL
                    existing_article = session.query(Article).filter(Article.url == article_data["url"]).first()
                    if existing_article:
                        logger.debug(f"Article with URL already exists: {article_data['url']}")
                        continue

                    # Create new Article instance
                    new_article = Article(
                        url=article_data.get("url"),
                        title=article_data.get("title", ""),
                        content=article_data.get("content", ""),
                        published_date=article_data.get("date", "")
                    )

                    session.add(new_article)
                    inserted_count += 1

                # Commit the entire batch
                session.commit()
                logger.info(f"Successfully saved {inserted_count} new articles.")

        except SQLAlchemyError as e:
            logger.error(f"Database error while saving batch of articles: {e}")
        except Exception as e:
            logger.error(f"Unexpected error while saving batch of articles: {e}")

        return inserted_count

    def get_recent_articles(self, limit: int = 50) -> List[Dict[str, str]]:
        """Retrieves the most recently scraped articles from the database.

        Args:
            limit (int, optional): The maximum number of articles to retrieve.
                Defaults to 50.

        Returns:
            List[Dict[str, str]]: A list of dictionaries representing the articles,
                ordered descending by their scrape time.
        """
        articles_list: List[Dict[str, str]] = []
        try:
            with self.get_session() as session:
                # Query articles, ordering by most recently scraped
                results = session.query(Article).order_by(Article.scraped_at.desc()).limit(limit).all()

                for article in results:
                    articles_list.append({
                        "id": str(article.id),
                        "url": article.url,
                        "title": article.title,
                        "content": article.content,
                        "published_date": article.published_date,
                        "scraped_at": str(article.scraped_at)
                    })
        except SQLAlchemyError as e:
            logger.error(f"Database error while retrieving articles: {e}")
        except Exception as e:
            logger.error(f"Unexpected error while retrieving articles: {e}")

        return articles_list

    def get_statistics(self) -> Dict[str, int]:
        """Retrieves statistics about the database content.

        Returns:
            Dict[str, int]: A dictionary containing various statistics
                (e.g., 'total_articles').
        """
        stats: Dict[str, int] = {"total_articles": 0}
        try:
            with self.get_session() as session:
                # Get total count of articles
                total = session.query(func.count(Article.id)).scalar()
                stats["total_articles"] = total if total else 0
        except SQLAlchemyError as e:
            logger.error(f"Database error while retrieving statistics: {e}")
        except Exception as e:
            logger.error(f"Unexpected error while retrieving statistics: {e}")

        return stats
