from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf
import pandas as pd
import numpy as np

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Full 222 F&O Stock Symbol List from uploaded file
FO_SYMBOLS = [
    '360ONE.NS', 'ABB.NS', 'ADANIENSOL.NS', 'ADANIENT.NS', 'ADANIGREEN.NS', 'ADANIPORTS.NS', 'ADANIPOWER.NS', 'ABCAPITAL.NS', 
    'ALKEM.NS', 'AMBER.NS', 'AMBUJACEM.NS', 'ANANDRATHI.NS', 'ANGELONE.NS', 'APLAPOLLO.NS', 'APOLLOHOSP.NS', 'ASHOKLEY.NS', 
    'ASIANPAINT.NS', 'ASTRAL.NS', 'ATHERENERG.NS', 'AUBANK.NS', 'AUROPHARMA.NS', 'DMART.NS', 'AXISBANK.NS', 'BAJAJ-AUTO.NS', 
    'BAJFINANCE.NS', 'BAJAJFINSV.NS', 'BAJAJHLDNG.NS', 'BANDHANBNK.NS', 'BANKBARODA.NS', 'BANKINDIA.NS', 'MAHABANK.NS', 
    'BDL.NS', 'BEL.NS', 'BHARATFORG.NS', 'BPCL.NS', 'BHARTIARTL.NS', 'BHEL.NS', 'BIOCON.NS', 'BLUESTARCO.NS', 'BOSCHLTD.NS', 
    'BRITANNIA.NS', 'BSE.NS', 'CANBK.NS', 'CDSL.NS', 'CGPOWER.NS', 'CHOLAFIN.NS', 'CIPLA.NS', 'COALINDIA.NS', 'COCHINSHIP.NS', 
    'COFORGE.NS', 'COLPAL.NS', 'CAMS.NS', 'CONCOR.NS', 'CROMPTON.NS', 'CUMMINSIND.NS', 'DABUR.NS', 'DELHIVERY.NS', 
    'DIVISLAB.NS', 'DIXON.NS', 'DLF.NS', 'DRREDDY.NS', 'EICHERMOT.NS', 'ETERNAL.NS', 'FEDERALBNK.NS', 'FORCEMOT.NS', 
    'FORTIS.NS', 'NYKAA.NS', 'GAIL.NS', 'GVT&D.NS', 'GLENMARK.NS', 'GMRAIRPORT.NS', 'GODFRYPHLP.NS', 'GODREJCP.NS', 
    'GODREJPROP.NS', 'GRASIM.NS', 'HAVELLS.NS', 'HCLTECH.NS', 'HDFCAMC.NS', 'HDFCBANK.NS', 'HDFCLIFE.NS', 'HEROMOTOCO.NS', 
    'HINDALCO.NS', 'HAL.NS', 'HINDPETRO.NS', 'HINDUNILVR.NS', 'HINDZINC.NS', 'POWERINDIA.NS', 'HYUNDAI.NS', 'ICICIBANK.NS', 
    'ICICILIFE.NS', 'ICICIGI.NS', 'IDFCFIRSTB.NS', 'INDIANB.NS', 'IEX.NS', 'IOC.NS', 'IRFC.NS', 'IREDA.NS', 'INDUSTOWER.NS', 
    'INDUSINDBK.NS', 'NAUKRI.NS', 'INFY.NS', 'INOXWIND.NS', 'INDIGO.NS', 'ITC.NS', 'JINDALSTEL.NS', 'JIOFIN.NS', 
    'JSWENERGY.NS', 'JSWSTEEL.NS', 'JUBLFOOD.NS', 'KALYANKJIL.NS', 'KAYNES.NS', 'KEI.NS', 'KFINTECH.NS', 'KOTAKBANK.NS', 
    'KPITTECH.NS', 'LTF.NS', 'LT.NS', 'LAURUSLABS.NS', 'LICHSGFIN.NS', 'LICI.NS', 'LODHA.NS', 'LTM.NS', 'LUPIN.NS', 
    'M&M.NS', 'MANAPPURAM.NS', 'MANKIND.NS', 'MARICO.NS', 'MARUTI.NS', 'MFSL.NS', 'MAXHEALTH.NS', 'MAZDOCK.NS', 
    'MOTILALOFS.NS', 'MPHASIS.NS', 'MCX.NS', 'MUTHOOTFIN.NS', 'NATIONALUM.NS', 'NBCC.NS', 'NESTLEIND.NS', 'NHPC.NS', 
    'NAM-INDIA.NS', 'NMDC.NS', 'NTPC.NS', 'OBEROIRLTY.NS', 'ONGC.NS', 'OIL.NS', 'PAYTM.NS', 'OFSS.NS', 'PAGEIND.NS', 
    'PATANJALI.NS', 'POLICYBZR.NS', 'PERSISTENT.NS', 'PETRONET.NS', 'PGEL.NS', 'PIIND.NS', 'PIDILITIND.NS', 'PNBHOUSING.NS', 
    'POLYCAB.NS', 'PFC.NS', 'POWERGRID.NS', 'PREMIERENE.NS', 'PRESTIGE.NS', 'PNB.NS', 'RADICO.NS', 'RVNL.NS', 'RBLBANK.NS', 
    'RECLTD.NS', 'RELIANCE.NS', 'SAGILITY.NS', 'MOTHERSON.NS', 'SBICARD.NS', 'SBILIFE.NS', 'SHREECEM.NS', 'SHRIRAMFIN.NS', 
    'ENRIN.NS', 'SIEMENS.NS', 'SOLARINDS.NS', 'SONACOMS.NS', 'SRF.NS', 'SBIN.NS', 'SAIL.NS', 'SUNPHARMA.NS', 'SUPREMEIND.NS', 
    'SUZLON.NS', 'SWIGGY.NS', 'TCS.NS', 'TATACONSUM.NS', 'TATAELXSI.NS', 'TMPV.NS', 'TATAPOWER.NS', 'TATASTEEL.NS', 
    'TECHM.NS', 'INDHOTEL.NS', 'PHOENIXLTD.NS', 'TITAN.NS', 'TORNTPHARM.NS', 'TRENT.NS', 'TIINDIA.NS', 'TVSMOTOR.NS', 
    'UJJIVANSFB.NS', 'ULTRACEMCO.NS', 'UNIONBANK.NS', 'UNITDSPR.NS', 'UNOMINDA.NS', 'UPL.NS', 'VBL.NS', 'VEDL.NS', 
    'VMM.NS', 'IDEA.NS', 'VOLTAS.NS', 'WAAREEENER.NS', 'WIPRO.NS', 'YESBANK.NS', 'ZYDUSLIFE.NS'
]

# Indicator Helper Functions
def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    val = float(100 - (100 / (1 + rs)).iloc[-1])
    return round(val, 2) if not np.isnan(val) else 0.0

def calculate_mfi(df, period=14):
    tp = (df['High'] + df['Low'] + df['Close']) / 3
    rmf = tp * df['Volume']
    pmf = rmf.where(tp > tp.shift(1), 0).rolling(window=period).sum()
    nmf = rmf.where(tp < tp.shift(1), 0).rolling(window=period).sum()
    mfi = 100 - (100 / (1 + (pmf / nmf)))
    val = float(mfi.iloc[-1])
    return round(val, 2) if not np.isnan(val) else 0.0

def calculate_williams_r(df, period=14):
    hh = df['High'].rolling(window=period).max()
    ll = df['Low'].rolling(window=period).min()
    denom = hh.iloc[-1] - ll.iloc[-1]
    wr = -100 * ((hh.iloc[-1] - df['Close'].iloc[-1]) / (denom if denom != 0 else 1))
    val = float(wr)
    return round(val, 2) if not np.isnan(val) else 0.0

@app.get("/")
def home():
    return {"status": "RBS Screener Backend running with 222 F&O stocks"}

# ------------------------------------------------------------------
# DEDICATED ENDPOINT: ORIGINAL UNTOUCHED RBS SCREENER
# ------------------------------------------------------------------
@app.get("/api/screener")
def get_rbs_screener():
    try:
        tickers_str = " ".join(FO_SYMBOLS)
        data = yf.download(tickers_str, period="5d", interval="1d", group_by="ticker", threads=True, progress=False)

        results = []
        for ticker in FO_SYMBOLS:
            try:
                df = data[ticker] if len(FO_SYMBOLS) > 1 else data
                df = df.dropna()

                if len(df) < 2:
                    continue

                current_price = float(df['Close'].iloc[-1])
                prev_close = float(df['Close'].iloc[-2])
                change_pct = round(((current_price - prev_close) / prev_close) * 100, 2)
                volume = int(df['Volume'].iloc[-1])

                # Core RBS Math (Unchanged)
                high = float(df['High'].iloc[-1])
                low = float(df['Low'].iloc[-1])
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
            except Exception:
                continue

        results.sort(key=lambda x: x["rbs_ratio"], reverse=True)
        return {"symbols": results}

    except Exception as e:
        return {"error": str(e), "symbols": []}

# ------------------------------------------------------------------
# DEDICATED ENDPOINT: TECHNICAL MATRIX (RSI / MFI / Williams %R)
# ------------------------------------------------------------------
@app.get("/api/indicators")
def get_indicators_screener():
    try:
        tickers_str = " ".join(FO_SYMBOLS)
        data = yf.download(tickers_str, period="1mo", interval="1d", group_by="ticker", threads=True, progress=False)

        results = []
        for ticker in FO_SYMBOLS:
            try:
                df = data[ticker] if len(FO_SYMBOLS) > 1 else data
                df = df.dropna()

                if len(df) < 20:
                    continue

                current_price = float(df['Close'].iloc[-1])
                prev_close = float(df['Close'].iloc[-2])
                change_pct = round(((current_price - prev_close) / prev_close) * 100, 2)

                rsi = calculate_rsi(df['Close'])
                mfi = calculate_mfi(df)
                williams_r = calculate_williams_r(df)

                signal = "Neutral"
                if rsi > 60 and mfi > 50 and williams_r > -20:
                    signal = "Bullish Momentum"
                elif rsi < 40 and mfi < 40 and williams_r < -80:
                    signal = "Bearish Momentum"

                results.append({
                    "symbol": ticker.replace(".NS", ""),
                    "live_price": round(current_price, 2),
                    "change_pct": change_pct,
                    "rsi": rsi,
                    "mfi": mfi,
                    "williams_r": williams_r,
                    "signal": signal
                })
            except Exception:
                continue

        results.sort(key=lambda x: x["rsi"], reverse=True)
        return {"symbols": results}

    except Exception as e:
        return {"error": str(e), "symbols": []}
