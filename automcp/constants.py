OUTPUT_TEMPLATE = '''
MCP server created at {server_path}

Add following MCP server configuration to mcp.json:
{{
    "mcpServers": {{
        "{safe_command_name}": {{
            "command": "uv",
            "args": [
                "--directory",
                "{save_dir}",
                "run",
                "{output_file_name}"
            ]
        }}
    }}
}}
'''
