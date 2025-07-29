from smolagents.models import LiteLLMModel, ChatMessage, Model
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(), override=True)


def model1(model_id, max_tokens):
 # This test requires actual API credentials and should be run separately
    model = LiteLLMModel(model_id=model_id, max_tokens=max_tokens)

    messages = [ChatMessage(
        role="user",
        content=[{
                "type": "text",
                "text": "To respond, use 1000 characters max. You are a supervisory agent that can delegate tasks to specialized ACP agents.\nAvailable agents:\n- function_engineer_agent: This is an agent that determines whether an agent is secure or not, depending on the use case.\nIt uses a RAG pattern to find answers in a PDF document and provides a secure communication protocol for agents to communicate with each other and with humans.\nUse it to help answer questions on designing secure communication protocols for AI agents.\n- designer_agent: This agent is designed to help with the design of a communication protocol for agents.\nIt can generate code based on a given prompt and can also search the web for information.\nUse it to help answer questions on designing communication protocols for AI agents.\n\nYour task is to:\n1. Analyze the user's request\n2. Call the appropriate agent(s) to gather information\n3. When you have a complete answer, ALWAYS call the final_answer tool with your response\n4. Do not provide answers directly in your messages - always use the final_answer tool\n5. If you have sufficient information to complete a task do not call out to another agent unless required\n\nRemember:\n- Always use the final_answer tool when you have a complete answer\n- Do not provide answers in your regular messages\n- Chain multiple agent calls if needed to gather all required information\n- The final_answer tool is the only way to return results to the user\n"
        }]
    )]

    return model.generate(messages=messages)



def model2(model_id, max_tokens):
    model = LiteLLMModel(model_id=model_id, max_tokens=max_tokens)

    messages = [
        {
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": "You are a supervisory agent that can delegate tasks to specialized ACP agents.\nAvailable agents:\n- function_engineer_agent: This is an agent that determines whether an agent is secure or not, depending on the use case.\nIt uses a RAG pattern to find answers in a PDF document and provides a secure communication protocol for agents to communicate with each other and with humans.\nUse it to help answer questions on designing secure communication protocols for AI agents.\n- designer_agent: This agent is designed to help with the design of a communication protocol for agents.\nIt can generate code based on a given prompt and can also search the web for information.\nUse it to help answer questions on designing communication protocols for AI agents.\n\nYour task is to:\n1. Analyze the user's request\n2. Call the appropriate agent(s) to gather information\n3. When you have a complete answer, ALWAYS call the final_answer tool with your response\n4. Do not provide answers directly in your messages - always use the final_answer tool\n5. If you have sufficient information to complete a task do not call out to another agent unless required\n\nRemember:\n- Always use the final_answer tool when you have a complete answer\n- Do not provide answers in your regular messages\n- Chain multiple agent calls if needed to gather all required information\n- The final_answer tool is the only way to return results to the user\n"
                }
            ]
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "What is the best way to design a communication protocol for agents to communicate with each other and with humans?"
                }
            ]
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Error occurred: Error while generating or parsing output:\n'dict' object has no attribute 'role'. Please try a different approach or provide a final answer."
                }
            ]
        }
    ]

    new_list = []
    for msj in messages:   
        new_list.append(
            ChatMessage(
                role = msj['role'],
                content = msj['content']
            )
        )


    print(new_list)
    return model.generate(messages=new_list)



def model3(model_id, max_tokens):
    from lists_of_chat_calls_with_model import step2
    model = LiteLLMModel(model_id=model_id, max_tokens=max_tokens, api_base="https://api.groq.com/openai/v1")

    new_list = []

    for msj in step2:   
        new_list.append(
            ChatMessage(
                role = msj['role'],
                content = msj['content']
            )
        )
        return model.generate(messages=new_list)


if __name__ == "__main__":

    model_id="groq/deepseek-r1-distill-llama-70b"
    max_tokens=1024

    # result = model1(model_id, max_tokens)
    # result = model2(model_id, max_tokens)
    result = model3(model_id, max_tokens)
    print("\n\n\n---------------------------------------",type(result))
    print(result)

    

