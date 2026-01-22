from crewai.tools import tool
import requests
from bs4 import BeautifulSoup
import feedparser
import wikipedia

@tool("GitHub Trends Search")
def github_trends_search(language: str = "") -> str:
    """Searches for trending repositories on GitHub to identify technology trends. Returns a list of trending repos with descriptions."""
    url = "https://github.com/trending"
    if language:
        url += f"/{language}"
    
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return f"Failed to fetch GitHub trends. Status code: {response.status_code}"
        
        soup = BeautifulSoup(response.content, 'html.parser')
        repos = soup.find_all('article', class_='Box-row')
        
        results = []
        for repo in repos[:10]:  # Top 10
            title_tag = repo.find('h1', class_='h3 lh-condensed')
            if title_tag:
                name = title_tag.text.strip().replace('\n', '').replace(' ', '')
            else:
                name = "Unknown"
            
            desc_tag = repo.find('p', class_='col-9 color-fg-muted my-1 pr-4')
            description = desc_tag.text.strip() if desc_tag else "No description"
            
            results.append(f"- Name: {name}\n  Description: {description}")
        
        return "\n".join(results) if results else "No trending repositories found."
    except Exception as e:
        return f"Error fetching GitHub trends: {str(e)}"

@tool("RSS Feed Reader")
def rss_feed_reader(feed_url: str) -> str:
    """Reads and summarizes the latest articles from a given RSS feed URL. Useful for getting latest news from tech blogs."""
    try:
        feed = feedparser.parse(feed_url)
        results = []
        for entry in feed.entries[:5]:  # Top 5
            title = entry.title
            summary = getattr(entry, 'summary', 'No summary')
            link = entry.link
            results.append(f"- Title: {title}\n  Summary: {summary}\n  Link: {link}")
        
        if not results:
            return "No entries found in feed."
            
        return "\n".join(results)
    except Exception as e:
        return f"Error reading RSS feed: {str(e)}"

@tool("Wikipedia Search")
def wikipedia_search(query: str) -> str:
    """Searches Wikipedia for information on a given topic. Returns a summary of the Wikipedia article."""
    try:
        results = wikipedia.search(query, results=3)
        if not results:
            return f"No Wikipedia results found for: {query}"
        
        summary = wikipedia.summary(results[0], sentences=5)
        return f"Wikipedia Summary for '{results[0]}':\n{summary}"
    except wikipedia.exceptions.DisambiguationError as e:
        options = e.options[:5]
        return f"Multiple Wikipedia pages found. Please be more specific. Options: {', '.join(options)}"
    except Exception as e:
        return f"Error searching Wikipedia: {str(e)}"
