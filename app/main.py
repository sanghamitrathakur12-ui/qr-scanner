from fastapi import FastAPI
import qrcode
import os
from fastapi.responses import FileResponse
from fastapi.responses import HTMLResponse

app = FastAPI()

QR_DIR = "qrcodes"
os.makedirs(QR_DIR, exist_ok=True)

@app.get("/")
def root():
    return {"status": "API is running"}

@app.get("/qr")
def generate_qr():
    target_url = "https://qr-scanner-lb6j.onrender.com"
    qr_path = f"{QR_DIR}/root_qr.png"

    qr = qrcode.make(target_url)
    qr.save(qr_path)

    return {
        "message": "QR code generated",
        "scan_url": target_url,
        "qr_image": qr_path
    }

@app.get("/qr/view")
def view_qr():
    return FileResponse("qrcodes/root_qr.png", media_type="image/png")

@app.get("/qr/page", response_class=HTMLResponse)
def qr_page():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>QR Code</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: #f4f6f8;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }
            .card {
                background: white;
                padding: 30px;
                border-radius: 12px;
                text-align: center;
                box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            }
            img {
                width: 250px;
                margin-top: 20px;
            }
        </style>
    </head>
    <body>
        <div class="card">
            <h2>Scan the QR Code</h2>
            <p>This QR redirects to the API root endpoint</p>
            <img src="/qr/view" alt="QR Code">
            <p><small>Scanning opens https://qr-scanner.onrender.com/</small></p>
        </div>
    </body>
    </html>
    """
