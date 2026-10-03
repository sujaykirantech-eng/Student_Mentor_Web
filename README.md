# Student Mentor — Web Version

A dark, student-facing Flask web interface around the existing Student Mentor diagnostic modules.

## Structure

```text
Student_Mentor_Web/
├── app.py
├── Main_v2.6_2.py
├── DoubtDiagnostic.py
├── DoubtDiagnostic_General.py
├── Class.py
├── Class10.py
├── Class11.py
├── Class12.py
├── Database.py
├── templates/
├── static/
├── requirements.txt
├── .env.example
├── .gitignore
└── run_windows.bat
```

## Run on Windows

```powershell
py -m pip install -r requirements.txt
py app.py
```

Open `http://127.0.0.1:5000/`.

## Logo and domain

The generated **Student Mentor Project** logo is included at `static/images/student-mentor-project-logo.png` and is used in the navbar, favicon and Open Graph metadata.

Set `STUDENT_MENTOR_DOMAIN` to the real public domain after deployment. The project currently uses `studentmentorproject.example` as a safe placeholder; it is not a registered/live domain. The application does not claim ownership of a domain.

## MySQL credentials — important

Real database credentials are **not stored in `Database.py` anymore**. The database layer reads:

```text
STUDENT_MENTOR_DB_HOST
STUDENT_MENTOR_DB_PORT
STUDENT_MENTOR_DB_USER
STUDENT_MENTOR_DB_PASSWORD
STUDENT_MENTOR_DB_NAME
```

Copy `.env.example` to `.env` for your own reference, or set the variables in PowerShell before starting the app. Do not commit `.env` to GitHub; `.gitignore` already excludes it.

Example PowerShell setup for a local MySQL installation:

```powershell
$env:STUDENT_MENTOR_DB_HOST="localhost"
$env:STUDENT_MENTOR_DB_PORT="3306"
$env:STUDENT_MENTOR_DB_USER="root"
$env:STUDENT_MENTOR_DB_PASSWORD="YOUR_PASSWORD"
$env:STUDENT_MENTOR_DB_NAME="student_mentor"
$env:STUDENT_MENTOR_SECRET="use-a-long-random-secret"
py app.py
```

The app can still render pages when MySQL is unavailable; database-backed history/persistence requires MySQL to be running and configured.

## GitHub safety

Before pushing this project, confirm there is no real password in tracked files. `.env` is ignored. Never commit a real database password, API key, or secret.
