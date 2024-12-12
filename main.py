from flask import Flask, render_template, request, jsonify

from pydub import AudioSegment
from model import model

import os

app = Flask("Sentire")

UPLOADS = "uploads"
os.makedirs(UPLOADS, exist_ok=True)

filename = f"./{UPLOADS}/output"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process-audio", methods=["post"])
def process_audio():
    audioData = request.files["audio"]
    audioData.save(f"{filename}.webm")

    audio_file = AudioSegment.from_file(f"{filename}.webm", format="webm")
    audio_file.export(f"{filename}.wav", format="wav")

    return jsonify({"data": model.prediction(f"{filename}.wav")[0][0]})

app.run(host="0.0.0.0", port=5000)