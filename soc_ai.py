from ollama import chat
import json
from pathlib import Path

MODEL = "llama3.1:8b"

SEVERITY_SCORES = {
    "Low": 1,
    "Medium": 2,
    "High": 3,
    "Critical": 4
}

PROJECT_DIR = Path(__file__).parent

ALERT_FILE = PROJECT_DIR / "alerts.json"
PROCESSED_FILE = PROJECT_DIR / "processed_alerts.json"

def load_alerts():
    with open(ALERT_FILE, "r") as f:
        return json.load(f)

def load_processed():
    try:
        with open(PROCESSED_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_processed(processed):
    with open(PROCESSED_FILE, "w") as f:
        json.dump(processed, f, indent=2)


def get_alert_fingerprint(alert):
    return f"{alert.get('rule','')}|{alert.get('srcip','')}|{alert.get('timestamp','')}"

def analyze_alert(alert):
    prompt = f"""
You are a SOC analyst.

Analyze this SIEM alert and return ONLY valid JSON.

Alert:
{json.dumps(alert, indent=2)}

Return format:
{{
  "severity": "Low|Medium|High|Critical",
  "confidence": 0,
  "attack_type": "",
  "mitre_attack": "",
  "explanation": "",
  "recommended_actions": []
}}

Rules:
- confidence must be an integer from 0 to 100
- Output ONLY JSON
- No markdown
- No extra text
"""

    response = chat(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    return json.loads(response["message"]["content"])

def determine_action(severity, confidence):
    score = SEVERITY_SCORES.get(severity, 0)

    if score >= 4:
        return "IMMEDIATE ESCALATION"

    elif score >= 3:
        if confidence >= 80:
            return "ANALYST REVIEW REQUIRED"
        else:
            return "VALIDATE BEFORE ESCALATION"

    elif score >= 2:
        return "QUEUE FOR REVIEW"

    else:
        return "LOG ONLY"

def main():
    alerts = load_alerts()
    processed = load_processed()

    print("\n===== SOC AI ANALYSIS START =====\n")

    report_output = []

    for i, alert in enumerate(alerts, start=1):

        fingerprint = get_alert_fingerprint(alert)

        if fingerprint in processed:
            continue

        print(f"\n--- ALERT {i} ---\n")

        result = analyze_alert(alert)

        severity = result.get("severity", "Low").title()
        confidence = int(result.get("confidence", 50))

        result["severity"] = severity
        result["confidence"] = confidence

        action = determine_action(
            severity,
            confidence
        )

        print(json.dumps(result, indent=2))
        print(f"\nCONFIDENCE: {confidence}%")
        print(f"SOC ACTION: {action}\n")

        report_output.append({
            "alert_id": i,
            "input": alert,
            "analysis": result,
            "soc_action": action
        })

        processed.append(fingerprint)

    # Write full report to file
    report_path = Path.home() / "soc-ai-data" / "soc_report.json"

    with open(report_path, "w") as f:
        json.dump(report_output, f, indent=2)

    save_processed(processed)
    print("\n===== SOC AI ANALYSIS COMPLETE =====")
    print(f"\nReport saved to: {report_path}\n")


if __name__ == "__main__":
    main()
