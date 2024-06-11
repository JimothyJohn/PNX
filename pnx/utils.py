import base64
from tenacity import retry, wait_random_exponential, stop_after_attempt
from termcolor import colored
import json
from tools.crypto import *


def show_json(obj):
    print(json.loads(obj.model_dump_json()))


GPT_MODEL = "gpt-4o"


@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
def chat_completion_request(messages, tools=None, tool_choice=None, model=GPT_MODEL):
    try:
        """
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice=tool_choice,
        )

        return response
        """
        return ""
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e


def pretty_print_conversation(messages):
    role_to_color = {
        "system": "red",
        "user": "green",
        "assistant": "blue",
        "function": "magenta",
    }

    for message in messages:
        if message["role"] == "system":
            print(
                colored(
                    f"system: {message['content']}\n", role_to_color[message["role"]]
                )
            )
        elif message["role"] == "user":
            print(
                colored(f"user: {message['content']}\n", role_to_color[message["role"]])
            )
        elif message["role"] == "assistant" and message.get("function_call"):
            print(
                colored(
                    f"assistant: {message['function_call']}\n",
                    role_to_color[message["role"]],
                )
            )
        elif message["role"] == "assistant" and not message.get("function_call"):
            print(
                colored(
                    f"assistant: {message['content']}\n", role_to_color[message["role"]]
                )
            )
        elif message["role"] == "function":
            print(
                colored(
                    f"function ({message['name']}): {message['content']}\n",
                    role_to_color[message["role"]],
                )
            )


# Function to encode the image as base64
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


async def tool_call(self, thread, run) -> None:
    if self.run.required_action is None:
        return

    tool_calls = self.run.required_action.submit_tool_outputs.tool_calls

    for tool in tool_calls:
        tool_outputs = []

        if tool.function.name == "get_coin_price":
            tool_query_string = eval(tool.function.arguments)["cryptocoin"]
            output = get_coin_price(tool_query_string)
            tool_outputs.append({"tool_call_id": tool.id, "output": f"{output}"})

        elif tool.function.name == "search_web":
            tool_query_string = eval(tool.function.arguments)["query"]
            output = search_web(tool_query_string)
            tool_outputs.append({"tool_call_id": tool.id, "output": f"{output}"})

        else:
            print(f"Error: function {tool.function.name} does not exist")

            # Submit all tool outputs at once after collecting them in a list

    if tool_outputs:
        try:
            run = await self.client.beta.threads.runs.submit_tool_outputs_and_poll(
                thread_id=thread.id,
                run_id=run.id,
                tool_outputs=tool_outputs,
            )
            print("Tool run started...", end="")
            while self.run.status == "queued" or self.run.status == "in_progress":
                print(".", end="")
                self.run = await self.client.beta.threads.runs.retrieve(
                    thread_id=self.thread.id,
                    run_id=self.run.id,
                )
                sleep(0.5)

        except Exception as e:
            print("Failed to submit tool outputs:", e)
    else:
        print("No tool outputs to submit.")

    if run.status == "completed":
        messages = self.client.beta.threads.messages.list(thread_id=self.thread.id)
        for message in messages:
            print(message)
    else:
        print(run.status)
