from yolonet.yolonet import Yolonet
import cv2

if __name__ == "__main__":
    img = cv2.imread("yolonet/imgs/messi.jpg")
    yolonet = Yolonet()
    bbox = yolonet.detect_bbox(img, imshow=True) # label, x, y, width, height

    for raw in bbox:
        print("[*] class:{} x:{} y:{} width:{} height:{} ".format(raw[0], int(raw[1]), raw[2], raw[3], raw[4]))