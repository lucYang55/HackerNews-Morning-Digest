# HackerNews-Morning-Digest
Using local Ollama models to create daily news reports based on HackerNews API. 

# HN Morning Digest

A local RAG pipeline that fetches the top stories from HackerNews every morning and generates a structured digest using a locally-running LLM.

## How it works

1. Fetches the top stories from the HackerNews API
2. Converts each story into a `llama_index` `Document` with (title, score, comments, author)
3. Embeds all documents into an in-memory vector store using `nomic-embed-text` via Ollama
4. Queries the index with a structured prompt using `dolphin-llama3:8b`
5. Outputs a morning digest to your terminal 

Prerequisites

You need three things installed before cloning this project.

1. Python 3.10+

2. Ollama
Ollama runs LLMs locally. Download it from [ollama.com](https://ollama.com) and install it, then start the server:
Leave this running in a separate terminal, or set it up as a background service (it installs one automatically on macOS and Linux).

3. The two required models
Pull both models — this only needs to be done once:

The LLM that writes the report
Ollama pull dolphin-llama3:8b

The embedding model for the vector index
ollama pull nomic-embed-text

Use a virtual environment:
python3 -m venv venv

To run daily on Mac, use CRON 
crontab -e

Match the time you want the new letter to execute 
* * * * cd /your/file/path/ && /path/to/executable rag.py >> /path/to/save/output/ 2>&1
