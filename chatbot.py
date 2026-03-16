#!/usr/bin/env python3
"""Terminal chatbot using LangGraph + Ollama (mistral:latest) with SQL features."""

from __future__ import annotations

import os
from typing import Annotated, List, Tuple, TypedDict

from database import db
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition


class ChatState(TypedDict):
    messages: Annotated[list, add_messages]
    thread_id: str


@tool
def sql_query_tool(query: str) -> str:
    """Execute a read-only SQL query on the chatbot database.

    Args:
        query: A SELECT SQL query string.

    Returns:
        Query results as formatted string.
    """
    try:
        results = db.execute_query(query)
        if not results:
            return "No results found."
        # Format results
        formatted = "\n".join([str(row) for row in results])
        return f"Query results:\n{formatted}"
    except Exception as e:
        return f"SQL Error: {str(e)}"


def build_graph(model_name: str, base_url: str):
    llm = ChatOllama(model=model_name, base_url=base_url, temperature=0.2)
    search_tool = DuckDuckGoSearchResults(
        name="web_search",
        description=(
            "Search the internet for recent or factual information. "
            "Use this before answering when the user asks for current events, "
            "latest updates, or web facts."
        ),
    )
    tools = [search_tool, sql_query_tool]
    llm_with_tools = llm.bind_tools(tools)

    def assistant_node(state: ChatState):
        response = llm_with_tools.invoke(state["messages"])
        return {"messages": [response]}

    builder = StateGraph(ChatState)
    builder.add_node("assistant", assistant_node)
    builder.add_node("tools", ToolNode(tools))
    builder.add_edge(START, "assistant")
    builder.add_conditional_edges("assistant", tools_condition)
    builder.add_edge("tools", "assistant")

    memory = MemorySaver()
    return builder.compile(checkpointer=memory)


def main() -> None:
    model_name = os.getenv("OLLAMA_MODEL", "mistral:latest")
    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    graph = build_graph(model_name=model_name, base_url=base_url)
    thread_id = "chat-session"
    config = {"configurable": {"thread_id": thread_id}}

    # Load previous messages
    previous_messages = db.load_messages(thread_id)
    initial_state = {"messages": previous_messages, "thread_id": thread_id}

    print(f"LangGraph chatbot started with model: {model_name}")
    print(f"Ollama endpoint: {base_url}")
    print("Web search tool: enabled (DuckDuckGo)")
    print("SQL query tool: enabled (read-only on chatbot.db)")
    print(f"Loaded {len(previous_messages)} previous messages.")
    print("Type 'exit' or 'quit' to stop.\n")

    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue

        if user_input.lower() in {"exit", "quit"}:
            print("Assistant: Bye!")
            break

        try:
            # Add user message
            initial_state["messages"].append(("user", user_input))
            db.save_message(thread_id, "user", user_input)

            result = graph.invoke(initial_state, config=config)

            # Extract assistant response
            assistant_message = result["messages"][-1].content
            print(f"Assistant: {assistant_message}\n")

            # Save assistant message
            db.save_message(thread_id, "assistant", assistant_message)

            # Update state for next iteration
            initial_state["messages"] = result["messages"]

        except Exception as exc:  # noqa: BLE001
            print("Assistant: I could not reach Ollama or generate a reply.")
            print("Check that Ollama is running and mistral is available.")
            print(f"Error details: {exc}\n")


if __name__ == "__main__":
    main()
