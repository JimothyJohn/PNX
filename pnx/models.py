from pydantic import BaseModel


class Problem(BaseModel):
    owner: str = ""
    goal: str
    location: str = ""
    constraints: str = ""


class Action(BaseModel):
    task: str
    expected_output: str
    tool_choice: str = "auto"
