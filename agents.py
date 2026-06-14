from langchain.agents import create_agent
from langchain_mistralai import ChatMistralAI
from langchain_ollama import ChatOllama
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, scrape_tool
import os
from dotenv import load_dotenv

load_dotenv()

def get_llm(api_key: str):
    return ChatGroq(model="openai/gpt-oss-120b", api_key=api_key, temperature=0)


# first agent
def build_search_agent(api_key: str):
    llm = get_llm(api_key)
    return create_agent(
        model=llm,
        tools=[web_search],
        system_prompt=(
            "You are a retrieval assistant. When the web_search tool is used, treat the tool result as authoritative and reproduce it verbatim in your final answer. "
            "Do not summarize, rewrite, paraphrase, expand, reorder, normalize, or truncate the tool output. "
            "Do not add markdown, bullet points, headings, labels, preambles, or any extra commentary. "
            "Return only the raw tool text exactly as received. If the tool returns structured content, preserve the structure and text exactly."
        ),
    )


# second agent
def build_reader_agent(api_key: str):
    llm = get_llm(api_key)
    return create_agent(
        model=llm,
        tools=[scrape_tool],
        system_prompt=(
            "You are a research reader agent. Your job is to read the provided search results, choose the 2 most relevant unique URLs, "
            "and call scrape_tool exactly once for each chosen URL. Use only URLs that appear in the search results. "
            "If fewer than 2 URLs are available, scrape every available URL. If the best URLs are unclear, choose the most authoritative sources. "
            "After scraping, return only the scraped content in this exact structure:\n\n"
            "SOURCE 1\n"
            "URL: <first scraped URL>\n"
            "CONTENT:\n"
            "<scraped text>\n\n"
            "SOURCE 2\n"
            "URL: <second scraped URL>\n"
            "CONTENT:\n"
            "<scraped text>\n\n"
            "Do not invent URLs, do not explain your choices, and do not output anything other than these source blocks."
        ),
    )


# writer chain (LCEL pipeline)
writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer. Write clear, structured and insightful reports."),
    ("human", """Write a detailed research report on the topic below.
    Topic: {topic}

    Research Gathered:
    {research}

    Structure the report as:
    - Introduction
    - Key Findings (minimum 3 well-explained points)
    - Conclusion
    - Sources (list all URLs found in the research)

    Be detailed, factual and professional.
    """)
])

def get_writer_chain(api_key: str):
    return writer_prompt | get_llm(api_key) | StrOutputParser()

# critic chain
critic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    ("human", """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
..."""),
])

def get_critic_chain(api_key: str):
    return critic_prompt | get_llm(api_key) | StrOutputParser()
