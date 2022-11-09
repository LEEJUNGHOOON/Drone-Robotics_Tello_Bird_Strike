from yolo.yolo import Yolo
import cv2

if __name__ == "__main__":
    img = cv2.imread("yolo/imgs/eagle.jpg")
    yolo = Yolo()
    bbox = yolo.detect_bbox(img, imshow=True) # label, x, y, width, height

    for raw in bbox:
        print("[*] class:{} x:{} y:{} width:{} height:{} ".format(raw[0], int(raw[1]), raw[2], raw[3], raw[4]))