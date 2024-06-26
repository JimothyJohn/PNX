import json
import os
import requests
from config import logger
import browser_cookie3
import zi_api_auth_client
from linkedin_api import Linkedin

"""
{
    "type": "function",
    "function": {
        "name": "get_linkedin_profile",
        "description": "Use this function to scrape a LinkedIn Profile.",
        "parameters": {
            "type": "object",
            "properties": {
                "profile_id": {
                    "type": "string",
                    "description": "URL of the profile to scrape. Example: 'satyanadella/' in https://www.linkedin.com/in/satyanadella/",
                }
            },
            "required": ["profile_id"],
        },
    },
},
"""

tools = [
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Use this function to do a Google search on the web.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "A query to search for on the web.",
                    }
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "scrape_website",
            "description": "Use this function to scrape a website.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "URL of the website to scrape.",
                    }
                },
                "required": ["url"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_contact",
            "description": "Use this function to get contact information for a specific person.",
            "parameters": {
                "type": "object",
                "properties": {
                    "firstName": {
                        "type": "string",
                        "description": "First name of the person.",
                    },
                    "lastName": {
                        "type": "string",
                        "description": "Last name of the person.",
                    },
                    "companyName": {
                        "type": "string",
                        "description": "Company the person works for.",
                    },
                },
                "required": ["firstName", "lastName", "companyName"],
            },
        },
    },
]


anthropic_tools = [
    {
        "name": "search_web",
        "description": "Use this function to do a Google search on the web.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "A query to search for on the web.",
                }
            },
            "required": ["query"],
        },
    },
    {
        "name": "scrape_website",
        "description": "Use this function to scrape a website.",
        "input_schema": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "URL of the website to scrape.",
                }
            },
            "required": ["url"],
        },
    },
]


def search_web(query: str) -> str:
    """
    Searches the web for a specific query.

    :param query: The query to search for.
    :return: The search results.
    """

    url = "https://google.serper.dev/search"

    payload = json.dumps({"q": query, "location": "United States"})
    headers = {
        "X-API-KEY": os.environ.get("SERPER_API_KEY"),
        "Content-Type": "application/json",
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    resultsJson = response.json()["organic"]

    logger.info(f"Found {len(resultsJson)} results for {query}")

    return response.text


def scrape_website(website: str) -> str:
    """
    Scrapes a website.

    :param website: The website to scrape.
    :return: The scrape results.
    """
    url = "https://scrape.serper.dev"

    payload = json.dumps(
        {
            "url": f"{website}",
        }
    )
    headers = {
        "X-API-KEY": os.environ.get("SERPER_API_KEY"),
        "Content-Type": "application/json",
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    responeJson = response.json()

    if hasattr(responeJson, "message"):
        return f"You need to scrape {website} again"

    domain = website.split(".")

    logger.info(f"Visiting {domain}...")

    # Limit the size of the output to 512KB
    # openai.BadRequestError: Error code: 400 - {'error': {'message': "'tool_outputs' too large: the combined tool outputs must be less than 512kb.", 'type': 'invalid_request_error', 'param': 'tool_outputs', 'code': 'invalid_value'}}
    max_size = 512 * 512  # 512KB in bytes
    output = response.text

    if len(output) > max_size:
        # Summarize the output to fit within the size limit
        summary = (
            f"Output too large to display. Content from {website} has been omitted."
        )
        return summary

    return response.text


def get_cookie_jar(
    domain_name: str = ".linkedin.com",
    # Find your cookie file here: https://www.digitalcitizen.life/cookies-location-windows-10/
    cookie_file: str = os.environ.get("COOKIE_FILE"),
) -> requests.cookies.RequestsCookieJar:
    # Recommended CHALLENGE workaround: https://github.com/tomquirk/linkedin-api/issues/392#issue-2286978242
    try:
        cookiejar_simple = browser_cookie3.firefox(
            domain_name=domain_name,
            cookie_file=cookie_file,
        )
    except:
        print("Error finding cookie file...")
        exit()

    cookiejar = requests.cookies.RequestsCookieJar()

    for cookie in cookiejar_simple:
        cookiejar.set_cookie(cookie)

    return cookiejar


def get_linkedin_profile(profile_id: str):
    # Authenticate using any Linkedin account credentials
    api = Linkedin(
        os.environ.get("LINKEDIN_USER"),
        os.environ.get("LINKEDIN_PASS"),
        cookies=get_cookie_jar(),
    )

    profile = api.get_profile(profile_id)
    print(f"LinkedIn profile: {profile}")

    return api.get_profile(str(profile_id))


def read_api_key(file: str = "pki.pem") -> str:
    key = ""
    if not os.path.isfile(file):
        print(
            f"Key file {file} not found, create an API key and save to {file}: https://admin.zoominfo.com/#/api"
        )
        exit()

    with open(file, "r") as f:
        key = f.read()

    return key


def create_token():
    key = read_api_key()
    token = zi_api_auth_client.pki_authentication(
        os.environ.get("ZOOMINFO_USER"), os.environ.get("ZOOMINFO_CLIENT_ID"), key
    )

    with open("jwt.pem", "w") as f:
        f.write(token)

    return


def get_token(file: str = "jwt.pem"):
    token = ""

    if not os.path.isfile(file):
        print(f"Token file {file} not found, getting new token...")
        create_token()
        exit()

    with open(file, "r") as f:
        token = f.read()

    return token

# https://api-docs.zoominfo.com/#2e5121fd-df42-41a4-95d6-0e8f24eebd92
def search_contacts(data: dict):
    response = check_response("https://api.zoominfo.com/search/contact", data)

    return response


# https://api-docs.zoominfo.com/#c145dd01-eb54-4fc2-bbdb-9edc04b7ea1b
def get_contact(firstName: str, lastName: str, companyName: str) -> str:
    data = {
        "matchPersonInput": [
            {
                "firstName": firstName,
                "lastName": lastName,
                "companyName": companyName,
            }
        ],
        "outputFields": [
            "email",
            "phone",
            "city",
            "zipCode",
            "state",
            "lastUpdatedDate",
            "jobTitle",
            "jobFunction",
            "companyDivision",
        ],
    }
    response = check_response("https://api.zoominfo.com/enrich/contact", data)
    try:
        if response.json()["result"][-1]["matchStatus"] != "FULL_MATCH":
            return f"No contact information found for {firstName} {lastName}"
    except:
        print("Error getting contact information")

    return response.text


def check_response(url: str, data: str = {}, method: str = "POST") -> requests.Response:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {get_token()}",
    }
    if method == "POST":
        response = requests.post(url, headers=headers, json=data)
    elif method == "GET":
        response = requests.get(url, headers=headers)
    else:
        print("Invalid method! Must be POST or GET")
        exit()

    if response.text == "Unauthorized":
        TOKEN = create_token()
        print(f"New token created, try again")
        exit()

    return response
