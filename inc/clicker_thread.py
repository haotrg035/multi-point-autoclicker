import threading
import time
from pynput.mouse import Controller, Button
from pynput.keyboard import Key, Listener as KeyListener

class Clicker(threading.Thread):
    def __init__(self, root):
        super(Clicker, self).__init__()
        self.root = root
        self.mouse = Controller()  # Bộ điều khiển chuột
        self.keyboard_listener = None
        self.click_points = root.click_points  # Lấy danh sách điểm click từ root
        self.is_clicking = False  # Trạng thái auto click
        self.is_recording = root.is_recording

    def run(self):
        while self.is_clicking:
            for point in self.click_points:
                if not self.is_clicking:
                    break  # Nếu dừng auto click thì thoát khỏi vòng lặp
                x, y, delay = point
                self.click_at_point(x, y)
                time.sleep(int(delay) / 1000 if delay else 0.5)  # Delay giữa các lần click
            time.sleep(0.1)  # Thời gian chờ giữa các chu kỳ click

    def click_at_point(self, x, y):
        print(f"Click chuột tại điểm ({x}, {y})")
        self.mouse.position = (x, y)  # Đặt vị trí chuột đến tọa độ x, y
        self.mouse.click(Button.left, 1)  # Click chuột trái 1 lần

    def start_clicking(self):
        """Bắt đầu auto click nếu chưa chạy"""
        if not self.is_clicking:
            self.root.btnStartClick.config(text="Dừng Auto [F3]")
            self.is_clicking = True
            if not self.is_alive():
                self.start()  # Khởi động thread mới

    def stop_clicking(self):
        """Dừng auto click"""
        print("Dừng auto click")
        self.is_clicking = False
        self.root.btnStartClick.config(text="Chạy Auto [F3]")

    def toggle_auto_click(self):
        """Chuyển đổi trạng thái giữa start và stop"""
        if self.is_clicking:
            self.stop_clicking()
        else:
            if not self.is_recording:
                # Tạo thread mới mỗi khi start_clicking được gọi lại
                new_clicker = Clicker(self.root)
                self.root.clicker = new_clicker  # Cập nhật clicker mới
                new_clicker.start_clicking()

    def on_key_press(self, key):
        """Lắng nghe phím F3 để bật/tắt auto click"""
        if key == Key.f3:
            self.toggle_auto_click()

    def start_keyboard_listener(self):
        """Bắt đầu lắng nghe bàn phím"""
        if self.keyboard_listener is None:
            self.keyboard_listener = KeyListener(on_press=self.on_key_press)
            self.keyboard_listener.start()

def InitClicker(root):
    clicker = Clicker(root)
    clicker.start_keyboard_listener()
    return clicker
