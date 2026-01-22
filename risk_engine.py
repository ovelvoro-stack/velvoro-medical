def risk_summary(face_result):
    risks = []
    if face_result["stress_risk"] == "High":
        risks.append("Stress indicators detected")

    return {
        "summary": ", ".join(risks),
        "action": "Doctor Review Required"
    }