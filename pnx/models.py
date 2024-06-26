from typing import Type
from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime
from typing import List
import json


class Problem(BaseModel):
    owner: str = ""
    location: str = ""
    statement: str = ""


class Article(BaseModel):
    website: HttpUrl
    title: Optional[str] = None
    author: Optional[str] = None
    publisher: str
    industry: str
    abstract: str
    published_date: Optional[datetime] = None

class Company(BaseModel):
    name: str
    website: HttpUrl
    industry: str
    hq_city: str
    hq_state: str
    employees: Optional[int]
    annual_revenue: Optional[int]
    relevance: str

class Contact(BaseModel):
    firstName: str
    lastName: str
    companyName: str
    linkedin: HttpUrl
    email: str
    mobile_number: str
    direct_number: str
    city: str
    relevance: str

class Outreach(BaseModel):
    firstName: str
    lastName: str
    companyName: str
    email: str
    message: str
    article: HttpUrl

class FunctionParameters(BaseModel):
    query: str


class FunctionDetails(BaseModel):
    name: str
    description: str
    parameters: FunctionParameters


class Tool(BaseModel):
    type: str
    function: FunctionDetails


class ToolsModel(BaseModel):
    tools: List[Tool]

    def to_json(self) -> str:
        """Convert the ToolsModel instance to a JSON string."""
        return json.dumps(self.dict(), indent=4)


class Action:
    def __init__(
        self,
        expected_output: Type[BaseModel],
        tool_choice: str = "auto",
        goal: str = "",
        constraints: str = "",
    ):
        self.expected_output = self.__create_output(expected_output.__annotations__)
        self.tool_choice = tool_choice
        self.goal = goal
        self.constraints = constraints

    def __create_output(self, output):
        return f"""
Start by explaining your thought process and reasoning to accomplish the task.
Finish by describing the positives and negatives about the reults you found.
Output the response as a JSON list of this object:

"thought_process": str
{output}
"satisfaction_with_results": str
"issues_with_results": str
"should_retry": bool
"""
