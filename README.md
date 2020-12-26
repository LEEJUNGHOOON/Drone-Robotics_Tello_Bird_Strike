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

```
$ python3 yolo_test.py
```