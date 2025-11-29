from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agente_persistente import chat_with_persistent_memory
import uvicorn

app = FastAPI(title="Helcio AI Agent API")

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    timestamp: str

@app.get("/")
async def root():
    return {"message": "🚀 Helcio AI Agent API - Agente com memória ativa!"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        response = chat_with_persistent_memory(request.message)
        return ChatResponse(response=response, timestamp="2025-11-28")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "healthy", "memoria": "ativa"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
