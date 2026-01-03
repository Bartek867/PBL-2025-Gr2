import sqlite3
import os

def init_db():
    db_file = 'maintenance.db'
    sql_file = 'db_schema.sql'

    # Jeśli baza już istnieje, usuwa ją, żeby stworzyć od nowa
    if os.path.exists(db_file):
        os.remove(db_file)
        print("Usunięto starą wersję bazy.")

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    print("Wczytuję plik SQL...")
    
    with open(sql_file, 'r', encoding='utf-8') as f:
        sql_script = f.read()
        
    cursor.executescript(sql_script)
    
    conn.commit()
    conn.close()
    print("✅ Powodzenie! Baza 'maintenance.db' została utworzona z Twojego schematu.")

if __name__ == "__main__":
    init_db()