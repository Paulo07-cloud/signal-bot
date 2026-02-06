from flask import Flask, request, jsonify

app = Flask(__name__)

# Yon fonksyon pou jenere siyal la
def get_signal(pair="EURUSD"):
    # Ou ka modifye siyal la isit la oswa ajoute lojik avanse
    return {
        "pair": pair,
        "signal": "BUY",        # Ou ka chanje sa a selon kondisyon
        "timeframe": "1m",
        "confidence": "75%"
    }

# Route pou siyal la
@app.route("/signal")
def signal():
    pair = request.args.get("pair", "EURUSD")
    data = get_signal(pair)
    return jsonify(data)

if __name__ == "__main__":
    # debug=True itil pou devlopman, li montre erè fasil
    app.run(debug=True)

