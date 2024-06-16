#!/usr/bin/env python3
import os
from openai import AsyncOpenAI
from pnx.utils import *
import asyncio

model = "gpt-4o"
client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


async def main():
    response = await client.chat.completions.create(
        model=model,
        messages={"role": "user", "content": "How are you today?"},
        temperature=0.2,
        max_tokens=500,
    )

    response.choices[0].message.content


if __name__ == "__main__":
    asyncio.run(main())
