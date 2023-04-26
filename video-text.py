import cv2
from flask import Flask, request, Response

app = Flask(__name__)

IP_ADDRESS = '10.2.71.238'


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
    return 'Success', 200


if __name__ == '__main__':
    app.run(host=IP_ADDRESS, port=8080, debug=True)
