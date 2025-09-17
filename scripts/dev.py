import asyncio
from activities import say_hello


async def main():
    result = await say_hello("Daniel")
    print(result)

asyncio.run(main())
