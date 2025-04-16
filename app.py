# app.py
from flask import Flask, request, jsonify
from producer import send_event

app = Flask(__name__)

@app.route('/send', methods=['POST'])
def send():
    data = request.get_json()
    send_event(data)
    return jsonify({"status": "sent"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=6000)
