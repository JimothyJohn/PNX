import os
import base64
import datetime
import json

NOW = datetime.datetime.now()
OUPTUT_FOLDER = f"outputs/{NOW.strftime('%Y-%m-%d_%H-%M-%S/')}"


# Function to encode the image as base64
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def save_messages(messages: list, filename: str) -> None:
    if not os.path.exists(OUPTUT_FOLDER):
        os.makedirs(OUPTUT_FOLDER)

    file_path = os.path.join(OUPTUT_FOLDER, filename)
    with open(file_path, "w") as f:
        json.dump(messages, f, indent=4)


def load_messages(filename: str) -> list:
    with open(filename, "r") as f:
        messages = json.load(f)
    return messages


def save_webpage(html_file: str) -> None:
    if not os.path.exists(OUPTUT_FOLDER):
        os.makedirs(OUPTUT_FOLDER)

    file_path = os.path.join(OUPTUT_FOLDER, "index.html")
    with open(file_path, "w") as f:
        f.write(html_file)
