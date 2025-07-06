from groq import Groq
from collections.abc import AsyncGenerator
from dotenv import load_dotenv, find_dotenv
from acp_sdk.models import Message, MessagePart
from acp_sdk.server import RunYield, RunYieldResume, Server

# Runyield and RunYieldResume are going to form part of
# our async generator function that will be used to
# yield results back to the client.
# And the server is going to form the context of our ACP server
# that will be used to run the agent.

from smolagents import CodeAgent, DuckDuckGoSearchTool, LiteLLMModel, VisitWebpageTool

# CodeAgent is a class that allows us to create an agent that can
# generate code based on a given prompt.
# DuckDuckGoSearchTool is a tool that allows us to search the web
# using DuckDuckGo.
# LiteLLMModel is a class that allows us to create a lightweight LLM model
# that can be used to generate code.
# VisitWebpageTool is a tool that allows us to visit a webpage
# and extract information from it.

load_dotenv(find_dotenv(), override=True)  # Load API key from environment variable
client = Groq()
server = Server()

model = LiteLLMModel(
    model_id = "groq/compound-beta",
    # model_id = "ollama/deepseek-r1:14b",
    max_tokens = 2048
)

@server.agent()
async def designer_agent(input: list[Message]) -> AsyncGenerator[RunYield, RunYieldResume]:
    """
    This agent is designed to help with the design of a communication protocol for agents.
    It can generate code based on a given prompt and can also search the web for information.
    Use it to help answer questions on designing communication protocols for AI agents.
    """
    # Create an instance of CodeAgent with the model and tools
    agent = CodeAgent(
        model = model,
        tools = [
            DuckDuckGoSearchTool(),
            VisitWebpageTool()
        ]
    )

    # Process the input messages
    # for message in input:
    #     response = await agent.run(message.content)
    #     yield RunYield(output=[MessagePart(content=response)])

    prompt = input[0].parts[0].content if input else "What is the best way to design a communication protocol for agents to communicate with each other and with humans?"
    try:
        response = agent.run(prompt)
        yield Message(
            parts = [MessagePart(content=str(response))]
        )
    except Exception as e:
        yield Message(
            parts = [MessagePart(content=f"Error: {str(e)}")]
        )

if __name__ == "__main__":
    # Start the server
    server.run(port=8000)
    
    # For execute the server in a python script, you may use the following command:
    # python -m acp_sdk.server lesson6_smolagents_server.py
    # or 
    # python lesson6_smolagents_server.py
    # or
    # python -m acp_sdk.server lesson6_smolagents_server.py --port 8000