from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf
import pandas as pd

app = FastAPI()

# Allow screener frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Your list of NSE symbols
SYMBOLS = [
    "BAJFINANCE.NS", "TCS.NS", "BHEL.NS", "ITC.NS", 
    "ASIANPAINT.NS", "ASTRAL.NS", "RECLTD.NS", "GODREJPROP.NS"
]

@app.get("/api/screener")
def get_screener_data():
    results = []
    
    # Batch download quotes from Yahoo Finance
    tickers = yf.Tickers(" ".join(SYMBOLS))
    
    for symbol in SYMBOLS:
        try:
            ticker = tickers.tickers[symbol]
            hist = ticker.history(period="2d") # Fetch last 2 days for OHLC & breakouts
            
            if len(hist) < 2:
                continue
                
            prev_day = hist.iloc[-2]
            curr_day = hist.iloc[-1]
            
            close = curr_day["Close"]
            high = curr_day["High"]
            low = curr_day["Low"]
            volume = curr_day["Volume"]
            prev_high = prev_day["High"]
            prev_low = prev_day["Low"]
            
            # --- RBS Formula Calculations ---
            day_range = high - low if high != low else 1
            buyer_factor = (close - low) / day_range
            seller_factor = (high - close) / day_range
            
            buyer_strength = volume * buyer_factor
            seller_strength = volume * seller_factor
            combined_score = buyer_strength - seller_strength
            
            rbs_ratio = (buyer_strength / seller_strength) if seller_strength > 0 else 1.0
            
            # Breakout / Breakdown Signal
            if close > prev_high:
                status = "Breakout Above"
            elif close < prev_low:
                status = "Breakdown Below"
            else:
                status = "Inside Range"
                
            results.append({
                "symbol": symbol.replace(".NS", ""),
                "live_price": round(close, 2),
                "change_pct": round(((close - prev_day["Close"]) / prev_day["Close"]) * 100, 2),
                "volume": int(volume),
                "buyer_strength": round(buyer_strength, 2),
                "seller_strength": round(seller_strength, 2),
                "combined_score": round(combined_score, 2),
                "rbs_ratio": round(rbs_ratio, 2),
                "status": status
            })
        except Exception as e:
            continue
            
    return {"symbols": results}
