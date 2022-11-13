from multiprocessing import process
from threading import Thread
import cv2
import time
from djitellopy import tello
from utils import *
from yolo import *
from mapping import *
from server_yolo import *


#
#bird_detection
#
def checkBird_detection():
    drone.stramon()
    img = drone.get_frame_read().frame
    img = cv2.resize(img, (1280, 720))
    #서버보내고
    bird, rotate, scale = detection_bird(img)
    if(bird):
        drone.rotate_counter_clockwise(rotate)
        drone.move_forward(scale)
        drone.flip_right()
        drone.move_back(scale)
        drone.rotate_counter_clockwise(-rotate)
    return


if __name__ == "__main__":
    map, unit = UI()
    unit_move = int(unit)
    print(map)
    print(len(map))
    print(unit)

    drone = initTello()
    drone.takeoff()
    drone.streamon()
    print(drone.get_battery())

    index = 0
    flag = 1
    time.sleep(3)
    for i in range(len(map)):
        move = map[index]
        print(move)
        while(move!=0):
            checkBird_detection()
            if(flag > 0):
                if( move > 0):
                    drone.move_forward(unit_move)
                    move-=1
                elif(move < 0):
                    drone.move_back(unit_move)
                    move+=1
            else:
                if( move > 0):
                    drone.move_left(unit_move)
                    move-=1
                elif(move < 0):
                    drone.move_right(unit_move)
                    move+=1
            time.sleep(unit_move/20)
        flag*=-1
        index+=1
    
    drone.streamoff()