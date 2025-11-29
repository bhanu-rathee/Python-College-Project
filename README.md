#🧭 StockSight — Python Stock Analysis App  
*A simple Tkinter-based stock analyzer using yfinance, gnews, and matplotlib.*

---

## 🚀 Overview
**StockSight** is a lightweight desktop application built with **Python + Tkinter** that allows users to:
- Fetch **live stock data** from Yahoo Finance  
- Plot **interactive charts** with `matplotlib`  
- View **latest news headlines** using `gnews`  
- Export historical data to **CSV**  

Perfect for quick technical analysis and financial insights — all in one window.

---

## ✨ Features
- 📊 Live stock prices & history (via **yfinance**)  
- 🧾 Technical indicators (SMA, EMA, Volume)  
- 📰 Company news feed (via **gnews**)  
- 💾 Data export to CSV  
- 🪟 Simple, responsive **Tkinter GUI**  
- 🧠 Supports both US and Indian tickers (e.g., `AAPL`, `RELIANCE.NS`)

---

## 🧰 Tech Stack
- **Frontend:** Tkinter  
- **Backend / Data:** yfinance, pandas  
- **Charts:** matplotlib  
- **News Feed:** gnews  
- **Language:** Python 3.9+

---

## ⚙️ Installation

```bash
# Clone the repository
git clone https://github.com/your-username/stocksight.git
cd stocksight

# (Optional) Create virtual environment
python -m venv .venv
# Activate it
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
