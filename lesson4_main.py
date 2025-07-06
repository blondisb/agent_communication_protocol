
from collections.abc import AsyncGenerator
from acp_sdk.models import Message, MessagePart 
from acp_sdk.server import RunYield, RunYieldResume, Server

from crewai import Crew, Task, Agent, LLM
from crewai_tools import RagTool

from groq import Groq
import warnings
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(), override=True)  # Load API key from environment variable
warnings.filterwarnings("ignore")

client = Groq()
server = Server()

llm = LLM(
    # model="groq/llama-3.3-70b-versatile",
    model="groq/compound-beta",
    max_tokens=1024
)

config = {
    "llm": {
        "provider": "groq",
        "config": {
            "model": "llama-3.3-70b-versatile",
        }
    },
    "embedder": {
        "provider": "ollama",
        "config": {
            "model": "nomic-embed-text",
        }
    }
}

rag_tool = RagTool(
    config = config,
    chunk_size = 1200,
    chunk_overlap=200
)

rag_tool.add(
    "./pdf/doc.pdf",
    data_type = "pdf_file"
)

# The agent that we want to make available in our ACP server 
# ACP makes the agent available trhoug the docstring, so we may to be specific about the function signature
# and the docstring of the function, so that it can be used by other agents or humans in the ACP server.
# The docstring should contain the description of the agent, its role, goal, backstory
@server.agent()
async def function_engineer_agent(input: list[Message]) -> AsyncGenerator[RunYield, RunYieldResume]:
    """
    This is an agent that determines whether an agent is secure or not, depending on the use case.
    It uses a RAG pattern to find answers in a PDF document and provides a secure communication protocol for agents to communicate with each other and with humans.
    Use it to help answer questions on designing secure communication protocols for AI agents.
    """

    engineer_agent = Agent(
        role = "Senior generative AI engineer",
        goal = "Determine wheter  agent is secure or not, depending on usecase", #"Design a communication protocol for agents to communicate with each other and with humans.",
        backstory = "You are a senior generative AI engineer with expertise in designing secure communication protocols for AI agents.",
        verbose = True,
        allow_delegation = False,
        llm = llm,
        tools = [rag_tool],
        max_retry_limits = 5
    )

    task1 = Task(
        #
        # We don't need a fix prompt anymore. We may use a dynamic prompt unpacking from input messages
        # description = "What is the best way to design a communication protocol for agents to communicate with each other and with humans?",
        description = input[0].parts[0].content if input else "What is the best way to design a communication protocol for agents to communicate with each other and with humans?",
        # If we have multiple prompts, we may loop over the input and create multiple tasks
        # 
        expected_output = "A secure communication protocol that ensures privacy and integrity of the messages exchanged between agents and humans.",
        agent = engineer_agent,
    )

    crew = Crew(
        agents = [engineer_agent],
        tasks = [task1],
        verbose = True
    )

    task_output = await crew.kickoff_async()
    
    # We have to use the yield method beacuse we're using a generator and also to comply with the ACP server requirements
    # The yield method will send the output to the ACP server, so that it can be used by other agents or humans
    # The output will be sent as a message part with the role "assistant"
    yield Message(
        # parts = [MessagePart(content = str(task_output), role="assistant")],
        parts = [MessagePart(content = str(task_output))]
    )
    
    print(task_output)
    
if __name__ == "__main__":
    # Start the server
    server.run(port=8001)
    
    
    # For execute the server in a python script, you may use the following command:
    # python -m acp_sdk.server lesson4_part2.py
    # or 
    # python lesson4_part2.py
    # or
    # python -m acp_sdk.server lesson4_part2.py --port 8000
    # or
    # python -m acp_sdk.server lesson4_part2.py --host 0.