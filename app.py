import azure.cognitiveservices.speech as speechsdk
from flask import Flask , render_template,request,flash
app=Flask(__name__)
app.secret_key="badambadam"
@app.route("/speech")
def index():
    return render_template("index.html")

@app.route("/speak", methods=["POST"])
def speak():
    speech_config = speechsdk.SpeechConfig(subscription="cc3a37f77cd24cdfa5a274c30bc318ab", region="centralindia")
    speech_config.speech_recognition_language="en-US"

    #To recognize speech from an audio file, use `filename` instead of `use_default_microphone`:
    #audio_config = speechsdk.audio.AudioConfig(filename="YourAudioFile.wav")
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    speech_recognition_result = speech_recognizer.recognize_once_async().get()

    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        flash("You Spoke : {}".format(speech_recognition_result.text))
    elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        flash("No speech could be recognized: {}".format(speech_recognition_result.no_match_details))
    elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_recognition_result.cancellation_details
        flash("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            flash("Error details: {}".format(cancellation_details.error_details))
    
    return render_template("index.html")
