import sqlite3
import shutil
from datetime import datetime
import os

DB_FILE = "helcio_memory.db"
BACKUP_DIR = "backups_memoria"

os.makedirs(BACKUP_DIR, exist_ok=True)

def backup():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"{BACKUP_DIR}/helcio_memory_{timestamp}.db"
    shutil.copy2(DB_FILE, backup_file)
    print(f"💾 Backup criado: {backup_file}")

if __name__ == "__main__":
    backup()
