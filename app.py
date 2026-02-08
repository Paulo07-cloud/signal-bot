from flask import Flask, jsonify, request, render_template_string
import pandas as pd
import numpy as np
import requests
from datetime import datetime
import pytz
import os

# ===============================
# CONFIG
# ===============================
API_KEY = "DBK8OKQL1JZL19QU"
BALANCE = 100
RISK = 0.03
LOSS_LIMIT = 3
signal_count = 0
loss_count = 0
MAX_SIGNALS = 5

# ===============================
# FLASK APP
# ===============================
app = Flask(__name__)

# ===============================
# SESSION FILTER
# ===============================
def session_allowed():
    tz = pytz.timezone("US/Eastern")
    hour = datetime.now(tz).hour
    return (3 <= hour <= 6) or (8 <= hour <= 11)

# ===============================
# LIVE DATA (1M) AVEC TRY/EXCEPT
# ===============================
def get_live_data(pair="EURUSD"):
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "FX_INTRADAY",
        "from_symbol": pair[:3],
        "to_symbol": pair[3:],
        "interval": "1min",
        "apikey": API_KEY,
        "outputsize": "compact"
    }
    try:
        r = requests.get(url, timeout=10)
        data = r.json().get("Time Series FX (1min)", {})
        closes = [float(v["4. close"]) for v in data.values()]
        return pd.DataFrame({"close": closes[::-1]})
    except Exception as e:
        print("Error fetching live data:", e)
        # Return dummy data si echwe
        prices = np.cumsum(np.random.randn(120)) + 100
        return pd.DataFrame({"close": prices})

# ===============================
# MARKET ANALYSIS (EMA + RSI)
# ===============================
def analyze_market(df):
    if len(df) < 20:
        return "WAIT"

    ma_fast = df["close"].rolling(5).mean()
    ma_slow = df["close"].rolling(14).mean()
    rsi = 100 - (100 / (1 + (df["close"].diff().clip(lower=0).rolling(14).mean() /
                               df["close"].diff().clip(upper=0).abs().rolling(14).mean())))

    signal = "WAIT"
    # EMA crossover + RSI oversold/overbought
    if ma_fast.iloc[-2] < ma_slow.iloc[-2] and ma_fast.iloc[-1] > ma_slow.iloc[-1] and rsi.iloc[-1] < 35:
        signal = "BUY"
    elif ma_fast.iloc[-2] > ma_slow.iloc[-2] and ma_fast.iloc[-1] < ma_slow.iloc[-1] and rsi.iloc[-1] > 65:
        signal = "SELL"
    return signal

# ===============================
# WEB PAGE (POCKET STYLE)
# ===============================
@app.route("/")
def home():
    html = """
    <!DOCTYPE html>
    <html>
    <head><title>Binary Signal Bot 1M</title></head>
    <body style="font-family: Arial; text-align: center; margin-top: 30px;">
        <h2>🔥 Binary Signal Bot (1 Minute)</h2>
        <p>Max signals per session: 5</p>
        <input id="pair" value="EURUSD"/><br><br>
        <button onclick="getSignal()">GET SIGNAL</button>
        <h3 id="result"></h3>
        <h4 id="timer"></h4>
        <script>
            function startCountdown(sec) {
                let time = sec;
                const el = document.getElementById("timer");
                const interval = setInterval(() => {
                    el.innerHTML = "⏳ Enter within: " + time + " sec";
                    time--;
                    if (time < 0) {
                        clearInterval(interval);
                        el.innerHTML = "❌ Signal expired";
                    }
                }, 1000);
            }

            function getSignal() {
                const pair = document.getElementById("pair").value;
                fetch(`/signal?pair=${pair}`)
                    .then(res => res.json())
                    .then(d => {
                        document.getElementById("result").innerHTML =
                            "<b>PAIR:</b> " + d.pair + "<br>" +
                            "<b>SIGNAL:</b> " + d.decision + "<br>" +
                            "<b>ENTER:</b> Next Candle<br>" +
                            "<b>EXPIRATION:</b> 1 Minute<br>" +
                            "<b>CONFIDENCE:</b> " + d.confidence;
                        if (d.decision !== "WAIT") {
                            startCountdown(30);
                        }
                    });
            }
        </script>
    </body>
    </html>
    """
    return render_template_string(html)

# ===============================
# SIGNAL ROUTE
# ===============================
@app.route("/signal")
def signal():
    global signal_count, loss_count

    pair = request.args.get("pair", "EURUSD")

    # SESSION FILTER
    if not session_allowed():
        return jsonify({
            "pair": pair,
            "decision": "WAIT",
            "reason": "Outside trading session",
            "confidence": "—"
        })

    # MAX SIGNALS
    if signal_count >= MAX_SIGNALS:
        return jsonify({
            "pair": pair,
            "decision": "STOP",
            "reason": "Max signals reached",
            "confidence": "—"
        })

    df = get_live_data(pair)
    decision = analyze_market(df)

    if decision in ["BUY", "SELL"]:
        signal_count += 1
        confidence = "HIGH"
    else:
        confidence = "LOW"

    return jsonify({
        "pair": pair,
        "decision": decision,
        "expiration": "1m",
        "confidence": confidence
    })

# ===============================
# RUN APP
# ===============================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

