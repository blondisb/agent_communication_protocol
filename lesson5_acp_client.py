import nest_asyncio
import asyncio
from colorama import Fore
from acp_sdk.client import Client

nest_asyncio.apply()

async def example() -> None:
    async with Client(base_url="http://localhost:8001") as client:
        run = await client.run_sync(
            agent = "function_engineer_agent",
            input = "What is the best way to design a communication protocol for agents to communicate with each other and with humans?"
        )

        print(Fore.YELLOW + run.output[0].parts[0].content + Fore.RESET)

if __name__ == "__main__":
    asyncio.run(example())
    
    # For execute the client in a python script, you may use the following command:
    # python -m acp_sdk.client lesson4_acp_client.py
    # or 
    # python lesson4_acp_client.py
    # or
    # python -m acp_sdk.client lesson4_acp_client.py --port 8000