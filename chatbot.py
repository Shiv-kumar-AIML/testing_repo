#!/usr/bin/env python3
"""Terminal chatbot using LangGraph + Ollama (mistral:latest)."""

from __future__ import annotations

import os
from typing import Annotated, TypedDict

from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages


class ChatState(TypedDict):
    messages: Annotated[list, add_messages]


def build_graph(model_name: str, base_url: str):
    llm = ChatOllama(model=model_name, base_url=base_url, temperature=0.2)

    def assistant_node(state: ChatState):
        response = llm.invoke(state["messages"])
        return {"messages": [response]}

    builder = StateGraph(ChatState)
    builder.add_node("assistant", assistant_node)
    builder.add_edge(START, "assistant")
    builder.add_edge("assistant", END)

    memory = MemorySaver()
    return builder.compile(checkpointer=memory)


def main() -> None:
    model_name = os.getenv("OLLAMA_MODEL", "mistral:latest")
    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    graph = build_graph(model_name=model_name, base_url=base_url)
    config = {"configurable": {"thread_id": "chat-session"}}

    print(f"LangGraph chatbot started with model: {model_name}")
    print(f"Ollama endpoint: {base_url}")
    print("Type 'exit' or 'quit' to stop.\n")

    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue

        if user_input.lower() in {"exit", "quit"}:
            print("Assistant: Bye!")
            break

        try:
            result = graph.invoke({"messages": [("user", user_input)]}, config=config)
            assistant_message = result["messages"][-1].content
            print(f"Assistant: {assistant_message}\n")
        except Exception as exc:  # noqa: BLE001
            print("Assistant: I could not reach Ollama or generate a reply.")
            print("Check that Ollama is running and mistral is available.")
            print(f"Error details: {exc}\n")


if __name__ == "__main__":
    main()
