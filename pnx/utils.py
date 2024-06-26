import os
import base64
import datetime
import json
from tools import *

NOW = datetime.datetime.now()
OUTPUT_FOLDER = f"outputs/{NOW.strftime('%Y-%m-%d_%H-%M-%S/')}"


# Function to encode the image as base64
def encode_image(image_path: str) -> str:
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


# Save chain of images as JSON
def save_messages(messages: list, filename: str = "messages.json") -> None:
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    file_path = os.path.join(OUTPUT_FOLDER, filename)
    with open(file_path, "w") as f:
        json.dump(messages, f, indent=4)


# Load chain of images JSON
def load_messages(filename: str = f"{OUTPUT_FOLDER}/messages.json") -> list:
    with open(filename, "r") as f:
        messages = json.loads(f.read())

    return messages


# Save webpage to HTML file
def save_webpage(html_file: str, filename: str = f"{OUTPUT_FOLDER}/index.html") -> None:
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    with open(filename, "w") as f:
        f.write(html_file)


async def get_tool_outputs(tool_calls: list) -> list:
    tool_outputs = []
    for tool in tool_calls:
        if tool.function.name == "search_web":
            tool_query_string = eval(tool.function.arguments)["query"]
            output = search_web(tool_query_string)
            tool_outputs.append({"tool_call_id": tool.id, "output": f"{output}"})

        elif tool.function.name == "scrape_website":
            tool_query_string = eval(tool.function.arguments)["url"]
            output = scrape_website(tool_query_string)
            tool_outputs.append({"tool_call_id": tool.id, "output": f"{output}"})

        elif tool.function.name == "get_linkedin_profile":
            tool_query_string = eval(tool.function.arguments)["profile_id"]
            logger.info(f"Getting LinkedIn profile {tool_query_string}...")
            output = get_linkedin_profile(tool_query_string)
            tool_outputs.append({"tool_call_id": tool.id, "output": f"{output}"})

        elif tool.function.name == "get_contact":
            firstName_string = eval(tool.function.arguments)["firstName"]
            lastName_string = eval(tool.function.arguments)["lastName"]
            companyName_string = eval(tool.function.arguments)["companyName"]
            logger.info(
                f"Getting contact info for {firstName_string} {lastName_string}..."
            )
            output = get_contact(firstName_string, lastName_string, companyName_string)
            logger.info(f"Received {output}...")
            tool_outputs.append({"tool_call_id": tool.id, "output": f"{output}"})

        else:
            logger.warning(f"Error: function {tool.function.name} does not exist")

    return tool_outputs
