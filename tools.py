from dotenv import load_dotenv
from langchain.tools import tool
import os
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient

load_dotenv()
tavily_api_key = os.getenv("TAVILY_API_KEY")

tavily = TavilyClient(api_key=tavily_api_key)


@tool
def web_search(query: str) -> str:
    """Search the web for the recent and reliable information on a topic. Returns titles, urls and snippets of the search results."""
    response = tavily.search(query=query, max_results=5)

    out = []

    for index, r in enumerate(response["results"], start=1):
        title = r["title"]
        url = r["url"]
        content = r["content"]
        out.append(
            f"Result {index}\n"
            f"Title: {title}\n"
            f"URL: {url}\n"
            f"Snippet: {content[:500]}\n"
        )

    return "\n---\n".join(out)


# print(web_search.invoke("What is the recent news of war?"))

@tool
def scrape_tool(url: str) -> str:
    """Scrape the content of a webpage. Returns the text content from given url for deep reading."""
    try:
        response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.text, 'html.parser')
        for tag in soup(['script', 'style', 'nav', 'footer']):
            tag.decompose()
        return soup.get_text(separator=' ', strip=True)[:3000]
    except Exception as e:
        return f"Error occurred while scraping the webpage: {str(e)}"


# print(scrape_tool.invoke("https://docs.langchain.com/oss/python/langchain/overview"))