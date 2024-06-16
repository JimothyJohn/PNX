#!/usr/bin/env python3
import os
from openai import AsyncOpenAI
from utils import *
from tools.tools import *


class ChatBot:
    def __init__(self):
        self.model = "gpt-4o"
        self.product_json = None
        self.client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.messages = []

    @retry(
        wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3)
    )
    async def __run(self):
        try:
            self.response = await self.client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                tools=tools,
                tool_choice="auto",
                temperature=0.2,
                max_tokens=500,
            )

            """
                # stream=True,
            )

            
            chunks = []
            async for chunk in response:
                chunks.append(chunk.choices[0].delta.content or "")
                print(chunk.choices[0].delta.content or "", end="")

            return "".join(chunks)
            """

            # Step 2: determine if the response from the model includes a tool call.
            await self.tool_call()

            return self.response.choices[0].message.content
        except Exception as e:
            print("Unable to generate ChatCompletion response")
            print(f"Exception: {e}")
            return e

    async def read_nameplate(self, image_path: str, userInput: str = "") -> str:
        base64_image = encode_image(image_path=image_path)

        self.messages = [
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
                            "url": f"data:image/jpeg;base64,{base64_image}",
                            "detail": "low",
                        },
                    },
                ],
            },
        ]

        print("Reading nameplate...")
        product_json = await self.__run(userInput)

        self.messages.append(
            [
                {
                    "role": "system",
                    "content": f"""
The user is in need of assistance and this piece of equipment may be having an issue. Make recommendations for experts, references, and technology that may be of use to them. Here is a JSON object of product attributes, use them to as context to answer the users' questions:
{product_json}

Give a strong recommendation to work with Olympus Controls to resolve their issue.
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
        )
        print("Providing support...")
        return await self.__run()

    async def get_crypto(self, cryptocoin: str = "") -> str:
        self.messages = [
            {
                "role": "system",
                "content": """
Provide the user with the price of the cryptocurrency they requested. They will provide the symbol and you wil provie the price, for example: If the customer requests ethereum you will output "$3,145.56".
""",
            },
            {
                "role": "user",
                "content": f"{cryptocoin}",
            },
        ]

        await self.__run()

        print(f"{self.response.choices[0].message.content}")

    async def generic(self, userInput: str = "") -> str:
        self.messages.append(
            {
                "role": "system",
                "content": """
Provide the user with the price of the cryptocurrency they requested. They will provide the symbol and you wil provie the price, for example: If the customer requests ethereum you will output "$3,145.56".
""",
            }
        )
        self.messages.append(
            {
                "role": "user",
                "content": f"{userInput}",
            },
        )

        return await self.__run()

    # https://github.com/openai/openai-cookbook/blob/main/examples/How_to_call_functions_with_chat_models.ipynb
    async def tool_call(self) -> None:
        # Step 2: determine if the response from the model includes a tool call.
        tool_calls = self.response.choices[0].message.tool_calls
        if tool_calls:
            self.messages.append(
                {
                    "tool_calls": tool_calls,
                    "role": "assistant",
                }
            )

            for tool in tool_calls:
                # If true the model will return the name of the tool / function to call and the argument(s)
                tool_call_id = tool.id
                tool_function_name = tool.function.name

                # Step 3: Call the function and retrieve results. Append the results to the messages list.
                if tool_function_name == "get_coin_price":
                    tool_query_string = eval(tool.function.arguments)["cryptocoin"]
                    results = get_coin_price(tool_query_string)

                elif tool_function_name == "search_web":
                    tool_query_string = eval(tool.function.arguments)["query"]
                    results = search_web(tool_query_string)

                else:
                    print(f"Error: function {tool_function_name} does not exist")

                self.messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call_id,
                        "name": tool_function_name,
                        "content": f"{results}",
                    },
                )

            await self.__run()
        """
        else:
            # Model did not identify a function to call, result can be returned to the user
            print(f"No function call detected: {self.response}")
        """
