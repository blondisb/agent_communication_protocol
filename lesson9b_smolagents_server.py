# Copy from the original ACP server code: lesson6_smol

from groq import Groq
from collections.abc import AsyncGenerator
from dotenv import load_dotenv, find_dotenv
from acp_sdk.models import Message, MessagePart
from acp_sdk.server import RunYield, RunYieldResume, Server
from crewai import Crew, Task, Agent, LLM

# Runyield and RunYieldResume are going to form part of
# our async generator function that will be used to
# yield results back to the client.
# And the server is going to form the context of our ACP server
# that will be used to run the agent.

from smolagents import CodeAgent, DuckDuckGoSearchTool, LiteLLMModel, VisitWebpageTool, ToolCallingAgent, ToolCollection
from mcp import StdioServerParameters
# CodeAgent is a class that allows us to create an agent that can
# generate code based on a given prompt.
# DuckDuckGoSearchTool is a tool that allows us to search the web
# using DuckDuckGo.
# LiteLLMModel is a class that allows us to create a lightweight LLM model
# that can be used to generate code.
# VisitWebpageTool is a tool that allows us to visit a webpage
# and extract information from it.

load_dotenv(find_dotenv(), override=True)  # Load API key from environment variable
server = Server()

model = LiteLLMModel(
    # model_id = "groq/deepseek-r1-distill-llama-70b"
    model_id="groq/moonshotai/kimi-k2-instruct"
    # model_id = "groq/mistral-saba-24b"
    # model_id = "ollama/deepseek-r1:14b",
    # model_id = "ollama/deepseek-r1:1.5b",
    # api_base = "http://localhost:11434/api/embeddings",
    # ,api_key=""
    ,api_base="https://api.groq.com/openai/v1"
    ,max_tokens = 528
)


# the full command or arg is:   UV run MCP server.py
server_parameters = StdioServerParameters(
    command = r"C:/Mega/Courses/DeeplearningAI/venvAI/Scripts/python.exe", #first part of command to acces the MCP server
    args = ["C:/Mega/Courses/DeeplearningAI/agent_communication_protocol/lesson9a_adding_MCP_server.py"],  # allows us to run and acces our list doctors tool inside mcpServer
    env=None
)

# the full command or arg is:   UV run MCP server.py
server_parameters = StdioServerParameters(
    command = "uv", #first part of command to acces the MCP server
    args = ["run", "lesson9a_adding_MCP_server.py"],  # allows us to run and acces our list doctors tool inside mcpServer
    env=None
)

@server.agent()
async def doctor_agent(input: list[Message]) -> AsyncGenerator[RunYield, RunYieldResume]:
    """
    This is a Doctor Agent which helps users find doctors near a sucursal restaurant.
    """
    # ToolCollection allows us to discover tools from mcp server
    with ToolCollection.from_mcp(server_parameters, trust_remote_code=True) as tool_collection:
        agent = ToolCallingAgent(tools = [*tool_collection.tools], model=model)
        prompt = input[0].parts[0].content

        print(
            "\n===========================\n BEFORE RUN \n:",
            [*tool_collection.tools],
            "\n", agent, "\n", prompt
        )

        response = agent.run(prompt)
        
    print("\n===========================\n YIELD \n:", Message(parts=[MessagePart(content=str(response))]))
    yield Message(parts=[MessagePart(content=str(response))])


@server.agent()
async def waiter_restaurant_agent(input: list[Message]) -> AsyncGenerator[RunYield, RunYieldResume]:
    """
    This is a CodeAgent which supports the restaurand to handle dishes based questions for customers.
    Current or prospective customers can use it to find answers about their menu doubts".
    This agent always response briefly.
    """
    # Create an instance of CodeAgent with the model and tools
    # ToolCallingAgent
    agent = CodeAgent (
        model = model,
        tools = [
            DuckDuckGoSearchTool(),
            VisitWebpageTool()
        ]
    )

    # Can i drink wine with pasta and chesee?
    prompt = input[0].parts[0].content if input else "What is the best pasta for mix with cheesee and tomatoes?"
    print("---", prompt)

    try:
        response = agent.run(task=prompt, max_steps=1)
        print("---", response)

        yield Message(
            parts = [MessagePart(content=str(response))]
        )

    except Exception as e:
        print("xxx", e)
        yield Message(
            parts = [MessagePart(content=f"Error: {str(e)}")]
        )

if __name__ == "__main__":
    # Start the server
    server.run(port=8002, reload=True)
    
    # For execute the server in a python script, you may use the following command:
    # python -m acp_sdk.server lesson6_smolagents_server.py
    # or 
    # python lesson6_smolagents_server.py
    # or
    # python -m acp_sdk.server lesson6_smolagents_server.py --port 8000
    # aa 