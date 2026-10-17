import yfinance as yf
from datetime import datetime, timedelta
import time
import threading

# Global cache for Nifty 50 benchmark prices
_nifty_cache = {}

def get_live_price(ticker_obj):
    """Get the live/latest price using fast_info (works during market hours).
    Falls back to last history close if fast_info is unavailable.
    """
    try:
        live = ticker_obj.fast_info.last_price
        if live and live > 0:
            return live
    except Exception:
        pass
    
    # Fallback: last close from recent history
    try:
        hist = ticker_obj.history(period="5d")
        hist = hist.dropna(subset=["Close"])
        if not hist.empty:
            return float(hist.iloc[-1]["Close"])
    except Exception:
        pass
    
    return None

def fetch_nifty_return(video_date: str) -> float:
    """Fetch Nifty 50 (^NSEI) return from video date to present."""
    if video_date in _nifty_cache:
        return _nifty_cache[video_date]
        
    try:
        start_dt = datetime.strptime(video_date, "%Y-%m-%d")
        nifty = yf.Ticker("^NSEI")
        hist = nifty.history(start=start_dt.strftime("%Y-%m-%d"))
        hist = hist.dropna(subset=["Close"])
        if hist.empty:
            _nifty_cache[video_date] = 0.0
            return 0.0
        nifty_start = float(hist.iloc[0]["Close"])
        nifty_curr = get_live_price(nifty)
        if nifty_curr is None:
            nifty_curr = float(hist.iloc[-1]["Close"])
        nifty_return = round(((nifty_curr - nifty_start) / nifty_start) * 100, 2)
        _nifty_cache[video_date] = nifty_return
        return nifty_return
    except Exception:
        _nifty_cache[video_date] = 0.0
        return 0.0

def fetch_stock_prices(ticker: str, video_date: str) -> dict:
    """Queries yfinance for the closing price on the video publish date,
    today's live price, stock return %, Nifty 50 benchmark return %, and alpha.
    Has a 15-second timeout to prevent hanging on bad/delisted tickers.
    """
    if not ticker or ticker == 'N/A':
        return None

    result_container = [None]
    exception_container = [None]

    def _fetch():
        try:
            print(f"Fetching prices for {ticker} starting from {video_date}...")
            start_dt = datetime.strptime(video_date, "%Y-%m-%d")
            ticker_obj = yf.Ticker(ticker)

            hist = ticker_obj.history(start=start_dt.strftime("%Y-%m-%d"))
            hist = hist.dropna(subset=["Close"])

            if hist.empty:
                time.sleep(1)
                hist = ticker_obj.history(start=start_dt.strftime("%Y-%m-%d"))
                hist = hist.dropna(subset=["Close"])

            current_price = get_live_price(ticker_obj)

            if hist.empty:
                if current_price is None:
                    print(f"  No data available for {ticker}")
                    return
                start_price = current_price
                change_pct = 0.0
            else:
                start_price = float(hist.iloc[0]["Close"])
                actual_start_date = hist.index[0].strftime("%Y-%m-%d")

                if current_price is None:
                    current_price = float(hist.iloc[-1]["Close"])

                change_pct = ((current_price - start_price) / start_price) * 100
                print(f"  Start: {start_price:.2f} on {actual_start_date}, Current: {current_price:.2f}, Change: {change_pct:+.2f}%")

            nifty_return = fetch_nifty_return(video_date)
            alpha = round(change_pct - nifty_return, 2)

            result_container[0] = {
                "start_price": round(start_price, 2),
                "current_price": round(current_price, 2),
                "change": f"{change_pct:+.2f}%",
                "change_pct": round(change_pct, 2),
                "nifty_return": f"{nifty_return:+.2f}%",
                "nifty_return_pct": nifty_return,
                "alpha": f"{alpha:+.2f}%",
                "alpha_pct": alpha
            }
        except Exception as e:
            exception_container[0] = e

    t = threading.Thread(target=_fetch, daemon=True)
    t.start()
    t.join(timeout=15)  # Hard 15-second timeout per ticker

    if t.is_alive():
        print(f"  TIMEOUT fetching prices for {ticker} — skipping")
        return None

    if exception_container[0]:
        print(f"  Error fetching {ticker}: {exception_container[0]}")
        return None

    return result_container[0]


if __name__ == "__main__":
    # Test price fetch
    res = fetch_stock_prices("CDSL.NS", "2021-05-20")
    print("Result:", res)
