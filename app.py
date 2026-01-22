from flask import Flask, request, render_template_string
import json, os
from datetime import datetime

app = Flask(__name__)

DB_FILE = "medical_db.json"
UPLOAD_FOLDER = "uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w") as f:
        json.dump([], f)

# ---------------- AI ENGINE ----------------
def ai_engine(bp, sugar, sleep, stress):
    conditions = []
    medicines = []

    try:
        bp = int(bp)
        sugar = int(sugar)
    except:
        return ["Invalid values"], []

    if bp > 140:
        conditions.append("High Blood Pressure")
        medicines.append("BP monitoring + lifestyle changes")

    if sugar > 180:
        conditions.append("Diabetes")
        medicines.append("Sugar control diet / medication")

    if sleep == "No":
        conditions.append("Sleep Disorder")

    if stress == "Yes":
        conditions.append("Stress Related Issue")

    return conditions, medicines

# ---------------- HOME ----------------
@app.route("/", methods=["GET", "POST"])
def index():
    ai_conditions = []
    ai_medicines = []
    report_info = []

    if request.method == "POST":
        doctor = request.form["doctor"]
        patient = request.form["patient"]
        phone = request.form["phone"]
        bp = request.form["bp"]
        sugar = request.form["sugar"]
        sleep = request.form["sleep"]
        stress = request.form["stress"]
        doctor_notes = request.form["doctor_notes"]

        ai_conditions, ai_medicines = ai_engine(bp, sugar, sleep, stress)

        file = request.files.get("report")
        if file and file.filename:
            file.save(os.path.join(UPLOAD_FOLDER, file.filename))
            report_info.append("Medical report uploaded: " + file.filename)

        record = {
            "date": str(datetime.now()),
            "doctor": doctor,
            "patient": patient,
            "phone": phone,
            "ai_conditions": ai_conditions,
            "ai_medicines": ai_medicines,
            "doctor_notes": doctor_notes,
            "final_decision": "Doctor Approved"
        }

        with open(DB_FILE) as f:
            data = json.load(f)
        data.append(record)
        with open(DB_FILE, "w") as f:
            json.dump(data, f, indent=2)

    return render_template_string("""
<h2>Velvoro Medical AI</h2>

<form method="post" enctype="multipart/form-data">

<h3>Doctor Details</h3>
Doctor Name: <input name="doctor" required><br><br>

<h3>Patient Details</h3>
Patient Name: <input name="patient" required><br><br>
Phone Number: <input name="phone" required><br><br>

BP: <input name="bp"><br><br>
Sugar: <input name="sugar"><br><br>

Sleep Proper?
<select name="sleep">
<option>Yes</option><option>No</option>
</select><br><br>

Stress?
<select name="stress">
<option>No</option><option>Yes</option>
</select><br><br>

Upload Report:
<input type="file" name="report"><br><br>

<h3>Doctor Notes (A–Z)</h3>
<textarea name="doctor_notes" rows="6" cols="60"
placeholder="Doctor can write full notes here..."></textarea><br><br>

<button type="submit">Run AI + Save Record</button>

</form>

<hr>

<h3>AI Draft (For Doctor Support)</h3>
<b>Conditions:</b>
<ul>{% for c in ai_conditions %}<li>{{c}}</li>{% endfor %}</ul>

<b>Medicines:</b>
<ul>{% for m in ai_medicines %}<li>{{m}}</li>{% endfor %}</ul>

<h3>Report Intelligence</h3>
<ul>{% for r in report_info %}<li>{{r}}</li>{% endfor %}</ul>

<p style="color:red;">
AI assisted system only. Final decision by registered doctor.
</p>
""",
ai_conditions=ai_conditions,
ai_medicines=ai_medicines,
report_info=report_info
)

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)