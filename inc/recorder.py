from pynput.mouse import Listener as MouseListener
# from inc.floating_image import FloatingImage
from inc.circle_drawer import CircleDrawer

class RecordClick:
    def __init__(self, root):
        self.root = root
        self.show_points = True
        self.record_button = root.btnRecord
        self.lvClickList = root.lvClickList
        self.click_circles = root.click_circles
        self.click_points = root.click_points
        self.add_click_point = root.add_click_point
        self.update_click_list = root.update_click_list
        self.is_clicking = root.is_clicking
        self.is_recording = root.is_recording
        self.mouse_listener = None  # Để lưu đối tượng listener

    def toggle_recording(self):
        self.is_recording = not self.is_recording
        if not self.is_recording or self.is_clicking:
            self.is_recording = False
            self.stop_mouse_listener()
        else:
            self.is_recording = True
            self.start_mouse_listener()
        self.record_button.config(text=f"{'Dừng ghi' if self.is_recording else 'Ghi click'} [F2]")

    def get_window_rect(self):
        x1 = self.root.root.winfo_rootx()
        y1 = self.root.root.winfo_rooty() - 35
        x2 = x1 + self.root.root.winfo_width()
        y2 = y1 + self.root.root.winfo_height() + 35
        return (x1, y1, x2, y2)
    
    def is_click_in_window(self, x, y):
        x1, y1, x2, y2 = self.get_window_rect()
        return x1 <= x <= x2 and y1 <= y <= y2

    def on_left_click(self, x, y, button, pressed):
        if not self.is_clicking:
            if pressed and button.name == "left" and not self.is_click_in_window(x, y) and self.is_recording:
                self.add_click_point(x, y)
                self.update_click_list()
                
                circle = CircleDrawer(x, y, len(self.click_points)).get_instance()
                self.click_circles.append(circle)
                self.click_circles[-1].root.mainloop()

    def start_mouse_listener(self):
        if self.mouse_listener is None:
            self.mouse_listener = MouseListener(on_click=self.on_left_click)
            self.mouse_listener.start()
                
    def stop_mouse_listener(self):
        if self.mouse_listener is not None:
            self.mouse_listener.stop()
            self.mouse_listener = None  # Đảm bảo listener dừng hoàn toàn
    
    def toggle_show_points(self):
        self.show_points = not self.show_points
        if self.show_points:
            self.show_circles()
        else:
            self.hide_circles()

    def hide_circles(self):
        print("Ẩn tất cả các vòng tròn")
        for circle in self.click_circles:
            circle.hide()

    def show_circles(self):
        print("Hiện tất cả các vòng tròn")
        for circle in self.click_circles:
            circle.show()

    def clear_circles(self):
        print("Xóa tất cả các vòng tròn")
        for circle in self.click_circles:
            circle.remove()
        self.click_circles.clear()  # Xóa danh sách vòng tròn

    def update_circles(self):
        print("Vẽ lại các vòng tròn theo danh sách")
        self.clear_circles()
        for i, (x, y) in enumerate(self.click_points):
            circle = CircleDrawer(x, y, i + 1)  # Vẽ lại vòng tròn theo click_points
            self.click_circles.append(circle)
