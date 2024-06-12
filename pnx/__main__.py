import asyncio
from assistant import Agent

agent = Agent()

async def main():
    # image_path = "nameplate2.jpg"
    await agent.initialize()
    
    userInput = input("What would you like to research?\n\n")
    await agent.find_sources(userInput=userInput)
    await agent.vet_sources()

if __name__ == "__main__":
    asyncio.run(main())
