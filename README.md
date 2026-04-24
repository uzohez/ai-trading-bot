# 🤖 AI Trading Bot (Deriv - Step Index)

Automated trading bot using EMA strategy, momentum confirmation, and risk management.

## 🚀 Features
- EMA 50 / EMA 200 trend filtering
- Pullback entry logic
- Momentum confirmation (price action)
- Automated SL & TP
- Real-time trade tracking
- Win rate and balance stats

## 🧠 Strategy Logic
- Trend: EMA crossover (50 vs 200)
- Entry: Pullback to EMA50
- Confirmation: Last 3 ticks momentum
- Risk: Fixed SL and TP

## ▶️ How to Run
```bash
pip install -r requirements.txt
python bot.py