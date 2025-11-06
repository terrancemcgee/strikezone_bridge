from fastapi import FastAPI, Request
import requests, json
from datetime import datetime

app = FastAPI()
GOOGLE_SHEET_WEBAPP = "https://script.google.com/macros/s/AKfycbwVmzzAmLsHNHkV7tdNqH3WlZ5yyNuzZF8nxwX-q4fbh5mK2o7rASpqwEZD3XEZcLVR/exec"

@app.post("/log")
async def log_to_google(request: Request):
    try:
        data = await request.json()
        required = {"symbol", "entry", "stopLoss", "takeProfits"}
        if not required.issubset(data.keys()):
            return {"status": "error", "message": f"Missing fields: {required - data.keys()}"}
        data["timestamp"] = datetime.utcnow().isoformat()
        resp = requests.post(GOOGLE_SHEET_WEBAPP, json=data, timeout=10)
        return {
            "status": "success" if resp.status_code == 200 else "fail",
            "google_response": resp.text
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
