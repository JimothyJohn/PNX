from models import *
from agent import Agent
from utils import *

writer_prompt = Problem(
    user="A marketer trying to explain how they can solve a specific problem by using focused, personal language that helps the reader.",
    location="Rogers, Arkansas",
    constraints="""
Only use common language, no jargon.
Explain the topic in a way the user would appreciate.
Be gracious and respectful with your message.
Be simple and to the point.
Offer sincerely to help.
""",
    goal=f"""
Craft a personalized message to a user that explains how you think you can help them.
Take a humble tone and offer to help in any way you can.
""",
)


async def web_development():
    dev = Agent(
        name="Writer",
        instructions="""
    You are an expert writer that creates messages tailored to a specific user. 
    You are an expert frontend web developer that creates HTML files.
    The websites you create helpfully summarize information.
    You do not write anything except HTML and css.
    """,
    )

    print("Initializing dev...           ", end="\r", flush=True)
    await dev.initialize()

    print("Creating website...")
    messages = load_messages(f"{OUPTUT_FOLDER}/messages.json")
    website = await dev.take_action(
        writer_prompt,
        Action(
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
""",
        ),
    )

    print(website)
    save_webpage(website["website"])
