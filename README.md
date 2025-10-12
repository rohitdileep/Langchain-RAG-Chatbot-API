# 🧠 LangChain RAG Chatbot API

A **FastAPI-based Retrieval-Augmented Generation (RAG)** chatbot API built with **LangChain**, **ChromaDB**, **PostgreSQL**, and **Groq/OpenAI GPT models**.  
This project provides a **production-ready conversational AI backend** that supports contextual memory, dynamic retrieval, and persistent conversation history.

---

## 🚀 Features

- ⚡ **FastAPI Backend** — High-performance, async REST API framework.
- 🧩 **LangChain Integration** — For retrieval, memory, and LLM orchestration.
- 🧠 **RAG (Retrieval-Augmented Generation)** — Combines vector search with LLM responses for grounded answers.
- 💾 **ChromaDB Vector Store** — Stores and retrieves document embeddings efficiently.
- 🧱 **PostgreSQL Support** — For storing user sessions and conversation history.
- 🤖 **Groq / OpenAI GPT models** — Powering the chatbot responses.
- 🧠 **History-Aware Retriever** — Maintains conversational context for natural interactions.
- 🔐 **Environment Config via `.env`** — Keeps secrets like API keys secure.

---

## 🏗️ Tech Stack

| Component | Technology |
|------------|-------------|
| Backend Framework | [FastAPI](https://fastapi.tiangolo.com/) |
| LLM Orchestration | [LangChain](https://www.langchain.com/) |
| Vector Database | [ChromaDB](https://www.trychroma.com/) |
| Relational Database | [PostgreSQL](https://www.postgresql.org/) |
| LLM Provider | [Groq](https://groq.com/) / [OpenAI GPT](https://platform.openai.com/) |
| ORM | [SQLAlchemy](https://www.sqlalchemy.org/) |
| Environment Config | [python-dotenv](https://pypi.org/project/python-dotenv/) |

---

## ⚙️ Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/rohitdileep/Langchain-RAG-Chatbot-API.git
cd Langchain-RAG-Chatbot-API


python -m venv venv
#for mac source venv/bin/activate
#On Windows: venv\Scripts\activate


pip install -r requirements.txt

OPENAI_API_KEY=your_openai_api_key
GROQ_API_KEY=your_groq_api_key
DATABASE_URL=postgresql://user:password@localhost:5432/chatbot_db
CHROMA_PATH=./chroma_db

##Run the command in Terminal
uvicorn main:app --reload


