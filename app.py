from flask import Flask, request, redirect, url_for, session, render_template_string
import csv, os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "velvoro_secret_key"

DATA_FILE = "doctor_records.csv"

HEADERS = [
    "DateTime","DoctorID","DoctorName",
    "PatientName","Phone","Age",
    "BP","Sugar","Stress",
    "Conditions","AI_Advice","DoctorNotes"
]

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow(HEADERS)

# ---------- LOGIN ----------
LOGIN_HTML = """
<h2>Velvoro Medical AI – Doctor Login</h2>
<form method="post">
Doctor ID:<br>
<input name="doctor_id" required><br><br>
PIN:<br>
<input type="password" name="pin" required><br><br>
<button type="submit">Login</button>
</form>
<p style="color:red;">{{error}}</p>
"""

@app.route("/", methods=["GET","POST"])
def login():
    error=""
    if request.method=="POST":
        if request.form["doctor_id"]=="doctor1" and request.form["pin"]=="1234":
            session["doctor_id"]=request.form["doctor_id"]
            return redirect("/app")
        else:
            error="Invalid Login"
    return render_template_string(LOGIN_HTML, error=error)

# ---------- MAIN APP ----------
APP_HTML = """
<h2>Velvoro Medical AI</h2>
<b>Doctor ID:</b> {{session['doctor_id']}} <br><br>

<form method="post">
Doctor Name:<br>
<input name="doctor_name" required><br><br>

Patient Name:<br>
<input name="patient_name" required><br><br>

Phone Number:<br>
<input name="phone"><br><br>

Age:<br>
<input name="age"><br><br>

BP (e.g 120/80):<br>
<input name="bp"><br><br>

Sugar:<br>
<input name="sugar"><br><br>

Stress:<br>
<select name="stress">
<option>No</option>
<option>Yes</option>
</select><br><br>

Doctor Notes:<br>
<textarea name="doctor_notes"></textarea><br><br>

<button type="submit">Run AI & Save</button>
</form>

{% if result %}
<hr>
<h3>AI Analysis Result</h3>
<b>Conditions:</b>
<ul>
{% for c in result.conditions %}
<li>{{c}}</li>
{% endfor %}
</ul>

<b>AI Suggested Advice:</b>
<ul>
{% for a in result.advice %}
<li>{{a}}</li>
{% endfor %}
</ul>

<p style="color:red;">
⚠ AI assisted system. Final diagnosis & prescription by registered doctor only.
</p>
{% endif %}

<br><a href="/logout">Logout</a>
"""

@app.route("/app", methods=["GET","POST"])
def app_page():
    if "doctor_id" not in session:
        return redirect("/")

    result=None

    if request.method=="POST":
        doctor_name=request.form["doctor_name"]
        patient=request.form["patient_name"]
        phone=request.form["phone"]
        age=request.form["age"]
        bp=request.form["bp"]
        sugar=request.form["sugar"]
        stress=request.form["stress"]
        notes=request.form["doctor_notes"]

        conditions=[]
        advice=[]

        if bp and bp!="120/80":
            conditions.append("High BP")
            advice.append("Reduce salt, monitor BP")

        if sugar and int(sugar)>140:
            conditions.append("High Sugar")
            advice.append("Sugar control diet & medication (doctor decision)")

        if stress=="Yes":
            conditions.append("Stress Risk")
            advice.append("Yoga, meditation, sleep correction")

        if not conditions:
            conditions.append("Vitals Normal")
            advice.append("Continue healthy lifestyle")

        with open(DATA_FILE,"a",newline="",encoding="utf-8") as f:
            csv.writer(f).writerow([
                datetime.now(),session["doctor_id"],doctor_name,
                patient,phone,age,bp,sugar,stress,
                ", ".join(conditions),
                ", ".join(advice),
                notes
            ])

        class R: pass
        result=R()
        result.conditions=conditions
        result.advice=advice

    return render_template_string(APP_HTML, result=result)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__=="__main__":
    app.run(debug=True)
