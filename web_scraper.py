#!/usr/bin/env python3
"""Web scraping utilities for the chatbot."""

import requests
from bs4 import BeautifulSoup
from langchain_core.tools import tool


@tool
def web_scrape_tool(url: str) -> str:
    """Scrape the main content from a web page.

    Args:
        url: The URL of the web page to scrape.

    Returns:
        Extracted text content from the page.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.extract()

        # Get text
        text = soup.get_text()

        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)

        # Limit to first 2000 characters to avoid too much data
        return text[:2000] + ("..." if len(text) > 2000 else "")

    except Exception as e:
        return f"Scraping error: {str(e)}"
