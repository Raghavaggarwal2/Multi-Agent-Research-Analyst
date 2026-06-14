# Lumina Research

Lumina Research is an AI-powered deep research intelligence tool built with Python, LangChain, and Streamlit. It orchestrates a multi-agent pipeline to search the web, scrape relevant sources, write a structured research report, and provide an expert critique of the final output.

## Overview

This project implements an autonomous research workflow that processes a user-defined topic through four distinct stages:

1. **Search Agent**: Uses the Tavily API to perform a web search and retrieves the top 5 recent, reliable results (titles, URLs, and snippets).
2. **Reader Agent**: Analyzes the search results to pick the 2 most relevant URLs and scrapes their full text content using BeautifulSoup for deep reading.
3. **Writer Chain**: Synthesizes the search intelligence and scraped content into a comprehensive research report, structured with an Introduction, Key Findings, Conclusion, and Sources.
4. **Critic Chain**: Reviews the generated report, scores it out of 10, identifies strengths and areas for improvement, and provides a one-line verdict.

## Features

- **Multi-Agent Architecture**: Built using LangChain agents and LCEL (LangChain Expression Language) pipelines.
- **Dual Interfaces**: 
  - **Streamlit App (`app.py`)**: A premium, beautifully styled web interface featuring a dynamic sidebar, real-time pipeline progress tracking, expandable intermediate results, and elegant typography for the final markdown report.
  <!-- - **CLI Pipeline (`pipeline.py`)**: A command-line interface to execute the research pipeline directly from the terminal. -->
- **Custom Tools**: Includes dedicated tools (`web_search` and `scrape_tool`) for information retrieval and content extraction.
- **LLM Integration**: Powered exclusively by **Groq** (`ChatGroq`) for blazing fast agentic reasoning. The application accepts the Groq API key securely at runtime via the UI or CLI prompts.

## Project Structure

- `app.py`: Streamlit frontend application with custom CSS styling and UI pipeline tracking.
- `pipeline.py`: The core sequential pipeline logic that executes the agents and chains step-by-step.
- `agents.py`: Definitions for the Search and Reader agents, as well as the Writer and Critic LCEL chains using Groq.
- `tools.py`: Tool definitions for web searching (TavilyClient) and webpage scraping (Requests & BeautifulSoup).

## Getting Started

### Prerequisites

- Python 3.12 or higher.
- A **Tavily API Key** (for web searching).
- A **Groq API Key** (provided dynamically when running the app).

### Installation

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   *(Note: A `uv.lock` is also present if you prefer using `uv` for dependency management).*

2. Create a `.env` file in the root directory to store your background tools key:
   ```env
   TAVILY_API_KEY=your_tavily_api_key
   ```

### Usage

**Run the Streamlit App:**
```bash
streamlit run app.py
```
*(You will be prompted to enter your Groq API Key securely in the sidebar).*

**Run via Command Line:**
```bash
python pipeline.py
```
*(The terminal will ask you for your Groq API Key and research topic before executing).*
