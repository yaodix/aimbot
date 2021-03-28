import time
from mouseInput.win32dll_input import Mouse


mouse = Mouse()
body = (400,400)
i = 0
mouse.click((0, 0), "left")
mouse.click((0, 0), "left")
mouse.click((0, 0), "left")
while i<3:
    mouse.move_mouse((200,200))

    time.sleep(0.5)
    mouse.click((200, 200), button_name="left")
    mouse.move_mouse((200+222,200))
    mouse.click((200+222,200),button_name="left")
    time.sleep(0.5)
    mouse.move_mouse((200+222,200+222))
    mouse.click((200+222,200+222),button_name="left")
    time.sleep(0.5)
    mouse.move_mouse((200,200+222))
    mouse.click((200,200+222),button_name="left")
    mouse.click((200,200+222),button_name="right")
    time.sleep(0.5)
    #mouse.click((20, 10), "left")
    i +=1

#mouse.click((100, 100), "right")