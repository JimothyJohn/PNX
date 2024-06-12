#!/usr/bin/env python3
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
                "required": ["website"],
            },
        },
    },
]
