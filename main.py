from flask import Flask, request, send_file
import subprocess

app = Flask(__name__)

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

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
