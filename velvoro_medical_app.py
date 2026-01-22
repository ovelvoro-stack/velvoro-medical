from flask import Flask, request, redirect, url_for, session, render_template_string

app = Flask(__name__)
app.secret_key = "velvoro_secret_key"

# -----------------------------
# USERS (Demo – later DB)
# -----------------------------
USERS = {
    "DOC001": {"name": "Dr. Raju", "role": "doctor"},
    "STF001": {"name": "Office Staff", "role": "staff"}
}

# -----------------------------
# DISEASE MASTER LIST
# -----------------------------
DISEASES = [
    "BP",
    "Diabetes",
    "Heart Risk",
    "Thyroid",
    "Fever",
    "Chest Pain",
    "Kidney Risk",
    "Liver Risk",
    "General Weakness"
]

# -----------------------------
# LOGIN PAGE
# -----------------------------
LOGIN_HTML = """
<!doctype html>
<title>Velvoro Medical Login</title>
<h2>Velvoro Medical System</h2>
<form method="post">
  <input name="code" placeholder="Doctor / Staff Code" required><br><br>
  <button type="submit">Login</button>
</form>
"""

# -----------------------------
# DASHBOARD (CRM STYLE)
# -----------------------------
DASHBOARD_HTML = """
<!doctype html>
<title>Velvoro Medical Dashboard</title>

<h2>Velvoro Medical</h2>
<p>
Logged in as: <b>{{ user.name }}</b> ({{ user.role }}) |
<a href="/logout">Logout</a>
</p>

<hr>

{% if user.role == "doctor" %}
<h3>Doctor Dashboard</h3>
<ul>
  <li><a href="/patient">New Patient Entry</a></li>
  <li>AI Risk Review (Phase-2)</li>
</ul>
{% else %}
<h3>Staff Panel</h3>
<ul>
  <li><a href="/patient">Patient Entry</a></li>
  <li><i>Records hidden (Doctor only)</i></li>
</ul>
{% endif %}
"""

# -----------------------------
# PATIENT ENTRY
# -----------------------------
PATIENT_HTML = """
<!doctype html>
<title>Patient Entry</title>

<h2>Velvoro Medical – Patient Entry</h2>
<p>
Logged in: {{ user.name }} |
<a href="/dashboard">Back</a> |
<a href="/logout">Logout</a>
</p>

<form method="post">
<input name="name" placeholder="Patient Name" required><br>
<input name="age" placeholder="Age" required><br>
<input name="phone" placeholder="Phone" required><br>
<input name="area" placeholder="Area"><br><br>

<label>Diseases / Complaints</label><br>
<select name="diseases" multiple size="6">
{% for d in diseases %}
  <option value="{{ d }}">{{ d }}</option>
{% endfor %}
</select><br><br>

<button type="submit">Save Patient</button>
</form>
"""

# -----------------------------
# ROUTES
# -----------------------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        code = request.form.get("code")
        if code in USERS:
            session["user"] = USERS[code]
            return redirect("/dashboard")
    return render_template_string(LOGIN_HTML)


@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")
    return render_template_string(
        DASHBOARD_HTML,
        user=session["user"]
    )


@app.route("/patient", methods=["GET", "POST"])
def patient():
    if "user" not in session:
        return redirect("/")

    if request.method == "POST":
        # Here data will be saved later (DB / Excel)
        return redirect("/dashboard")

    return render_template_string(
        PATIENT_HTML,
        user=session["user"],
        diseases=DISEASES
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)