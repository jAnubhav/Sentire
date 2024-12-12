# from flask import Flask, render_template, request
# from model import model

# from json import dumps

# import os

# app = Flask("Sentire")

# UPLOAD_FOLDER = 'uploads'
# os.makedirs(UPLOAD_FOLDER, exist_ok=True) 

# @app.route("/")
# def index():
#     return render_template("index.html")

# @app.route("/process-audio", methods=["POST"])
# def process_audio():
#     audioData = request.files["audio"]
#     audioData.save(f"./{UPLOAD_FOLDER}/output.webm")

#     from pydub import AudioSegment

#     given_audio = AudioSegment.from_file("./uploads/output.webm", format="webm")
#     given_audio.export("./uploads/output.wav", format="wav")
    
#     res = model.prediction("./uploads/output.wav")
    

#     return dumps({"data": res[0][0]})


# app.run(host="0.0.0.0", port=5000, debug=True)

from flask import Flask, render_template, request, jsonify

from pydub import AudioSegment
from model import model

import os, json

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