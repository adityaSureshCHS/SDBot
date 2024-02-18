from flask import Flask, redirect, render_template, url_for, request
import requests, json, time, os
import pip._vendor.requests
# `pip3 install assemblyai` (macOS)
# `pip install assemblyai` (Windows)
import assemblyai as aai
aai.settings.api_key = "6353fb2f46144cfc9c2bc46924ba3689"
transcriber = aai.Transcriber()
base_url = "https://api.assemblyai.com/v2"
headers = {
    "authorization": "6353fb2f46144cfc9c2bc46924ba3689"
}


app = Flask(__name__)

@app.route("/")
def main():
    return render_template("main.html", form_action_url1=url_for('speech_analysis'), form_action_url2=url_for('debate_analysis'))

@app.route("/record")
def record():
    return render_template("record.html", form_action_url1=url_for('analyze'), home=url_for('main'))



@app.route("/analyze")
def analyze():
    return render_template("analyze.html", form_action_url1=url_for('analysis_display'))

@app.route('/speechanalysis')
def speech_analysis():
    return render_template("speech_analysis.html", form_action_url1=url_for('record'), home=url_for('main'))
# transcript = transcriber.transcribe("./my-local-audio-file.wav")

@app.route('/debateanalysis')
def debate_analysis():
    return render_template("debate_analysis.html", form_action_url2=url_for('analysis_display'), home=url_for('main'))

@app.route('/analysis_display', methods=["GET", "POST"])
def analysis_display():
    if request.method == "POST":
        data = request.form['fullPath']
        print(data)
        dir_path = os.path.dirname(os.path.realpath(__file__))
        os.chdir(dir_path)
        rel = os.path.relpath(data)
        print(rel)
        with open(rel, "rb") as f:
            response = requests.post(base_url + "/upload", headers=headers, data=f)
        upload_url = response.json()["upload_url"]
        video = upload_url
        config = aai.TranscriptionConfig(speaker_labels=True, sentiment_analysis=True)
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(
            video,
            config
        )
        senText = []
        senSen = []
        senCon = []
        senTime = []
        print("The audio of the video that was recorded: " + transcript.text)
        count = 1
        for sentiment_result in transcript.sentiment_analysis:
            print("Major excerpt number ")
            print(count)
            print(sentiment_result.text)
            print("Sentiment was: " + sentiment_result.sentiment)  # POSITIVE, NEUTRAL, or NEGATIVE
            print("Confidence in verdict is: " )
            print(sentiment_result.confidence)
            print(f"Timestamp pof sentiment: {sentiment_result.start} - {sentiment_result.end}")
        
        data = {
            "text": transcript.text,
            "indText": senText,
            "indSen": senSen,
            "indCon": senCon,
            "indTime": senTime
        }
        return data
    '''
    for utterance in transcript.utterances:
        print(f"Speaker {utterance.speaker}: {utterance.text}")
    
    for sentiment_result in transcript.sentiment_analysis:
        print(sentiment_result.text)
        print(sentiment_result.sentiment)  # POSITIVE, NEUTRAL, or NEGATIVE
        print(sentiment_result.confidence)
        print(f"Timestamp: {sentiment_result.start} - {sentiment_result.end}")
    '''
    return ""




if __name__== '__app__':
    app.debug = True
    app.run()