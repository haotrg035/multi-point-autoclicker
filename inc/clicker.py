import threading
import time
from pynput.mouse import Controller, Button

class Clicker(threading.Thread):
    def __init__(self, root):
        super(Clicker, self).__init__()
        self.root = root
        self.mouse = Controller()  # Bộ điều khiển chuột

        self.click_points = root.click_points  # Lấy danh sách điểm click từ root
        self.is_recording = root.is_recording

    def run(self):
        while self.root.is_clicking:
            for point in self.click_points:
                if not self.root.is_clicking:
                    break 
                
                x, y, delay = point
                self.click_at_point(x, y)
                time.sleep(int(delay) / 1000)
                
                if not self.root.is_clicking:
                    break 

            time.sleep(0.1)
            if not self.root.is_clicking:
                break 

    def click_at_point(self, x, y):
        print(f"Click chuột tại điểm ({x}, {y})")
        self.mouse.position = (x, y)  # Đặt vị trí chuột đến tọa độ x, y
        self.mouse.click(Button.left, 1)  # Click chuột trái 1 lần            

def InitClicker(root):
    clicker = Clicker(root)
    # clicker.start()  # Khởi động thread ngay khi bắt đầu chương trình
    return clicker

