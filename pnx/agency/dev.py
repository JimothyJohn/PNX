from models import *
from agent import Agent
from utils import *

dev_prompt = Problem(
    owner="A market researcher trying to understand how they can engage highly-qualified industry contacts.",
    location="Rogers, Arkansas",
)

dev_action = Action(
    constraints="""
Only create a single, index.html file.
Do not use any external libraries or frameworks.
Do not use any external stylesheets.
Do not use any javascript.
Do not use any images.
""",
    goal=f"""
Create a website via a single index.html file that will show the contact information for each person in the "outreaches" along with the message and article content in an easy to read format.
Use a simple flexible grid layout that's designed to be scrolled like on mobile where the user scrolls through the outreaches.
""",
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
""",
)


async def web_development(filename: str = f"{OUTPUT_FOLDER}/messages.json"):
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

    print("Creating website...           ", end="\r", flush=True)
    messages = load_messages(filename)
    website = await dev.take_action(
        dev_prompt,
        Action(
            constraints="""
Only create a single, index.html file.
Do not use any external libraries, frameworks, or stylesheets.
Do not use any javascript or images.
""",
            goal=f"""
Create a website via a single index.html file that will show the contact information for each person in the list below along with the message and article content in an easy to read format.
Use a simple flexible grid layout that's designed to be scrolled like on mobile where the user scrolls through the outreaches.
Contacts:
{messages[-2]['contacts']}
Messages:
{messages[-1]['messages']}
""",
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
""",
        ),
    )

    save_webpage(website["website"])
