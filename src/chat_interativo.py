from agente_langgraph import chat_with_memory
import os

print("🤖 CHAT INTERATIVO COM MEMÓRIA PERSISTENTE")
print("Digite 'sair' para terminar\n")

while True:
    user_input = input("Você: ").strip()
    if user_input.lower() in ['sair', 'exit', 'quit']:
        print("👋 Até logo Helcio!")
        break
    
    response = chat_with_memory(user_input)
    print(f"🤖 Assistente: {response}\n")
