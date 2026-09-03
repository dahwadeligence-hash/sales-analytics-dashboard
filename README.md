# Sales Analytics Dashboard

This branch adds a Flask-based web dashboard and a separate input page backed by SQLite.

Quick start (VS Code):

1. Create a Python venv and install deps

```bash
python -m venv venv
# macOS / Linux
source venv/bin/activate
# Windows (PowerShell)
# .\venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

2. Run the app (it will initialize the SQLite DB from schema.sql if missing):

```bash
python app.py
```

3. Open the app in your browser:

- Dashboard: http://127.0.0.1:5000/dashboard
- Input page: http://127.0.0.1:5000/input

Files added on branch feature/dashboard
- app.py
- schema.sql
- requirements.txt
- templates/input.html
- templates/dashboard.html
- static/js/dashboard.js
- static/css/style.css
- .vscode/launch.json

If you want PostgreSQL or MySQL instead of SQLite, tell me and I will update app.py and provide connection settings and migration instructions.
