from agent import Agent
from tools import tools
from models import *
from utils import *

research_problem = Problem(
    owner="""
Industrial automation engineer that works with local manufacturers to automate manufacturing processses with automation hardware, not software, and provide an automation roadmap that will help them incorporate continuous improvement
""",
    location="Rogers, Arkansas",
    constraints="""
Do not include executives, only local managers, as we won't be able to contact high-level, national contacts.
Do not recommend or mention blockchain technology as we sell hardware and blockchain doesn't work in the manufacturing space.
Avoid Fortune 500 companies and prioritize small local businesses as this company doesn't have the nationwide infrastructure to support them.
Avoid companies with less than 25 people because we need to work with stable, reputable organizations.
Only provide companies with headquarters that are in close proximity because we'll have a better chance to engage decision makers.
Focus on contacts that would be interested in technology to improve tracking, safety, and traceability.
""",
    goal="""
Research articles on how automation technology is solving problems in manufacturing.
Identify 10 local food manucturers that may have this problem.
Identify 3 key decision makers at these manufacturers that may be a victim of this problem.
Extract their contact information, at least email and direct or mobile phone number.
Use the articles to create personalized content for each of these contacts.
Make recommendations of where to add personalizations and changes based on the target.
""",
)


async def research():
    researchAssistant = Agent(
        name="Research Assistant",
        tools=tools,
        instructions="""
You are a helpful open source intelligence internet researcher that will use publicly available information on the internet to solve a problem.
You use the search_web tool to find information and provide detailed sources and the scrape_website tool to extract useful information from webpages.
You provided detailed, thoughtful responses and explain your reasoning.
You only use sources from reputable organizations.
You prefer academic, non-corporate, unbiased information.
You only use information less than 4 years old.
You verify that all information provided is accurate and up-to-date.
You provide links for all external information.
""",
    )

    print("Initializing Research Assistant...           ", end="\r", flush=True)
    await researchAssistant.initialize()

    print("Comprehending problem...               ", end="\r", flush=True)
    plan = await researchAssistant.take_action(
        research_problem,
        Action(
            task="""
You will be given a problem, describe the problem in detail.
Explain the context and identify any other relevant information that will help understand the problem.
Explain your thought process and how you would approach the problem.
Outline an action plan in detail that will help solve the problem.
""",
            expected_output="""
Output the description as this JSON object:
{
    "problem": "detailed problem statement.",
    "thought_process": "detailed thought process that will help solve the problem."
    "relevant_info": "relevant information that if provided will help you understand the problem."
    "plan": ["step one", "step two", "step three", ...],
}
""",
        ),
    )

    print("Executing the plan...                ", end="\r\n", flush=True)
    for step in plan["plan"]:
        print(step)
        await researchAssistant.take_action(
            research_problem,
            Action(
                tool_choice="required",
                task=f"""
Take a thorough approach to {step} while outlining your thought process along the way.
Identify any areas that caused confusion or require further research.
Explain if the result is satisfactory or not and why.
""",
                expected_output="""
Output the result as a JSON object with the following fields:
{
    "step": "planStep",
    "results": "your results here",
    "success": "description of the level of success"
    "missing_info": "any information that was missing or unclear"
)
""",
            ),
        )

    save_messages(researchAssistant.messages, "messages.json")
