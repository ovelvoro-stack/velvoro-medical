from flask import Flask, request, render_template_string
from datetime import datetime
import os
import csv

app = Flask(__name__)

# ================= STORAGE FILES =================
DOCTOR_FILE = "doctor_records.csv"
ADMIN_FILE = "admin_records.csv"

HEADERS = [
    "DateTime", "DoctorName", "PatientName", "Phone",
    "Age", "BP", "Sugar", "Stress",
    "Conditions", "Medicines", "DoctorNotes", "ReportFile"
]

def init_files():
    for file in [DOCTOR_FILE, ADMIN_FILE]:
        if not os.path.exists(file):
            with open(file, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(HEADERS)

init_files()

# ================= AI ENGINE =================
def ai_engine(bp, sugar, stress):
    conditions = []
    medicines = []

    try:
        s, d = bp.split("/")
        s, d = int(s), int(d)
        if s >= 140 or d >= 90:
            conditions.append("High BP")
            medicines.append("Amlodipine class BP medicine (doctor to finalize dose)")
        else:
            conditions.append("Normal BP")
    except:
        conditions.append("Invalid BP")

    try:
        sugar = int(sugar)
        if sugar >= 126:
            conditions.append("High Sugar")
            medicines.append("Metformin class medicine (doctor discretion)")
        else:
            conditions.append("Normal Sugar")
    except:
        conditions.append("Invalid Sugar")

    if stress == "Yes":
        conditions.append("Stress")
        medicines.append("Stress management, yoga, meditation ± anxiolytic (doctor decides)")

    if not medicines:
        medicines.append("Lifestyle advice & monitoring")

    return conditions, medicines

# ================= UI =================
HTML = """
<h2>Velvoro Medical AI</h2>
<form method="post" enctype="multipart/form-data">
Doctor Name:<br><input name="doctor" required><br>
Patient Name:<br><input name="patient" required><br>
Phone Number:<br><input name="phone" required><br>
Age:<br><input name="age"><br>
BP (120/80):<br><input name="bp"><br>
Sugar:<br><input name="sugar"><br>
Stress:
<select name="stress"><option>No</option><option>Yes</option></select><br><br>

Doctor Notes:<br>
<textarea name="notes" style="width:300px;height:80px;"></textarea><br>

Upload Report:<br>
<input type="file" name="report"><br><br>

<button type="submit">Run AI + Save</button>
</form>

{% if result %}
<hr>
<b>Conditions:</b>
<ul>{% for c in result.conditions %}<li>{{c}}</li>{% endfor %}</ul>

<b>Medicines:</b>
<ul>{% for m in result.medicines %}<li>{{m}}</li>{% endfor %}</ul>

<b>Saved Successfully ✔</b><br><br>
<span style="color:red">
AI assisted system only. Final decision by registered doctor.
</span>
{% endif %}
"""

# ================= ROUTE =================
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        data = {
            "dt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "doctor": request.form["doctor"],
            "patient": request.form["patient"],
            "phone": request.form["phone"],
            "age": request.form.get("age", ""),
            "bp": request.form.get("bp", ""),
            "sugar": request.form.get("sugar", ""),
            "stress": request.form.get("stress"),
            "notes": request.form.get("notes", "")
        }

        report_name = ""
        file = request.files.get("report")
        if file and file.filename:
            os.makedirs("uploads", exist_ok=True)
            report_name = datetime.now().strftime("%Y%m%d%H%M%S_") + file.filename
            file.save(os.path.join("uploads", report_name))

        conditions, medicines = ai_engine(data["bp"], data["sugar"], data["stress"])

        row = [
            data["dt"], data["doctor"], data["patient"], data["phone"],
            data["age"], data["bp"], data["sugar"], data["stress"],
            ", ".join(conditions), ", ".join(medicines),
            data["notes"], report_name
        ]

        # SAVE FOR DOCTOR
        with open(DOCTOR_FILE, "a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(row)

        # SAVE FOR ADMIN (VELVORO)
        with open(ADMIN_FILE, "a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(row)

        return render_template_string(
            HTML,
            result={"conditions": conditions, "medicines": medicines}
        )

    return render_template_string(HTML, result=None)

if __name__ == "__main__":
    app.run(debug=True)
