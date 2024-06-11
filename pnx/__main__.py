import asyncio
from bot import ChatBot
from assistant import Assistant

bot = ChatBot()
assistant = Assistant()

userInput = "Not blank"

async def main():
    # Test with different image sizes
    # image_path = "nameplate2.jpg"
    await assistant.initialize()
    
    # while userInput != "":
    userInput = input("Prompt: ")
    response = await assistant.test(userInput=userInput)

if __name__ == "__main__":
    asyncio.run(main())
