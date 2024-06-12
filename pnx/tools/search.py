#!/usr/bin/env python3
import requests
import json
import os
from .website import scrape_website

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
