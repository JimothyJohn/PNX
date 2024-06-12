#!/usr/bin/env python3
import requests
import json
import os

def scrape_website(website: str) -> str:
    """
    Scrapes a website.

    :param website: The website to scrape.
    :return: The scrape results.
    """
    url = "https://scrape.serper.dev"

    payload = json.dumps({
    "url": f"{website}",
    })
    headers = {
    "X-API-KEY": os.environ.get("SERPER_API_KEY"),
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)