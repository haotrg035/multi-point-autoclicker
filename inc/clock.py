import time
import threading
from tkinter import Label
from inc.utils import get_api_time

class Clock:
    def __init__(self, root):
        self.time_label = Label(root, font=('calibri', 12, 'bold'))
        self.time_label.pack(anchor='center')
        self.time_label.place(x=0, y=-2, relwidth=1, relheight=1)

        self.start_time = None
        self.start_tick = time.time() * 1000  # Khởi tạo thời gian hệ thống (miligiây)
        self.delta = 0
        self.root = root

    def start_clock(self):
        # Tạo một thread để cập nhật đồng hồ, giúp giao diện không bị treo
        clock_thread = threading.Thread(target=self.update_clock)
        clock_thread.daemon = True
        clock_thread.start()

    def update_clock(self):
        while True:
            # Tính toán thời gian đã trôi qua kể từ khi khởi tạo
            elapsed = (time.time() * 1000) - self.start_tick + self.delta
            current_time = self.start_time + elapsed

            # Chuyển đổi miligiây thành HH:MM:SS:MS
            hour, rem = divmod(current_time / 1000, 3600)
            minute, rem = divmod(rem, 60)
            second, milli = divmod(rem, 1)

            # Cập nhật giao diện đồng hồ
            self.time_label.config(text=f"{int(hour):02}:{int(minute):02}:{int(second):02}:{int(milli * 1000):03}")
            time.sleep(0.05)  # Chờ 50ms trước khi cập nhật lại

def InitClock(clock_frame):
    # Lấy thời gian từ API
    api_time = get_api_time()
    start_time = (api_time['hour'] * 3600000 + api_time['minute'] * 60000 +
                  api_time['seconds'] * 1000 + api_time['milliSeconds'])
    
    # Khởi tạo đối tượng Clock và truyền root vào
    clock = Clock(clock_frame)
    clock.start_time = start_time
    clock.start_clock()  # Bắt đầu đồng hồ

    return clock
