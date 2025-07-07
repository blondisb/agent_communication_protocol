
--------------------------------------------------------------------------------------------------
OLLAMA

    Steps:

    Pull model from Ollama, in powershell
    - execute server
    - test model



--------------------------------------------------------------------------------------------------
JSON REQUEST

    AGENT 1:
    http://localhost:8001/runs

        {
        // "agent_name": "function_engineer_agent",
        "agent_name": "designer_agent",
        "input": [
            {
            "parts": [
                {
                "content": "What is the best way to design a communication protocol for agents to communicate with each other and with humans?"
                }
            ]
            }
        ]
        }


    AGENT 2:
    http://localhost:8000/runs

        {
        // "agent_name": "function_engineer_agent",
        "agent_name": "designer_agent",
        "input": [
            {
            "parts": [
                {
                "content": "What is the best way to design a communication protocol for agents to communicate with each other and with humans?"
                }
            ]
            }
        ]
        }