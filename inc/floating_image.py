import tkinter as tk
from PIL import Image, ImageTk
import os

class FloatingImage:
    def __init__(self, x, y, image_path):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.wm_attributes("-topmost", True)
        self.root.geometry(f"+{x}+{y}")
        
        # Kiểm tra xem hình ảnh có tồn tại không
        if not os.path.exists(image_path):
            print(f"Không tìm thấy hình ảnh: {image_path}")
            self.root.destroy()
            return

        try:
            self.image = Image.open(image_path)
            self.photo = ImageTk.PhotoImage(self.image)

            # Tạo nhãn để hiển thị hình ảnh
            self.label = tk.Label(self.root, image=self.photo)
            self.label.image = self.photo
            self.label.pack()
        except Exception as e:
            print(f"Có lỗi xảy ra khi tải hình ảnh: {e}")
            self.root.destroy()  # Đóng cửa sổ nếu có lỗi

        self.root.mainloop()

# Sử dụng hàm
# x, y = 100, 200  # Thay đổi tọa độ theo ý bạn
# FloatingImage(x, y)