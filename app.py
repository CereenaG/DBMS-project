from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

# ---------------- DB CONNECTION ----------------
def get_db_connection():
    conn = sqlite3.connect("hospital.db")
    conn.row_factory = sqlite3.Row
    return conn

def get_doctors():
    conn = get_db_connection()
    doctors = conn.execute("SELECT username, name, department FROM doctors").fetchall()
    conn.close()
    return doctors

app = Flask(__name__)
app.secret_key = "your_secret_key"

# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("home.html")

# ---------------- ADMIN LOGIN ----------------
@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = get_db_connection()
        admin = conn.execute(
            "SELECT * FROM admins WHERE username=? AND password=?", 
            (username, password)
        ).fetchone()
        conn.close()

        if admin:
            session["user"] = admin["username"]
            session["role"] = "admin"
            return redirect(url_for("admin_dashboard"))
        else:
            error = "Invalid credentials"
    return render_template("admin.html", error=error)

@app.route("/admin/appointments")
def admin_appointments():
    if session.get("role") != "admin":
        return redirect(url_for("admin_login"))

    conn = get_db_connection()
    appointments = conn.execute("""
        SELECT a.id, a.date, a.status, 
               p.name AS patient_name, 
               d.name AS doctor_name, 
               d.department
        FROM appointments a
        JOIN patients p ON a.patient_id = p.id
        JOIN doctors d ON a.doctor_id = d.id
    """).fetchall()
    conn.close()

    return render_template("admin_appointments.html", appointments=appointments)

@app.route("/admin/dashboard")
def admin_dashboard():
    if session.get("role") != "admin":
        return redirect(url_for("admin_login"))

    conn = get_db_connection()
    appointments = conn.execute("""
        SELECT a.id, a.date, a.status,
               p.name AS patient_name,
               d.name AS doctor_name,
               d.department AS department
        FROM appointments a
        JOIN patients p ON a.patient_id = p.id
        JOIN doctors d ON a.doctor_id = d.id
    """).fetchall()
    conn.close()

    return render_template("admin_dashboard.html", appointments=appointments)

@app.route("/admin/delete_appointment/<int:appt_id>", methods=["POST"])
def delete_appointment(appt_id):
    if session.get("role") != "admin":
        return redirect(url_for("admin_login"))

    conn = get_db_connection()
    conn.execute("DELETE FROM appointments WHERE id = ?", (appt_id,))
    conn.commit()
    conn.close()

    return redirect(url_for("admin_dashboard"))


# ---------------- DOCTOR LOGIN ----------------
@app.route("/doctor", methods=["GET", "POST"])
def doctor_login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = get_db_connection()
        doctor = conn.execute(
            "SELECT * FROM doctors WHERE username=? AND password=?", 
            (username, password)
        ).fetchone()
        conn.close()

        if doctor:
            session["user"] = doctor["username"]
            session["role"] = "doctor"
            return redirect(url_for("doctor_dashboard"))
        else:
            error = "Invalid credentials"
    return render_template("doctor.html", error=error)

@app.route("/doctor/dashboard")
def doctor_dashboard():
    if session.get("role") != "doctor":
        return redirect(url_for("doctor_login"))

    conn = get_db_connection()
    appointments = conn.execute("""
        SELECT a.id, a.date, a.status,
               p.name AS patient_name
        FROM appointments a
        JOIN patients p ON a.patient_id = p.id
        JOIN doctors d ON a.doctor_id = d.id
        WHERE d.username = ?
    """, (session["user"],)).fetchall()
    conn.close()

    return render_template("doctor_dashboard.html", appointments=appointments)

@app.route("/doctor/appointments")
def doctor_appointments():
    if session.get("role") != "doctor":
        return redirect(url_for("doctor_login"))

    conn = get_db_connection()
    appointments = conn.execute("""
        SELECT a.id, a.date, a.status,
               p.name AS patient_name
        FROM appointments a
        JOIN patients p ON a.patient_id = p.id
        JOIN doctors d ON a.doctor_id = d.id
        WHERE d.username = ?
    """, (session["user"],)).fetchall()
    conn.close()

    return render_template("doctor_appointments.html", appointments=appointments)

@app.route("/doctor/mark_treated/<int:appt_id>", methods=["POST"])
def mark_treated(appt_id):
    if session.get("role") != "doctor":
        return redirect(url_for("doctor_login"))

    conn = get_db_connection()
    conn.execute("UPDATE appointments SET status = 'Treated' WHERE id = ?", (appt_id,))
    conn.commit()
    conn.close()

    return redirect(url_for("doctor_dashboard"))




# ---------------- PATIENT LOGIN ----------------
@app.route("/patient", methods=["GET", "POST"])
def patient_login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = get_db_connection()
        patient = conn.execute(
            "SELECT * FROM patients WHERE username=? AND password=?", 
            (username, password)
        ).fetchone()
        conn.close()

        if patient:
            session["user"] = patient["username"]
            session["role"] = "patient"
            return redirect(url_for("patient_dashboard"))
        else:
            error = "Invalid credentials"
    return render_template("patient.html", error=error)

@app.route("/patient/dashboard")
def patient_dashboard():
    if session.get("role") == "patient":
        return render_template("patient_dashboard.html", user=session.get("user"))
    return redirect(url_for("patient_login"))

# ---------------- PATIENT REGISTRATION ----------------
@app.route("/patient/register", methods=["GET", "POST"])
def patient_register():
    error = None
    success = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        name = request.form["name"]

        conn = get_db_connection()
        # check if username already exists
        existing = conn.execute("SELECT * FROM patients WHERE username=?", (username,)).fetchone()

        if existing:
            error = "❌ Username already taken. Please choose another."
        else:
            conn.execute(
                "INSERT INTO patients (username, password, name) VALUES (?, ?, ?)",
                (username, password, name)
            )
            conn.commit()
            success = "✅ Registration successful! Please login."
        conn.close()

    return render_template("patient_register.html", error=error, success=success)

# ---------------- BOOK APPOINTMENT ----------------
@app.route("/book_appointment", methods=["GET", "POST"])
def book_appointment():
    if "user" not in session or session.get("role") != "patient":
        return redirect(url_for("patient_login"))

    conn = get_db_connection()

    if request.method == "POST":
        doctor_username = request.form["doctor"]
        date = request.form["date"]

        # Get patient_id
        patient = conn.execute("SELECT id FROM patients WHERE username=?", (session["user"],)).fetchone()
        # Get doctor_id
        doctor = conn.execute("SELECT id FROM doctors WHERE username=?", (doctor_username,)).fetchone()

        if patient and doctor:
            conn.execute(
                "INSERT INTO appointments (patient_id, doctor_id, date, time, status) VALUES (?, ?, ?, ?, ?)",
                (patient["id"], doctor["id"], date, "00:00", "Pending")
            )
            conn.commit()
            conn.close()
            return render_template("book_appointment.html", doctors=get_doctors(), success="✅ Appointment booked successfully!")
        else:
            conn.close()
            return render_template("book_appointment.html", doctors=get_doctors(), error="❌ Invalid patient or doctor.")

    conn.close()
    return render_template("book_appointment.html", doctors=get_doctors())

# ---------------- PRESCRIPTION (Doctor adds medicines) ----------------
@app.route("/doctor/prescribe/<int:appt_id>", methods=["GET", "POST"])
def prescribe(appt_id):
    if session.get("role") != "doctor":
        return redirect(url_for("doctor_login"))

    conn = get_db_connection()
    appointment = conn.execute(
        """SELECT a.id, p.id AS patient_id, p.name AS patient_name, d.id AS doctor_id
           FROM appointments a
           JOIN patients p ON a.patient_id = p.id
           JOIN doctors d ON a.doctor_id = d.id
           WHERE a.id = ?""", (appt_id,)
    ).fetchone()

    if request.method == "POST":
        medicine = request.form["medicine"]
        notes = "" 

        conn.execute(
            "INSERT INTO prescriptions (appointment_id, doctor_id, patient_id, medicine, notes, date) VALUES (?, ?, ?, ?, ?, DATE('now'))",
            (appt_id, appointment["doctor_id"], appointment["patient_id"], medicine, notes)
        )
        conn.commit()
        conn.close()
        return redirect(url_for("doctor_dashboard"))

    conn.close()
    return render_template("prescribe.html", appointment=appointment)

# ---------------- PHARMACY LOGIN ----------------
@app.route("/pharmacy", methods=["GET", "POST"])
def pharmacy_login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == "pharmacy" and password == "pharmacy123":
            session["user"] = username
            session["role"] = "pharmacy"
            return redirect(url_for("pharmacy_dashboard"))
        else:
            error = "Invalid credentials"
    return render_template("pharmacy_login.html", error=error)

# ---------------- PHARMACY DASHBOARD ----------------
@app.route("/pharmacy/dashboard")
def pharmacy_dashboard():
    if session.get("role") != "pharmacy":
        return redirect(url_for("pharmacy_login"))

    conn = get_db_connection()
    prescriptions = conn.execute(
        """SELECT pr.id, pr.medicine, pr.notes, pr.date,
                  p.name AS patient_name, d.name AS doctor_name
           FROM prescriptions pr
           JOIN patients p ON pr.patient_id = p.id
           JOIN doctors d ON pr.doctor_id = d.id"""
    ).fetchall()
    conn.close()

    return render_template("pharmacy_dashboard.html", prescriptions=prescriptions)

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
