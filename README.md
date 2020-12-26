# tello-bird-detection

## yolonet テスト

yolonet/yolonet.pyからdetect_bboxを呼び出す。

テスト：以下を実行する。

$ python3 yolonet_test.py


## server_yolonet.py
server.pyをコピーしてbird detectionだけを変更したもの。
yolonet.detext_bboxは [classname, x(左上), y(左上), width, height]の形で出力しているので、birdのbboxを追加する