#!/usr/bin/env python3
"""
MCP Server para expor o Agente Helcio com Ollama para VS Code, Gemini-CLI, etc.
"""

import json
import sys
import os
from typing import Any
import httpx
from pydantic import BaseModel

# Configuração
AGENT_URL = "http://localhost:8000"  # URL do seu FastAPI (ajustar se necessário)
OLLAMA_URL = "http://localhost:11434"

class ToolResult(BaseModel):
    type: str = "text"
    text: str

def send_json_rpc(method: str, params: dict | None = None) -> None:
    """Envia resposta JSON-RPC 2.0 via stdout"""
    response = {
        "jsonrpc": "2.0",
        "result": params or {},
        "id": 1
    }
    print(json.dumps(response), file=sys.stdout)
    sys.stdout.flush()

def chat_with_helcio_agent(message: str) -> str:
    """Faz chamada HTTP POST para seu agente FastAPI"""
    try:
        response = httpx.post(
            f"{AGENT_URL}/chat",
            json={"message": message},
            timeout=30.0
        )
        if response.status_code == 200:
            return response.json().get("response", "Erro na resposta")
        return f"Erro HTTP {response.status_code}"
    except Exception as e:
        return f"Erro ao conectar ao agente: {str(e)}"

def run_ollama_model(model: str, prompt: str) -> str:
    """Chama Ollama diretamente (fallback se agente não disponível)"""
    try:
        response = httpx.post(
            f"{OLLAMA_URL}/api/generate",
            json={"model": model, "prompt": prompt},
            timeout=60.0
        )
        if response.status_code == 200:
            lines = response.text.strip().split('\n')
            full_response = ""
            for line in lines:
                if line:
                    data = json.loads(line)
                    full_response += data.get("response", "")
            return full_response
        return f"Erro Ollama: {response.status_code}"
    except Exception as e:
        return f"Erro Ollama: {str(e)}"

def handle_initialize() -> dict:
    """Inicialização MCP - chamada quando VS Code/Gemini conecta"""
    return {
        "protocolVersion": "2024-11-05",
        "capabilities": {},
        "serverInfo": {
            "name": "Helcio-Agent-MCP",
            "version": "1.0.0"
        }
    }

def handle_tools() -> dict:
    """Lista ferramentas disponíveis"""
    return {
        "tools": [
            {
                "name": "helcio_chat",
                "description": "Chat com o agente Helcio (com memória persistente)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "string",
                            "description": "Mensagem para o agente"
                        }
                    },
                    "required": ["message"]
                }
            },
            {
                "name": "run_ollama",
                "description": "Executa modelo Ollama diretamente",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "model": {
                            "type": "string",
                            "description": "Nome do modelo (ex: llama3.2:1b)",
                            "default": "llama3.2:1b"
                        },
                        "prompt": {
                            "type": "string",
                            "description": "Prompt para o modelo"
                        }
                    },
                    "required": ["prompt"]
                }
            },
            {
                "name": "agent_health",
                "description": "Verifica saúde do agente Helcio",
                "inputSchema": {
                    "type": "object",
                    "properties": {}
                }
            }
        ]
    }

def handle_call_tool(name: str, arguments: dict) -> dict:
    """Executa uma ferramenta solicitada"""
    if name == "helcio_chat":
        message = arguments.get("message", "")
        result = chat_with_helcio_agent(message)
        return {"content": [{"type": "text", "text": result}]}
    
    elif name == "run_ollama":
        model = arguments.get("model", "llama3.2:1b")
        prompt = arguments.get("prompt", "")
        result = run_ollama_model(model, prompt)
        return {"content": [{"type": "text", "text": result}]}
    
    elif name == "agent_health":
        try:
            httpx.get(f"{AGENT_URL}/health", timeout=5.0)
            return {"content": [{"type": "text", "text": "✅ Agente Helcio está online"}]}
        except:
            return {"content": [{"type": "text", "text": "❌ Agente Helcio offline"}]}
    
    return {"content": [{"type": "text", "text": "Ferramenta desconhecida"}]}

def main():
    """Loop principal do servidor MCP"""
    print("Iniciando MCP Server para Helcio Agent...", file=sys.stderr)
    
    for line in sys.stdin:
        try:
            request = json.loads(line)
            method = request.get("method", "")
            params = request.get("params", {})
            
            if method == "initialize":
                result = handle_initialize()
            elif method == "tools/list":
                result = handle_tools()
            elif method == "tools/call":
                tool_name = params.get("name", "")
                arguments = params.get("arguments", {})
                result = handle_call_tool(tool_name, arguments)
            else:
                result = {"error": f"Método desconhecido: {method}"}
            
            response = {
                "jsonrpc": "2.0",
                "result": result,
                "id": request.get("id", 1)
            }
            print(json.dumps(response))
            sys.stdout.flush()
        
        except Exception as e:
            print(json.dumps({"error": str(e)}))
            sys.stdout.flush()

if __name__ == "__main__":
    main()
