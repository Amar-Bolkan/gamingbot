import pygetwindow as gw

from ctypes import *

import pynput.keyboard
import win32gui
import win32ui
import numpy as np
from pynput.keyboard import Controller


class Game:

    def __init__(self, name):
        self.name = self._get_full_window_name(name)

    def _get_full_window_name(self, win_name):
        alltitles = gw.getAllTitles()
        title = [t for t in alltitles if win_name in t][0]
        return title

    def focus_game_window(self):
        hwnd = win32gui.FindWindow(None, self.name)
        kbd = Controller()
        kbd.press(pynput.keyboard.Key.alt)
        try:
            win32gui.SetForegroundWindow(hwnd)
        finally:
            kbd.release(pynput.keyboard.Key.alt)

    def capture_state(self):
        # Adapted from https://stackoverflow.com/questions/19695214/screenshot-of-inactive-window-printwindow-win32gui

        windll.user32.SetProcessDPIAware()
        hwnd = win32gui.FindWindow(None, self.name)

        left, top, right, bottom = win32gui.GetClientRect(hwnd)
        w = right - left
        h = bottom - top

        hwnd_dc = win32gui.GetWindowDC(hwnd)
        mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
        save_dc = mfc_dc.CreateCompatibleDC()
        bitmap = win32ui.CreateBitmap()
        bitmap.CreateCompatibleBitmap(mfc_dc, w, h)
        save_dc.SelectObject(bitmap)

        # If Special K is running, this number is 3. If not, 1
        result = windll.user32.PrintWindow(hwnd, save_dc.GetSafeHdc(), 3)

        bmpinfo = bitmap.GetInfo()
        bmpstr = bitmap.GetBitmapBits(True)

        img = np.frombuffer(bmpstr, dtype=np.uint8).reshape((bmpinfo["bmHeight"], bmpinfo["bmWidth"], 4))
        img = np.ascontiguousarray(img)[..., :-1]  # make image C_CONTIGUOUS and drop alpha channel

        if not result:  # result should be 1
            win32gui.DeleteObject(bitmap.GetHandle())
            save_dc.DeleteDC()
            mfc_dc.DeleteDC()
            win32gui.ReleaseDC(hwnd, hwnd_dc)
            raise RuntimeError(f"Unable to acquire screenshot! Result: {result}")

        return img

    def make_input(self):
        pass