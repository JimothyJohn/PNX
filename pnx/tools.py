#!/usr/bin/env python3
import json
import os
import requests

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_coin_price",
            "description": "Use this function to get the current price of a cryptocoin.",
            "parameters": {
                "type": "object",
                "properties": {
                    "cryptocoin": {
                        "type": "string",
                        "description": f"""
A specific cryptocoin. For example, 'bitcoin' for Bitcoin, 'ethereum' for Ethereum, etc. 
""",
                    }
                },
                "required": ["cryptocoin"],
            },
        },
    },
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
                        "description": f"""
A query to search for on the web.
""",
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
                        "description": f"""
URL of the website to scrape.
""",
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

    # link = response.json()["organic"][0]["link"]
    with open("search_output.json", "w") as f:
        json.dump(response.json(), f, indent=4)

    return response.text


def get_coin_price(cryptocoin: str) -> float:
    """
    Fetches the current price of a cryptocurrency in USD from the CoinGecko API.

    :param cryptocoin: The name of the cryptocurrency (e.g., 'bitcoin', 'ethereum').
    :return: The current price of the cryptocurrency in USD.
    """
    api_url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": cryptocoin, "vs_currencies": "usd"}
    response = requests.get(api_url, params=params)
    response.raise_for_status()
    data = response.json()
    return data[cryptocoin]["usd"]


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
