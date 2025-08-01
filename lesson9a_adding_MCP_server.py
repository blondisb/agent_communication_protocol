from colorama import Fore
from mcp.server.fastmcp import FastMCP
import json
import requests
# MCP Server is going to return a lisst of doctors in United States
# <>
mcp = FastMCP("doctorserver")

@mcp.tool()
def list_doctors(state:str) -> str:
    """This tool returns doctos that may be near you

    Args:
        state (str): the two letter state code that you live in.
        Example payload: "CA" 

    Returns:
        str: a list of doctors that may be near you
        Example Response "{"DOC001":{"name":"Dr Jhon James", "specialty":"Cardiology"...}...}"
    """
    print(f"🟢 Processing state: {state}", flush=True)

    url = 'https://raw.githubusercontent.com/nicknochnack/ACPWalkthrough/refs/heads/main/doctors.json'
    resp = requests.get(url)
    doctors = json.loads(resp.text)
    
    matches = [doctor for doctor in doctors.values() if doctor['address']['state'] == state]
    return str(matches)

if __name__ == "__main__":
    try:
        print("🟢 doctor_server.py started", flush=True)
        mcp.run(transport="sse")
        # mcp.run(transport="stdio")
    except Exception as e:
        print(e)
        raise e