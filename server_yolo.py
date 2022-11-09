import cv2
import numpy as np

from flask import Flask, request, render_template  # , current_app
from PIL import Image
from yolo.yolo import Yolo

app = Flask(__name__)

# カスケードファイルのパス
CASCADE_FACE = './haarcascade_frontalface.xml'
CASCADE_BIRD = './cascade_bird.xml'


@app.route('/')
def index():
    return "Hello World!"

@app.route('/test', methods=['POST'])
def test():
    image_file = request.files.get('image')
    img = np.array(Image.open(image_file))
    print(img.shape)
    return "Hello World!"

def gen_message_by_objs(objs, frame):
    if not len(objs):
        return None

    H, W, _ = frame.shape
    G = (H//2, W//2)

    areas = [w*h for (_, _, w, h) in objs]
    idx = np.argmin(areas)
    centers = [(y+h//2, x+w//2) for (x, y, w, h) in objs]
    target = centers[idx]

    diffY = G[0] - target[0]
    diffX = target[1] - G[1]

    msg = ""
    if diffX > 0:
        msg += "right"
    else:
        msg += "left"
    msg += ":" + str(abs(diffX))

    msg += ","
    if diffY > 0:
        msg += "up"
    else:
        msg += "down"
    msg += ":" + str(abs(diffY))

    return msg


def detect_bird(img):
    yolo = Yolo()
    bbox = yolo.detect_bbox(img, imshow=False)
    birds = []
    for b in bbox:
        print(b)
        if b[0] =="bird":
            birds.append(b[1:5])
    
    if len(bbox) == 0:
        print("no detection")
    
    return birds


@app.route('/bird_detection', methods=['GET','POST'])
def bird_inference():
    image_file = request.files.get('image')

    # 画像の読み込み
    img = np.array(Image.open(image_file))
    birds = detect_bird(img)

    msg = gen_message_by_objs(birds, img)
    if msg is None:
        msg = "Not found"
    return msg


def detect_face(img):
    # 画像をグレースケール変換
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # カスケード分類器の読み込み
    cascade = cv2.CascadeClassifier(CASCADE_FACE)

    # 顔検出の実行: 人数分のBBの配列を出力
    faces = cascade.detectMultiScale(gray)

    return faces


@app.route('/face_detection', methods=['POST'])
def face_inference():
    image_file = request.files.get('image')

    # 画像の読み込み
    img = np.array(Image.open(image_file))

    if img.shape[2] == 3:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    elif img.shape[2] == 4:
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGRA)

    faces = detect_face(img)

    msg = gen_message_by_objs(faces, img)
    if msg is None:
        msg = "Not found"
    return msg


if __name__ == '__main__':
    app.run(host="0.0.0.0")
