# Wazuh SIEM + AI-Assisted SOC Analyst

A cybersecurity lab project combining **Wazuh SIEM** with a locally hosted **Llama 3.1:8b large language model through Ollama** to automate security alert analysis and assist with SOC investigation workflows.

## Project Overview

This project demonstrates an end-to-end security monitoring and AI-assisted alert analysis workflow.

Wazuh serves as the SIEM platform responsible for collecting and presenting security telemetry and alerts. A custom Python-based SOC analyst application then processes alert data and uses a locally hosted LLM to analyze security events.

The AI analyst evaluates each alert and produces structured security assessments containing:

* Severity
* Confidence score
* Attack type
* MITRE ATT&CK mapping
* Explanation
* Recommended actions

The project also applies automated SOC decision logic based on alert severity and AI confidence, helping prioritize which events should receive immediate escalation, analyst review, validation, or routine logging.

## Architecture

```text
Wazuh SIEM
     │
     │ Security Alerts
     ▼
alerts.json
     │
     ▼
Python SOC Analyst
     │
     ├── Alert Deduplication
     │
     ├── Llama 3.1:8b Analysis
     │
     ├── Severity Assessment
     │
     ├── Confidence Evaluation
     │
     ├── MITRE ATT&CK Mapping
     │
     └── SOC Action Determination
     │
     ▼
soc_report.json
```

The `watch_alerts.py` monitoring script can continuously watch the alert data and automatically initiate analysis when new alert information is detected.

## Key Features

### Wazuh SIEM Monitoring

The project uses Wazuh to provide centralized security monitoring and investigation capabilities, including:

* Security event collection
* Alert monitoring
* Severity-based event classification
* Vulnerability/security event visibility
* MITRE ATT&CK visibility
* Alert investigation and event context

### Local AI Security Analysis

The custom Python application uses **Ollama** to run **Llama 3.1:8b locally**.

The model receives structured SIEM alert information and returns a standardized JSON security assessment.

Example output structure:

```json
{
  "severity": "High",
  "confidence": 92,
  "attack_type": "Credential Access",
  "mitre_attack": "T1110",
  "explanation": "Multiple failed authentication attempts may indicate a password guessing attack.",
  "recommended_actions": [
    "Review authentication logs",
    "Investigate source IP",
    "Validate affected account activity"
  ]
}
```

### Automated SOC Decision Logic

The application converts AI-generated severity and confidence information into an operational response category.

Possible outcomes include:

* `IMMEDIATE ESCALATION`
* `ANALYST REVIEW REQUIRED`
* `VALIDATE BEFORE ESCALATION`
* `QUEUE FOR REVIEW`
* `LOG ONLY`

This demonstrates how AI output can be incorporated into a structured security operations workflow rather than simply generating unrestricted natural-language responses.

### Alert Deduplication

The application generates a fingerprint for each alert using key event information:

```text
rule | source IP | timestamp
```

Previously processed alerts are stored separately so that the same event is not repeatedly analyzed.

### Automated Monitoring

`watch_alerts.py` monitors the alert data source for changes.

When new alert data is detected, the monitoring process automatically launches the SOC analysis workflow.

## Technologies Used

* Python
* Wazuh
* Ollama
* Llama 3.1:8b
* JSON
* MITRE ATT&CK
* Ubuntu
* VirtualBox
* Git / GitHub

## Project Structure

```text
wazuh-ai-assisted-soc/
│
├── soc_ai.py
├── watch_alerts.py
├── requirements.txt
├── .gitignore
│
├── screenshots/
│
└── docs/
```

### Core Files

**`soc_ai.py`**

Main SOC analysis application responsible for:

* Loading alerts
* Deduplicating events
* Sending alerts to the local LLM
* Processing AI responses
* Determining SOC actions
* Generating security reports

**`watch_alerts.py`**

Automated monitoring script that watches for changes to incoming alert data and triggers the SOC analysis workflow.

**`requirements.txt`**

Contains the Python dependency required to run the application.

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd wazuh-ai-assisted-soc
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

Activate it on macOS/Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install and configure Ollama

Install Ollama and make sure the required model is available locally:

```bash
ollama pull llama3.1:8b
```

The application expects the model name:

```python
MODEL = "llama3.1:8b"
```

### 5. Provide alert data

The application expects an `alerts.json` file containing security alert data.

For portfolio/public repository purposes, real or sensitive alert data should not be committed to GitHub.

## Running the Project

### Run the SOC Analyst

```bash
python3 soc_ai.py
```

### Run the Automated Monitor

```bash
python3 watch_alerts.py
```

The monitoring process watches the alert data for changes and automatically launches the analysis workflow when new information is detected.

## Security and Privacy

This project was intentionally designed around a **local LLM architecture**.

Security alert data is processed locally through Ollama rather than being sent to a cloud-based AI API.

The repository also excludes sensitive and generated files through `.gitignore`, including:

* Environment variables
* Local alert data
* Generated reports
* Processed alert records
* Virtual environments
* Python cache files

## Screenshots

The `screenshots/` directory contains documentation of the project, including:

1. Wazuh Deployment Environment
2. Wazuh Security Events and MITRE ATT&CK Dashboard
3. Security Event Discovery
4. AI Analyst Initialization
5. AI-Powered Alert Analysis
6. Automated SOC Decision Logic
7. Automated Alert Processing Pipeline
8. Automated Alert Monitoring
9. AI Security Report Generation
10. Sample SIEM Alerts
11. Wazuh Alert Investigation and Event Context

## Skills Demonstrated

This project demonstrates practical experience with:

* SIEM deployment and monitoring
* Security event investigation
* Python automation
* Local LLM integration
* AI-assisted security analysis
* Alert prioritization
* MITRE ATT&CK analysis
* SOC workflow automation
* JSON data processing
* Alert deduplication
* Automated report generation
* Linux security tooling
* Virtualized security environments

## Project Goals

The primary goal of this project was to explore how locally hosted AI models can assist security operations by reducing repetitive alert-analysis tasks while maintaining analyst oversight.

Rather than replacing the SOC analyst, the system is designed to provide structured analysis and prioritization that can help an analyst determine which events deserve additional investigation.

## Future Development

Potential future improvements include:

* Direct Wazuh API integration
* Automated ingestion of live Wazuh alerts
* Expanded MITRE ATT&CK correlation
* Additional alert enrichment
* Improved confidence calibration
* Analyst feedback mechanisms
* Web-based SOC analyst dashboard
* Additional local LLM models for comparison
* Automated case/ticket creation

## Author

**Bradley Lueking**

Cybersecurity | GRC | Security Operations | AI-Assisted Security

This project was developed as part of a hands-on cybersecurity and AI portfolio demonstrating practical application of security monitoring, automation, and locally hosted artificial intelligence.
