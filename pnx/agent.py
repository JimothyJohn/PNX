import os
import json
from openai import AsyncOpenAI
from utils import *
from tools import *
from events import AsyncEventHandler
from models import *


class Agent:
    def __init__(
        self,
        model: str = "gpt-4o-2024-05-13",
        api_key: str = os.environ.get("OPENAI_API_KEY"),
        instructions: str = "",
        additional_instructions: str = "",
        name: str = "Agent",
        tools: list = [],
        temperature: float = 0.2,
    ) -> None:
        self.model = model
        self.client = AsyncOpenAI(api_key=api_key)
        self.run = None
        self.instructions = instructions
        self.additional_instructions = additional_instructions
        self.temperature = temperature
        self.name = name
        self.tools = tools
        self.messages = []

    async def initialize(self) -> None:
        self.assistant = await self.client.beta.assistants.create(
            name=self.name,
            instructions=self.instructions,
            tools=self.tools,
            model=self.model,
            temperature=self.temperature,
        )
        self.thread = await self.client.beta.threads.create()

    async def __run(
        self, additional_instructions: str = "", tool_choice="auto"
    ) -> dict:
        # https://platform.openai.com/docs/assistants/overview?context=with-streaming
        async with self.client.beta.threads.runs.stream(
            thread_id=self.thread.id,
            assistant_id=self.assistant.id,
            tool_choice=tool_choice,
            additional_instructions=additional_instructions,
            response_format={"type": "json_object"},
            event_handler=AsyncEventHandler(),
        ) as stream:
            await stream.until_done()
            if hasattr(stream, "get_final_run_steps") and callable(
                getattr(stream, "get_final_run_steps")
            ):
                steps = await stream.get_final_run_steps()
            else:
                return

        if hasattr(steps[-1].step_details, "tool_calls"):
            tool_calls = steps[-1].step_details.tool_calls
            await self.tool_call(tool_calls, steps[-1].run_id)
        else:
            tool_calls = None

        lastMessage = await self.client.beta.threads.messages.list(self.thread.id)
        print(f"Messages: {lastMessage.data[0].content}")
        message_content = (
            lastMessage.data[0].content[0].text.value if lastMessage.data else None
        )
        messageJson = {}

        if message_content:
            print(f"Response content: {message_content}")  # Debugging line
            print(f"Response content: {message_content}")  # Debugging line
            try:
                messageJson = json.loads(message_content)
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {e}")
                print(f"Response content: {message_content}")
                return {"error": "Invalid JSON response"}
        else:
            print("No message content to parse.")
            return {"error": "Empty response"}

        self.messages.append(messageJson)
        return messageJson

    async def take_action(self, problem: Problem, action: Action) -> dict:
        await self.client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="assistant",
            content=f"""
I am a {problem.owner} trying to {problem.goal} in {problem.location}.
{problem.constraints}.
""",
        )
        await self.client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="user",
            content=f"""
{action.task}.
{action.expected_output}.
""",
        )

        return await self.__run()

    async def tool_call(self, tool_calls: list, run_id: str) -> None:
        tool_outputs = []
        for tool in tool_calls:
            if tool.function.name == "get_coin_price":
                tool_query_string = eval(tool.function.arguments)["cryptocoin"]
                output = get_coin_price(tool_query_string)
                tool_outputs.append({"tool_call_id": tool.id, "output": f"{output}"})

            elif tool.function.name == "search_web":
                tool_query_string = eval(tool.function.arguments)["query"]
                output = search_web(tool_query_string)
                tool_outputs.append({"tool_call_id": tool.id, "output": f"{output}"})

            elif tool.function.name == "scrape_website":
                tool_query_string = eval(tool.function.arguments)["url"]
                output = scrape_website(tool_query_string)
                tool_outputs.append({"tool_call_id": tool.id, "output": f"{output}"})

            else:
                print(f"Error: function {tool.function.name} does not exist")

        if tool_outputs:
            try:
                async with self.client.beta.threads.runs.submit_tool_outputs_stream(
                    thread_id=self.thread.id,
                    run_id=run_id,
                    tool_outputs=tool_outputs,
                    event_handler=AsyncEventHandler(),
                ) as stream:
                    await stream.until_done()

            except Exception as e:
                print("Failed to submit tool outputs:", e)
        else:
            print("No tool outputs to submit.")

    async def upload(self, filename: str) -> None:
        await self.client.files.create(file=open(f"{filename}", "rb"), purpose="vision")
