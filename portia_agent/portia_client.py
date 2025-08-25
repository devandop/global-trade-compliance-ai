import os
from portia import Portia, Config, DefaultToolRegistry, McpToolRegistry

class PortiaClient:
    def __init__(self, portia_api_key: str, xero_client_id: str, xero_client_secret: str):
        print("Initializing Portia SDK Client...")
        config = Config.from_default(api_key=portia_api_key)
        
        tool_registry = DefaultToolRegistry(config) + McpToolRegistry.from_stdio_connection(
            server_name="xero",
            command="npx",
            args=["-y", "@xeroapi/xero-mcp-server@latest"],
            env={
                "XERO_CLIENT_ID": xero_client_id,
                "XERO_CLIENT_SECRET": xero_client_secret,
            },
        )
        
        self.portia_sdk = Portia(config=config, tools=tool_registry)
        print("Portia SDK Client Initialized Successfully.")

    def get_sdk(self):
        return self.portia_sdk
