- **File Name**: components.py
- **Purpose**: Defines individual, reusable Streamlit UI components (like article cards) for the main application.
- **Dependencies**:
  - `streamlit` as `st`
  - `typing` (e.g., `Dict`)
- **Variables/Constants**:
  - `MAX_CONTENT_LENGTH: int = 200` (Truncate long content snippets)
- **Classes & Methods**:
  - `def display_article_card(article: Dict[str, str]) -> None:`
  - `def truncate_text(text: str, max_len: int) -> str:`
- **Logic / Workflow**:
  - `truncate_text`: If `text` length is greater than `max_len`, return the truncated string appended with `...`. Otherwise, return original `text`.
  - `display_article_card`:
    1. Create a container or expander using `st.container()` or `st.expander(article['title'])`.
    2. Display the `published_date` in a smaller or colored font using `st.caption` or markdown HTML.
    3. Display the truncated `content` using `st.write` or `st.markdown`.
    4. Provide a clickable link `[Read More](article['url'])` using `st.markdown`.
    5. Ensure proper visual separation between cards using horizontal rules (`st.divider()`) or container styling.
