'''
多线程瞄准-射击代码
'''

from __future__ import absolute_import  #绝对引用
from __future__ import division
from __future__ import print_function
import numpy as np
import mss
import time
import multiprocessing
from multiprocessing import Pipe
from win32dll_input import Mouse
from input_controller import InputController, MouseButton, KeyboardKey, character_keyboard_key_mapping
import os
import cv2
from opts import opts
from detectors.detector_factory import detector_factory
from input_controllers.native_win32_input_controller import NativeWin32InputController

display_time = 2  #每隔dispaly_time显示一次fps
title = "aimbot"
fps =0
pos_scale=1.25   #重要！！！屏幕放大分辨率,游戏鼠标灵敏度必须调为0
names  = ['enemy_0_head', 'enemy_0_body', 'enemy_1_head', 'enemy_1_body', 'enemy_2_head',
      'enemy_2_body', 'hostage_0']
test={"force":True}

sct = mss.mss()
mouse = Mouse()
calibShotPos = (0,0)  #没有目标时在左上角放空枪用于校准射击点
start_time = time.time()
monitor = {"top": 0, "left": 0, "width": int(800*pos_scale)-100, "height": int(600*pos_scale)-50}
args = [
    "ctdet",
    "--load_model", "C:\\MyData\\AI_game\\model_last_res_18.pth",
    "--arch", "res_18",
    "--head_conv", "64"
]
opt = opts().init(args=args)
os.environ['CUDA_VISIBLE_DEVICES'] = opt.gpus_str
opt.debug = max(opt.debug, 1)
Detector = detector_factory[opt.task]
detector = Detector(opt)
input = NativeWin32InputController()
mouse = Mouse()
detector.pause = False

def draw_res(img,names, results,show_txt=False,enable_bot=False):
    heads_loc =[]
    body_loc = []
    #cv2.circle(img, shotPos2PixelLoc(calibShotPos), 22, (0, 255, 255), thickness=2)  # 用于校正射击点
    #cv2.circle(img, shotPos2PixelLoc(calibShotPos2), 22, (0, 255, 255), thickness=2)  # 用于校正射击点
    for j in range(1, len(names) + 1):
        for bbox in results[j]:
            if bbox[4] > 0.3:
                bbox = np.array(bbox, dtype=np.int32)
                # cat = (int(cat) + 1) % 80

                cat = int(j-1)
                # print('cat', cat, self.names[cat])
                head_c = (124,252,0)
                body_c = (127,255,212)
                c = (0,255,0)
                if not enable_bot:
                    head_c =c
                    body_c =c
                #print('cat', cat, self.names[cat])
                conf = bbox[4]
                txt = '{}{:.1f}'.format(names[cat], conf)
                font = cv2.FONT_HERSHEY_SIMPLEX
                cat_size = cv2.getTextSize(txt, font, 0.5, 2)[0]
                if "head" in txt:
                    img = cv2.rectangle(
                        img, (bbox[0], bbox[1]), (bbox[2], bbox[3]), head_c, 1)
                    heads_loc.append((int((bbox[0]+bbox[2])/2),int((bbox[1]+bbox[3])/2)))
                elif 'body' in txt:
                    img = cv2.rectangle(
                        img, (bbox[0], bbox[1]), (bbox[2], bbox[3]), body_c, 1)
                    body_loc.append((int((bbox[0]+bbox[2])/2),int((bbox[1]+bbox[3])/2)))

                if show_txt:
                    img = cv2.rectangle(img,
                                  (bbox[0], bbox[1] - cat_size[1] - 2),
                                  (bbox[0] + cat_size[0], bbox[1] - 2), c, -1)
                    img =cv2.putText(img, txt, (bbox[0], bbox[1] - 2),
                                font, 0.5, (0, 0, 0), thickness=1, lineType=cv2.LINE_AA)

    return  img,heads_loc,body_loc

def grab_screen(p_input):
    while True:
        # Get raw pixels from the screen, save it to a Numpy array ,and convert BGRA to BGR
        img = np.array(sct.grab(monitor))[:,:,0:3]
        p_input.send(img)

def show_screen(p_output2):
    global fps, start_time
    cv2.namedWindow(title)
    cv2.moveWindow(title, 1000, 10)
    while True:
        img = p_output2.recv()
        cv2.imshow(title, img)
        fps+=1
        TIME = time.time() - start_time
        if (TIME) >= display_time :
            print("FPS: ", fps / (TIME))
            fps = 0
            start_time = time.time()
        # Press "q" to quit
        if cv2.waitKey(3) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break
def shot(target:tuple):
    shot_x = target[0]
    shot_y = target[1]
    shot_x = int(shot_x / pos_scale)
    shot_y = int(shot_y / pos_scale)
    shot = (shot_x, shot_y)
    # print('mouse loc:',shot_x,shot_y)
    mouse.move_mouse(shot)
    input.click(**test)
    input.click(**test)
    input.click(button=MouseButton.RIGHT, duration=0.05, **test)

def pixelLoc2shotPos(target:tuple):
    shot_x = target[0]
    shot_y = target[1]
    shot_x = int(shot_x / pos_scale)
    shot_y = int(shot_y / pos_scale)
    shot = (shot_x, shot_y)
    return  shot
def shotPos2PixelLoc(pos:tuple):
    pos_x = pos[0]
    pos_y = pos[1]
    loc_x = int(pos_x / pos_scale)
    loc_y = int(pos_y /pos_scale)
    loc = (loc_x, loc_y)
    return  loc

def detection(p_output,p_intput2):

    mouse.move_mouse((0,0))
    input.click(**test)
    while True:
        img = p_output.recv()
        ret = detector.run(img)
        results = ret['results']
        showimg, heads, bodys = draw_res(img, names, results, show_txt=False, enable_bot=True)
        p_intput2.send(showimg)
        if len(bodys) is 0:
            shot(calibShotPos)
            #shot(calibShotPos2)
        else:
            for body in bodys:
                shot(body)
            if len(bodys)<2:
                for head in heads:
                   shot(head)

if __name__=="__main__":
    p_output,p_input = Pipe()
    p_output2,p_input2 = Pipe()
    # creating new processes
    p1 = multiprocessing.Process(target=grab_screen, args=(p_input, ))
    p2 = multiprocessing.Process(target=detection, args=(p_output,p_input2, ))
    p3 = multiprocessing.Process(target=show_screen, args=(p_output2, ))

    # starting our processes
    p1.start()
    p2.start()
    p3.start()