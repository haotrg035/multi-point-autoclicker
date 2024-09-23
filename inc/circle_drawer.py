import tkinter as tk

class CircleDrawer:
    def __init__(self, x, y, content, radius=15):
        self.root = tk.Tk()
        self.root.overrideredirect(True)  # Ẩn thanh tiêu đề của cửa sổ
        self.root.wm_attributes("-topmost", True)  # Đặt cửa sổ ở trên cùng
        self.root.geometry(f"+{x-radius}+{y-radius}")  # Đặt vị trí của cửa sổ
        self.root.attributes('-transparentcolor','#f0f0f0')
        
         # Tạo Canvas với nền trong suốt
        self.canvas = tk.Canvas(self.root, width=radius * 2, height=radius * 2)
        self.canvas.pack()

        # Tạo vòng tròn
        self.circle = self.canvas.create_oval(2, 2, radius * 2, radius * 2, outline='red', width=2)
        self.text = self.canvas.create_text(radius, radius, text=content, font=('Arial', 10), fill="white")

        # self.root.mainloop()
    
    def hide(self):
        self.canvas.itemconfig(self.circle, state='hidden')
        self.canvas.itemconfig(self.text, state='hidden')

    def show(self):
        self.canvas.itemconfig(self.circle, state='normal')
        self.canvas.itemconfig(self.text, state='normal')

    def remove(self):
        """Xóa vòng tròn và văn bản khỏi canvas"""
        self.canvas.delete(self.circle)
        self.canvas.delete(self.text)
        self.root.destroy()
    
    def get_instance(self):
        return self
