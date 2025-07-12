from flask import Flask, request, send_file
import subprocess
import requests
import os

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

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
