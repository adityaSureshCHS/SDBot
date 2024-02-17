import pip._vendor.requests
# `pip3 install assemblyai` (macOS)
# `pip install assemblyai` (Windows)
import assemblyai as aai

from flask import Flask, redirect

app = Flask(__name__)

@app.route("/")
def main():
    return redirect("templates/main.html")

@app.route("/record")
def record():
    return redirect("templates/record.html")

aai.settings.api_key = "6353fb2f46144cfc9c2bc46924ba3689"
transcriber = aai.Transcriber()
# transcript = transcriber.transcribe("./my-local-audio-file.wav")

