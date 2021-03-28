
'''
d3dshot录屏测试代码
'''
import d3dshot
import time
import cv2 as cv
import numpy
#import matplotlib.pyplot as plt

while True:
    d = d3dshot.create(capture_output="numpy") #capture_output="numpy"
    d.capture(region=(0,0,1000,750))
    FPS = ""
    cnt = 0
    fps=0
    name ="C:\\MyData\\AI_game\\8.avi"
    fourcc = cv.VideoWriter_fourcc(*'MJPG')
    out = cv.VideoWriter(name, fourcc, 5.0, (1000, 750))
    while True:
        t1 = time.time()
        img = d.get_latest_frame()

        if img is not  None:
            img = img[:, :, ::-1]
            cnt =cnt+1
            img = cv.putText(img,FPS,(10,10),1,1,(0,255,0),2)
            cv.imshow("win",img)
            #out.write(img)
           #plt.imshow(img)

            #plt.show()
            time.sleep(0.01)
            cv.waitKey(1)
            if cnt==20:
                cnt=0
                try:
                    fps = 10000.0 /((time.time()-t1)*10000.0)
                except:
                    pass
            FPS = "FPS: "+str(int(fps))

