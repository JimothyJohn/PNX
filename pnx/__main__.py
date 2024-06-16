import asyncio
from agent import Agent
from models import *
from utils import *
from research import research

dev_prompt = Prompt(
    user="Industrial automation engineer that works with local manufacturers to automate manufacturing processses with automation hardware, not software, and provide an automation roadmap that will help them incorporate continuous improvement.",
    location="Rogers, Arkansas",
    constraints="""
Only create a single, index.html file.
Do not use any external libraries or frameworks.
Do not use any external stylesheets.
Do not use any external scripts.
""",
    goal=f"""
Create a website frontend via a single index.html file that will outline the elements of the steps involved in the messages.
Clearly separate and outline the steps on the webpage.
Use a simple markdown-like layout that's designed to be scrolled like on mobile.
""",
    problem="Tracking, safety, and traceability in food manufacturing.",
    sources=["https://hbr.org/"],
)

dev = Agent(
    name="Web Dev",
    instructions="""
You create website that helpfully summarize information.
""",
)


async def main():
    await research()


if __name__ == "__main__":
    asyncio.run(main())
