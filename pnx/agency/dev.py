from models import *
from agent import Agent
from utils import *

dev_prompt = Problem(
    user="A market researcher trying to understand which companies, contacts, and technologies they should focus on.",
    location="Rogers, Arkansas",
    constraints="""
Only create a single, index.html file.
Do not use any external libraries or frameworks.
Do not use any external stylesheets.
Do not use any javascript.
Do not use any images.
""",
    goal=f"""
Create a website via a single index.html file that will outline the elements of the steps involved in the plan.
Clearly separate and outline the steps on the webpage.
Use a simple markdown-like layout that's designed to be scrolled like on mobile.
Include images if they help the context.
""",
)

async def web_development():
    dev = Agent(
        name="Web Dev",
        instructions="""
    You are an expert frontend web developer that creates HTML files.
    The websites you create helpfully summarize information.
    You do not write anything except HTML and css.
    """,
    )

    print("Initializing dev...           ", end="\r", flush=True)
    await dev.initialize()

    print("Creating website...")
    messages = load_messages("outputs/2024-06-17_11-53-28/messages.json")
    website = await dev.take_action(dev_prompt, Action(
        task=f"Create a website that outlines the steps involved in the plan: {messages}",
        expected_output="""
Output the entire website HTML text into a JSON object in its single key called website:
{
    "website": 
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Research Plan</title>
    <style>
      body {
        font-family: Arial, sans-serif;
        margin: 20px;
      }
      p {
        color: #333;
        font-size: 18px;
      }
      /* Add more styles as needed */
    </style>
  </head>
  <body>
	<p>Website goes here</p>
  </body>
</html>
""",))

    print(website)
    save_webpage(website["website"])
