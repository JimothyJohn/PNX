#!/usr/bin/env python3
import requests
import json
import os


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
