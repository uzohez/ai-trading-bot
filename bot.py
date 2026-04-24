import websocket
import json
import time
import os

# ==============================
# CONFIG (SAFE)
# ==============================
API_TOKEN = os.getenv("DERIV_API_TOKEN")  # <-- secure
APP_ID = "1089"
SYMBOL = "R_10"

if not API_TOKEN:
    raise ValueError("❌ Please set DERIV_API_TOKEN as an environment variable")

prices = []
last_signal_time = 0

# ==============================
# ACCOUNT TRACKING
# ==============================
balance = 1000
stake = 10
wins = 0
losses = 0
total_trades = 0

active_trade = None

# ==============================
# SEND DATA
# ==============================
def send(ws, data):
    ws.send(json.dumps(data))

# ==============================
# EMA
# ==============================
def calculate_ema(period):
    if len(prices) < period:
        return None
    return sum(prices[-period:]) / period

# ==============================
# STRATEGY
# ==============================
def check_signal():
    global last_signal_time

    if len(prices) < 200:
        return None

    ema50 = calculate_ema(50)
    ema200 = calculate_ema(200)
    price = prices[-1]

    # TREND
    if price > ema50 and ema50 > ema200:
        trend = "BUY"
    elif price < ema50 and ema50 < ema200:
        trend = "SELL"
    else:
        return None

    # PULLBACK
    if abs(price - ema50) > 1.0:
        return None

    # MOMENTUM
    if len(prices) < 5:
        return None

    recent = prices[-5:]

    if trend == "BUY" and not (recent[-1] > recent[-2] > recent[-3]):
        return None

    if trend == "SELL" and not (recent[-1] < recent[-2] < recent[-3]):
        return None

    # COOLDOWN
    if time.time() - last_signal_time < 20:
        return None

    last_signal_time = time.time()
    return trend

# ==============================
# OPEN TRADE
# ==============================
def open_trade(direction, price):
    global active_trade, total_trades

    sl = price - 5 if direction == "BUY" else price + 5
    tp = price + 10 if direction == "BUY" else price - 10

    active_trade = {
        "direction": direction,
        "entry": price,
        "sl": sl,
        "tp": tp
    }

    total_trades += 1

    print(f"\n🚀 OPEN {direction} @ {price}")
    print(f"SL: {sl} | TP: {tp}")

# ==============================
# CHECK TRADE
# ==============================
def check_trade(price):
    global active_trade, balance, wins, losses

    if not active_trade:
        return

    direction = active_trade["direction"]
    sl = active_trade["sl"]
    tp = active_trade["tp"]

    if direction == "BUY":
        if price <= sl:
            balance -= stake
            losses += 1
            print("❌ LOSS")
            active_trade = None
        elif price >= tp:
            balance += stake * 2
            wins += 1
            print("✅ WIN")
            active_trade = None

    elif direction == "SELL":
        if price >= sl:
            balance -= stake
            losses += 1
            print("❌ LOSS")
            active_trade = None
        elif price <= tp:
            balance += stake * 2
            wins += 1
            print("✅ WIN")
            active_trade = None

# ==============================
# STATS
# ==============================
def print_stats():
    if total_trades == 0:
        return

    win_rate = (wins / total_trades) * 100

    print("\n📊 STATS")
    print(f"Balance : {balance}")
    print(f"Trades  : {total_trades}")
    print(f"Wins    : {wins}")
    print(f"Losses  : {losses}")
    print(f"WinRate : {round(win_rate,2)}%\n")

# ==============================
# ACTIVE TRADE
# ==============================
def show_active_trade():
    if active_trade:
        print("📌 ACTIVE TRADE:")
        print(f"Type  : {active_trade['direction']}")
        print(f"Entry : {active_trade['entry']}")
        print(f"SL    : {active_trade['sl']}")
        print(f"TP    : {active_trade['tp']}\n")

# ==============================
# ON MESSAGE
# ==============================
def on_message(ws, message):
    data = json.loads(message)

    if "tick" in data:
        price = data["tick"]["quote"]
        prices.append(price)

        print(f"Price: {price}")

        check_trade(price)

        if not active_trade:
            signal = check_signal()
            if signal:
                open_trade(signal, price)

        print_stats()
        show_active_trade()

# ==============================
# CONNECTION
# ==============================
def on_open(ws):
    print("✅ Connected to Deriv")

    send(ws, {"authorize": API_TOKEN})
    time.sleep(1)

    send(ws, {
        "ticks": SYMBOL,
        "subscribe": 1
    })

def on_error(ws, error):
    print("❌ Error:", error)

def on_close(ws, close_status_code, close_msg):
    print("🔌 Disconnected")

# ==============================
# START
# ==============================
if __name__ == "__main__":
    ws = websocket.WebSocketApp(
        f"wss://ws.derivws.com/websockets/v3?app_id={APP_ID}",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )

    ws.run_forever()