from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import RedirectResponse
import validators
import qrcode
import os
import uuid

app = FastAPI()

QR_DIR = "qrcodes"
os.makedirs(QR_DIR, exist_ok=True)

url_store = {}

PUBLIC_BASE_URL = PUBLIC_BASE_URL = "https://your-app-name.onrender.com"  # later replace with domain

@app.get("/")
def root():
    return {"status": "API is running"}

@app.get("/analyze")
def analyze_and_generate_qr(url: str = Query(...)):

    if not validators.url(url):
        raise HTTPException(status_code=400, detail="Invalid URL")

    qr_id = str(uuid.uuid4())

    # store mapping
    url_store[qr_id] = url

    # QR will point to YOUR scan URL
    scan_url = f"{PUBLIC_BASE_URL}/scan/{qr_id}"

    qr_path = f"{QR_DIR}/{qr_id}.png"
    qr = qrcode.make(scan_url)
    qr.save(qr_path)

    return {
        "message": "QR generated",
        "scan_url": scan_url,
        "final_destination": url,
        "qr_id": qr_id,
        "qr_image": qr_path
    }

@app.get("/scan/{qr_id}")
def scan_qr(qr_id: str):

    if qr_id not in url_store:
        raise HTTPException(status_code=404, detail="Invalid QR")

    final_url = url_store[qr_id]
    return RedirectResponse(url=final_url)
