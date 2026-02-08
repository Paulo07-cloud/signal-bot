from flask import Flask, request, jsonify, render_template_string
import pandas as pd
import numpy as np
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator
import random

app = Flask(__name__)

# ===============================
# FAKE MARKET DATA (SIMULATION)
# ===============================
def get_market_data():
    prices = np.cumsum(np.random.randn(200)) + 100
    return pd.DataFrame({"close": prices})

# ===============================
# PAGE WEB
# ===============================
@app.route("/")
def home():
    html = """
    <!DOCTYPE html>
    <html>
    <head><title>Trading Signal Bot PRO</title></head>
    <body style="font-family: Arial; text-align: center; margin-top: 30px;">
        <h2>🚀 Trading Signal Bot PRO</h2>

        <input id="pair" value="EURUSD"/><br><br>

        <select id="expiry">
            <option value="1m">1 Minute</option>
            <option value="5m" selected>5 Minutes</option>
            <option value="15m">15 Minutes</option>
        </select><br><br>

        <button onclick="getSignal()">GET SIGNAL</button>
        <h3 id="result"></h3>

        <script>
            function getSignal() {
                const pair = document.getElementById("pair").value;
                const expiry = document.getElementById("expiry").value;

                fetch(`/signal?pair=${pair}&expiry=${expiry}`)
                    .then(res => res.json())
                    .then(d => {
                        document.getElementById("result").innerHTML =
                            "<b>PAIR:</b> " + d.pair + "<br>" +
                            "<b>SIGNAL:</b> " + d.signal + "<br>" +
                            "<b>STRENGTH:</b> " + d.strength + "<br>" +
                            "<b>EXPIRY:</b> " + d.expiry;
                    });
            }
        </script>
    </body>
    </html>
    """
    return render_template_string(html)

# ===============================
# BOT PRO LOGIC
# ===============================
@app.route("/signal")
def signal():
    pair = request.args.get("pair", "EURUSD")
    expiry = request.args.get("expiry", "5m")

    df = get_market_data()

    rsi = RSIIndicator(df["close"], window=14).rsi().iloc[-1]
    ema50 = EMAIndicator(df["close"], window=50).ema_indicator().iloc[-1]
    ema200 = EMAIndicator(df["close"], window=200).ema_indicator().iloc[-1]
    price = df["close"].iloc[-1]

    signal = "NO TRADE"
    strength = "WEAK"

    if ema50 > ema200 and rsi < 35:
        signal = "BUY"
        strength = "STRONG"
    elif ema50 < ema200 and rsi > 65:
        signal = "SELL"
        strength = "STRONG"

    return jsonify({
        "pair": pair,
        "signal": signal,
        "strength": strength,
        "expiry": expiry,
        "rsi": round(rsi, 2),
        "trend": "UP" if ema50 > ema200 else "DOWN"
    })

if __name__ == "__main__":
    app.run()
