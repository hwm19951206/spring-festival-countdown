import tkinter as tk
from datetime import datetime, timedelta
from lunardate import LunarDate
import threading
import time

def get_next_spring_festival():
    """获取下一个春节的公历日期"""
    today = datetime.today()
    year = today.year

    # 尝试今年的春节
    try:
        this_year_sf = LunarDate(year, 1, 1).toSolarDate()
    except ValueError:
        this_year_sf = None

    # 尝试明年的春节
    next_year_sf = LunarDate(year + 1, 1, 1).toSolarDate()

    if this_year_sf and this_year_sf >= today.date():
        return datetime.combine(this_year_sf, datetime.min.time())
    else:
        return datetime.combine(next_year_sf, datetime.min.time())

def format_timedelta(td):
    """将 timedelta 转换为 天、小时、分钟、秒"""
    total_seconds = int(td.total_seconds())
    if total_seconds < 0:
        return "春节快乐！"
    days = total_seconds // 86400
    hours = (total_seconds % 86400) // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{days} 天 {hours:02d} 小时 {minutes:02d} 分 {seconds:02d} 秒"

class CountdownApp:
    def __init__(self, root):
        self.root = root
        self.root.title("春节倒计时")
        self.root.geometry("400x180")
        self.root.resizable(False, False)
        self.root.attributes("-topmost", True)  # 置顶
        self.root.configure(bg="#ffeaa7")

        # 标题
        self.label_title = tk.Label(
            root,
            text="距离春节还有",
            font=("Microsoft YaHei", 18, "bold"),
            bg="#ffeaa7",
            fg="#2d3436"
        )
        self.label_title.pack(pady=15)

        # 倒计时显示
        self.label_countdown = tk.Label(
            root,
            text="",
            font=("Microsoft YaHei", 16),
            bg="#ffeaa7",
            fg="#e17055"
        )
        self.label_countdown.pack(pady=10)

        # 春节日期提示
        self.sf_date = get_next_spring_festival()
        self.label_date = tk.Label(
            root,
            text=f"春节日期：{self.sf_date.strftime('%Y年%m月%d日')}",
            font=("Microsoft YaHei", 12),
            bg="#ffeaa7",
            fg="#636e72"
        )
        self.label_date.pack(pady=5)

        # 启动倒计时线程
        self.running = True
        self.thread = threading.Thread(target=self.update_countdown, daemon=True)
        self.thread.start()

        # 关闭窗口时退出线程
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def update_countdown(self):
        while self.running:
            now = datetime.now()
            diff = self.sf_date - now
            text = format_timedelta(diff)
            self.label_countdown.config(text=text)
            time.sleep(1)

    def on_closing(self):
        self.running = False
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = CountdownApp(root)
    root.mainloop()