from agents import build_search_agent, build_reader_agent, writer_chain, critic_chain
from rich import print


def run_research_pipeline(topic: str) -> dict:
    state = {}

    # search agent
    search_agent = build_search_agent()
    print("\n=== Running Search Agent ===")
    search_result = search_agent.invoke({
        "messages": [("user", f"Find recent, reliable, detailed and relevant information on the topic: {topic}")]
    })
    state["search_result"] = search_result["messages"][-1].content

    print("\n=== Search Result ===")
    print(state["search_result"])

    # reader agent
    reader_agent = build_reader_agent()
    print("\n=== Running Reader Agent ===")
    reader_result = reader_agent.invoke({
        "messages": [("user",
                    f"Based on the following search results about: {topic}, "
                    f"pick the 2 most relevant URLs from the search results and scrape both for deeper and detailed information.\n\n"
                    f"Search Results:\n{state['search_result']}"
                    )]
    })
    state["reader_result"] = reader_result["messages"][-1].content

    print("\n=== Reader Result ===")
    print(state["reader_result"])

    # writer chain
    print("\n=== Running Writer Chain ===")
    research_combined = (
        f"Search Results:\n{state['search_result']}\n\n"
        f"Deep Reading:\n{state['reader_result']}"
    )

    state["report"] = writer_chain.invoke({
        "topic": topic,
        "research": research_combined
    })
    print("\n=== Generated Report ===")
    print(state["report"])

    # critic chain
    print("\n=== Running Critic Chain ===")

    state["feedback"] = critic_chain.invoke({
        "report": state["report"]
    })
    print("\n=== Critique ===")
    print(state["feedback"])

    return state


if __name__ == "__main__":
    topic = input("\n Enter a research topic: ")
    run_research_pipeline(topic)
