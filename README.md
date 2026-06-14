# Lumina Research

Lumina Research is an AI-powered deep research intelligence tool built with Python, LangChain, and Streamlit. It orchestrates a multi-agent pipeline to search the web, scrape relevant sources, write a structured research report, and provide an expert critique of the final output.

## Overview

This project implements an autonomous research workflow that processes a user-defined topic through four distinct stages:

1. **Search Agent**: Uses the Tavily API to perform a web search and retrieves the top 5 recent, reliable results (titles, URLs, and snippets).
2. **Reader Agent**: Analyzes the search results to pick the 2 most relevant URLs and scrapes their full text content using BeautifulSoup for deep reading.
3. **Writer Chain**: Synthesizes the search intelligence and scraped content into a comprehensive research report, structured with an Introduction, Key Findings, Conclusion, and Sources.
4. **Critic Chain**: Reviews the generated report, scores it out of 10, identifies strengths and areas for improvement, and provides a one-line verdict.

## Features

- **Multi-Agent Architecture**: Built using LangChain's `create_agent` and LCEL (LangChain Expression Language) pipelines.
- **Dual Interfaces**: 
  - **Streamlit App (`app.py`)**: A modern, visually appealing web interface with real-time pipeline progress tracking, expandable intermediate results, and a text download option for the final report.
  - **CLI Pipeline (`pipeline.py`)**: A command-line interface to execute the research pipeline directly from the terminal.
- **Custom Tools**: Includes dedicated tools (`web_search` and `scrape_tool`) for information retrieval and content extraction.
- **LLM Integration**: Currently configured to run with `ChatOllama` (defaulting to the `gemma4:31b-cloud` model), with scaffolding in place for MistralAI and Groq integrations.

## Project Structure

- `app.py`: Streamlit frontend application with custom CSS styling and UI pipeline tracking.
- `pipeline.py`: The core sequential pipeline logic that executes the agents and chains step-by-step.
- `agents.py`: Definitions for the Search and Reader agents, as well as the Writer and Critic LCEL chains.
- `tools.py`: Tool definitions for web searching (TavilyClient) and webpage scraping (Requests & BeautifulSoup).
- `main.py`: Project entry point stub.

## Getting Started

### Prerequisites

- Python 3.12 or higher.
- API Keys for Tavily and your chosen LLM provider (e.g., Ollama, Mistral, Groq).

### Installation

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   *(Note: A `uv.lock` is also present if you prefer using `uv` for dependency management).*

2. Create a `.env` file in the root directory and add your API keys:
   ```env
   TAVILY_API_KEY=your_tavily_api_key
   OLLAMA_API_KEY=your_ollama_api_key
   # MISTRALAI_API_KEY=your_mistral_api_key
   # GROQ_API_KEY=your_groq_api_key
   ```

### Usage

**Run the Streamlit App:**
```bash
streamlit run app.py
```

**Run via Command Line:**
```bash
python pipeline.py
```
