'''
单线程瞄准射击代码
'''

from __future__ import absolute_import  #绝对引用
from __future__ import division
from __future__ import print_function
import torch
import pyautogui
from input_controllers.native_win32_input_controller import NativeWin32InputController
from win32dll_input import Mouse

import mss
import time
import numpy as np
import cv2
import _init_paths

from input_controller import InputController, MouseButton, KeyboardKey, character_keyboard_key_mapping

import os
import cv2
from opts import opts
from detectors.detector_factory import detector_factory

names  = ['enemy_0_head', 'enemy_0_body', 'enemy_1_head', 'enemy_1_body', 'enemy_2_head',
      'enemy_2_body', 'hostage_0']

test={"force":True}
def draw_res(img,names, results,show_txt=False,enable_bot=False):
    heads_loc =[]
    body_loc = []

    for j in range(1, len(names) + 1):
        for bbox in results[j]:
            if bbox[4] > 0.3:
                bbox = np.array(bbox, dtype=np.int32)
                # cat = (int(cat) + 1) % 80

                cat = int(j-1)
                # print('cat', cat, self.names[cat])
                head_c = (0,0,255)
                body_c = (255,0,0)
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
                        img, (bbox[0], bbox[1]), (bbox[2], bbox[3]), head_c, 2)
                    heads_loc.append((int((bbox[0]+bbox[2])/2),int((bbox[1]+bbox[3])/2)))
                elif 'body' in txt:
                    img = cv2.rectangle(
                        img, (bbox[0], bbox[1]), (bbox[2], bbox[3]), body_c, 2)
                    body_loc.append((int((bbox[0]+bbox[2])/2),int((bbox[1]+bbox[3])/2)))

                if show_txt:
                    img = cv2.rectangle(img,
                                  (bbox[0], bbox[1] - cat_size[1] - 2),
                                  (bbox[0] + cat_size[0], bbox[1] - 2), c, -1)
                    img =cv2.putText(img, txt, (bbox[0], bbox[1] - 2),
                                font, 0.5, (0, 0, 0), thickness=1, lineType=cv2.LINE_AA)

    return  img,heads_loc,body_loc


def demo(opt):
    os.environ['CUDA_VISIBLE_DEVICES'] = opt.gpus_str
    opt.debug = max(opt.debug, 1)
    Detector = detector_factory[opt.task]
    detector = Detector(opt)
    input = NativeWin32InputController()
    mouse = Mouse()
    detector.pause = False
    enable_bot= True
    pyautogui.FAILSAFE = False
    #mouse.move_mouse((0,0))
    pyautogui.move(0,0)
    mouse.move_mouse((0,0))
    time.sleep(1)
    input.click(**test)
    input.click(**test)
    #pyautogui.click(clicks=2)
    with mss.mss() as sct:
        # Part of the screen to capture
        monitor = {"top": 0, "left": 0, "width": 900, "height": 650}
        cv2.namedWindow("OpenCV/Numpy normal")
        cv2.moveWindow("OpenCV/Numpy normal", 1020, 10)
        pre_pos = (0, 0)
        while "Screen capturing":
            last_time = time.time()  #初始化点位
            # Get raw pixels from the screen, save it to a Numpy array
            img = np.array(sct.grab(monitor))[:,:,0:3]
            ret = detector.run(img)
            results = ret['results']
            img,heads,bodys = draw_res(img,names,results,show_txt=False,enable_bot=enable_bot)

            if enable_bot:
                print("bodys",bodys)
                for body in bodys:
                    shot_x = body[0]
                    shot_y = body[1]
                    shot_x =int(shot_x/1000.0*800)
                    shot_y = int(shot_y/750.0*600)
                    shot = (shot_x,shot_y)
                    mouse.move_mouse(shot)
                    mouse.double_click(shot)
                    #input.click(**test)
                    #input.click(**test)
                    #mouse.click(body,button_name='right')
                    input.click(button=MouseButton.RIGHT,duration=0.05, **test)
                    #pyautogui.rightClick()
            cv2.imshow("OpenCV/Numpy normal", img)
            #print('pred time:',ret['tot'])
            # Display the picture
            print("fps: {}".format(1 / (time.time() - last_time)))

            # Press "q" to quit
            k =cv2.waitKey(2)
            if  k == ord("q"):
                cv2.destroyAllWindows()
                break
            elif k== ord("s"):
                enable_bot = not  enable_bot



if __name__ == '__main__':
  args = [
      "ctdet",
     "--load_model","C:\\MyData\\AI_game\\model_last_res_18.pth",
      "--arch","res_18",
      "--head_conv","64"

  ]
  opt = opts().init(args=args)
  demo(opt)