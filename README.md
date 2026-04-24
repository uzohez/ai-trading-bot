# 🤖 AI Trading Bot (Deriv - Step Index)

An automated trading system that generates trade signals using EMA strategy, momentum confirmation, and built-in risk management.

---

## 🚀 Features

- 📈 EMA 50 / EMA 200 trend detection  
- 🎯 Pullback-based entry logic  
- ⚡ Momentum confirmation (price action)  
- 🛑 Stop Loss & Take Profit automation  
- 📊 Real-time trade tracking  
- 📉 Win rate & performance statistics  

---

## 🧠 Strategy Overview

The bot follows a structured trading approach:

- **Trend Identification:** EMA 50 vs EMA 200  
- **Entry Condition:** Price retracement to EMA 50  
- **Confirmation:** Last 3 ticks momentum alignment  
- **Risk Management:** Fixed Stop Loss and Take Profit  

---

## ⚙️ Tech Stack

- Python  
- WebSocket API (Deriv)  
- Real-time data processing  

---

## ▶️ Getting Started

### 1. Install dependencies
```bash
pip install -r requirements.txt