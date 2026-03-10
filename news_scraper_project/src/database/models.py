"""Defines the SQLAlchemy ORM models for the SQLite database.

This module contains the database models mapped to the SQLite tables using
SQLAlchemy's Object-Relational Mapping (ORM) capabilities.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base

# Define the base class for declarative class definitions
Base = declarative_base()

class Article(Base):
    """SQLAlchemy model representing a news article.

    This class defines the structure of the 'articles' table in the database,
    which stores the scraped news data.

    Attributes:
        id (Column): The primary key for the article.
        url (Column): The unique URL of the scraped article.
        title (Column): The title of the article.
        content (Column): The main body content of the article.
        published_date (Column): The publication date of the article as a string.
        scraped_at (Column): The timestamp indicating when the article was scraped.
    """
    __tablename__: str = "articles"

    id: Column = Column(Integer, primary_key=True, autoincrement=True)
    url: Column = Column(String(512), unique=True, nullable=False)
    title: Column = Column(String(255), nullable=False)
    content: Column = Column(Text, nullable=False)
    published_date: Column = Column(String(100), nullable=True)
    scraped_at: Column = Column(DateTime, default=datetime.utcnow)
