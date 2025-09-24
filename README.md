### Langchain Agent Assistant
A prototype multi-server agent system built with LangChain and Model Context Protocol (MCP) that provides intelligent assistance through various specialized tools and services.

### Overview
This project demonstrates a sophisticated agent architecture that connects to multiple MCP servers (both custom and remote) to provide a wide range of capabilities including web search, weather information, mathematical operations, 
and travel recommendations through a unified conversational interface.

### Features
  - Multi-Server Architecture: Connects to 4 different MCP servers
  - Dual Interface: Both CLI (client.py) and Web UI (Streamlit [main.py]) options
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










# SOPher - Technical Documentation for src/

This document provides a concise, comprehensive reference for the Python source code under src/ in the SOPher project. It describes the purpose of each module, its public API, data models used, and how data flows through the system.

Table of Contents
- [Overview](#overview)
- [Project Architecture & Data Flow](#project-architecture--data-flow)
- [Module API Reference](#module-api-reference)
- [Key Data Models](#key-data-models)
- [Data Flow (Concise)](#data-flow-concise)
- [Configuration & Environment](#configuration--environment)
- [Development, Testing & Validation](#development--testing--validation)
- [Appendix: File References](#appendix-file-references)

## Overview
The src/ directory implements the core runtime for the SOPher bot, including data ingestion, retrieval, and natural language processing orchestration.
It wires together an internal knowledge base, a Google Search fallback, and an Azure OpenAI LLM for evaluation and responses.

## Project Architecture & Data Flow
- Data ingestion: MCPExcelConnector reads Excel files from data/ and converts them into LangChain Documents.
- Context enrichment: Documents are enriched to include contextual summaries for better retrieval.
- Storage & indexing: A FAISS-based vector store stores embeddings; a TF-IDF keyword index is built for lexical retrieval.
- Retrieval: An AdvancedRetriever fuses semantic and lexical signals, then applies a reranker to produce final documents.
- LLM & evaluation: The selected documents are fed as context to an Azure OpenAI model for responses and optional evaluation via RAGAS.

## Module API Reference

### src/vector_db.py
Public class: VectorDatabase
- __init__(index_path: str, embedding_model: str = "all-MiniLM-L6-v2")
- build_or_load_index(documents: List[Document]) -> FAISS
Description: Builds a FAISS index or loads an existing one for the provided documents. Uses HuggingFace embeddings.
See: [`src/vector_db.py`](src/vector_db.py:1) for code reference.

### src/keyword_db.py
Public class: KeywordDatabase
- __init__(index_path: str)
- build_or_load_index(documents: List[Document])
- retrieve(query: str, k: int = 10) -> List[Document]
Description: TF-IDF based lexical retrieval over enriched documents.
See: [`src/keyword_db.py`](src/keyword_db.py:1)

### src/mcp_connector.py
Public class: MCPExcelConnector
- __init__(data_dir: str)
- get_all_documents() -> List[Document]
Description: Reads Excel data sources from the data/ directory and exposes a list of Content Documents.
See: [`src/mcp_connector.py`](src/mcp_connector.py:1)

### src/my_data_source.py
Public class: MyDataSource
- __init__(name: str = "ExcelKB")
- render_data(context, memory, tokenizer, max_tokens) -> Result
- _enrich_documents(documents) -> List[Document]
- name property
Description: Combines internal KB with a Google Search fallback; exposes internal retriever.
See: [`src/my_data_source.py`](src/my_data_source.py:1)

### src/retriever.py
Public class: AdvancedRetriever
- retrieve(query: str, k_semantic: int = 10, k_keyword: int = 5, k_fusion: int = 10, k_final: int = 8, k: int = None) -> List[Document]
Description: Fusion of semantic and lexical results followed by reranking.
See: [`src/retriever.py`](src/retriever.py:1)

### src/Search_tool.py
Public class: GoogleSearchTool
- __init__(api_key: str, cse_id: str)
- search(query: str, num_results: int = 5) -> List[Document]
Description: Lightweight Google Custom Search wrapper; returns Documents with metadata.
See: [`src/Search_tool.py`](src/Search_tool.py:1)

### src/custom_say_command.py
Public function: say_command(context, state, data, feedback_loop_enabled: bool = False) -> str
Description: Robust JSON-handling for AI-generated messages and citations; returns a string response or sends a Teams message.
See: [`src/custom_say_command.py`](src/custom_say_command.py:1)

### src/app.py
Web API entrypoint for the bot; defines /api/messages route and launches the app.
See: [`src/app.py`](src/app.py:1)

### src/bot.py
Bot logic: LLM integration, conversation events, and error handling.
See: [`src/bot.py`](src/bot.py:1)

### src/chatbot_evaluation.py
Evaluation harness using RAGAS; runtime may require Azure credentials.
See: [`src/chatbot_evaluation.py`](src/chatbot_evaluation.py:1)

### src/config.py
Central configuration class with environment-based values.
See: [`src/config.py`](src/config.py:1)

## Key Data Models
- Document (LangChain) - page_content and metadata fields
- Tensor embeddings produced by HuggingFace embeddings
- TF-IDF vectors for keyword retrieval

## Data Flow (Concise)
1. MCPExcelConnector reads Excel data.
2. Documents are enriched and stored in a FAISS vector store and a TF-IDF index.
3. AdvancedRetriever performs semantic and lexical retrieval; Reranker reorders results.
4. Context assembled into <context> blocks; passed to LLM for answers.
5. Optional evaluation via chatbot_evaluation.py.

## Configuration & Environment
- Python 3.x
- Requirements: See requirements.txt
- Env vars: AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_MODEL_DEPLOYMENT_NAME, GOOGLE_API_KEY, GOOGLE_CSE_ID

## Development, Testing & Validation
- Run the app: python src/app.py
- Run tests: (if any) pytest or unittest (based on project setup)
- Linting guidelines: flake8/black

## Appendix: File References
- vector_db: [`src/vector_db.py`](src/vector_db.py:1)
- keyword_db: [`src/keyword_db.py`](src/keyword_db.py:1)
- mcp_connector: [`src/mcp_connector.py`](src/mcp_connector.py:1)
- my_data_source: [`src/my_data_source.py`](src/my_data_source.py:1)
- retriever: [`src/retriever.py`](src/retriever.py:1)
- Search_tool: [`src/Search_tool.py`](src/Search_tool.py:1)
- custom_say_command: [`src/custom_say_command.py`](src/custom_say_command.py:1)
- app: [`src/app.py`](src/app.py:1)
- bot: [`src/bot.py`](src/bot.py:1)
- chatbot_evaluation: [`src/chatbot_evaluation.py`](src/chatbot_evaluation.py:1)
- config: [`src/config.py`](src/config.py:1)

