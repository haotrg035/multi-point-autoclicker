import os
import tkinter as tk
from tkinter import ttk
from pynput.keyboard import Key, Listener as KeyListener
from inc.clock import InitClock
from inc.recorder import RecordClick
from inc.clicker import Clicker

class AutoClickerAppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Mijn Kliker")
        self.root.geometry("360x400")
        self.root.resizable(False, False)  # Make the window not resizable
        self.root.attributes("-topmost", True)  # Always on top

        self.is_clicking = False
        self.is_recording = False
        self.click_points = []
        self.click_circles = []
        self.click_image = None
        self.click_image_path = os.path.abspath(__file__ + '/../../assets/circle-outline.png')

        self.init_gui(root)
        self.clocker = InitClock(self.clock_frame)
        self.recorder = RecordClick(self)

        self.init_listeners()

    def init_gui(self, root):
        # Group box for the clock
        self.clock_frame = tk.LabelFrame(root, text="Đồng hồ", padx=10, pady=10)
        self.clock_frame.place(x=8, y=4, width=342, height=50)

        # Time input fields
        input_height = 1
        label_time_y = 60
        input_time_y = 85
        section_two_y = input_time_y + 32 + 20

        # Hour input
        tk.Label(root, text="Giờ:").place(x=8, y=label_time_y, height=24)
        self.inpHours = tk.Entry(root, width=12)
        self.inpHours.place(x=8, y=input_time_y, height=24)

        # Minute input
        tk.Label(root, text="Phút:").place(x=94, y=label_time_y, height=24)
        self.inpMinutes = tk.Entry(root, width=12)
        self.inpMinutes.place(x=94, y=input_time_y, height=24)

        # Second input
        tk.Label(root, text="Giây:").place(x=180, y=label_time_y, height=24)
        self.inpSeconds = tk.Entry(root, width=12)
        self.inpSeconds.place(x=180, y=input_time_y, height=24)

        # Millisecond input
        tk.Label(root, text="Mili giây:").place(x=266, y=label_time_y, height=24)
        self.inpMilseconds = tk.Entry(root, width=12)
        self.inpMilseconds.place(x=266, y=input_time_y, height=24)

        # Interval input
        tk.Label(root, text="Lần chạy:").place(x=266, y=input_time_y + 25, height=24)
        self.inpInterval = tk.Entry(root, width=12)
        self.inpInterval.insert(0, "1")
        self.inpInterval.place(x=266, y=input_time_y + 50, height=24)

        # Delay input
        tk.Label(root, text="Delay:").place(x=140, y=section_two_y + 42, height=24)
        self.inpDelay = tk.Entry(root, width=12)
        self.inpDelay.insert(0, "100")
        self.inpDelay.place(x=178, y=section_two_y + 44, height=22)

        # Execute Click Button
        self.btnStartClick = tk.Button(root, text="Chạy Auto [F3]", command=self.handle_execute_click)
        self.btnStartClick.place(x=8, y=input_time_y + 30, width=254, height=46)

        # Record Button
        self.btnRecord = tk.Button(root, text="Ghi click [F2]", command=self.handle_record_click)
        self.btnRecord.place(x=266, y=section_two_y + 43, width=84, height=24)

        # Toggle Show Points Button
        self.btnToggleShowPoints = tk.Button(root, text="Ẩn điểm click", command=self.handle_toggle_show_points)
        self.btnToggleShowPoints.place(x=8, y=section_two_y + 43, width=84, height=24)

        # ListView for Click Steps
        self.lvClickList = ttk.Treeview(root, columns=("STT", "X", "Y", "Delay"), show='headings')
        self.lvClickList.heading("STT", text="STT", anchor='s')
        self.lvClickList.heading("X", text="X", anchor='e')
        self.lvClickList.heading("Y", text="Y", anchor='e')
        self.lvClickList.heading("Delay", text="Delay", anchor='center')

        self.lvClickList.column("STT", width=20, anchor='s')
        self.lvClickList.column("X", width=50, anchor='e')
        self.lvClickList.column("Y", width=50, anchor='e')
        self.lvClickList.column("Delay", width=70, anchor='center')

        self.lvClickList.place(x=8, y=section_two_y + 75, width=342, height=175)
    
    def update_click_list(self):
        self.lvClickList.delete(*self.lvClickList.get_children())
        for idx, (x, y, delay) in enumerate(self.click_points, start=1):
            self.lvClickList.insert("", "end", values=(idx, x, y, delay))

    def add_click_point(self, x, y):
        self.click_points.append((x, y, self.inpDelay.get()))
        print(f"Đã ghi nhận click tại vị trí: ({x}, {y})")

    # Event Handlers (Cần phát triển thêm cho chức năng)
    def handle_execute_click(self):
        self.is_clicking = not self.is_clicking
        if self.is_clicking and not self.is_recording:
            self.recorder.hide_circles()
            self.clicker = Clicker(self)
            self.clicker.start()
        else:
            self.recorder.show_circles()
            self.is_clicking = False
            self.clicker.join()
        self.btnStartClick.config(text=f"{'Dừng' if self.is_clicking else 'Chạy'} Auto [F3]")

    def handle_record_click(self):
        self.recorder.toggle_recording()

    def handle_toggle_show_points(self):
        self.recorder.toggle_show_points()

    def init_listeners(self):
        self.start_f2_kb_listener()
        self.start_f3_kb_listener()
        self.start_esc_kb_listener()

    def start_f2_kb_listener(self):
        def on_press(key):
            if key == Key.f2:
                self.handle_record_click()

        self.f2_listener = KeyListener(on_press=on_press)
        self.f2_listener.start()

    def start_f3_kb_listener(self):
        def on_press(key):
            if key == Key.f3:
                self.handle_execute_click()
                
        self.f3_listener = KeyListener(on_press=on_press)
        self.f3_listener.start()

    def start_esc_kb_listener(self):
        def on_press(key):
            if key == Key.esc:
                print("Phím Esc được nhấn, thoát chương trình.")
                self.quit_app()  # Gọi hàm để thoát ứng dụng

        # Khởi tạo listener để lắng nghe phím
        self.esc_listener = KeyListener(on_press=on_press)
        self.esc_listener.start()
    
    def quit_app(self):
        print("Đang thoát chương trình...")
        
        self.is_clicking = False
        self.is_recording = False

        # Dừng vòng lặp tkinter và thoát ứng dụng
        self.root.quit()
        self.esc_listener.stop()
        self.f3_listener.stop()
        self.f2_listener.stop()

# Khởi chạy giao diện
def InitGUI():
    rootInstance = tk.Tk()
    AutoClickerAppGUI(rootInstance)
    rootInstance.mainloop()