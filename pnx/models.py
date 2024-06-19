from pydantic import BaseModel


class Problem(BaseModel):
    owner: str = ""
    location: str = ""
    statement: str = ""


class Action(BaseModel):
    expected_output: str = ""
    tool_choice: str = "auto"
    goal: str = ""
    constraints: str = ""
