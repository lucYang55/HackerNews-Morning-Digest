# HackerNews Morning Digest (Local RAG + Ollama)
<img width="1684" height="584" alt="Screenshot 2026-04-08 at 11 17 29 AM" src="https://github.com/user-attachments/assets/6f223475-d350-49e5-87f2-59dbedf0ad2a" />

A fully local Retrieval-Augmented Generation (RAG) pipeline that automatically generates a structured morning news digest from Hacker News using locally hosted LLMs via Ollama. This project is designed to give you a concise, engineer-focused overview of the most relevant Hacker News stories each day—without relying on external APIs or paid LLM services.

Overview

The system runs as a daily job that:

- Pulls top stories from the Hacker News API
- Processes and embeds them into a vector index
- Uses a local LLM to synthesize insights
- Outputs a readable morning digest directly to your terminal or a log file

# Architecture

This project follows a simple RAG pipeline:

1. Data Ingestion

Fetches top stories from the Hacker News API, including:

Title
Score (upvotes)
Number of comments
Author

Each story is converted into a structured Document object using llama_index.

1. Embedding + Indexing
Documents are embedded using the nomic-embed-text model via Ollama
Embeddings are stored in an in-memory vector store
Enables semantic retrieval over the top stories

2. Query + Generation
A structured prompt is sent to a local LLM (dolphin-llama3:8b)
The model retrieves relevant stories from the index
It generates a clean, summarized morning digest

3. Output
The final digest is printed to the terminal
Optionally redirected to a file for logging or later reading

Features
100% local execution (no external LLM APIs)
Daily automated news generation
Structured, developer-focused summaries
Lightweight and fast with in-memory indexing
Easily extensible (e.g., add filtering, ranking, or personalization)
Prerequisites

# Make sure the following are installed before running the project:

1. Python
  Python 3.10 or higher

2. Ollama
  Ollama is used to run both the LLM and embedding models locally.
  Download and install from:
  https://ollama.com

# Start the Ollama server (if not already running):

Pull the required models (only needed once):

LLM (for generating the digest):

- ollama pull dolphin-llama3:8b

Embedding model (for vector search):

- ollama pull nomic-embed-text

# Setup

Create and activate a virtual environment:
  python3 -m venv venv
  source venv/bin/activate

Install dependencies (example):
  pip install -r requirements.txt

Run manually:
  python rag.py

This will:
  Fetch the latest Hacker News stories
  Build the vector index
  Generate and print the digest
  Automating with Cron (macOS/Linux)

To run the digest automatically every morning, use cron.

Open your crontab:

- crontab -e

Add a scheduled job (example: run every day at 9:00 AM):

0 9 * * * cd /your/project/path && /path/to/python rag.py >> /path/to/output.log 2>&1

Breakdown:
  0 9 * * * → runs at 9:00 AM daily
  cd → ensures correct working directory
  >> output.log → appends output to a log file
  2>&1 → captures errors along with output
