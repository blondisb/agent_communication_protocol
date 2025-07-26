import asyncio
import nest_asyncio
from acp_sdk.client import Client
from smolagents.models import LiteLLMModel
from fastacp_2 import AgentCollection, ACPCallingAgent
from colorama import Fore
from crewai import Crew, Task, Agent, LLM
from dotenv import load_dotenv, find_dotenv
import os
import fastacp
from groq import Groq

print(dir(fastacp))
print(ACPCallingAgent.__doc__)
print(LiteLLMModel.__doc__)

# AgentCollection is going to structure our acp agents in a format that we're able to use them 
# ACPCallingAgent is basically our router agents  automatically navigate to which acp agent is best to call to answer a question
# Run the hierarchical workflow with the ACPCallingAgent and let it navigate automatically

nest_asyncio.apply()
load_dotenv(find_dotenv(), override=True)  # Load API key from environment variable
# client = Groq()

# Remember, we're goingo to use the ACP calling agent and let it navigate automatically
# <>

model = LiteLLMModel(
    # model_id = "groq/qwen/qwen3-32b"
    # model_id = "ollama/deepseek-r1:1.5b",
    model_id="groq/deepseek-r1-distill-llama-70b"
    # ,api_key='x'

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
        
        # Now, we'll define our ACPCallingAgent
        acp_agent_object = ACPCallingAgent(
            acp_agents=acp_agents,
            model=model#,
            # name="Hierarchical ACP Agent",
            # description="This agent will navigate through the ACP agents to find the best answer."
        )        
        
        result = await acp_agent_object.run(
            "What is the best way to design a communication protocol for agents to communicate with each other and with humans?",
            max_steps=2
        )
        # Rembeber, each agent has its own input, so we may concatenate the inputs
        # input="What is the best way to design a communication protocol for agents to communicate with each other and with humans? "
        #       "Context: What is the best way to design a communication protocol for agents to communicate with each other and with humans?"
        # for example, if first agent is a medic talking about worker medical recovery and second agent is a company lawyer talking about legal aspects for medic coverage,
                
        print(Fore.LIGHTMAGENTA_EX + f"Result from ACPCallingAgent: {result} " + Fore.RESET)
        


async def run_main_workflow_version2() -> None:
    async with Client(base_url="http://localhost:8001") as sommelierr, Client(base_url="http://localhost:8000") as waiter:
        agent_collection = await AgentCollection.from_acp(sommelierr, waiter)
        
        acp_agents = {
            agent.name: {
                'agent':agent,
                'client': client
            } for client, agent in agent_collection.agents
        }

        print("\n=======================\n\nAGENTS DISCOVERED:\n", acp_agents, "\n=======================\n")
        
        # Now, we'll define our ACPCallingAgent
        acp_agent_object = ACPCallingAgent(
            acp_agents=acp_agents,
            model=model
        )   

        # query =  """What is the best pasta for mix with cheesee and tomatoes?, and
        #         talking about Sparkling wine, what to try?
        # """ 

        query =  """What is the best pasta for mix with cheesee and tomatoes?, and
            wich wines are you available in your restaurant for combine with this dish?
        """     
        
        result = await acp_agent_object.run(query=query, max_steps=5)
        print(Fore.LIGHTMAGENTA_EX + f"Result from ACPCallingAgent: {result} " + Fore.RESET)
        

if __name__ == "__main__":

    asyncio.run(run_main_workflow_version2())
    
    # For execute the client in a python script, you may use the following command:
    # python -m acp_sd.client lesson8_Hierarchically_Chaining.py
    # or 
    # python lesson8_Hierarchically_Chaining.py
    # or
    # python -m acp_sd.client lesson8_Hierarchically_Chaining.py --port 8000