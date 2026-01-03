import sqlite3
import time
import random

# Nazwa DB
DB_NAME = 'maintenance.db'

def run_simulator():
    print(f"🚀 Uruchamiam symulator maszyn...") 
    print("Naciśnij Ctrl+C, aby zatrzymać.")

    try:
        while True:
            # 1. łączenie z bazą
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()

            # 2. Generowanie losowych danych
            # Maszyna A, B lub C
            machine_id = random.choice(['Machine_A', 'Machine_B', 'Machine_C'])
            # Temperatura )
            temperature = round(random.uniform(60, 90), 2)
            # Wibracje 
            vibration = round(random.uniform(0, 5), 2)
            # Prąd 
            current = round(random.uniform(10, 20), 2)

            # 3. Zapisywanie do bazy
            cursor.execute('''
                INSERT INTO measurements (machine_id, temperature, vibration, current)
                VALUES (?, ?, ?, ?)
            ''', (machine_id, temperature, vibration, current))

            conn.commit()
            conn.close()

            print(f"✅ Zapisano: {machine_id} | Temperature: {temperature}C | Vibration: {vibration}")
            
            # Pomiar co 2 sekundy
            time.sleep(2)

    except KeyboardInterrupt:
        print("\n🛑 Symulator zatrzymany przez użytkownika.")

if __name__ == "__main__":
    run_simulator()