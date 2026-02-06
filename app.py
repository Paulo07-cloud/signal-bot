from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "BOT SIYAL POCKET OPTION AP MACHE ✅"

@app.route("/signal")
def signal():
    return jsonify({
        "pair": "EUR/USD",
        "signal": "BUY",
        "expiration": "1 MIN"
    })

if __name__ == "__main__":
    app.run()
@app.route("/signal")
def signal():
    pair = request.args.get("pair", "EURUSD")

    data = {
        "pair": pair,
        "signal": "BUY",
        "timeframe": "1m",
        "confidence": "75%"
    }

    return jsonify(data)
