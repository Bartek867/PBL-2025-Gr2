# simulator.py
import time, random, sqlite3
from datetime import datetime
import numpy as np

DB = "predmaint.db"
MACHINE_COUNT = 5
SLEEP_SECONDS = 2  # jak często generujemy nowe odczyty per maszyna

def init_db():
    with sqlite3.connect(DB) as conn:
        cur = conn.cursor()
        cur.executescript(open("db_schema.sql").read())
        # insert machines if empty
        cur.execute("SELECT COUNT(*) FROM machines")
        if cur.fetchone()[0] == 0:
            for i in range(1, MACHINE_COUNT+1):
                cur.execute("INSERT INTO machines (machine_id, name, location, install_date) VALUES (?, ?, ?, ?)",
                            (i, f"Machine-{i}", f"Line-{(i%3)+1}", datetime.now().date()))
        conn.commit()

def baseline_readings(machine_id):
    # baseline depends on machine id to differ machines
    temp_base = 65 + (machine_id*3)  # degrees
    vib_base = 0.5 + (machine_id*0.1)
    cur_base = 10 + (machine_id*1)
    return temp_base, vib_base, cur_base

def maybe_spike(value, scale=1.0):
    if random.random() < 0.02:  # 2% chance of a spike
        return value + value * (0.3 + random.random()*0.7) * scale
    return value

def generate_reading(machine_id):
    temp_base, vib_base, cur_base = baseline_readings(machine_id)
    temp = np.random.normal(temp_base, 0.8)
    vibration = abs(np.random.normal(vib_base, 0.05))
    current = np.random.normal(cur_base, 0.7)
    # occasional drift
    if random.random() < 0.005:
        temp += 10 * random.random()
    # spikes
    temp = maybe_spike(temp, 1.0)
    vibration = maybe_spike(vibration, 0.5)
    current = maybe_spike(current, 0.8)
    return temp, vibration, current

def write_measurement(conn, machine_id, ts, temp, vibration, current):
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO measurements (machine_id, ts, temperature, vibration, current) VALUES (?, ?, ?, ?, ?)",
        (machine_id, ts, temp, vibration, current)
    )

def main_loop():
    init_db()
    while True:
        ts = datetime.utcnow().isoformat()
        with sqlite3.connect(DB) as conn:
            for m in range(1, MACHINE_COUNT+1):
                temp, vib, cur_val = generate_reading(m)
                write_measurement(conn, m, ts, float(temp), float(vib), float(cur_val))
            conn.commit()
        time.sleep(SLEEP_SECONDS)

if __name__ == "__main__":
    main_loop()
