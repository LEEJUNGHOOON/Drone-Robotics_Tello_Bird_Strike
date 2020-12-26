# tello-bird-detection

<p align="center">
  <img src="./drone-bird-detection-sequence2.png">
</p>

## dowload weight
```
$ cd yolo  
$ wget https://pjreddie.com/media/files/yolov3.weights
```

## yolo テスト

yolo/yolo.pyからdetect_bboxを呼び出す。

テスト：以下を実行する。
```
$ python3 yolo_test.py
```

## server_yolo.py
server.pyをコピーしてbird detectionだけを変更したもの。
yolo.detext_bboxは [classname, x(左上), y(左上), width, height]の形で出力しているので、birdのbboxを追加する