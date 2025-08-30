### Langchain Agent Assistant
A prototype multi-server agent system built with LangChain and Model Context Protocol (MCP) that provides intelligent assistance through various specialized tools and services.

### Overview
This project demonstrates a sophisticated agent architecture that connects to multiple MCP servers (both custom and remote) to provide a wide range of capabilities including web search, weather information, mathematical operations, 
and travel recommendations through a unified conversational interface.

### Features
  - Multi-Server Architecture: Connects to 4 different MCP servers
  - Dual Interface: Both CLI and Web UI (Streamlit) options
  - Real-time Tool Integration: 12 tools across multiple domains
  - Intelligent Agent: Uses Groq's Llama3-70b model with ReAct pattern
  - Docker Support: Fully containerized deployment
  - CI/CD Pipeline: Automated testing, security scanning, and deployment

### Available Tools
#### Custom MCP Servers:
  - Math Operations (mathserver.py): Basic arithmetic operations (add, subtract, multiply, divide)
  - Google Search (google_search_server.py): Web search, image search, news search, site-specific search
  - Weather Services (weather_server.py): Current weather, and 5-day forecasts

#### Remote MCP Server:
  - Airbnb Search (External NPM package): Travel and accommodation recommendations

### Architecture
<img width="677" height="333" alt="Image" src="https://github.com/user-attachments/assets/4613241e-7bde-4b71-85aa-8a5ad6b6a4dd" />
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   User Input    │───▶│  LangChain Agent │───▶│   Tool Router   │
└─────────────────┘    │  (Groq Llama3)   │    └─────────────────┘
                       └──────────────────┘            │
                                                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                    MultiServerMCPClient                         │
├─────────────────┬─────────────────┬─────────────────┬───────────┤
│   Math Server   │  Weather Server │ Google Search   │  Airbnb   │
│   (Custom)      │   (Custom)      │   (Custom)      │ (Remote)  │
└─────────────────┴─────────────────┴─────────────────┴───────────┘


### Prerequisites
  - Python: 3.13+
  - Node.js: 20+ (for Airbnb MCP server)
  - API Keys: Google Custom Search API and ID, OpenWeatherMap API, Groq API

### Example Queries
  - Weather: "What's the current temperature in Gurugram, India?"
  - Search: "Find recent news about AI developments?"
  - Math: "Calculate 15 multiplied by 23?"
  - Search: "Search for Python tutorials on stackoverflow.com?"

### License
  - This project is intended as a prototype and demonstration of MCP architecture with LangChain agents.


