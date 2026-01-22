def velvoro_engine(data):
    conditions = []
    confidences = []
    protocols = []
    medicines = []
    tests = []

    age = int(data.get("age", 0))
    symptoms = data.get("symptoms", "").lower()
    sbp = int(data.get("sbp", 0)) if data.get("sbp") else 0
    dbp = int(data.get("dbp", 0)) if data.get("dbp") else 0

    if sbp >= 140 or dbp >= 90:
        conditions.append("High Blood Pressure Risk")
        confidences.append("80%")
        protocols.append("Hypertension management protocol")
        medicines.append("Antihypertensive category")
        tests.append("BP monitoring")

    if age >= 45:
        conditions.append("Age-related cardiac risk")
        confidences.append("75%")
        protocols.append("Cardiac screening protocol")
        medicines.append("Cardiac support category")
        tests.append("ECG")

    if "chest pain" in symptoms:
        conditions.append("Possible cardiac symptoms")
        confidences.append("70%")
        protocols.append("Immediate cardiac evaluation")

    return {
        "conditions": ", ".join(conditions),
        "confidences": ", ".join(confidences),
        "protocols": ", ".join(protocols),
        "medicines": ", ".join(set(medicines)),
        "tests": ", ".join(set(tests))
    }