# kavach: Compliance & Hygiene Checker (Web UI)

A Flask-based web tool to automate domain checks for Google MCM onboarding.

## Setup

1. Clone the repo:
   ```bash
   git clone https://github.com/yourorg/kavach.git
   cd kavach
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   playwright install
   ```

## Usage

```bash
python app.py
```

Open your browser at http://localhost:5000, enter a domain, and view the JSON report.
```