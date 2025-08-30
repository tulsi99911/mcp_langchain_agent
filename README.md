### Langchain Agent Assistant
A prototype multi-server agent system built with LangChain and Model Context Protocol (MCP) that provides intelligent assistance through various specialized tools and services.

### Overview
This project demonstrates a sophisticated agent architecture that connects to multiple MCP servers (both custom and remote) to provide a wide range of capabilities including web search, weather information, mathematical operations, and travel recommendations through a unified conversational interface.

### Features
Multi-Server Architecture: Connects to 4 different MCP servers
Dual Interface: Both CLI and Web UI (Streamlit) options
Real-time Tool Integration: 12 tools across multiple domains
Intelligent Agent: Uses Groq's Llama3-70b model with ReAct pattern
Docker Support: Fully containerized deployment
CI/CD Pipeline: Automated testing, security scanning, and deployment

### Available Tools
## Custom MCP Servers:
Math Operations (mathserver.py): Basic arithmetic operations (add, subtract, multiply, divide)
Google Search (google_search_server.py): Web search, image search, news search, site-specific search
Weather Services (weather_server.py): Current weather, and 5-day forecasts

## Remote MCP Server:
Airbnb Search (External NPM package): Travel and accommodation recommendations

### Architecture
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
Python: 3.13+
Node.js: 20+ (for Airbnb MCP server)
API Keys: Google Custom Search API and ID, OpenWeatherMap API, Groq API

🚀 Quick Start
1. Clone the Repository
bashgit clone <repository-url>
cd langchain-agent-assistant
2. Environment Setup
Create a .env file in the root directory:
env# Required API Keys
GROQ_API_KEY=your_groq_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
GOOGLE_ENGINE_ID=your_google_custom_search_engine_id_here
WEATHER_API_KEY=your_openweathermap_api_key_here
3. Installation Options
Option A: Using UV (Recommended)
bashpip install uv OR Using Pip
uv pip install -r requirements.txt
Option B: Using Pip
bashpip install -r requirements.txt
Option C: Using Docker
bashdocker build -t langchain-mcp-agent .
docker run -p 8501:8501 --env-file .env langchain-mcp-agent




### Usage
Web Interface (Recommended)
bashcd src
streamlit run main.py
Open http://localhost:8501 in your browser
Command Line Interface
bashcd src
python client.py
Docker Deployment
bash# Build the image
docker build -t langchain-mcp-agent .

# Run the container
docker run -p 8501:8501 --env-file .env langchain-mcp-agent


### Example Queries
Weather: "What's the current temperature in Gurugram, India?"
Search: "Find recent news about AI developments"
Math: "Calculate 15 multiplied by 23"
Images: "Search for images of mountain landscapes of Himachal Pradesh, india?"
Travel: "Find accommodations in Paris"
Site Search: "Search for Python tutorials on stackoverflow.com"

### License
This project is intended as a prototype and demonstration of MCP architecture with LangChain agents.
Built with: LangChain • Model Context Protocol • Groq • Streamlit • Docker
