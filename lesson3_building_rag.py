from crewai import Crew, Task, Agent, LLM
from crewai_tools import RagTool
from groq import Groq
import warnings
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(), override=True)  # Load API key from environment variable
client = Groq()
warnings.filterwarnings("ignore")

llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    # model="openai/gpt-4.1-nano-2025-04-14",
    max_tokens=1024
)

# config = {
#     "llm": {
#         "provider": "openai",
#         "config": {
#             "model": "gpt-4.1",
#         }
#     },
#     "embedding_model": {
#         "provider": "openai",
#         "config": {
#             "model": "text-embedding-ada-002"
#         }
#     }
# }

# https://docs.crewai.com/en/concepts/llms#groq

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
            # "base_url":"http://localhost:11434/api/embeddings",
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


engineer_agent = Agent(
    role = "Senior generative AI engineer",
    goal = "Determine wheter agent is secure or not, depending on usecase", #"Design a communication protocol for agents to communicate with each other and with humans.",
    backstory = "You are a senior generative AI engineer with expertise in designing secure communication protocols for AI agents.",
    verbose = True,
    allow_delegation = False,
    llm = llm,
    tools = [rag_tool],
    max_retry_limits = 5
)

task1 = Task(
    description = "What is the best way to design a communication protocol for agents to communicate with each other and with humans?",
    expected_output = "A secure communication protocol that ensures privacy and integrity of the messages exchanged between agents and humans.",
    agent = engineer_agent,
)

crew = Crew(
    agents = [engineer_agent],
    tasks = [task1],
    verbose = True
)

task_output = crew.kickoff()
print(task_output)