# Pranjal Kamra: Stock Intelligence & Host Disclosures Extraction Engine (2021–2026)

An institutional-grade financial engineering, bilingual NLP, and equity analytics pipeline that ingests, extracts, analyzes, and benchmarks stock recommendations from **Pranjal Kamra** (Founder of Finology, 5.8M+ YouTube audience) from **January 1, 2021 to October 2026**.

---

## 📊 Dataset & Dashboard Highlights

* **Total Video Episodes Ingested**: **180+ YouTube Episodes & Finology Podcasts** (January 2021 – October 2026).
* **Total Stock Picks Extracted**: **196 High-Conviction Stock Mentions**.
* **Host Personal Holdings**: **13 Verified Disclosures** with verbatim Hindi/English spoken quotes and second-accurate YouTube jump links (`&t=...s`).
* **"What Happened Afterward?" Trajectories Showcase**: Dedicated section tracking 8 flagship multi-year case studies (BSE Ltd, CDSL, Coal India, TVS Motor, Titan, ITC, DMart, Sreeleathers) comparing initial recommendation prices against CMP, business execution outcomes, and multiple expansions.
* **11th Column in Master Table**: Color-coded trajectory indicators on every row (🚀 Multibagger $\ge 100\%$, 📈 High Growth $\ge 30\%$, ✅ Compounded $\ge 0\%$, 📉 Corrected $< 0\%$, ⚖️ Evaluated).
* **Nifty 50 Alpha Engine**: Date-accurate historical benchmark fetching (`^NSEI`) calculating individual stock alpha outperformance over holding horizons.
* **Instant In-Memory Performance**: Pure client-side **0ms instant search**, debounced live input, multi-tier pagination (50/100/All), and descending date sorting.

---

## 🧠 Pranjal Kamra's 6 Core Investment Principles

1. **Avoid Turnaround Traps & Value Illusions (The "Low PE" Trap)**
   * Avoid businesses suffering from structural disruption, regulatory head-winds, or mountain-sized debt (e.g. Vodafone Idea, Yes Bank, Suzlon). A low PE or single-digit stock price is rarely a bargain if earnings quality is deteriorating.

2. **Capital-Light Monopolies & Toll-Booth Moats**
   * Prioritize businesses with unassailable economic moats and non-linear scalability: exchanges, depositories, credit bureaus, and specialized monopolies (e.g. BSE Ltd, CDSL, MCX, DreamFolks). When transaction volume surges, operating margins expand exponentially without heavy capex.

3. **High ROE / ROCE & Clean, Debt-Free Balance Sheets**
   * Businesses consistently generating Return on Equity ($ROE > 15\text{--}20\%$) and Return on Capital Employed ($ROCE > 20\%$) with little to no debt compound investor wealth far faster. High-debt companies hand all their earnings to lenders during rate hike cycles.

4. **Niche Category Monopolies & Pricing Dominance**
   * Seek differentiated category champions that command extreme consumer loyalty, unique regulatory permits, or localized operational moats (e.g. Wonderla Holidays, Cera Sanitaryware, Sreeleathers). High barriers to entry protect profit margins from commoditization.

5. **Cash Flow Over Accounting Profit (The Real Cash Generation Filter)**
   * Net profit (PAT) can be manipulated via aggressive revenue recognition; Free Cash Flow (FCF) and Operating Cash Flow (OCF) cannot. Insist on companies where cumulative operating cash flows consistently match or exceed reported net profits over 5-year cycles.

6. **Long-Term Secular Compounding & Anti-Trading Discipline**
   * Wealth creation requires holding resilient market-share leaders (e.g. Pidilite, Titan, Avenue Supermarts/DMart) across multi-year cycles. Minimizing portfolio turnover, ignoring daily market noise, and letting compounding work uninterrupted beats frequent tactical trading.

---

## 🚀 High-Conviction Trajectory Flagship Case Studies

| Stock | Video Date | Initial Price ➔ CMP | Return % | Alpha vs Nifty | Real-World Business Outcome |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **BSE Ltd.** (`BSE.NS`) | 2021-09-11 | ₹129.98 ➔ ₹3,363.00 | **▲ +2,487.3%** *(25x Multibagger)* | **α +2,437.4%** | Weekly Sensex/Bankex contracts scaled derivative market share from 0% to 20%+, driving non-linear multiple expansion. |
| **CDSL** (`CDSL.NS`) | 2021-05-20 | ₹410.04 ➔ ₹1,286.90 | **▲ +213.9%** *(Multibagger)* | **α +158.6%** | Active Demat accounts in India surged from 4 Cr to 16 Cr+; zero-debt monopoly benefited from retail equity surge. |
| **Coal India** (`COALINDIA.NS`) | 2021-05-20 | ₹94.29 ➔ ₹417.20 | **▲ +342.5%** *(Multibagger)* | **α +287.2%** | Peak thermal power baseload demand, heightened e-auction premiums, and aggressive dividend distribution compounded 4.4x. |
| **TVS Motor** (`TVSMOTOR.NS`) | 2023-03-14 | ₹1,033.96 ➔ ₹4,095.10 | **▲ +296.1%** *(Multibagger)* | **α +265.9%** | Premium 2-wheeler product mix, EV transition (iQube), and sustained 11%+ EBITDA margins beat peer volume growth. |
| **Titan Company** (`TITAN.NS`) | 2021-06-24 | ₹1,747.84 ➔ ₹4,444.80 | **▲ +154.3%** *(Multibagger)* | **α +104.9%** | Unorganized-to-organized jewelry shift; Tanishq wedding retail expansion and CaratLane omni-channel growth. |
| **ITC Ltd.** (`ITC.NS`) | 2021-05-20 | ₹158.41 ➔ ₹263.50 | **▲ +66.3%** *(Compounded)* | **α +11.1%** | Cigarette pricing power funded FMCG scale, culminating in the value-unlocking ITC Hotels demerger and high dividend yield. |
| **Avenue Supermarts (DMart)** (`DMART.NS`) | 2021-06-24 | ₹3,323.80 ➔ ₹3,342.00 | **✅ +0.55%** *(Compounded)* | **α -48.9%** | Radhakishan Damani's owned-store property model provided cost resilience against metro Quick-Commerce headwinds. |
| **Sreeleathers** (`SREEL.NS`) | 2026-10-13 | ₹284.95 ➔ ₹280.35 | **⚖️ -1.61%** *(Stable)* | **α -3.48%** | 16.5-day inventory turnover vs 180-day peer average; lean 0.4% ad-spend model capturing mass unorganized market share. |

---

## 🛠️ Pipeline Architecture

1. **Video Ingestion & Manifest**: Downloads metadata and playlists across 180+ episodes.
2. **Transcript Processing** (`transcripts_cache/`): Retrieves full transcripts and segment timestamps using YouTube Transcript API.
3. **NLP Extraction Engine** (`extract_batch_2021_2026.py`): Leverages Gemini models to extract stock sentiment, growth drivers, promoter governance, and personal holdings.
4. **Ticker Resolution Engine** (`ticker_resolver.py`): Fuzzy matches company names against official National Stock Exchange (`EQUITY_L.csv`) listings.
5. **Pricing & Alpha Engine** (`pricing.py`): Pulls historical start prices, live CMP via `yfinance`, and computes Nifty 50 benchmark returns and excess Alpha.
6. **Dashboard Generator** (`generate_pranjal_html.py`): Builds the self-contained, interactive `report.html` with 0ms client-side search, sorting, and trajectory analysis.

---

## 🚀 Getting Started

### Prerequisites
* Python 3.9+
* Required packages:
  ```bash
  pip install yfinance google-generativeai youtube-transcript-api python-dotenv pandas
  ```

### Generate Dashboard
```bash
python generate_pranjal_html.py
```
Open [`report.html`](report.html) directly in any modern browser.

---

## 📄 License
MIT License. For educational and research purposes.
