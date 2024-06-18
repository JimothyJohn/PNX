#!/usr/bin/env python3
import asyncio
from agency.dev import web_development
from agency.research import research


async def main():
    await research()
    await web_development(filename="outputs/2024-06-18_02-23-37/messages.json")


if __name__ == "__main__":
    asyncio.run(main())
