# Logistics MVP

Minimal logistics system - one vertical slice at a time.

## Setup (Windows)

```powershell
cd "c:\logistics projects\logistics_mvp"
pip install -r requirements.txt
uvicorn src.interfaces.api:app --reload
```

Open http://127.0.0.1:8000/docs
