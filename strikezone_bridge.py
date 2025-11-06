from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

# Your Google Apps Script Web App URL
GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbzqq06rNhz_-u2UbRUOgwgCR2DMZj4bfkZDGhROCvIvZIM1jzRQ0KiCM0D6VVMYh3GN/exec"

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

    # Send the data to Google Sheets via Apps Script
    response = requests.post(GOOGLE_SCRIPT_URL, json=trade_data)

    if response.status_code == 200:
        print("✅ Trade sent to Google Sheet successfully:", trade_data)
        return {"status": "success", "received": trade_data}
    else:
        print("❌ Failed to send trade:", response.text)
        return {"status": "error", "message": response.text}
