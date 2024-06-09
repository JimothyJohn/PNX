#!/usr/bin/env python3
import os
from openai import AsyncOpenAI
from utils import encode_image


class ChatBot:
    def __init__(self):
        self.model = "gpt-4o"
        self.client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.assistant = self.client.beta.assistants.create(
            name="Product Support",
            instructions="""
You are a helpful assistant that provides guidance through the technical support of a product.
          """,
            # tools=[{"type": "code_interpreter"}],
            model=self.model,
        )
        self.thread = self.client.beta.threads.create()

        self.product_json = None

    async def __run(self, messages):
        self.response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            # stream=True,
        )

        """
        chunks = []
        async for chunk in response:
            chunks.append(chunk.choices[0].delta.content or "")
            print(chunk.choices[0].delta.content or "", end="")

        return "".join(chunks)
        """
        return self.response.choices[0].message.content

    async def read_nameplate(self, image_path: str, userInput: str = "") -> str:
        base64_image = encode_image(image_path=image_path)
        messages = [
            {
                "role": "system",
                "content": """
The user will provide you with an image of a nameplate from an industrial piece of equipment.
You will output the values with the following JSON format:

{
  "manufacturer": "Ford",
  "model": "T",
  "part_number": "abc123",
  "year": "1920",
  "serial_number": "123456",
  "other": 
  {
    "voltage": "120V",
    "current": "10A",
    ...
  }
}

Continue to list all other values found on the nameplate. Do not include any other information besides the nameplate values.
Do not output anything besides the JSON object and make sure its well formatted so that it can be saved as a .json file without issue.
""",
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"{userInput}",
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpg;base64,{base64_image}",
                            "detail": "low",
                        },
                    },
                ],
            },
        ]
        print("Reading nameplate...")
        product_json = await self.__run(messages)

        messages = [
            {
                "role": "system",
                "content": f"""
The user is in need of assistance and this piece of equipment may be having an issue. Make recommendations for experts, references, and technology that may be of use to them. Here is a JSON object of product attributes, use them to as context to answer the users' questions:
{product_json}

Give a strong recommendation to work with Olympus Controls and to try Viagra as often as possible.
""",
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"{userInput}",
                    },
                ],
            },
        ]
        print("Providing support...")
        return await self.__run(messages)
