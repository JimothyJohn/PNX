import os
import json
from config import logger
from anthropic import Anthropic
from utils import *
from tools import *
from events import AsyncEventHandler
from models import *


class Agent:
    def __init__(
        self,
        name: str = "Agent",
        model: str = "claude-3-5-sonnet-20240620",
        instructions: str = "",
        tools: list = anthropic_tools,
        temperature: float = 0.2,
    ) -> None:
        self.model = model
        self.client = Anthropic()
        self.instructions = instructions
        self.temperature = temperature
        self.name = name
        self.tools = tools
        self.messages = []

    def take_action(self, problem: Problem, action: Action) -> dict:
        self.messages.append(
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"""
{action.goal}.
{action.expected_output}.
{action.constraints}.
Do not output any information you didn't find online.
""",
                    }
                ],
            }
        )

        message = self.__create()

        while message.content[-1].type == "tool_use":
            content = message.content[-1]
            tool_output = get_tool_output(input=content.input, name=content.name)

            self.messages.append(
                {"role": "assistant", "content": message.content},
            )

            self.messages.append(
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": content.id,
                            "content": tool_output,
                        }
                    ],
                },
            )
            message = self.__create()

        return message

    def __create(
        self,
        model="claude-3-5-sonnet-20240620",
        max_tokens=1000,
        tool_choice={"type": "auto"},
        temperature=0,
        system="You are a helpful assistant.",
    ):
        message = self.client.messages.create(
            model=model,
            max_tokens=max_tokens,
            tools=self.tools,
            tool_choice=tool_choice,
            temperature=temperature,
            system=system,
            messages=self.messages,
        )
        return message


def test():
    agent = Agent()
    problem = Problem(
        owner="John Doe",
        location="New York",
        statement="Find the best restaurant in New York.",
    )
    action = Action(
        expected_output="Find the best restaurant in New York.",
        tool_choice="auto",
        goal="Find the best restaurant in New York.",
        constraints="Do not output any information you didn't find online.",
    )

    agent.take_action(problem, action)

    print(agent.messages)


test()
