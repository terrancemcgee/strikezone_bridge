from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

# Updated Google Script URL
GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz5T2LUgZTrywKg4xj25j0wnUNAwGdL_5F2liv3kujN_F4pSMOoAC3ojHFXOn-NnuFT/exec"

class Trade(BaseModel):
    symbol: str
    entry: float
    stopLoss: float
    takeProfits: list[float]
    confidence: int
    sentimentMix: str
    phase: str
    strategyNotes: str
    outcome: str

@app.post("/log")
async def log_trade(trade: Trade):
    trade_data = trade.dict()

    # Send to Google Sheets via Apps Script
    try:
        response = requests.post(GOOGLE_SCRIPT_URL, json=trade_data)
        response.raise_for_status()
        print("✅ Trade successfully sent to Google Sheet:", trade_data)
        return {"status": "success", "received": trade_data}
    except Exception as e:
        print("❌ Error sending to Google Sheet:", e)
        return {"status": "error", "message": str(e)}
