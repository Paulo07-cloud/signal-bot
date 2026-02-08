from flask import Flask, request, jsonify, render_template_string
import pandas as pd
import numpy as np
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator
import time

app = Flask(__name__)

# ===============================
# CONFIG BINARY
# ===============================
TIMEFRAME = "1m"
MAX_SIGNALS = 5
signal_count = 0

# ===============================
# FAKE MARKET DATA (SIMULATION)
# ===============================
def get_market_data():
    prices = np.cumsum(np.random.randn(120)) + 100
    return pd.DataFrame({"close": prices})

# ===============================
# PAGE WEB (POCKET STYLE)
# ===============================
@app.route("/")
def home():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Binary Signal Bot 1M</title>
    </head>
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
                            "<b>SIGNAL:</b> " + d.signal + "<br>" +
                            "<b>ENTER:</b> Next Candle<br>" +
                            "<b>EXPIRATION:</b> 1 Minute<br>" +
                            "<b>CONFIDENCE:</b> " + d.confidence;
                        if (d.signal !== "WAIT") {
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
# BINARY SIGNAL LOGIC
# ===============================
@app.route("/signal")
def signal():
    global signal_count

    if signal_count >= MAX_SIGNALS:
        return jsonify({
            "signal": "SESSION LIMIT REACHED",
            "confidence": "—"
        })

    df = get_market_data()

    rsi = RSIIndicator(df["close"], window=14).rsi().iloc[-1]
    ema20 = EMAIndicator(df["close"], window=20).ema_indicator().iloc[-1]
    ema50 = EMAIndicator(df["close"], window=50).ema_indicator().iloc[-1]

    signal = "WAIT"
    confidence = "LOW"

    if ema20 > ema50 and rsi < 35:
        signal = "BUY"
        confidence = "HIGH"
        signal_count += 1

    elif ema20 < ema50 and rsi > 65:
        signal = "SELL"
        confidence = "HIGH"
        signal_count += 1

    return jsonify({
        "pair": request.args.get("pair", "EURUSD"),
        "signal": signal,
        "confidence": confidence
    })

if __name__ == "__main__":
    app.run()

