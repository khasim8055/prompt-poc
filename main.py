from fastapi import FastAPI
from pydantic import BaseModel
import uuid

app = FastAPI(title="Prompt Distribution PoC")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/packs")
def packs():
    return [
        {"id": "pack-101", "title": "Marketing Prompts", "preview": "10 prompts for landing pages"},
        {"id": "pack-102", "title": "Job Search Prompts", "preview": "8 prompts for CV + cover letter"},
        {"id": "pack-103", "title": "Study Prompts", "preview": "12 prompts for summaries + quizzes"},
    ]

class BuyRequest(BaseModel):
    pack_id: str

@app.post("/buy")
def buy(req: BuyRequest):
    license_key = f"LIC-{uuid.uuid4().hex[:12].upper()}"
    return {"pack_id": req.pack_id, "license_key": license_key}

class RedeemRequest(BaseModel):
    license_key: str

@app.post("/redeem")
def redeem(req: RedeemRequest):
    # No DB in this PoC: just validate format
    ok = req.license_key.startswith("LIC-") and len(req.license_key) >= 10
    return {"valid": ok, "message": "access_granted" if ok else "invalid_key"}
