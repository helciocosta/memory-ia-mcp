from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage
from typing import List
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatOllama(model=os.getenv("OLLAMA_MODEL"))

class AgentMemory:
    def __init__(self):
        self.messages = []
    
    def add_message(self, role, content):
        self.messages.append({"role": role, "content": content})
        if len(self.messages) > 20:  # Limita memória
            self.messages = self.messages[-10:]
    
    def get_context(self):
        return self.messages[-8:]  # Últimas 8 mensagens

memory = AgentMemory()

def chat_with_memory(user_input):
    memory.add_message("user", user_input)
    
    context = "\n".join([f"{m['role']}: {m['content']}" for m in memory.get_context()])
    
    prompt = f"""Você é assistente do Helcio, desenvolvedor Python FastAPI.

Histórico recente:
{context}

PERGUNTA: {user_input}
RESPOSTA em português:"""
    
    response = llm.invoke(prompt)
    memory.add_message("assistant", response.content)
    return response.content

print("✅ Agente LangGraph + Memória SIMPLES CRIADO!")
