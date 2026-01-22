from crewai_tools import BaseTool, WikipediaSearchTool
import requests
from bs4 import BeautifulSoup
import feedparser

class GitHubTrendsTool(BaseTool):
    name: str = "GitHub Trends Search"
    description: str = "Searches for trending repositories on GitHub to identify technology trends. Returns a list of trending repos with descriptions."

    def _run(self, language: str = "") -> str:
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
            for repo in repos[:10]: # Top 10
                title_tag = repo.find('h1', class_='h3 lh-condensed')
                if title_tag:
                    name = title_tag.text.strip().replace('\n', '').replace(' ', '')
                else:
                    name = "Unknown"
                
                desc_tag = repo.find('p', class_='col-9 color-fg-muted my-1 pr-4')
                description = desc_tag.text.strip() if desc_tag else "No description"
                
                results.append(f"- Name: {name}\n  Description: {description}")
            
            return "\n".join(results)
        except Exception as e:
            return f"Error fetching GitHub trends: {str(e)}"

class RSSFeedTool(BaseTool):
    name: str = "RSS Feed Reader"
    description: str = "Reads and summarizes the latest articles from a given RSS feed URL. Useful for getting latest news from tech blogs."

    def _run(self, feed_url: str) -> str:
        try:
            feed = feedparser.parse(feed_url)
            results = []
            for entry in feed.entries[:5]: # Top 5
                title = entry.title
                summary = getattr(entry, 'summary', 'No summary')
                link = entry.link
                results.append(f"- Title: {title}\n  Summary: {summary}\n  Link: {link}")
            
            if not results:
                return "No entries found in feed."
                
            return "\n".join(results)
        except Exception as e:
            return f"Error reading RSS feed: {str(e)}"

# Instantiate tools
github_tool = GitHubTrendsTool()
rss_tool = RSSFeedTool()
# Wikipedia tool will be instantiated in the agent definition or here if needed with default config
wikipedia_tool = WikipediaSearchTool()

from langchain_community.tools import DuckDuckGoSearchRun
search_tool = DuckDuckGoSearchRun()
