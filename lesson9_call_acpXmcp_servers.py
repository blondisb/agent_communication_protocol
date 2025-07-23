import asyncio
import nest_asyncio
from acp_sdk.client import Client
from colorama import Fore

nest_asyncio.apply()

async def run_doctor_workflow() -> None:
    async with Client(base_url="http://localhost:8000") as waiter:
        run1 = await waiter.run_sync(
            agent="doctor_agent",
            input="I'm based in Atlanta, GA. Are they any cardiologists near me?"
        )
        
        content = run1.output[0].parts[0].content
        print(Fore.LIGHTMAGENTA_EX+ content + Fore.RESET)

if __name__ == '__main__':
    asyncio.run(run_doctor_workflow())
    
    