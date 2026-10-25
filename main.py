from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf

app = FastAPI()

# Enable CORS so your Vercel frontend can talk to Render
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sample liquid NSE symbols list to test your mobile screener
SYMBOLS = [
    "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", 
    "ICICIBANK.NS", "SBIN.NS", "BHARTIARTL.NS", "ITC.NS"
]

@app.get("/")
def home():
    return {"message": "RBS Screener Backend is running successfully!"}

@app.get("/api/screener")
def get_screener():
    results = []
    
    for ticker in SYMBOLS:
        try:
            stock = yf.Ticker(ticker)
            df = stock.history(period="5d")
            
            if df.empty or len(df) < 2:
                continue
                
            current_price = float(df['Close'].iloc[-1])
            prev_close = float(df['Close'].iloc[-2])
            change_pct = round(((current_price - prev_close) / prev_close) * 100, 2)
            volume = int(df['Volume'].iloc[-1])
            
            # Proprietary RBS (Buyer/Seller Strength) sample calculation logic
            high = float(df['High'].iloc[-1])
            low = float(df['Low'].iloc[-1])
            open_price = float(df['Open'].iloc[-1])
            
            buyer_strength = current_price - low
            seller_strength = high - current_price
            combined_score = round(buyer_strength - seller_strength, 2)
            
            rbs_ratio = round(buyer_strength / (seller_strength if seller_strength != 0 else 0.01), 2)
            
            status = "Neutral"
            if rbs_ratio > 1.5 and change_pct > 0:
                status = "Breakout Above"
            elif rbs_ratio < 0.8 and change_pct < 0:
                status = "Breakdown Below"

            results.append({
                "symbol": ticker.replace(".NS", ""),
                "live_price": round(current_price, 2),
                "change_pct": change_pct,
                "volume": volume,
                "combined_score": combined_score,
                "rbs_ratio": rbs_ratio,
                "status": status
            })
        except Exception as e:
            print(f"Error fetching {ticker}: {e}")
            
    return {"symbols": results}
