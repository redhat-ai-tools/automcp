# server.py
import os
from mcp.server.fastmcp import FastMCP
from automcp.pipeline import AutoMCP_Pipeline
from automcp.utils import safe_name

# Create an MCP server
mcp = FastMCP("Auto MCP")

save_dir = os.getenv(
    'AUTOMCP_SERVER_DIR',
    os.path.join(
        os.path.expanduser("~"),
        '.automcp'
    )
)

OUTPUT_TEMPLATE = '''
MCP server created at {server_path}

Add following server configuration to mcp.json:
{{
    "{safe_command_name}": {{
        "command": "uv",
        "args": [
            "--directory",
            "{save_dir}",
            "run",
            "{safe_command_name}_server.py"
        ]
    }}
}}
'''

# Add an addition tool
@mcp.tool()
def create_mcp_server(command: str) -> str:
    """Create MCP server for a CLI utility or executable program."""
    pipeline = AutoMCP_Pipeline()
    server_template = pipeline.run(command, "--help")
    
    os.makedirs(save_dir, exist_ok=True)
    safe_command_name = safe_name(command)
    server_path = os.path.join(save_dir, f"{safe_command_name}_server.py")

    with open(server_path, "w") as f:
        f.write(server_template)

    return OUTPUT_TEMPLATE.format(
        server_path=server_path,
        safe_command_name=safe_command_name,
        save_dir=save_dir
    )
