# LangGraph + Ollama Chatbot (`mistral:latest`)

This project is a terminal chatbot built with:
- `langgraph`
- `langchain-ollama`
- Ollama model: `mistral:latest`

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
- Type `exit` or `quit` to stop.
# testing_repo
