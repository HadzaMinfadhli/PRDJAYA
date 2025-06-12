from flask import Flask, request, jsonify
import json
import time
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, "tds.json")
app = Flask(__name__)

@app.route('/submit', methods=['POST'])
def receive_data():
    tds_value = request.form.get('tds') or (request.get_json(silent=True) or {}).get('tds')
    if tds_value:
        try:
            data = {
                "timestamp": time.strftime('%Y-%m-%dT%H:%M:%SZ'),
                "tds": float(tds_value)
            }
            with open(JSON_PATH, "w") as f:
                json.dump(data, f)
            print("✅ Data berhasil disimpan:", data)
            return "Data TDS berhasil diterima", 200
        except Exception as e:
            print("❌ Error konversi/simpan:", e)
            return "Format TDS tidak valid", 400
    return "Tidak ada nilai TDS yang diterima", 400

@app.route('/tds', methods=['GET'])
def send_data():
    try:
        with open("tds.json", "r") as f:
            data = json.load(f)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({"timestamp": None, "tds": None}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
