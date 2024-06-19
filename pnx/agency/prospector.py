from agent import Agent
from tools import tools
from models import *
from utils import *

prospect_problem = Problem(
    owner="""
Industrial automation engineer that works with local manufacturers to automate manufacturing processses with automation hardware, not software, and provide an automation roadmap that will help them incorporate continuous improvement
""",
    location="Rogers, Arkansas",
    statement="""
tracking, safety, and traceability in food manufacturing.
""",
)

researchArticles = Action(
    constraints="""
You only use sources from reputable organizations because they will provide the msot creidble information and don't have special interests.
You prefer academic, non-corporate, unbiased information.
Do not research blockchain technology as we sell hardware and blockchain doesn't work in the manufacturing space.
""",
    goal=f"""
Find 5 highly-qualified articles about {prospect_problem.statement}
""",
    expected_output="""
Output the response as a JSON list:
[
    {
        "website": HttpUrl
        "title": Optional[str] = None
        "author": Optional[str] = None
        "publisher": str
        "industry": str
        "abstract": str
        "published_date": Optional[datetime] = None
    },
    ...
]
""",
)

researchCompanies = Action(
    tool_choice="required",
    goal=f"""
Identify 10 local manufacturers in {prospect_problem.location} that may have a problem with {prospect_problem.statement}.
    """,
    constraints="""
Avoid large companies and prioritize small, local businesses as this company doesn't have the nationwide infrastructure to support large customers.
Do not include nationwide or international companies because it's harder to grow business when multiple geographies are involved.
Do not include nationally-recognized brands because people are already aware of them.
Avoid companies with less than 25 people because we need to work with stable, reputable organizations.
Only provide companies with headquarters that are in close proximity because we'll have a better chance to engage decision makers.
""",
    expected_output="""
Output the response as a JSON list:
[
    {
        "name": str
        "website": HttpUrl
        "industry": str
        "hq_city": str
        "hq_state": str
        "employees": Optional[int]
        "annual_revenue": Optional[int]
        "relevance": str
    },
    ...
]
""",
)

findContacts = Action(
    tool_choice="required",
    goal=f"""
Identify 3 employees at each of the 5 manufacturers for a total of 15 contacts that may have problems with {prospect_problem.statement}. 
Provide as much contact information as possible.
""",
    constraints="""
Do not include executives, only managers, as we won't be able to contact high-level, national contacts.
""",
    expected_output="""
Output the response as a JSON list:
[
    {
        "firstName": str
        "lastName": str
        "companyName": str
        "linkedin": HttpUrl
        "email": str
        "mobile number": str
        "direct number": str
        "city": str
        "relevance": str
    },
    ...
]
""",
)

engageContacts = Action(
    goal=f"""
Use the articles to create personalized content for each of these contacts.
""",
    constraints="""
Use a very short, casual, respectful message.
Don't waste their time by adding to much unnecessary wording.
Use a specific article and explain why you thought it was relevant.
Ask for nothing in return, just let them know you're well qualified to provide the information and understand their problem.
""",
    expected_output="""
Output the response as a JSON list:
[
    {
        "firstName": str
        "lastName": str
        "companyName": str
        "message": str
        "article": url
    },
    ...
]
""",
)

researchAssistant = Agent(
    name="Research Assistant",
    tools=tools,
    instructions="""
You are a helpful open source intelligence internet researcher that will use publicly available information on the internet to solve a problem.
You use the search_web tool to find information and provide detailed sources and the scrape_website tool to extract useful information from webpages.
You provided detailed, thoughtful responses and explain your reasoning.
You only use information less than 4 years old.
You verify that all information provided is accurate and up-to-date.
You provide links for all external information.
""",
)


async def prospect():
    print("Researching articles...               ", end="\r", flush=True)
    articles = await researchAssistant.take_action(prospect_problem, researchArticles)

    print("Researching companies...                ", end="\r\n", flush=True)
    companies = await researchAssistant.take_action(prospect_problem, researchCompanies)

    print("Finding contacts...                ", end="\r\n", flush=True)
    await researchAssistant.take_action(prospect_problem, findContacts)

    print("Creating outreach...                ", end="\r\n", flush=True)
    outreaches = await researchAssistant.take_action(prospect_problem, engageContacts)

    save_messages(researchAssistant.messages, "messages.json")
