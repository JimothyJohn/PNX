#!/usr/bin/env python3
import os
from openai import AsyncOpenAI
from utils import *
from time import sleep
from tools.tools import *
from tools.crypto import *
from events import EventHandler

class Assistant:
    def __init__(
        self, model: str = "gpt-4o", api_key: str = os.environ.get("OPENAI_API_KEY")
    ):
        self.model = model
        self.client = AsyncOpenAI(api_key=api_key)
        self.run = None

    async def initialize(self):
        self.assistant = await self.client.beta.assistants.create(
            name="Senior Researcher",
            instructions="""
You only use primary sources from reputable institutions and cite them accordingly.
You avoid company publications and secondary sources.
You search the web for sources and information.
You look through websites to find relevant information.
You prefer academic, non-corporate, unbiased information from other experts.
Your sources only include articles, blog posts, research papers, and transcripts, not whole websites or publications.
You only use the most recent data as possible.
Your sources will be used by the Market Analyst.
""",
            tools=tools,
            # tool_choice="auto",
            model=self.model,
        )
        self.thread = await self.client.beta.threads.create()

    async def __run(self) -> None:
        # https://platform.openai.com/docs/assistants/overview?context=with-streaming
        # https://github.com/PrefectHQ/marvin/blob/95e2936f576e28af7aa354c77c03a307ea4471c7/src/marvin/beta/assiostants/runs.py#L219
        async with self.client.beta.threads.runs.stream(
            thread_id=self.thread.id,
            assistant_id=self.assistant.id,
            instructions="Please address the user as Jane Doe. The user has a premium account.",
            event_handler=EventHandler(),
        ) as stream:
            steps = await stream.get_final_run_steps()

        try:
            tool_calls = steps[-1].step_details.tool_calls
        except:
            tool_calls = None

        if tool_calls: 
            await self.tool_call(tool_calls, steps[-1].run_id)


    async def test(self, userInput: str) -> None:
        await self.client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="assistant",
            content=f"""
Discover highly credible, relevant, and reputable primary sources related to {userInput}.
Provide at least 5 primary sources that will provide context and help the audience understand how and where to do further research.
Include the website, title, author, abstract, and published date of each source.
""",
        )
        await self.client.beta.threads.messages.create(
            thread_id=self.thread.id, role="user", content=f"{userInput}"
        )
        await self.__run()

    async def tool_call(self, tool_calls, run_id) -> None:
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

            else:
                print(f"Error: function {tool.function.name} does not exist")

        if tool_outputs:
            try:
                async with self.client.beta.threads.runs.submit_tool_outputs_stream(
                    thread_id=self.thread.id,
                    run_id=run_id,
                    tool_outputs=tool_outputs,
                    event_handler=EventHandler(),
                ) as stream:
                    await stream.get_final_run_steps()

            except Exception as e:
                print("Failed to submit tool outputs:", e)
        else:
            print("No tool outputs to submit.")

    async def upload(self, filename) -> None:
        await self.client.files.create(file=open(f"{filename}", "rb"), purpose="vision")
