#!/usr/bin/env python3
import asyncio
from agency.dev import web_development
from agency.research import research


async def main():
    # await research()
    await web_development()


if __name__ == "__main__":
    asyncio.run(main())
