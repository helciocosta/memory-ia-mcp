from agente_langgraph import chat_with_memory

print("=== 🧠 TESTE MEMÓRIA SIMPLES + OLLAMA ===\n")

print("🧠 TESTE 1: Apresentação")
resp1 = chat_with_memory("Meu nome é Helcio. Sou desenvolvedor Python FastAPI.")
print("Resposta 1:", resp1[:150], "\n")

print("🧠 TESTE 2: Teste memória")
resp2 = chat_with_memory("Qual meu nome e profissão?")
print("Resposta 2 (com memória):", resp2)

print("\n" + "="*60)
print("✅ Se mencionar 'Helcio' + 'FastAPI' = MEMÓRIA FUNCIONANDO!")
print("="*60)
