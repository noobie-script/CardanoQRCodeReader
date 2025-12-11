import re
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

QR_PATTERN = r"NOME:(.*?);COGNOME:(.*?);GRUPPO:(.*)"

validate_qr = set()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/validate", methods=["POST"])
def validate():
    data = request.json.get("qr_text", "")
    match = re.match(QR_PATTERN, data)

    if not match:
        return jsonify({"success": False, "error": "QR non valido"}), 400
    
    if data in validate_qr:
        return jsonify({"success": False, "error": "QR già utilizzato"}), 400

    nome = match.group(1).strip()
    cognome = match.group(2).strip()
    gruppo = match.group(3).strip()

    validate_qr.add(data)

    return jsonify({
        "success": True,
        "nome": nome,
        "cognome": cognome,
        "gruppo": gruppo
    })

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
