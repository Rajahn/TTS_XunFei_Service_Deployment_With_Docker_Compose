import base64

from flask import Flask, request, jsonify, redirect
import requests
import os

app = Flask(__name__)

TTS_INSTANCES = ["tts1:5000","tts2:5000","tts3:5000"]


@app.route('/tts', methods=['POST'])
def dispatch_request():
    for instance in TTS_INSTANCES:
        response = requests.get(f"http://{instance}/check_tts_status")
        if response.status_code == 200 and response.json()["status"]:
            # Redirect request to the free TTS instance
            tts_response = requests.post(f"http://{instance}/tts", json=request.json)

            # Ensure the request was successful
            if tts_response.status_code == 200:
                # Convert raw audio data to a JSON response
                audio_data_encoded = base64.b64encode(tts_response.content).decode('utf-8')
                return jsonify({"audio_data": audio_data_encoded}), 200

    return jsonify({"error": "All TTS instances are busy."}), 503

@app.route('/count', methods=['GET'])
def count():
    return len(TTS_INSTANCES)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
