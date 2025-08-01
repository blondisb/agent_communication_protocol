import asyncio
import nest_asyncio
from acp_sdk.client import Client
from colorama import Fore

nest_asyncio.apply()

async def run_doctor_workflow() -> None:
    async with Client(base_url="http://localhost:8000") as doctor_finder:
        run1 = await doctor_finder.run_sync(
            agent="doctor_agent",
            input="I'm based in Atlanta, GA. Are they any cardiologists near me?"
        )
        
        print("\n========================\n run1: \n", run1)
        try:
            content = run1.output[0].parts[0].content
            print(Fore.LIGHTMAGENTA_EX+ content + Fore.RESET)
        except Exception as e:
            content = run1.error.message
            print(Fore.RED+ content + Fore.RESET)
            raise e

if __name__ == '__main__':
    asyncio.run(run_doctor_workflow())
    
    