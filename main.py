import pip._vendor.requests
# `pip3 install assemblyai` (macOS)
# `pip install assemblyai` (Windows)
import assemblyai as aai
aai.settings.api_key = "6353fb2f46144cfc9c2bc46924ba3689"
transcriber = aai.Transcriber()

from flask import Flask, redirect

app = Flask(__name__)

@app.route("/")
def main():
    return redirect("templates/main.html")

@app.route("/record")
def record():
    return redirect("templates/record.html")

@app.route("/analyze/<video>")
def analyze(video):
    config = aai.TranscriptionConfig(speaker_labels=True, sentiment_analysis=True)

    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(
        video,
        config=config
    )
    for utterance in transcript.utterances:
        print(f"Speaker {utterance.speaker}: {utterance.text}")
    for sentiment_result in transcript.sentiment_analysis:
        print(sentiment_result.text)
        print(sentiment_result.sentiment)  # POSITIVE, NEUTRAL, or NEGATIVE
        print(sentiment_result.confidence)
        print(f"Timestamp: {sentiment_result.start} - {sentiment_result.end}")
    return redirect()


# transcript = transcriber.transcribe("./my-local-audio-file.wav")

