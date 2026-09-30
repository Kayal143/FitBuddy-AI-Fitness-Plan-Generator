FITBUDDY - DEADLINE SAFE DEMO

1. Open this folder in VS Code.
2. Open Terminal in the FitBuddy folder.
3. Create environment:
   python -m venv .venv

4. Activate on Windows:
   .venv\Scripts\activate

5. Install:
   pip install -r requirements.txt

6. Run:
   uvicorn app.main:app --reload

7. Open:
   http://127.0.0.1:8000

This version intentionally does NOT require Gemini/API keys or a database.
It gives a working 7-day fitness-plan demo and an update-plan flow.
