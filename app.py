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
