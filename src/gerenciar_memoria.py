import sqlite3
import sys
from datetime import datetime

DB_FILE = "helcio_memory.db"

def print_stats():
    conn = sqlite3.connect(DB_FILE)
    total = conn.execute("SELECT COUNT(*) FROM messages").fetchone()[0]
    today = conn.execute("SELECT COUNT(*) FROM messages WHERE date(timestamp) = date('now')").fetchone()[0]
    print(f"📊 ESTATÍSTICAS MEMÓRIA HELCIO")
    print(f"Total mensagens: {total}")
    print(f"Mensagens hoje: {today}")

def list_recent(n=10):
    conn = sqlite3.connect(DB_FILE)
    print(f"\n🧠 ÚLTIMAS {n} MENSAGENS:")
    for row in conn.execute(f"SELECT role, content, timestamp FROM messages ORDER BY id DESC LIMIT {n}"):
        print(f"[{row[2][:16]}] {row[0].upper()}: {row[1][:80]}...")
    conn.close()

def clear_memory():
    confirm = input("⚠️  LIMPAR TODA MEMÓRIA? (sim/não): ")
    if confirm.lower() == 'sim':
        conn = sqlite3.connect(DB_FILE)
        conn.execute("DELETE FROM messages")
        conn.commit()
        print("🗑️  Memória limpa!")
        conn.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "stats":
            print_stats()
        elif cmd == "recent":
            list_recent(20)
        elif cmd == "clear":
            clear_memory()
    else:
        print_stats()
        list_recent(5)
