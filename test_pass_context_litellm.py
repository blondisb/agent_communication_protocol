from smolagents.models import ChatMessage as CTM2
from smolagents.models import LiteLLMModel
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(), override=True)

messages = [
    {"role": "system", "content": [{"type": "text", "text": "You are a helpful assistant. You'll answer all user's request. Then you will write: The final answer is..."}]},
    {"role": "user", "content": [{"type": "text", "text": "What is the weather in Paris? And what time is in Munich?"}]},
    {"role": "assistant", "content": [{"type": "text", "text": "Let me check the weather for you."}]},
    {"role": "user", "content": [{"type": "text", "text": "Observation: It's sunny and 25°C."}]}
]

# Prepare messages as CTM2 objects
ctm2_messages = [
    CTM2(role=msg["role"], content=msg["content"])
    for msg in messages
]

# Initialize the LiteLLM model (example with OpenAI GPT-3.5)
llm = LiteLLMModel(
    model_id="groq/deepseek-r1-distill-llama-70b",
    max_tokens=1024,
    api_base="https://api.groq.com/openai/v1"
)

# Call the model with all context
response = llm(
    ctm2_messages,
    stop_sequences=["Observation:", "Calling agents:"],
    tools_to_call_from=[],  # or your list of tools
)

print(response.content)