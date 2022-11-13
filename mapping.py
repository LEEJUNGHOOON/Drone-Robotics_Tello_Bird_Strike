import numpy as np
import tkinter
import cv2
from tkinter import Entry, Text, filedialog

oldx = oldy = -1 # 좌표 기본값 설정
paths = []
unit = 0
num = 0
move_paths = []
drone_start = 0
unit_m = 0

def UI():
    window=tkinter.Tk()

    #UI초기값
    window.title("BIRD STRIKE!")
    window.geometry("640x400+500+200")
    window.resizable(False, False)

    #문구 설정
    label=tkinter.Label(window, text="BIRD STRIKE!", width=30, height=3, fg="black", relief="solid")
    label.pack()

    def opendir():
        global oldx, oldy, paths, unit, move_paths # 밖에 있는 oldx, oldy 불러옴

        oldx = oldy = -1 # 좌표 기본값 설정
        paths = []
        unit = 0
        def on_mouse(event, x, y, flags, param):
            # event는 마우스 동작 상수값, 클릭, 이동 등등
            # x, y는 내가 띄운 창을 기준으로 좌측 상단점이 0,0이 됌
            # flags는 마우스 이벤트가 발생할 때 키보드 또는 마우스 상태를 의미, Shif+마우스 등 설정가능
            # param은 영상이룻도 있도 전달하고 싶은 데이타, 안쓰더라도 넣어줘야함

            global oldx, oldy, paths, unit, num # 밖에 있는 oldx, oldy 불러옴
            if event == cv2.EVENT_LBUTTONDOWN: # 왼쪽이 눌러지면 실행
                num+= 2
                if(oldx == -1 & oldy == -1):
                    oldx, oldy = x, y
                    unit = -1
                    paths = paths + [x,y]
                    return
                    
                cv2.line(maps, (oldx, oldy), (x, y), (0, 0, 255), 4, cv2.LINE_AA)
                cv2.imshow('map', maps)
                # if(unit == -1):
                #     unit = 0
                #     while True:
                #         unit_string = str(unit) + 'm'
                #         box = messagebox.showinfo('Please input the unit size.(m)','Please input the unit size.(m)\n'+unit_string)
                        
                #         k = cv2.waitKey(1) & 0xFF   # 키보드 입력값을 받고
                #         print(k)
                #         if 47 < k & k < 58:
                #             unit = 10*unit + k-48
                #         if k == 8:
                #             temp = unit % 10
                #             unit = (unit - temp)/10 
                #         if k == 13:               # esc를 누르면 종료
                #             print(unit)
                #             break
                        
                paths = paths + [x,y]
                oldx, oldy = x, y # 그림을 그리고 또 좌표 저장
                

        root = tkinter.Toplevel()#toplevel은 새창
        root.withdraw()
        map_res1 = filedialog.askopenfilename(parent=root,initialdir='./',title='Please Select a Map File')
	    #한글 경로 시 폼 변환
        map_array = np.fromfile(map_res1,np.uint8)
        maps = cv2.imdecode(map_array,cv2.IMREAD_COLOR)
        
        cv2.namedWindow('map')
        cv2.setMouseCallback('map', on_mouse, maps)
        
        while True:
            cv2.imshow('map', maps)    # 화면을 보여준다.

            k = cv2.waitKey(1) & 0xFF   # 키보드 입력값을 받고
                
            if k == 27:               # esc를 누르면 종료
                break

        cv2.destroyAllWindows()

        flag = 1
        for i in range (0,num-2):
            if(flag == 1):
                temp = int(paths[i]-paths[i+2])
                minus = 1
                if(temp < 0):
                    temp *=-1
                    minus *= -1
                temp_num = int(temp/10)
                temp_num *= minus
            else:
                temp = paths[i]-paths[i+2]
                minus = 1
                if(temp < 0):
                    temp *=-1
                    minus *= -1
                temp_num = int(temp/10)
                temp_num *= minus
            flag *= -1
            move_paths = move_paths + [temp_num]
        #move_path(일단 단위 10)
        #첫재줄 +:w/-:s
        #둘째줄 +:d/-:a
        print(move_paths)

    #맵 버튼
    button = tkinter.Button(window, text="지도 설정", overrelief="solid", width=15, command=opendir, repeatdelay=1000, repeatinterval=100)
    button.pack()

    ent = Entry(window) # root라는 창에 입력창 생성
    ent.pack()
    label = tkinter.Label(window,text = "단위를 입력해주세요(cm).")
    label.pack()
    def setunit():
        global unit_m
        unit_m = ent.get() 
        print(unit_m)
    button = tkinter.Button(window, text="단위 설정", overrelief="solid", width=15, command=setunit, repeatdelay=1000, repeatinterval=100)
    button.pack()

    #닫기버튼
    window.protocol("WM_DELETE_WINDOW", window.destroy)
    window.mainloop()

    return move_paths, unit_m
