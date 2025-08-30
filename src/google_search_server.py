from fastmcp import FastMCP
import requests
import json
from typing import List, Dict, Any
import os
from dotenv import load_dotenv
import sys
load_dotenv()

mcp = FastMCP("GoogleSearchHub")
def get_google_search_config():
    api_key = os.getenv("GOOGLE_API_KEY")
    engine_id = os.getenv("GOOGLE_ENGINE_ID")
    return api_key, engine_id

@mcp.tool()
def google_search(query: str, max_results: int = 10, start_index: int = 1) -> List[Dict[str, Any]]:
    api_key, engine_id = get_google_search_config()
    url = "https://www.googleapis.com/customsearch/v1"
    params = {'key': api_key,'cx': engine_id,'q': query,'num': min(max_results, 10), 'start': start_index}
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    results = []
    if 'items' in data:
        for item in data['items']:
            results.append({
                "title": item.get("title", ""),
                "snippet": item.get("snippet", ""),
                "link": item.get("link", ""),
                "displayLink": item.get("displayLink", ""),
                "source": "Google Custom Search",
                "searchInformation": {
                    "totalResults": data.get("searchInformation", {}).get("totalResults", "0"),
                    "searchTime": data.get("searchInformation", {}).get("searchTime", "0")
                }
            })
    return results
    

@mcp.tool()
def google_image_search(query: str, max_results: int = 10) -> List[Dict[str, Any]]:
    api_key, engine_id = get_google_search_config()
    url = "https://www.googleapis.com/customsearch/v1"
    params = {'key': api_key,'cx': engine_id,'q': query,'num': min(max_results, 10),'searchType': 'image'}
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    results = []
    if 'items' in data:
        for item in data['items']:
            results.append({
                "title": item.get("title", ""),
                "link": item.get("link", ""),
                "displayLink": item.get("displayLink", ""),
                "thumbnail": item.get("image", {}).get("thumbnailLink", ""),
                "contextLink": item.get("image", {}).get("contextLink", ""),
                "width": item.get("image", {}).get("width", 0),
                "height": item.get("image", {}).get("height", 0),
                "source": "Google Image Search"
            })
    return results


@mcp.tool()
def google_news_search(query: str, max_results: int = 10) -> List[Dict[str, Any]]:
    api_key, engine_id = get_google_search_config()
    news_query = f"{query} news"
    url = "https://www.googleapis.com/customsearch/v1"
    params = {'key': api_key,'cx': engine_id,'q': news_query,'num': min(max_results, 10),'sort': 'date'  }
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    results = []
    if 'items' in data:
        for item in data['items']:
            date_info = ""
            if 'pagemap' in item and 'metatags' in item['pagemap']:
                metatags = item['pagemap']['metatags'][0] if item['pagemap']['metatags'] else {}
                date_info = metatags.get('article:published_time', '') or metatags.get('pubdate', '')
            results.append({
                "title": item.get("title", ""),
                "snippet": item.get("snippet", ""),
                "link": item.get("link", ""),
                "displayLink": item.get("displayLink", ""),
                "publishedDate": date_info,
                "source": "Google News Search"
            })
    return results


@mcp.tool()
def google_search_with_site(query: str, site: str, max_results: int = 10) -> List[Dict[str, Any]]:
    site_query = f"site:{site} {query}"
    return google_search(site_query, max_results)


if __name__ == "__main__":
    transport = "stdio" 
    if len(sys.argv) > 1:
        transport = sys.argv[1]
    if transport == "stdio":
        mcp.run(transport="stdio")







