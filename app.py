from flask import Flask, request, redirect, url_for, session, render_template_string
from datetime import datetime
import csv, os

app = Flask(__name__)
app.secret_key = "VELVORO_SECURE_2026"

# =========================
# LOGIN CREDENTIALS
# =========================
DOCTORS = {
    "doctor1": "1234",   # Doctor ID : PIN
}

DATA_FILE = "doctor_records.csv"

HEADERS = [
    "DateTime","DoctorID","DoctorName","PatientName","Phone",
    "Age","BP","Sugar","Stress","DoctorNotes"
]

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow(HEADERS)

# =========================
# CORPORATE BASE TEMPLATE
# =========================
BASE_CSS = """
<style>
body {
    font-family: 'Segoe UI', Arial, sans-serif;
    background: #f4f6f9;
    margin: 0;
}
.header {
    background: #0b3c5d;
    color: white;
    padding: 15px 30px;
    font-size: 22px;
    font-weight: 600;
}
.container {
    max-width: 900px;
    margin: 30px auto;
    background: white;
    padding: 30px;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
h2 {
    color: #0b3c5d;
    border-bottom: 2px solid #e0e0e0;
    padding-bottom: 10px;
}
label {
    display: block;
    margin-top: 15px;
    font-weight: 600;
}
input, select, textarea {
    width: 100%;
    padding: 10px;
    margin-top: 6px;
    border-radius: 4px;
    border: 1px solid #ccc;
}
textarea { height: 120px; }
button {
    margin-top: 20px;
    padding: 12px 20px;
    background: #0b3c5d;
    color: white;
    border: none;
    font-size: 16px;
    border-radius: 4px;
    cursor: pointer;
}
button:hover {
    background: #092f49;
}
.footer {
    text-align: center;
    font-size: 13px;
    color: #777;
    margin-top: 40px;
}
.error {
    color: red;
    margin-top: 15px;
}
.logout {
    float: right;
    font-size: 14px;
}
.logout a {
    color: white;
    text-decoration: none;
}
</style>
"""

# =========================
# LOGIN PAGE
# =========================
LOGIN_HTML = BASE_CSS + """
<div class="header">
    Velvoro Medical AI – Doctor Login
</div>

<div class="container">
    <h2>Secure Doctor Access</h2>

    <form method="post">
        <label>Doctor ID</label>
        <input name="doctor_id" required>

        <label>PIN</label>
        <input name="pin" type="password" required>

        <button type="submit">Login</button>
    </form>

    {% if error %}
    <div class="error">{{ error }}</div>
    {% endif %}
</div>

<div class="footer">
    © 2026 Velvoro Software Solution – Medical AI System
</div>
"""

# =========================
# MEDICAL FORM PAGE
# =========================
APP_HTML = BASE_CSS + """
<div class="header">
    Velvoro Medical AI
    <div class="logout"><a href="/logout">Logout</a></div>
</div>

<div class="container">
    <h2>Patient Consultation Panel</h2>

    <form method="post">
        <label>Doctor Name</label>
        <input name="doctor_name" required>

        <label>Patient Name</label>
        <input name="patient_name" required>

        <label>Phone Number</label>
        <input name="phone" required>

        <label>Age</label>
        <input name="age">

        <label>BP</label>
        <input name="bp" placeholder="120/80">

        <label>Sugar</label>
        <input name="sugar">

        <label>Stress Level</label>
        <select name="stress">
            <option>No</option>
            <option>Yes</option>
        </select>

        <label>Doctor Notes</label>
        <textarea name="notes"></textarea>

        <button type="submit">Save Record</button>
    </form>
</div>

<div class="footer">
    This system is confidential & for authorized doctors only.
</div>
"""

# =========================
# ROUTES
# =========================
@app.route("/", methods=["GET","POST"])
def login():
    if request.method == "POST":
        did = request.form["doctor_id"]
        pin = request.form["pin"]

        if did in DOCTORS and DOCTORS[did] == pin:
            session["doctor"] = did
            return redirect("/app")
        else:
            return render_template_string(LOGIN_HTML, error="Invalid Doctor ID or PIN")

    return render_template_string(LOGIN_HTML)

@app.route("/app", methods=["GET","POST"])
def app_page():
    if "doctor" not in session:
        return redirect("/")

    if request.method == "POST":
        with open(DATA_FILE, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M"),
                session["doctor"],
                request.form["doctor_name"],
                request.form["patient_name"],
                request.form["phone"],
                request.form["age"],
                request.form["bp"],
                request.form["sugar"],
                request.form["stress"],
                request.form["notes"]
            ])
        return redirect("/app")

    return render_template_string(APP_HTML)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(debug=True)
