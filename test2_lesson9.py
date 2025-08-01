import asyncio
from mcp import StdioServerParameters
from mcp.agent.fastmcp import FastMCPAgent

async def main():
    # Setup FastMCP agent connected to the subprocess
    agent = FastMCPAgent(
        name="doctor-agent",
        server=StdioServerParameters(command=["python", "doctor_server.py"])
    )

    # Call the remote tool
    response = await agent.list_doctors(state="CA")
    
    print("📋 Doctors in CA:", response)

# Run it
asyncio.run(main())
