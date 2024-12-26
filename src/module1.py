import time
import tkinter as tk
from tkinter import ttk, messagebox

# 进程状态
NEW = "新建"
READY = "就绪"
RUNNING = "运行"
WAITING = "等待"
TERMINATED = "终止"

class Process:
    """进程控制块 (PCB)"""
    def __init__(self, pid, priority, burst_time):
        self.pid = pid
        self.priority = priority
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.state = NEW

    def __repr__(self):
        return f"进程(pid={self.pid}, 优先级={self.priority}, 状态={self.state}, 剩余时间={self.remaining_time})"

class Clock:
    """用于模拟时间的类"""
    def __init__(self):
        self.ready_queue = []
        self.completed = []
        self.time_slice = 2  # 默认时间片

    def set_time_slice(self, time_slice):
        self.time_slice = time_slice

    def add_process(self, process):
        process.state = READY
        self.ready_queue.append(process)

    def fcfs(self):
        if not self.ready_queue:
            return "无可运行进程"
        process = self.ready_queue[0]
        process.state = RUNNING
        process.remaining_time -= 1
        if process.remaining_time <= 0:
            process.remaining_time = 0
            process.state = TERMINATED
            self.completed.append(self.ready_queue.pop(0))
            return f"完成: {process}"
        return f"运行中: {process}"

    def rr(self):
        if not self.ready_queue:
            return "无可运行进程"
        process = self.ready_queue.pop(0)
        process.state = RUNNING
        run_time = min(process.remaining_time, self.time_slice)
        process.remaining_time -= run_time
        if process.remaining_time > 0:
            process.state = READY
            self.ready_queue.append(process)
        else:
            process.state = TERMINATED
            self.completed.append(process)
            return f"完成: {process}"
        return f"运行中: {process}"

    def priority_scheduling(self):
        if not self.ready_queue:
            return "无可运行进程"
        self.ready_queue.sort(key=lambda p: p.priority)
        return self.fcfs()

    def sjf(self):
        if not self.ready_queue:
            return "无可运行进程"
        self.ready_queue.sort(key=lambda p: p.burst_time)
        return self.fcfs()

    def srtf(self):
        if not self.ready_queue:
            return "无可运行进程"
        self.ready_queue.sort(key=lambda p: p.remaining_time)
        return self.fcfs()

class ProcessManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("进程管理模拟系统")

        self.clock = Clock()
        self.scheduler_algorithm = tk.StringVar(value="fcfs")

        # GUI Components
        self.setup_gui()

    def setup_gui(self):
        frame_controls = tk.Frame(self.root)
        frame_controls.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(frame_controls, text="选择调度算法:").pack(side=tk.LEFT)
        ttk.Combobox(frame_controls, textvariable=self.scheduler_algorithm,
                     values=["fcfs", "rr", "priority", "sjf", "srtf"],
                     state="readonly").pack(side=tk.LEFT, padx=5)

        tk.Button(frame_controls, text="设置时间片", command=self.set_time_slice).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_controls, text="推进时间", command=self.advance_time).pack(side=tk.LEFT, padx=5)

        frame_process = tk.Frame(self.root)
        frame_process.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(frame_process, text="创建新进程 (PID 优先级 所需时间):").pack(side=tk.LEFT)
        self.entry_process = tk.Entry(frame_process)
        self.entry_process.pack(side=tk.LEFT, padx=5)

        tk.Button(frame_process, text="创建进程", command=self.create_process).pack(side=tk.LEFT, padx=5)

        frame_log = tk.Frame(self.root)
        frame_log.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        tk.Label(frame_log, text="日志:").pack(anchor=tk.W)
        self.text_log = tk.Text(frame_log, state="disabled", height=15)
        self.text_log.pack(fill=tk.BOTH, expand=True)

    def log(self, message):
        self.text_log.configure(state="normal")
        self.text_log.insert(tk.END, message + "\n")
        self.text_log.configure(state="disabled")
        self.text_log.see(tk.END)

    def set_time_slice(self):
        if self.scheduler_algorithm.get() == "rr":
            time_slice = tk.simpledialog.askinteger("设置时间片", "请输入时间片大小:")
            if time_slice is not None and time_slice > 0:
                self.clock.set_time_slice(time_slice)
                self.log(f"时间片已设置为 {time_slice}")
            else:
                self.log("无效的时间片大小")
        else:
            self.log("当前调度算法不支持设置时间片")

    def advance_time(self):
        algorithm = self.scheduler_algorithm.get()
        if algorithm == "fcfs":
            result = self.clock.fcfs()
        elif algorithm == "rr":
            result = self.clock.rr()
        elif algorithm == "priority":
            result = self.clock.priority_scheduling()
        elif algorithm == "sjf":
            result = self.clock.sjf()
        elif algorithm == "srtf":
            result = self.clock.srtf()
        else:
            result = "未知调度算法"
        self.log(result)

    def create_process(self):
        try:
            pid, priority, burst_time = map(int, self.entry_process.get().split())
            pcb = Process(pid, priority, burst_time)
            self.clock.add_process(pcb)
            self.log(f"已创建进程: {pcb}")
        except ValueError:
            self.log("输入格式错误，请输入: PID 优先级 所需时间")

if __name__ == "__main__":
    root = tk.Tk()
    app = ProcessManagerApp(root)
    root.mainloop()
