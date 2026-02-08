from flask import Flask, request, jsonify, render_template_string
import random

app = Flask(__name__)

# ===============================
# PAGE WEB (INTERFACE TRADING)
# ===============================
@app.route("/")
def home():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Trading Signal Bot</title>
    </head>
    <body style="font-family: Arial; text-align: center; margin-top: 40px;">
        <h2>📈 Trading Signal Bot</h2>

        <input id="pair" value="EURUSD"/><br><br>

        <select id="expiry">
            <option value="1m">1 Minute</option>
            <option value="5m">5 Minutes</option>
            <option value="15m">15 Minutes</option>
        </select><br><br>

        <button onclick="getSignal()">GET SIGNAL</button>
        <br><br>

        <h3 id="decision"></h3>

        <script>
            function getSignal() {
                const pair = document.getElementById("pair").value;
                const expiry = document.getElementById("expiry").value;

                fetch(`/signal?pair=${pair}&expiry=${expiry}`)
                    .then(res => res.json())
                    .then(data => {
                        document.getElementById("decision").innerHTML =
                            "<b>PAIR:</b> " + data.pair + "<br>" +
                            "<b>DECISION:</b> " + data.signal + "<br>" +
                            "<b>EXPIRATION:</b> " + data.expiry + "<br>" +
                            "<b>CONFIDENCE:</b> " + data.confidence;
                    });
            }
        </script>
    </body>
    </html>
    """
    return render_template_string(html)

# ===============================
# LOGIQUE SIGNAL
# ===============================
@app.route("/signal")
def signal():
    pair = request.args.get("pair", "EURUSD")
    expiry = request.args.get("expiry", "1m")

    signal = random.choice(["BUY", "SELL"])

    return jsonify({
        "pair": pair,
        "signal": signal,
        "expiry": expiry,
        "confidence": "80%"
    })

if __name__ == "__main__":
    app.run()





