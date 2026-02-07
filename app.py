from flask import Flask, request, jsonify

app = Flask(__name__)

# Route AKEY (OBLIGATWA)
@app.route("/")
def home():
    return jsonify({
        "status": "Signal Bot is running ✅",
        "how_to_use": "/signal?pair=EURUSD"
    })

# Route SIGNAL
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

if __name__ == "__main__":
    app.run()


