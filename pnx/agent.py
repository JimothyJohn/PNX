import os
import json
from config import logger
from openai import AsyncAzureOpenAI, AsyncOpenAI
from utils import *
from tools import *
from events import AsyncEventHandler
from models import *

class Agent:
    def __init__(
        self,
        name: str = "Agent",
        model: str = "gpt-4o-2024-05-13",
        api_key: str = os.environ.get("OPENAI_API_KEY"),
        instructions: str = "",
        tools: list = [],
        temperature: float = 0.2,
    ) -> None:
        self.model = model
        self.client = AsyncOpenAI(api_key=api_key)
        if os.environ.get("PLATFORM") == "azure":
            self.model = os.environ.get("AZURE_OPENAI_DEPLOYMENT")
            self.client = AsyncAzureOpenAI(
                api_key=os.environ.get("AZURE_OPENAI_API_KEY"),  
                api_version=os.environ.get("AZURE_OPENAI_API_VERSION"),
                azure_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT"),
            )

        self.instructions = instructions
        self.temperature = temperature
        self.name = name
        self.tools = tools
        self.messages = []
        self.assistant = None
        self.thread = None

    async def __run(
        self, additional_instructions: str = "", tool_choice="auto"
    ) -> dict:

        if self.assistant == None: 
            self.assistant = await self.client.beta.assistants.create(
                name=self.name,
                instructions=self.instructions,
                tools=self.tools,
                model=self.model,
                temperature=self.temperature,
            )

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
                logger.warning("No steps this run!")
                return

        while hasattr(steps[-1].step_details, "tool_calls"):
            tool_calls = steps[-1].step_details.tool_calls

            tool_outputs = await self.tool_outputs(tool_calls, run_id=steps[-1].id)

            async with self.client.beta.threads.runs.submit_tool_outputs_stream(
                thread_id=self.thread.id,
                run_id=steps[-1].run_id,
                tool_outputs=tool_outputs,
                event_handler=AsyncEventHandler(),
            ) as stream:
                await stream.until_done()
                if hasattr(stream, "get_final_run_steps") and callable(
                    getattr(stream, "get_final_run_steps")
                ):
                    steps = await stream.get_final_run_steps()
                else:
                    return

        lastMessage = await self.client.beta.threads.messages.list(self.thread.id)
        message_content = (
            lastMessage.data[0].content[0].text.value if lastMessage.data else None
        )
        messageJson = {}

        if message_content:
            try:
                messageJson = json.loads(message_content)
                self.messages.append(messageJson)
            except json.JSONDecodeError as e:
                logger.warning(f"JSON decode error: {e}")
                exit()
        else:
            logger.warning("No message content to parse.")

        return messageJson

    async def take_action(self, problem: Problem, action: Action) -> dict:
        if self.thread == None: 
            self.thread = await self.client.beta.threads.create()

        await self.client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="user",
            content=f"""
{action.goal}.
{action.expected_output}.
{action.constraints}.
""",
        )

        return await self.__run()

    async def tool_outputs(self, tool_calls: list, run_id: str) -> list:
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
                output = scrape_website(tool_query_string)
                tool_outputs.append({"tool_call_id": tool.id, "output": f"{output}"})

            elif tool.function.name == "get_contact_info":
                tool_query_string = eval(tool.function.arguments)["firstName", "lastName", "companyName"]
                output = scrape_website(tool_query_string)
                tool_outputs.append({"tool_call_id": tool.id, "output": f"{output}"})

            else:
                logger.warning(f"Error: function {tool.function.name} does not exist")

        return tool_outputs

    async def upload(self, filename: str) -> None:
        await self.client.files.create(file=open(f"{filename}", "rb"), purpose="vision")
