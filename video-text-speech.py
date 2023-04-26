import cv2
import os
from gtts import gTTS
from flask import Flask, request, Response

app = Flask(__name__)
IP_ADDRESS = 'sahan.local'


def announcement(text):
    # Initialize gTTS with the text to convert
    speech = gTTS(text, lang='en', slow=False, tld='com')

    # Save the audio file to a temporary file
    speech_file = 'speech.mp3'
    speech.save(speech_file)

    # Play the audio file
    os.system("mpg321 speech.mp3")


def generate():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(generate(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/', methods=['POST'])
def receive_text():
    text = request.json['text']
    print('Received text:', text)
    announcement(text)
    return 'Success', 200


if __name__ == '__main__':
    app.run(host=IP_ADDRESS, port=8080, debug=True)