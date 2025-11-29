

text
# Memory-IA MCP Server

**Model Context Protocol (MCP) Server** - Agente IA com Memória Persistente para VS Code, Gemini-CLI, Cursor e outras ferramentas.

## 🚀 Features

- **Chat com Memória Persistente** - Agente IA com contexto SQLite
- **Ollama Integrado** - Suporte a modelos locais (llama3.2, qwen, etc)
- **JSON-RPC Protocol** - Comunicação padronizada MCP
- **Auto-Restart** - Serviço systemd com restart automático
- **Multi-Client** - Funciona em VS Code, Gemini-CLI, terminal, etc

## 📋 Stack

- **Python 3.12** com FastAPI
- **LangGraph + LangChain** para agentes
- **SQLite** para memória persistente
- **Ollama** para LLM local
- **systemd** para gerenciamento

## 🔧 Instalação

### 1. Clonar repositório

cd ~
git clone https://github.com/seu-usuario/memory-ia-mcp.git
cd memory-ia-mcp

text

### 2. Criar ambiente virtual

python3 -m venv memorivenv
source memorivenv/bin/activate

text

### 3. Instalar dependências

pip install -r requirements.txt

text

### 4. Executar MCP Server

./run_mcp.sh

text

## 🎯 Uso Rápido

### Terminal

echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | python src/mcp_server.py

text

### VS Code
1. Configuração em `~/.config/Code/User/mcp.json`
2. Abra Command Palette: `Ctrl+Shift+P`
3. Procure por `MCP: List Servers`
4. Selecione `memory-ia-agent`

### Gemini-CLI

gemini-cli --mcp-server /home/helcio/memory-ia-mcp/src/mcp_server.py

text

## 📡 Ferramentas Disponíveis

| Tool | Descrição |
|------|-----------|
| `memory_chat` | Chat com memória persistente |
| `run_ollama` | Executar modelo Ollama direto |
| `agent_health` | Status do agente |

## 🛠️ Serviço systemd

### Status

sudo systemctl status memory-ia-mcp.service

text

### Logs

sudo journalctl -u memory-ia-mcp -f

text

### Controle

sudo systemctl restart memory-ia-mcp
sudo systemctl stop memory-ia-mcp
sudo systemctl start memory-ia-mcp

text

## 📂 Estrutura

memory-ia-mcp/
├── src/
│ ├── mcp_server.py
│ ├── agente_langgraph.py
│ ├── agente_persistente.py
│ └── api_agente.py
├── config/
│ └── mcp.json
├── docs/
│ └── DEVELOPMENT.md
├── tests/
│ └── test_mcp.py
├── run_mcp.sh
├── requirements.txt
└── README.md

text

## 🔐 Configuração

Crie `.env`:

OLLAMA_URL=http://localhost:11434
AGENT_PORT=8000
DEBUG=False

text

## 📖 Documentação

- [Desenvolvimento](docs/DEVELOPMENT.md)
- [Model Context Protocol](https://modelcontextprotocol.io)

## 🤝 Contribuições

Sinta-se livre para abrir issues e PRs!

---

**Desenvolvido com ❤️**  
**Última atualização:** Nov 28, 2025
