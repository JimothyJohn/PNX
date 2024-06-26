#!/usr/bin/env python3
import asyncio
# from agency.dev import web_development
# from agency.research import research
from agency.prospector import prospect
from tools import get_token


async def main():
    # Get JWT token
    get_token()
    await prospect()
    # await web_development()
    # await web_development(filename="outputs/2024-06-19_04-42-56/messages.json")


if __name__ == "__main__":
    asyncio.run(main())
