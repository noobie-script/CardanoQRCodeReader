import re
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

QR_PATTERN = r"ID:(.*?);NOME:(.*?);COGNOME:(.*?);GRUPPO:(.*)"

validate_ids = set()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/validate", methods=["POST"])
def validate():
    data = request.json.get("qr_text", "")

    match = re.match(QR_PATTERN, data)

    if not match:
        return jsonify({"success": False, "error": "QR non valido"}), 400
    
    qr_id = match.group(1).strip()
    nome = match.group(2).strip()
    cognome = match.group(3).strip()
    gruppo = match.group(4).strip()

    if qr_id in validate_ids:
        return jsonify({"success": False, "error": "QR già utilizzato"}), 400
    
    validate_ids.addr(qr_id)

    return jsonify({
        "success": True,
        "id": qr_id,
        "nome": nome,
        "cognome": cognome,
        "gruppo": gruppo
    })

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
