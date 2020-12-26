"""
Simple camera streaming script

Press 'Q' key to exit.
"""
import cv2
import numpy as np

from timeit import default_timer as timer
from server_yolonet import detect_bird

def main():
    cap = cv2.VideoCapture(1)
    cap.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc('M','J','P','G'))

    accum_time = 0
    curr_fps = 0
    fps = "FPS: ??"
    prev_time = timer()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        curr_time = timer()
        exec_time = curr_time - prev_time
        prev_time = curr_time
        accum_time += exec_time
        curr_fps = curr_fps + 1

        if accum_time > 1:
            accum_time -= 1
            fps = "FPS: " + str(curr_fps)
            curr_fps = 0

        cv2.putText(frame, text=fps, org=(3, 15), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=0.50, color=(255, 0, 0), thickness=2)

        faces = detect_bird(frame)
        for (x, y, w, h) in faces:
            frame = cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        H, W, _ = frame.shape
        G = (H//2, W//2)
        print("Gravity:", G)

        if len(faces):
            areas = [w*h for (_,_,w,h) in faces]
            idx = np.argmin(areas)
            centers = [(y+h//2, x+w//2) for (x,y,w,h) in faces]
            target = centers[idx]
            print("target:", target)

            diffY = G[0] - target[0]
            diffX = target[1] - G[1]

            msg = ""
            if diffX > 0:
                msg += "right"
            else:
                msg += "left"
            msg+= ":" + str(abs(diffX))

            msg += ","
            if diffY > 0:
                msg += "up"
            else:
                msg += "down"
            msg += ":" + str(abs(diffY))

            print(msg)    
            
        cv2.putText(frame, text=fps, org=(3, 15), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=0.50, color=(255, 0, 0), thickness=2)

        cv2.imshow("frame", frame)

        # Display the resulting frame
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
