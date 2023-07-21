import os
from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
from googletrans import Translator

app = Flask(__name__)

# Function to perform speech-to-text conversion
def speech_to_text(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Error: Could not understand audio"
    except sr.RequestError as e:
        return f"Error: {e}"

# Function to perform translation
def translate_text(text, target_language):
    translator = Translator()
    translated_text = translator.translate(text, dest=target_language).text
    return translated_text

# Route to serve the HTML page
@app.route('/')
def home_page():
    return render_template('home.html')

# Route to handle the speech-to-text conversion and translation
@app.route('/speech-to-text-and-translate', methods=['POST'])
def convert_speech_to_text_and_translate():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file found'})

    audio_file = request.files['audio']
    if audio_file.filename == '':
        return jsonify({'error': 'No selected file'})

    # Save the uploaded audio file temporarily
    temp_audio_path = "temp_audio.wav"
    audio_file.save(temp_audio_path)

    # Perform the speech-to-text conversion
    text = speech_to_text(temp_audio_path)

    # Remove the temporary audio file
    os.remove(temp_audio_path)

    if 'target_language' in request.form:
        target_language = request.form['target_language']
        translated_text = translate_text(text, target_language)
    else:
        translated_text = text

    return jsonify({'text': text, 'translated_text': translated_text})

if __name__ == '__main__':
    app.run(debug=True)
