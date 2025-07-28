
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
    # model="groq/meta-llama/llama-4-scout-17b-16e-instruct",
    model="groq/deepseek-r1-distill-llama-70b",
    api_base="https://api.groq.com/openai/v1",
    # model="groq/mistral-saba-24b",
    # model = "ollama/deepseek-r1:1.5b",
    # max_tokens=128,
    max_completion_tokens = 1024
)

config = {
    "llm": {
        "provider": "groq",
        # "provider": "ollama",
        "config": {
            # "model": "groq/meta-llama/llama-4-scout-17b-16e-instruct",
            "model" : "groq/deepseek-r1-distill-llama-70b",
            # "model": "deepseek-r1-distill-llama-70b",
            # "model": "groq/mistral-saba-24b",
            # "model": "deepseek-r1:1.5b",
            # "api_base" : "https://api.groq.com/openai/v1/models",
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
    # "./pdf/doc.pdf",
    "./pdf/wine.pdf",
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
    It may uses ONLY a RAG pattern to find answers in a PDF document and provides a secure communication protocol for agents to communicate with each other and with humans.
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
        max_retry_limits = 1
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
    print([MessagePart(content = str(task_output))])
    print("---")
    print([MessagePart(content = str(task_output), role="assistant")])

    yield Message(
        # parts = [MessagePart(content = str(task_output), role="assistant")],
        parts = [MessagePart(content = str(task_output))]
    )
    
    print(task_output)



# The agent that we want to make available in our ACP server 
# ACP makes the agent available trhoug the docstring, so we may to be specific about the function signature
# and the docstring of the function, so that it can be used by other agents or humans in the ACP server.
# The docstring should contain the description of the agent, its role, goal, backstory
@server.agent()
async def wine_expert_agent(input: list[Message]) -> AsyncGenerator[RunYield, RunYieldResume]:
    """
    This is an agent that determines which wine is the most appropiate for each dish.
    It may uses ONLY  a RAG pattern to find availables wine in this restaurant. Those are in a PDF document and provides information about every kind of wine and grape.
    Use it to help answer questions on designing secure communication protocols for AI agents.
    If question is not about WINES, this agent respond: "CALL OTHER AGENT"
    """

    sommelierr_agent = Agent(
        role = "wine expert sommelierr",
        goal = "give an specific and very short recommendation of three types of wine and its brief description.",
        backstory = "You are a swine expert sommelierr with expertise in every kind of wine, grape and cup (depending on dish and wine)",
        verbose = True,
        allow_delegation = False,
        llm = llm,
        tools = [rag_tool],
        max_retry_limits = 1
    )

    print("\n====================\n INPUT PROMPT:\n", input[0].parts[0].content)

    task = Task(
        #
        # We don't need a fix prompt anymore. We may use a dynamic prompt unpacking from input messages
        description = input[0].parts[0].content if input else "What is the best wine for a dinner with spaguetti and cheese. If i like sweet flavors?",
        # If we have multiple prompts, we may loop over the input and create multiple tasks
        # 
        expected_output = "An specific recommendation of three types of wine",
        agent = sommelierr_agent,
    )

    crew = Crew(
        agents = [sommelierr_agent],
        tasks = [task],
        verbose = True
    )

    task_output = await crew.kickoff_async()
    
    # We have to use the yield method beacuse we're using a generator and also to comply with the ACP server requirements
    # The yield method will send the output to the ACP server, so that it can be used by other agents or humans
    # The output will be sent as a message part with the role "assistant"
    print("\n====================\n AGENT RESPONSE:\n", [MessagePart(content = str(task_output))])

    yield Message(
        # parts = [MessagePart(content = str(task_output), role="assistant")],
        parts = [MessagePart(content = str(task_output))]
    )
    
    print(task_output)
    
if __name__ == "__main__":
    # Start the server
    server.run(port=8001, reload=True)
    
    
    # For execute the server in a python script, you may use the following command:
    # python -m acp_sdk.server lesson4_part2.py
    # or 
    # python lesson4_part2.py
    # or
    # python -m acp_sdk.server lesson4_part2.py --port 8000
    # or
    # python -m acp_sdk.server lesson4_part2.py --host 0.