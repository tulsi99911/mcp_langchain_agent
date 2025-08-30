import json
import os
import asyncio
from langchain.callbacks.base import BaseCallbackHandler
from langchain_core.messages import SystemMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()
class VerboseCallbackHandler(BaseCallbackHandler):
    def on_tool_start(self, serialized_tool: dict, input_str: str, **kwargs) -> None:
        tool_name = serialized_tool.get("name", "Unknown Tool")
        print(f"Calling tool: {tool_name}")

async def main():
    with open("config/servers_connection.json", "r") as f:
        server_config = json.load(f)

    for server_name, config in server_config.items():
        if "env" in config:
            for key, value in config["env"].items():
                if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
                    env_var_name = value[2:-1]
                    env_var_value = os.getenv(env_var_name)
                    if env_var_value is None:
                        print(f"Warning: Environment variable {env_var_name} not set for server {server_name}. This tool may not function correctly.")
                    config["env"][key] = env_var_value
    
    client = MultiServerMCPClient(server_config)
    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
    tools = await client.get_tools()
    model = ChatGroq(model="llama3-70b-8192")
    system_prompt_message = SystemMessage(
        content=(
            "You are a helpful and knowledgeable assistant. Your primary goal is to provide accurate and relevant information using the available tools.\n"
            "Here are the rules you must follow:\n"
            "3. If a tool fails or provides an empty response, explain the situation to the user and try a different tool or method if possible.\n"
            "4. Be polite in your answers."
        )
    )
    agent_executor = create_react_agent(model, tools)
    print(f"Loaded {len(tools)} tools from {len(server_config)} servers")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break
        print("Assistant is thinking...")
        messages = [system_prompt_message, {"role": "user", "content": user_input}]
        assistant_response = await agent_executor.ainvoke(
            {"messages": messages},      # [{"role": "user", "content": user_input}]
            {"callbacks": [VerboseCallbackHandler()]}
        )
        print("Assistant:", assistant_response['messages'][-1].content)

if __name__ == "__main__":
    asyncio.run(main())

















































