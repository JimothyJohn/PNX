import json
import os
import requests

tools = [
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Use this function to do a Google search on the web.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "A query to search for on the web.",
                    }
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "scrape_website",
            "description": "Use this function to scrape a website.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "URL of the website to scrape.",
                    }
                },
                "required": ["url"],
            },
        },
    },
]


def search_web(query: str) -> str:
    """
    Searches the web for a specific query.

    :param query: The query to search for.
    :return: The search results.
    """

    url = "https://google.serper.dev/search"

    payload = json.dumps({"q": query, "location": "United States"})
    headers = {
        "X-API-KEY": os.environ.get("SERPER_API_KEY"),
        "Content-Type": "application/json",
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.text


def scrape_website(website: str) -> str:
    """
    Scrapes a website.

    :param website: The website to scrape.
    :return: The scrape results.
    """
    url = "https://scrape.serper.dev"

    payload = json.dumps(
        {
            "url": f"{website}",
        }
    )
    headers = {
        "X-API-KEY": os.environ.get("SERPER_API_KEY"),
        "Content-Type": "application/json",
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.text
