ACP
https://agentcommunicationprotocol.dev/introduction/welcome
https://github.com/i-am-bee/acp/tree/main/python 

--------------------------------------------------------------------------------------------------
OLLAMA
--------------------------------------------------------------------------------------------------


    Steps:

    Pull model from Ollama, in powershell
    # command to pull
        > ollama pull nomic-embed-text

    # command to start
        > execute server
    
     # test embedding:
        > $body = @{
                model = "nomic-embed-text"
                prompt = "This is an example sentence to embed."
            } | ConvertTo-Json

            $response = Invoke-RestMethod -Uri "http://localhost:11434/api/embeddings" `
                                        -Method Post `
                                        -Body $body `
                                        -ContentType "application/json"


    # Powershell command to validate if Ollama server is running
    Get-Process -Name "ollama" -ErrorAction SilentlyContinue

    # Or check if the Ollama API is responding
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:11434" -UseBasicParsing -TimeoutSec 2
        Write-Output "Ollama server is running."
    } catch {
        Write-Output "Ollama server is not running."
    }



--------------------------------------------------------------------------------------------------
WORKFLOW
--------------------------------------------------------------------------------------------------
    1. Run AGENT 01 server in lesson4 main
    2. Run AGENT 02 server in lesson6_smolagents
    3. Execute someone else's client ()
        lesson4 (most basic) ----> lesson8 (advanced) ACP code





--------------------------------------------------------------------------------------------------
JSON REQUEST
--------------------------------------------------------------------------------------------------


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