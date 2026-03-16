# LangGraph + Ollama Chatbot (`mistral:latest`)

This project is a terminal chatbot built with:
- `langgraph`
- `langchain-ollama`
- `langchain-community` (web search tool)
- Ollama model: `mistral:latest`
- SQLite database for persistent chat history
- SQL query tool for database interactions
- Web scraping tool for extracting page content
- Voice assistance tools for speech input/output

## 1) Prerequisites

- Python 3.10+
- Ollama installed and running

Start Ollama service (if needed):

```bash
ollama serve
```

Pull the model:

```bash
ollama pull mistral:latest
```

## 2) Install dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 3) Run chatbot

```bash
python chatbot.py
```

## 4) Optional environment variables

- `OLLAMA_MODEL` (default: `mistral:latest`)
- `OLLAMA_BASE_URL` (default: `http://localhost:11434`)

Example:

```bash
export OLLAMA_MODEL=mistral:latest
export OLLAMA_BASE_URL=http://localhost:11434
python chatbot.py
```

## Notes

- Conversation memory is kept during the current run using LangGraph's in-memory checkpointing.
- Web search is enabled using DuckDuckGo. The assistant can call search when your prompt needs recent or factual internet info.
- Chat history is persisted in `chatbot.db` (SQLite) across runs.
- SQL query tool allows read-only queries on the database (e.g., view chat history).
- Web scraping tool extracts text content from URLs for analysis.
- Voice tools: `voice_input_tool` for speech-to-text, `voice_output_tool` for text-to-speech.
- Type `exit` or `quit` to stop.
# testing_repo
