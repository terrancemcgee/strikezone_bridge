from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

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
    print("✅ Trade received:", trade.dict())
    return {"status": "success", "received": trade.dict()} 
