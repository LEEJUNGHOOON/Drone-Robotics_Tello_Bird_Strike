import cv2
import numpy as np

from flask import Flask, request, render_template  # , current_app
from PIL import Image

app = Flask(__name__)

# カスケードファイルのパス
CASCADE_PATH = './haarcascade_frontalface.xml'


@app.route('/')
def index():
    return "Hello World!"


def detect_face(img):
    # 画像をグレースケール変換
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # カスケード分類器の読み込み
    cascade = cv2.CascadeClassifier(CASCADE_PATH)

    # 顔検出の実行: 人数分のBBの配列を出力
    faces = cascade.detectMultiScale(gray)

    return faces


@app.route('/face_detection', methods=['POST'])
def inference():
    image_file = request.files.get('image')

    # 画像の読み込み
    img = np.array(Image.open(image_file))

    if img.shape[2] == 3:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    elif img.shape[2] == 4:
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGRA)

    faces = detect_face(img)

    # 検出結果の可視化
    img_copy = img.copy()
    for (x, y, w, h) in faces:
        img_copy = cv2.rectangle(img_copy, (x, y), (x+w, y+h), (255, 0, 0), 2)

    cv2.imwrite("tmp.png", img_copy)

    return "face detected successfully"


if __name__ == '__main__':
    app.run(host="0.0.0.0")
