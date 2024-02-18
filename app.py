from flask import Flask, redirect, render_template, url_for, request
import pip._vendor.requests
# `pip3 install assemblyai` (macOS)
# `pip install assemblyai` (Windows)
import assemblyai as aai
aai.settings.api_key = "6353fb2f46144cfc9c2bc46924ba3689"
transcriber = aai.Transcriber()



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

@app.route('/analysis_display')
def analysis_display():
    video = request.args.get('data')
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
    return render_template("analysisdisplay.html")

if __name__== '__app__':
    app.debug = True
    app.run()