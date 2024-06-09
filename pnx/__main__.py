import asyncio
from bot import ChatBot

bot = ChatBot()


async def main():
    # Test with different image sizes
    image_path = "nameplate2.jpg"
    userInput = input("What seems to be the issue? ")
    response = await bot.read_nameplate(image_path, userInput=userInput)
    # response = await bot.provide_assistance(userInput=userInput)
    print(response)


if __name__ == "__main__":
    asyncio.run(main())
