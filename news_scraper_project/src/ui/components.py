"""Reusable Streamlit UI components for the dashboard.

This module provides common UI components, such as article cards,
to be used within the main Streamlit application for displaying
scraped news data cleanly.
"""

from typing import Dict

import streamlit as st

MAX_CONTENT_LENGTH: int = 200

def truncate_text(text: str, max_len: int) -> str:
    """Truncates text to a specified maximum length.

    Args:
        text (str): The original text string.
        max_len (int): The maximum allowed length.

    Returns:
        str: The truncated string appended with '...' if it exceeds max_len,
        otherwise the original string.
    """
    if not text:
        return ""
    if len(text) > max_len:
        return text[:max_len].rsplit(' ', 1)[0] + "..."
    return text

def display_article_card(article: Dict[str, str]) -> None:
    """Displays a single news article as a styled Streamlit component.

    Uses Streamlit's expander and markdown capabilities to present the
    article title, publication date, a truncated snippet of the content,
    and a link to read the full article.

    Args:
        article (Dict[str, str]): A dictionary containing article data
            such as 'title', 'published_date', 'content', and 'url'.
    """
    title = article.get("title", "No Title")

    with st.expander(title):
        # Display published date if available
        published_date = article.get("published_date")
        if published_date:
            st.caption(f"📅 Published: {published_date}")

        # Display truncated content
        content = article.get("content", "")
        truncated = truncate_text(content, MAX_CONTENT_LENGTH)
        st.write(truncated)

        # Display link to the original article
        url = article.get("url")
        if url:
            st.markdown(f"[Read Full Article Here]({url})")

        st.divider()
