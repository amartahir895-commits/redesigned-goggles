from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse
import io
import qrcode
from textblob import TextBlob
import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # 1. Isay import karein

app = FastAPI()

# 2. Ye block poora copy karke 'app = FastAPI()' ke foran baad likhen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ... baaki aapka purana code niche rahega
app = FastAPI()

@app.get("/")
def home():
    return {"status": "Active", "message": "Smart Utility API is running!ammar op"}

# 1. Sentiment Analysis Tool
@app.get("/analyze-sentiment")
def analyze(text: str):
    analysis = TextBlob(text)
    sentiment = "Positive" if analysis.sentiment.polarity > 0 else "Negative" if analysis.sentiment.polarity < 0 else "Neutral"
    return {"original_text": text, "sentiment": sentiment, "score": analysis.sentiment.polarity}

# 2. QR Code Generator
@app.get("/generate-qr")
def generate_qr(data: str):
    img = qrcode.make(data)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")

# 3. Web Scraper (Extract Title/Description)
@app.get("/web-info")
def web_info(url: str):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string if soup.title else "No Title"
        return {"url": url, "title": title}
    except:
        return {"error": "Could not fetch website data"}
