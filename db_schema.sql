-- Tabela Maszyn (katalog urządzeń)
CREATE TABLE IF NOT EXISTS machines (
    machine_id TEXT PRIMARY KEY,
    model TEXT,
    location TEXT,
    install_date DATE
);

-- Tabela Pomiarów (dane z czujników: temperatura, drgania)
CREATE TABLE IF NOT EXISTS measurements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    machine_id TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    temperature REAL,
    vibration REAL,
    current REAL,
    FOREIGN KEY (machine_id) REFERENCES machines (machine_id)
);

-- Tabela Alertów (wykryte awarie)
CREATE TABLE IF NOT EXISTS alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    machine_id TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    description TEXT,
    severity TEXT,
    FOREIGN KEY (machine_id) REFERENCES machines (machine_id)
);

-- Tabela Logów (kto i kiedy korzystał)
CREATE TABLE IF NOT EXISTS audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_type TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    details TEXT
);

-- Przykładowe maszyny
INSERT OR IGNORE INTO machines (machine_id, model, location) VALUES 
('Machine_A', 'Robot_Arm_V1', 'Hala_1'),
('Machine_B', 'Conveyor_Belt_X', 'Hala_2');