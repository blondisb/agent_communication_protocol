import asyncio
import nest_asyncio
from acp_sdk.client import Client
from colorama import Fore

nest_asyncio.apply()

async def run_workflow() -> None:
    async with Client(base_url = "http://localhost:8001") as engineer, Client(base_url = "http://localhost:8000") as designer:
        
        run1 = await designer.run_sync(
            agent = "designer_agent",
            input = "What is the best way to design a communication protocol for agents to communicate with each other and with humans?"
        )

        content = run1.output[0].parts[0].content
        print(Fore.LIGHTMAGENTA_EX + content + Fore.RESET)

        run2 = await engineer.run_sync(
            agent = "function_engineer_agent",
            input = f"Context: {content} \n\nWhat is the best way to design a communication protocol for agents to communicate with each other and with humans?"
        )

        content2 = run2.output[0].parts[0].content
        print(Fore.LIGHTCYAN_EX + content2 + Fore.RESET)

if __name__ == "__main__":
    asyncio.run(run_workflow())
    
    # For execute the client in a python script, you may use the following command:
    # python -m acp_sd.client lesson7_client.py
    # or 
    # python lesson6_client.py
    # or
    # python -m acp_sd.client lesson7_client.py --port 8000