from agent import Agent
from tools import tools
from models import *
from utils import *

my_prompt = Prompt(
    user="Industrial automation engineer that works with local manufacturers to automate manufacturing processses with automation hardware, not software, and provide an automation roadmap that will help them incorporate continuous improvement.",
    location="Rogers, Arkansas",
    constraints="""
Do not recommend or mention blockchain technology.
Do not create any messages or outreach to the contacts, just provide relevant information and context.
Avoid Fortune 500 companies and prioritize small cap businesses as this company doesn't have the nationwide infrastructure to support them.
Avoid companies with less than 25 people because we need to work with stable, reputable organizations.
Only provide companies with headquarters that are in close proximity because we'll have a better chance to engage decision makers.""",
    goal=f"""
Identify and profile key decision makers at local manufacturers that could use technology to solve the problem then provide their contact information.
""",
    problem="Tracking, safety, and traceability in food manufacturing.",
    sources=["https://hbr.org/"],
)


async def research():
    researchAssistant = Agent(
        name="Research Assistant",
        tools=tools,
        instructions="""
  You are a helpful assistant that aids the researcher in learning how they can solve a problem.
  You provided detailed, thoughtful responses that help explain your reasoning.
  You only use primary sources from reputable institutions and cite them accordingly.
  You avoid company publications and secondary sources.
  You prefer academic, non-corporate, unbiased information from other experts.
  You only use articles, blog posts, research papers, and transcripts, not whole websites or publications.
  You only use the most recent data as possible.
  """,
    )

    print("Initializing Research Assistant...", end="\r", flush=True)
    await researchAssistant.initialize()

    # Describe problem
    print("Comprehending problem...", end="\r", flush=True)
    problem = await researchAssistant.take_action(
        user_message=f"""
I am a {my_prompt.user}.
I'm trying to solve {my_prompt.problem} around {my_prompt.location}.
Here are my constraints: {my_prompt.constraints}.
My goal is to {my_prompt.goal}.)
""",
        additional_instructions="""
You will be given a problem statement, describe the problem statement in detail.
Incorporate the context and any relevant information that will help understand the problem.
Outline an action plan in detail that will help solve the problem.
""",
        expected_output="""
Output the description as this JSON object:
{
    "problem": "detailed problem statement.",
    "thought_process": "detailed thought process that will help solve the problem."
    "relevant_info": "relevant information that if provided will help you understand the problem."
    "approaches": ["approach one", "approach two", "approach three", ...],
    "keywords": ["keyword one", "keyword two", "keyword three", ...],
}
""",
    )

    # Create a plan
    print("Devising a plan...", end="\r", flush=True)
    plan = await researchAssistant.take_action(
        user_message=f"""
My problem is {problem['problem']}.
I'm thinking that {problem['thought_process']}.
I need to find {problem['relevant_info']}.
I want to try only the approaches from this list that can be done with internet research: {problem['approaches']}.
I recommend using some of these keywords to aid in your search: {problem['keywords']}.
""",
        additional_instructions="""
You will be given a problem statement, outline a plan to solve the problem only using further internet research.
Be very detailed and explain your thought process at each step.
Use an active language that helps the user understand exactly what will be needed.
""",
        expected_output="""
Output the plan as a JSON object with the following fields:
{
    "plan": ["step one", "step two", "step three", ...],
}
""",
    )

    # Execute the plan
    print("Executing the plan...", end="\r\n", flush=True)
    for step in plan["plan"]:
        print(step, end="\r", flush=True)
        await researchAssistant.take_action(
            user_message=f"""
Use your work so far to execute this step of the overall plan and explain the process in detail: {step}.
""",
            additional_instructions="""
Take a thorough approach to completing the action while outlining your thought process along the way.
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
        )

    save_messages(researchAssistant.messages, "messages.json")

    print(researchAssistant.messages)
