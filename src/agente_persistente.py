import sqlite3
import os
from langchain_ollama import ChatOllama
from dotenv import load_dotenv

load_dotenv()
llm = ChatOllama(model=os.getenv("OLLAMA_MODEL"))

DB_FILE = "helcio_memory.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT,
            content TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def add_message(role, content):
    conn = sqlite3.connect(DB_FILE)
    conn.execute("INSERT INTO messages (role, content) VALUES (?, ?)", (role, content))
    conn.commit()
    conn.close()

def get_recent_messages(limit=6):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.execute("SELECT role, content FROM messages ORDER BY id DESC LIMIT ?;", (limit,))
    messages = [{"role": row[0], "content": row[1]} for row in cursor.fetchall()][::-1]
    conn.close()
    return messages

def chat_with_persistent_memory(user_input):
    add_message("user", user_input)
    history = get_recent_messages(6)
    
    context = "\n".join([f"{m['role']}: {m['content']}" for m in history[-4:]])
    
    prompt = f"""Você é assistente do Helcio (dev Python FastAPI).

CONTEXTO RECENTE:
{context}

Pergunta: {user_input}

Responda EM PORTUGUÊS, DIRETO, SEM CÓDIGO, máximo 2 frases."""

    response = llm.invoke(prompt)
    add_message("assistant", response.content)
    return response.content

init_db()
print("✅ Agente OTIMIZADO com MEMÓRIA SQLITE!")
