import json
import os
import requests
from config import logger

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

    resultsJson = response.json()["organic"]

    logger.info(f"Found {len(resultsJson)} results for {query}")

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

    responeJson = response.json()

    if hasattr(responeJson, "message"):
        return f"You need to scrape {website} again"

    domain = website.split(".")

    logger.info(f"Visiting {domain[1]}.{domain[2]}...")

    # Limit the size of the output to 512KB
    # openai.BadRequestError: Error code: 400 - {'error': {'message': "'tool_outputs' too large: the combined tool outputs must be less than 512kb.", 'type': 'invalid_request_error', 'param': 'tool_outputs', 'code': 'invalid_value'}}
    max_size = 512 * 512  # 512KB in bytes
    output = response.text

    if len(output) > max_size:
        # Summarize the output to fit within the size limit
        summary = (
            f"Output too large to display. Content from {website} has been omitted."
        )
        return summary

    return response.text
