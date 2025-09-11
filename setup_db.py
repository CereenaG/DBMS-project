import sqlite3

# Connect to database (it will create hospital.db if not exists)
conn = sqlite3.connect("hospital.db")
cursor = conn.cursor()

# ---------------- TABLE CREATION ----------------

# Admins
cursor.execute("""
CREATE TABLE IF NOT EXISTS admins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

# Patients
cursor.execute("""
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    gender TEXT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

# Doctors
cursor.execute("""
CREATE TABLE IF NOT EXISTS doctors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    department TEXT NOT NULL,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

# Appointments
cursor.execute("""
CREATE TABLE IF NOT EXISTS appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    doctor_id INTEGER,
    date TEXT NOT NULL,
    time TEXT NULL,
    status TEXT DEFAULT 'Pending',
    FOREIGN KEY(patient_id) REFERENCES patients(id),
    FOREIGN KEY(doctor_id) REFERENCES doctors(id)
)
""")

# Prescriptions
cursor.execute("""
CREATE TABLE IF NOT EXISTS prescriptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    appointment_id INTEGER,
    doctor_id INTEGER,
    patient_id INTEGER,
    medicine TEXT NOT NULL,
    notes TEXT,
    date TEXT NOT NULL,
    FOREIGN KEY(appointment_id) REFERENCES appointments(id),
    FOREIGN KEY(doctor_id) REFERENCES doctors(id),
    FOREIGN KEY(patient_id) REFERENCES patients(id)
)
""")

# Pharmacy
cursor.execute("""
CREATE TABLE IF NOT EXISTS pharmacy (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

# ---------------- INSERT SAMPLE DATA ----------------

# Admin
cursor.execute("INSERT OR IGNORE INTO admins (username, password) VALUES (?, ?)", ("admin", "admin123"))

# Doctors
doctors = [
    ("Dr. A", "Cardiology", "dra", "passA"),
    ("Dr. B", "Cardiology", "drb", "passB"),
    ("Dr. C", "Neurology", "drc", "passC"),
    ("Dr. D", "Neurology", "drd", "passD"),
    ("Dr. E", "Orthopedics", "dre", "passE"),
    ("Dr. F", "Orthopedics", "drf", "passF"),
    ("Dr. G", "Dermatology", "drg", "passG"),
    ("Dr. H", "Dermatology", "drh", "passH"),
    ("Dr. I", "Pediatrics", "dri", "passI"),
    ("Dr. J", "Pediatrics", "drj", "passJ"),
]
cursor.executemany(
    "INSERT OR IGNORE INTO doctors (name, department, username, password) VALUES (?, ?, ?, ?)", 
    doctors
)

# Patient
cursor.execute(
    "INSERT OR IGNORE INTO patients (name, age, gender, username, password) VALUES (?, ?, ?, ?, ?)",
    ("Test Patient", 25, "Female", "patient", "patient123")
)

# Pharmacy user (default login)
cursor.execute("INSERT OR IGNORE INTO pharmacy (username, password) VALUES (?, ?)", ("pharmacy", "pharmacy123"))

# Commit and close
conn.commit()
conn.close()

print("✅ All 5 tables created with sample data in hospital.db")
