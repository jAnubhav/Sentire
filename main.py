from flask import Flask, render_template, request
from io import BytesIO

from model import model

app = Flask("Sentire")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process-audio", methods=["POST"])
def getData():
    # audioData = BytesIO(request.files["audio"].stream.read())   
    # result = model.prediction(audioData)

    # print(result[0][0])
    # print(result)

    return "done"


app.run(host="0.0.0.0", port=5000, debug=True)