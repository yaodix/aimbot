import win32gui, win32api, win32con, ctypes


class Mouse:
    """It simulates the mouse"""
    MOUSEEVENTF_MOVE = 0x0001 # mouse move
    MOUSEEVENTF_LEFTDOWN = 0x0002 # left button down
    MOUSEEVENTF_LEFTUP = 0x0004 # left button up
    MOUSEEVENTF_RIGHTDOWN = 0x0008 # right button down
    MOUSEEVENTF_RIGHTUP = 0x0010 # right button up
    MOUSEEVENTF_MIDDLEDOWN = 0x0020 # middle button down
    MOUSEEVENTF_MIDDLEUP = 0x0040 # middle button up
    MOUSEEVENTF_WHEEL = 0x0800 # wheel button rolled
    MOUSEEVENTF_ABSOLUTE = 0x8000 # absolute move
    SM_CXSCREEN = 0
    SM_CYSCREEN = 1

    def _do_event(self, flags, x_pos, y_pos, data, extra_info):
        """generate a mouse event"""
        #print("X merric", ctypes.windll.user32.GetSystemMetrics(self.SM_CXSCREEN))
        #print("Y merric", ctypes.windll.user32.GetSystemMetrics(self.SM_CYSCREEN))
        #x_calc = 65536 * x_pos / ctypes.windll.user32.GetSystemMetrics(self.SM_CXSCREEN) + 1 #65536
        #y_calc = 65536 * y_pos / ctypes.windll.user32.GetSystemMetrics(self.SM_CYSCREEN) + 1
        x_calc = x_pos
        y_calc = y_pos
        return ctypes.windll.user32.mouse_event(flags, ctypes.c_uint(x_calc), ctypes.c_int(y_calc),
                                                ctypes.c_int(data), ctypes.c_int(extra_info))

    def _get_button_value(self, button_name, button_up=False):
        """convert the name of the button into the corresponding value"""
        buttons = 0
        if button_name.find("right") >= 0:
            buttons = self.MOUSEEVENTF_RIGHTDOWN
        if button_name.find("left") >= 0:
            buttons = buttons + self.MOUSEEVENTF_LEFTDOWN
        if button_name.find("middle") >= 0:
            buttons = buttons + self.MOUSEEVENTF_MIDDLEDOWN
        if button_up:
            buttons = buttons << 1
        return buttons

    def move_mouse(self, pos):
        """move the mouse to the specified coordinates"""
        (x, y) = pos
        old_pos = self.get_position()
        x =  x if (x != -1) else old_pos[0]
        y =  y if (y != -1) else old_pos[1]
        self._do_event(self.MOUSEEVENTF_MOVE + self.MOUSEEVENTF_ABSOLUTE, x, y, 0, 0)

    def press_button(self, pos=(-1, -1), button_name="left", button_up=False):
        """push a button of the mouse"""
        self.move_mouse(pos)
        self._do_event(self.get_button_value(button_name, button_up), 0, 0, 0, 0)

    def click(self, pos=(-1, -1), button_name= "left"):
        """Click at the specified placed"""
        self.move_mouse(pos)
        self._do_event(self._get_button_value(button_name, False)+self._get_button_value(button_name, True), 0, 0, 0, 0)

    def double_click (self, pos=(-1, -1), button_name="left"):
        """Double click at the specifed placed"""
        for i in range(2):
            self.click(pos, button_name)

    def get_position(self):
        """get mouse position"""
        return win32api.GetCursorPos()