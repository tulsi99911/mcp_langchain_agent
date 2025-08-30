import streamlit as st
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
    def __init__(self):
        self.tool_calls_log = []
    def on_tool_start(self, serialized_tool: dict, input_str: str, **kwargs) -> None:
        tool_name = serialized_tool.get("name", "Unknown Tool")
        self.tool_calls_log.append(f"Calling tool: {tool_name}")


@st.cache_resource
def initialize_agent():
    st.write("Initializing agent and loading tools...")
    with open("config/servers_connection.json", "r") as f:
        server_config = json.load(f)

    for server_name, config in server_config.items():
        if "env" in config:
            for key, value in config["env"].items():
                if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
                    env_var_name = value[2:-1]
                    env_var_value = os.getenv(env_var_name)
                    if env_var_value is None:
                        st.warning(f"Warning: Environment variable {env_var_name} not set for server {server_name}. This tool may not function correctly.")
                    config["env"][key] = env_var_value
    
    client = MultiServerMCPClient(server_config)
    tools = asyncio.run(client.get_tools())
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
    st.success(f"Loaded {len(tools)} tools from {len(server_config)} servers. Agent ready!")
    return agent_executor, system_prompt_message

# --- Streamlit UI ---
st.set_page_config(page_title="Langchain Agent Chat", page_icon="🤖")
st.title("🤖 Langchain Agent Assistant")
st.markdown("Ask me anything! I use available tools to provide accurate and relevant information.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize the agent
agent_executor, system_prompt_message = initialize_agent()

if agent_executor is None:
    st.stop()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What would you like to know?"):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("assistant"):
        callback_handler = VerboseCallbackHandler()
        with st.spinner("Assistant is thinking..."):
            agent_messages = [system_prompt_message] + [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
            assistant_response = asyncio.run(agent_executor.ainvoke({"messages": agent_messages}, {"callbacks": [callback_handler]} ))
            response_content = assistant_response['messages'][-1].content
            if callback_handler.tool_calls_log:
                with st.expander("Tool Called: "):
                    for log_entry in callback_handler.tool_calls_log:
                        st.info(log_entry)
            st.markdown(response_content)
            st.session_state.messages.append({"role": "assistant", "content": response_content})
           
