import asyncio
import nest_asyncio
from acp_sdk.client import Client
from smolagents import LiteLLMModel
from fastacp import AgentCollection, ACPCallingAgent
from colorama import Fore

import fastacp
print(dir(fastacp))
print(ACPCallingAgent.__doc__)

# AgentCollection is going to structure our acp agents in a format that we're able to use them 
# ACPCallingAgent is basically our router agents  automatically navigate to which acp agent is best to call to answer a question
# Run the hierarchical workflow with the ACPCallingAgent and let it navigate automatically

nest_asyncio.apply()

# Remember, we're goingo to use the ACP calling agent and let it navigate automatically
# <>

model = LiteLLMModel(
    model_id = "groq/compound-beta"
)

async def run_main_workflow() -> None:
    async with Client(base_url="http://localhost:8001") as engineer, Client(base_url="http://localhost:8000") as designer:
        agent_collection = await AgentCollection.from_acp(engineer, designer)
        
        acp_agents = {
            agent.name: {
                'agent':agent,
                'client': client
            } for client, agent in agent_collection.agents
        }
        
        print(acp_agents)
        
        # Now, we'll define our ACPCallingAgent
        acpAgent = ACPCallingAgent(
            acp_agents=acp_agents,
            model=model#,
            # name="Hierarchical ACP Agent",
            # description="This agent will navigate through the ACP agents to find the best answer."
        )
        
        
        result = await acpAgent.run(
            "What is the best way to design a communication protocol for agents to communicate with each other and with humans?"
        )
        # Rembeber, each agent has its own input, so we may concatenate the inputs
        # input="What is the best way to design a communication protocol for agents to communicate with each other and with humans? "
        #       "Context: What is the best way to design a communication protocol for agents to communicate with each other and with humans?"
        # for example, if first agent is a medic talking about worker medical recovery and second agent is a company lawyer talking about legal aspects for medic coverage,
        
        
        print(Fore.LIGHTMAGENTA_EX + f"Result from ACPCallingAgent: {result} " + Fore.RESET)
        
        
if __name__ == "__main__":
    asyncio.run(run_main_workflow())
    
    # For execute the client in a python script, you may use the following command:
    # python -m acp_sd.client lesson8_Hierarchically_Chaining.py
    # or 
    # python lesson8_Hierarchically_Chaining.py
    # or
    # python -m acp_sd.client lesson8_Hierarchically_Chaining.py --port 8000