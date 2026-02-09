from fastapi import FastAPI, Request
import qrcode
import os
from fastapi.responses import FileResponse, PlainTextResponse
from fastapi.responses import HTMLResponse
from fastapi import Query
from fastapi.responses import RedirectResponse

app = FastAPI()

QR_DIR = "qrcodes"
os.makedirs(QR_DIR, exist_ok=True)
DEFAULT_TARGET_URL = "https://qr-scanner-lb6j.onrender.com"

@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    accept = request.headers.get("accept", "")

    # Postman / CLI tools → TEXT
    if "text/plain" in accept:
        return PlainTextResponse(
            "QR Scanner API is running.\n"
            "Use /qr to generate default QR.\n"
            "Use /qr/page to view QR."
        )
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
        <title>QR Scanner Service</title>

        <style>
            * {
                box-sizing: border-box;
                margin: 0;
                padding: 0;
                font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
            }

            body {
                min-height: 100vh;
                background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
                color: #fff;
            }

            .container {
                max-width: 420px;
                width: 100%;
                background: rgba(255, 255, 255, 0.08);
                backdrop-filter: blur(12px);
                border-radius: 18px;
                padding: 35px 30px;
                text-align: center;
                box-shadow: 0 25px 45px rgba(0, 0, 0, 0.4);
                animation: fadeIn 0.6s ease-in-out;
            }

            @keyframes fadeIn {
                from {
                    opacity: 0;
                    transform: translateY(20px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }

            h1 {
                font-size: 26px;
                margin-bottom: 12px;
            }

            p {
                font-size: 15px;
                color: #ddd;
                margin-bottom: 28px;
                line-height: 1.5;
            }

            .actions {
                display: flex;
                flex-direction: column;
                gap: 14px;
            }

            .form-input {
                display: flex;
                flex-direction: column;
                gap: 14px;
                margin-top: 10px;
            }

            /* URL input */
            .form-input input {
                width: 100%;
                padding: 14px 16px;
                border-radius: 12px;
                border: none;
                outline: none;
                font-size: 15px;
                background: rgba(255, 255, 255, 0.9);
                color: #333;
                transition: box-shadow 0.2s ease, transform 0.1s ease;
            }

            @media (max-width: 480px) {
                .form-input input {
                    padding: 16px;
                    font-size: 14px;
                }
            }

            .btn {
                display: inline-block;
                padding: 14px 26px;
                background: linear-gradient(135deg, #00c6ff, #0072ff);
                color: #fff;
                text-decoration: none;
                font-weight: 600;
                border-radius: 30px;
                transition: transform 0.2s ease, box-shadow 0.2s ease;
                box-shadow: 0 10px 25px rgba(0, 114, 255, 0.4);
            }

            @media (max-width: 480px) {
                .btn {
                    font-size: 15px;
                    padding: 16px 20px;
                    margin-bottom: 10px;
                    max-width: 100%;
                    border-radius: 24px;
                }
            }

            @media (max-width: 768px) {
                .btn {
                    font-size: 16px;
                    padding: 15px 24px;
                    max-width: 100%;
                }
            }

            .btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 15px 30px rgba(0, 114, 255, 0.6);
            }

            .btn.secondary {
                background: linear-gradient(135deg, #43cea2, #185a9d);
                box-shadow: 0 10px 25px rgba(24, 90, 157, 0.4);
            }

            .btn.secondary:hover {
                box-shadow: 0 15px 30px rgba(24, 90, 157, 0.6);
            }

            .footer {
                margin-top: 30px;
                font-size: 12px;
                color: #aaa;
            }
        </style>
    </head>

    <body>
        <div class="container">
            <h1>QR Scanner Service</h1>
            <p>
                Generate and scan QR codes that redirect users
                to public URLs using a FastAPI backend.
            </p>

           <div class="actions">
                <form action="/qr/page" method="get" class="form-input">
                    <input 
                        type="url" 
                        name="url" 
                        placeholder="https://example.com (optional)" 
                    />
                    <button type="submit" class="btn">Generate QR</button>
                </form>

                <!-- Generate QR (default target URL) -->
                <a href="/qr" class="btn">Generate Default QR</a>
            </div>


            <div class="footer">
                Powered by FastAPI • Public QR Redirect System
            </div>
        </div>
    </body>
    </html>
    """

@app.get("/qr")
def generate_default_qr():
    target_url = DEFAULT_TARGET_URL

    qr_path = f"{QR_DIR}/root_qr.png"
    qr = qrcode.make(target_url)
    qr.save(qr_path)

    # 🔁 Redirect directly to QR page
    return RedirectResponse(url="/qr/page")


@app.get("/qr/view")
def view_qr():
    return FileResponse("qrcodes/root_qr.png", media_type="image/png")

@app.get("/qr/page", response_class=HTMLResponse)
def qr_page(url: str | None = Query(default=None)):

    final_url = url if url else DEFAULT_TARGET_URL

    qr_path = f"{QR_DIR}/root_qr.png"
    qr = qrcode.make(final_url)
    qr.save(qr_path)

    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
        <title>QR Scanner</title>

        <style>
            * {
                box-sizing: border-box;
                margin: 0;
                padding: 0;
                font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
            }

            body {
                min-height: 100vh;
                background: linear-gradient(135deg, #667eea, #764ba2);
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }

            .card {
                background: #ffffff;
                max-width: 380px;
                width: 100%;
                padding: 30px 25px;
                border-radius: 16px;
                text-align: center;
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
                animation: fadeIn 0.6s ease-in-out;
            }

            @keyframes fadeIn {
                from {
                    opacity: 0;
                    transform: translateY(20px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }

            .title {
                font-size: 24px;
                font-weight: 700;
                color: #333;
                margin-bottom: 10px;
            }

            .subtitle {
                font-size: 14px;
                color: #666;
                margin-bottom: 25px;
            }

            .qr-container {
                background: #f4f6f8;
                padding: 15px;
                border-radius: 12px;
                display: inline-block;
            }

            .qr-container img {
                width: 220px;
                height: 220px;
            }

            .info {
                margin-top: 20px;
                font-size: 14px;
                color: #555;
            }

            .info strong {
                color: #000;
            }

            .footer {
                margin-top: 25px;
                font-size: 12px;
                color: #888;
            }
        </style>
    </head>

    <body>
        <div class="card">
            <div class="title">Scan the QR Code</div>
            <div class="subtitle">
                Scan this code to open the public URL
            </div>

            <div class="qr-container">
                <img src="/qr/view" alt="QR Code" />
            </div>

            <div class="info">
                Scanning will redirect you to<br />
                <strong>the main application page</strong>
            </div>

            <div class="footer">
                Powered by FastAPI • QR Scanner Service
            </div>
        </div>
    </body>
    </html>
    """