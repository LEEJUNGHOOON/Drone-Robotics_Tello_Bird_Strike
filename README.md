# tello-bird-detection

<p align="center">
  <img src="./drone-bird-detection-sequence2.png">
</p>

## download weight
```
$ wget -P yolo https://pjreddie.com/media/files/yolov3.weights
```

## yolo テスト

yolo/yolo.pyからdetect_bboxを呼び出す。

```
$ python3 yolo_test.py
```