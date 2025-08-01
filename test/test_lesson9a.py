import subprocess
import json
import threading
import uuid

def read_stdout(pipe):
    while True:
        line = pipe.readline()
        if not line:
            break
        if line.strip():  # ignore empty lines
            print("🔵 Response:", line.strip())

# Start the subprocess
process = subprocess.Popen(
    ['python', '..\lesson9a_adding_MCP_server.py'],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    bufsize=1
)

# Start a thread to continuously read stdout
threading.Thread(target=read_stdout, args=(process.stdout,), daemon=True).start()

# Create a JSON-RPC request to call the `list_doctors` tool
request = {
    "id": str(uuid.uuid4()),
    "jsonrpc": "2.0",
    "method": "list_doctors",
    "params": {
        "state": "CA"
    }
}

# Send request
json_data = json.dumps(request)
print("🟡 Sending:", json_data)
process.stdin.write(json_data + "\n")
process.stdin.flush()
