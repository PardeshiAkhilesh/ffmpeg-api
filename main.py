from flask import Flask, request, send_file
import subprocess
import requests
import os
from gtts import gTTS

app = Flask(__name__)
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

@app.route('/')
def home():
    return "FFmpeg API is running!"

@app.route('/extract-audio', methods=['POST'])
def extract_audio():
    video = request.files['video']
    video.save("input.mp4")
    subprocess.run([
        'ffmpeg', '-i', 'input.mp4',
        '-vn', '-acodec', 'pcm_s16le',
        '-ar', '16000', '-ac', '1', 'audio.wav'
    ])
    return send_file("audio.wav", as_attachment=True)

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    audio = request.files['audio']
    files = {
        'file': ('audio.wav', audio, 'audio/wav')
    }
    headers = {
        'Authorization': f'Bearer {OPENAI_API_KEY}'
    }
    data = {
        'model': 'whisper-1'
    }
    response = requests.post(
        'https://api.openai.com/v1/audio/transcriptions',
        headers=headers,
        files=files,
        data=data
    )
    return response.json()

@app.route('/translate', methods=['POST'])
def translate_text():
    data = request.get_json()
    hindi_text = data.get("text")
    target_language = data.get("target_language", "en")  # default to English

    import openai
    openai.api_key = os.environ.get("OPENAI_API_KEY")

    prompt = f"Translate the following from Hindi to {target_language}:\n{hindi_text}"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful translator."},
            {"role": "user", "content": prompt}
        ]
    )

    translated = response['choices'][0]['message']['content']
    return {"translated_text": translated}

@app.route('/gtts', methods=['POST'])
def gtts_tts():
    data = request.get_json()
    text = data.get("text")
    lang = data.get("lang", "en")

    tts = gTTS(text=text, lang=lang)
    tts.save("gtts_output.mp3")

    return send_file("gtts_output.mp3", as_attachment=True)

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
