# APIIT Bot

A small Flask chatbot demo with an HTML/CSS/JavaScript front end and a rule-based Python response engine.

## Run locally

1. Install Python 3.10 or later.
2. Open a terminal in this folder and create a virtual environment:

   ```powershell
   py -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

3. Install the packages:

   ```powershell
   pip install -r requirements.txt
   ```

4. Start the app:

   ```powershell
   python app.py
   ```

5. Open http://127.0.0.1:5000 in your browser.

## Deploy on Render

Create a **Web Service** connected to this GitHub repository. Use:

- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn app:app`

The Flask service serves both the page and `/chat`, so the browser does not need an ngrok URL or an ngrok token.

## Project files

- `app.py` — Flask routes and chatbot response rules.
- `static/index.html` — chatbot front end.
- `static/apiit_logo_png.png` — logo image used by the page.

## Note

This is an educational demo. Its admissions answers were taken from the project notebook and may be outdated or incomplete. Confirm fees, entry requirements, intake dates, and other official details with APIIT before relying on them.
