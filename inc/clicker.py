import threading
import time
from pynput.mouse import Controller, Button

class Clicker(threading.Thread):
    def __init__(self, root):
        super(Clicker, self).__init__()
        self.root = root
        self.mouse = Controller()  # Bộ điều khiển chuột

        self.click_points = root.click_points
        self.is_recording = root.is_recording

    def run(self):
        while self.root.is_clicking:
            if int(self.root.click_interval) > 0:
                for i in range(int(self.root.click_interval)):
                    for point in self.click_points:
                        if not self.root.is_clicking:
                            self.root.stop_clicking()
                            break 
                        x, y, delay = point
                        self.click_at_point(x, y)
                        time.sleep(int(delay) / 1000)
            self.root.stop_clicking()


    def click_at_point(self, x, y):
        print(f"Click chuột tại điểm ({x}, {y})")
        self.mouse.position = (x, y)
        self.mouse.click(Button.left, 1)

