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

@app.get("/")
def home():
    return {"status": "Detailed RBS Screener Backend Active"}

@app.get("/api/screener")
def get_deep_rbs_screener():
    try:
        tickers_str = " ".join(FO_SYMBOLS)
        data = yf.download(tickers_str, period="5d", interval="1d", group_by="ticker", threads=True, progress=False)

        raw_list = []
        for ticker in FO_SYMBOLS:
            try:
                df = data[ticker] if len(FO_SYMBOLS) > 1 else data
                df = df.dropna()

                if len(df) < 2:
                    continue

                # Current Day OHLCV
                c_open = float(df['Open'].iloc[-1])
                c_high = float(df['High'].iloc[-1])
                c_low = float(df['Low'].iloc[-1])
                c_close = float(df['Close'].iloc[-1])
                c_vol = float(df['Volume'].iloc[-1])

                # Previous Day OHLCV
                p_open = float(df['Open'].iloc[-2])
                p_high = float(df['High'].iloc[-2])
                p_low = float(df['Low'].iloc[-2])
                p_close = float(df['Close'].iloc[-2])

                day_range = c_high - c_low
                prev_day_range = p_high - p_low

                # Buyer / Seller Ratios
                if day_range > 0:
                    bs = (c_close - c_low) / day_range
                    ss = (c_high - c_close) / day_range
                else:
                    bs = 0.5
                    ss = 0.5

                if prev_day_range > 0:
                    prev_bs = (p_close - p_low) / prev_day_range
                    prev_ss = (p_high - p_close) / prev_day_range
                    prev_r_factor = prev_bs - prev_ss
                else:
                    prev_r_factor = 0.0

                buyer_strength = bs * c_vol
                seller_strength = ss * c_vol
                buyer_weighted = buyer_strength
                seller_weighted = seller_strength
                combined_score = buyer_weighted - seller_weighted

                rbs_ratio = bs - ss
                change_r_factor = rbs_ratio - prev_r_factor

                buyer_seller_ratio = bs / ss if ss > 0 else (999.0 if bs > 0 else 1.0)

                # Breakout / Breakdown condition matching your Google Sheet
                if c_high > p_high:
                    status = "Breakout Above"
                elif c_low < p_low:
                    status = "Breakdown Below"
                else:
                    status = "Inside Range"

                raw_list.append({
                    "symbol": ticker.replace(".NS", ""),
                    "live_price": round(c_close, 2),
                    "p_open": round(p_open, 2),
                    "p_high": round(p_high, 2),
                    "p_low": round(p_low, 2),
                    "p_close": round(p_close, 2),
                    "c_open": round(c_open, 2),
                    "c_high": round(c_high, 2),
                    "c_low": round(c_low, 2),
                    "c_close": round(c_close, 2),
                    "c_vol": int(c_vol),
                    "buyer_strength": round(buyer_strength, 2),
                    "seller_strength": round(seller_strength, 2),
                    "buyer_weighted": round(buyer_weighted, 2),
                    "seller_weighted": round(seller_weighted, 2),
                    "combined_score": round(combined_score, 2),
                    "bs": round(bs, 4),
                    "ss": round(ss, 4),
                    "rbs_ratio": round(rbs_ratio, 4),
                    "status": status,
                    "buyer_seller_ratio": round(buyer_seller_ratio, 4),
                    "prev_r_factor": round(prev_r_factor, 4),
                    "change_r_factor": round(change_r_factor, 4)
                })
            except Exception:
                continue

        # Add Volume Rank & Combined Rank across all fetched symbols
        raw_list.sort(key=lambda x: x["c_vol"], reverse=True)
        for rank, item in enumerate(raw_list, 1):
            item["vol_rank"] = rank

        raw_list.sort(key=lambda x: x["combined_score"], reverse=True)
        for rank, item in enumerate(raw_list, 1):
            item["combined_rank"] = rank

        # Default sort by RBS Ratio descending
        raw_list.sort(key=lambda x: x["rbs_ratio"], reverse=True)

        return {"symbols": raw_list}

    except Exception as e:
        return {"error": str(e), "symbols": []}
