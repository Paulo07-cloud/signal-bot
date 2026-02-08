from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# ===============================
# PAGE WEB (INTERFACE UTILISATEUR)
# ===============================
@app.route("/")
def home():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Trading Signal Bot</title>
    </head>
    <body style="font-family: Arial; text-align: center; margin-top: 50px;">
        <h2>📈 Trading Signal Bot</h2>

        <input id="pair" placeholder="Eg: EURUSD" value="EURUSD"/>
        <br><br>
        <button onclick="getSignal()">GET SIGNAL</button>

        <h3 id="result"></h3>

        <script>
            function getSignal() {
                const pair = document.getElementById("pair").value;
                fetch("/signal?pair=" + pair)
                    .then(res => res.json())
                    .then(data => {
                        document.getElementById("result").innerHTML =
                            "PAIR: " + data.pair + "<br>" +
                            "SIGNAL: " + data.signal + "<br>" +
                            "TIMEFRAME: " + data.timeframe + "<br>" +
                            "CONFIDENCE: " + data.confidence;
                    });
            }
        </script>
    </body>
    </html>
    """
    return render_template_string(html)

# ===============================
# API SIGNAL (BOT LA)
# ===============================
@app.route("/signal")
def signal():
    pair = request.args.get("pair", "EURUSD")

    return jsonify({
        "pair": pair,
        "signal": "BUY",
        "timeframe": "1m",
        "confidence": "75%"
    })

# ===============================
# LANS APP LA
# ===============================
if __name__ == "__main__":
    app.run()



