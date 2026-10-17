import json
from datetime import datetime
import yfinance as yf

def update_dataset():
    print("Loading master_stocks_dataset.json...")
    with open("master_stocks_dataset.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"Loaded {len(data)} records.")

    # Fetch Nifty 50 historical data once
    print("Fetching Nifty 50 (^NSEI) historical data...")
    nifty = yf.Ticker("^NSEI")
    hist = nifty.history(start="2020-01-01")
    hist = hist.dropna(subset=["Close"])
    
    # Current Nifty price
    try:
        live = nifty.fast_info.last_price
        if not live or live <= 0:
            live = float(hist.iloc[-1]["Close"])
    except Exception:
        live = float(hist.iloc[-1]["Close"])
    
    nifty_cmp = float(live)
    print(f"Nifty CMP: {nifty_cmp:.2f}")

    def get_nifty_for_date(date_str):
        if not date_str:
            return None
        sub = hist[hist.index >= date_str]
        if sub.empty:
            return 0.0
        nifty_start = float(sub.iloc[0]["Close"])
        return round(((nifty_cmp - nifty_start) / nifty_start) * 100, 2)

    updated_count = 0
    for item in data:
        date_str = item.get("date")
        nifty_ret = get_nifty_for_date(date_str) if date_str else None
        
        change_val = item.get("change")
        if change_val and change_val != "N/A" and nifty_ret is not None:
            try:
                change_pct = float(str(change_val).replace("%", "").replace("+", ""))
                alpha = round(change_pct - nifty_ret, 2)
                item["nifty_return"] = f"{nifty_ret:+.2f}%"
                item["nifty_return_pct"] = nifty_ret
                item["alpha"] = f"{alpha:+.2f}%"
                item["alpha_pct"] = alpha
            except Exception as e:
                item["nifty_return"] = f"{nifty_ret:+.2f}%"
                item["nifty_return_pct"] = nifty_ret
                item["alpha"] = "N/A"
                item["alpha_pct"] = None
        elif nifty_ret is not None:
            item["nifty_return"] = f"{nifty_ret:+.2f}%"
            item["nifty_return_pct"] = nifty_ret
            item["alpha"] = "N/A"
            item["alpha_pct"] = None
        else:
            item["nifty_return"] = "N/A"
            item["nifty_return_pct"] = None
            item["alpha"] = "N/A"
            item["alpha_pct"] = None
        
        updated_count += 1

    with open("master_stocks_dataset.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully updated all {updated_count} records with Nifty benchmark returns and Alpha!")

if __name__ == "__main__":
    update_dataset()
