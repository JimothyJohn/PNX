from agent import Agent
from tools import tools
from models import *
from utils import *

prospect_problem = Problem(
    owner="""
Industrial automation engineer that works with local manufacturers to automate manufacturing processses with automation hardware, not software, and provides an automation roadmap that will help them incorporate continuous improvement
""",
    location="Fort Smith, AR",
    statement="""
OEM machine design for food manufacturing.
""",
)

researchArticles = Action(
    tool_choice="required",
    constraints="""
You only use sources from reputable organizations because they will provide the most credible information and don't have special interests.
You prefer academic, non-corporate, unbiased information as it should be of the highest quality.
You will not research blockchain technology as we sell hardware and blockchain doesn't work in the manufacturing space.
You will focus on articles related to operations, not investment.
""",
    goal=f"""
Use the search_web and search_website functions to find 5 highly-qualified articles about {prospect_problem.statement}
""",
    expected_output=Article)

researchCompanies = Action(
    tool_choice="required",
    goal=f"""
Use the search_web and search_website functions to identify 5 highly-qualified local manufacturers in {prospect_problem.location} that may have a problem with {prospect_problem.statement}.
    """,
    constraints=f"""
You will avoid large companies and prioritize small, local businesses as this company doesn't have the nationwide infrastructure to support large customers.
You will not include nationwide or international companies because it's harder to grow business when multiple geographies are involved.
You will not include nationally-recognized brands because people are already aware of them.
You will avoid companies with less than 25 people because we need to work with stable, reputable organizations.
You will only provide companies with headquarters that are in close proximity because we'll have a better chance to engage decision makers.
You will not include resellers, logistics companies, or consultancies because they do not actually make anything.
You will only provide companies that design, manufacture, and deploy OEM machinery because they are the most likely to have a problem with {prospect_problem.statement}.
""",
    expected_output=Company)


findContacts = Action(
    tool_choice="required",
    goal=f"""
Use the search_web and scrape_website function to identify 3 employees at each of the 5 manufacturers for a total of 15 contacts that may have problems with {prospect_problem.statement}. 
Provide as much contact information as possible.
""",
    constraints="""
Do not include executives, only managers that would likely be involved in the manufacturing process, as we won't be able to contact high-level, national contacts.
""",
    expected_output=Contact)

getContactsInfo = Action(
    tool_choice="required",
    goal=f"""
Use the get_contact function to get the contact's information and use search_web to get the contact's LinkedIn profile, 
Provide as much contact information as possible.
""",
    expected_output=Contact)

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
    expected_output=Outreach)

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
    """
    print("Researching articles...               ", end="\r", flush=True)
    articles = await researchAssistant.take_action(prospect_problem, researchArticles)
    save_messages(articles, "articles.json")
    """
   
    print("Researching companies...                ", end="\r", flush=True)
    companies = await researchAssistant.take_action(prospect_problem, researchCompanies)
    save_messages(companies, "companies.json")

    print("Finding contacts...                ", end="\r", flush=True)
    contacts = await researchAssistant.take_action(prospect_problem, findContacts)
    save_messages(contacts, "contacts.json")

    
    print("Finding contact info...                ", end="\r", flush=True)
    contact_info = await researchAssistant.take_action(prospect_problem, getContactsInfo)
    save_messages(contact_info, "contact_info.json")

    
    """
    print("Creating outreach...                ", end="\r", flush=True)
    outreaches = await researchAssistant.take_action(prospect_problem, engageContacts)
    save_messages(outreaches, "outreaches.json")
    """

    save_messages(researchAssistant.messages, "messages.json")
