import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog

# 进程状态定义常量
NEW = "新建"
READY = "就绪"
RUNNING = "运行"
WAITING = "等待"
TERMINATED = "终止"


# 进程类，模拟进程控制块 (PCB)
class Process:
    """进程控制块 (PCB)"""

    def __init__(self, pid, priority, burst_time):
        self.pid = pid  # 进程ID
        self.priority = priority  # 进程优先级
        self.burst_time = burst_time  # 进程所需CPU时间
        self.remaining_time = burst_time  # 剩余时间
        self.state = NEW  # 初始状态为"新建"

    def __repr__(self):
        return f"进程(pid={self.pid}, 优先级={self.priority}, 状态={self.state}, 剩余时间={self.remaining_time})"
    62


# 时钟类，用于模拟调度器
class Clock:
    """用于模拟时间的类"""

    def __init__(self):
        self.ready_queue = []  # 就绪队列
        self.completed = []  # 完成的进程列表
        self.time_slice = 2  # 默认时间片大小

    def set_time_slice(self, time_slice):
        """设置时间片大小"""
        self.time_slice = time_slice

    def add_process(self, process):
        """将进程添加到就绪队列"""
        process.state = READY
        self.ready_queue.append(process)

    def fcfs(self):
        """先来先服务调度算法"""
        if not self.ready_queue:
            return "无可运行进程"
        process = self.ready_queue[0]
        process.state = RUNNING  # 设置进程为运行状态
        process.remaining_time -= 1  # 执行时间减少1
        if process.remaining_time <= 0:
            process.remaining_time = 0
            process.state = TERMINATED  # 执行完毕，进程终止
            self.completed.append(self.ready_queue.pop(0))  # 从就绪队列移除
            return f"完成: {process}"
        process.state = RUNNING  # 如果未完成，恢复为就绪状态
        return f"运行中: {process}"

    def rr(self):
        """轮转调度算法"""
        if not self.ready_queue:
            return "无可运行进程"
        process = self.ready_queue.pop(0)  # 取出第一个进程
        process.state = RUNNING
        run_time = min(process.remaining_time, self.time_slice)  # 运行时间为时间片或剩余时间，取最小
        process.remaining_time -= run_time
        if process.remaining_time > 0:
            process.state = RUNNING
            self.ready_queue.append(process)  # 如果没完成，放回就绪队列
        else:
            process.state = TERMINATED
            self.completed.append(process)  # 完成，加入已完成列表
            return f"完成: {process}"
        return f"运行中: {process}"

    def priority_scheduling(self):
        """优先级调度算法"""
        if not self.ready_queue:
            return "无可运行进程"
        self.ready_queue.sort(key=lambda p: p.priority)  # 按优先级排序
        return self.fcfs()  # 使用FCFS算法执行调度

    def sjf(self):
        """最短作业优先调度算法"""
        if not self.ready_queue:
            return "无可运行进程"
        self.ready_queue.sort(key=lambda p: p.burst_time)  # 按作业时间（burst_time）排序
        return self.fcfs()  # 使用FCFS算法执行调度

    def srtf(self):
        """最短剩余时间优先调度算法"""
        if not self.ready_queue:
            return "无可运行进程"
        self.ready_queue.sort(key=lambda p: p.remaining_time)  # 按剩余时间排序
        return self.fcfs()  # 使用FCFS算法执行调度


# 进程管理模拟系统的GUI应用
class ProcessManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("进程管理模拟系统")  # 设置窗口标题

        self.clock = Clock()  # 创建时钟实例
        self.scheduler_algorithm = tk.StringVar(value="fcfs")  # 默认调度算法为fcfs

        # 初始化界面组件
        self.setup_gui()

    def setup_gui(self):
        """设置GUI界面"""
        # 控制面板：选择调度算法和操作按钮
        frame_controls = tk.Frame(self.root)
        frame_controls.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(frame_controls, text="选择调度算法:").pack(side=tk.LEFT)
        self.scheduler_combobox = ttk.Combobox(frame_controls, textvariable=self.scheduler_algorithm,
                                                 values=["fcfs", "rr", "priority", "sjf", "srtf"],
                                                 state="readonly")
        self.scheduler_combobox.pack(side=tk.LEFT, padx=5)
        self.scheduler_combobox.bind("<<ComboboxSelected>>", self.clear_log)  # 绑定算法选择事件

        tk.Button(frame_controls, text="设置时间片", command=self.set_time_slice).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_controls, text="推进时间", command=self.advance_time).pack(side=tk.LEFT, padx=5)

        # 进程创建面板
        frame_process = tk.Frame(self.root)
        frame_process.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(frame_process, text="创建新进程 (PID 优先级 所需时间):").pack(side=tk.LEFT)
        self.entry_process = tk.Entry(frame_process)  # 输入框，用于输入新进程的PID、优先级、所需时间
        self.entry_process.pack(side=tk.LEFT, padx=5)

        tk.Button(frame_process, text="创建进程", command=self.create_process).pack(side=tk.LEFT, padx=5)

        # 日志面板，显示调度和进程信息
        frame_log = tk.Frame(self.root)
        frame_log.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        tk.Label(frame_log, text="日志:").pack(anchor=tk.W)
        self.text_log = tk.Text(frame_log, state="disabled", height=15)  # 禁用的Text控件显示日志
        self.text_log.pack(fill=tk.BOTH, expand=True)

    def log(self, message):
        """向日志窗口添加信息"""
        self.text_log.configure(state="normal")
        self.text_log.insert(tk.END, message + "\n")
        self.text_log.configure(state="disabled")
        self.text_log.see(tk.END)

    def clear_log(self, event=None):
        """清空日志"""
        self.text_log.configure(state="normal")
        self.text_log.delete(1.0, tk.END)
        self.text_log.configure(state="disabled")

    def set_time_slice(self):
        """设置时间片，只有在选择轮转调度算法时才允许设置"""
        if self.scheduler_algorithm.get() == "rr":
            time_slice = tk.simpledialog.askinteger("设置时间片", "请输入时间片大小:")  # 弹出输入框让用户输入时间片
            if time_slice is not None and time_slice > 0:
                self.clock.set_time_slice(time_slice)  # 设置时钟的时间片大小
                self.log(f"时间片已设置为 {time_slice}")
            else:
                self.log("无效的时间片大小")
        else:
            self.log("当前调度算法不支持设置时间片")

    def advance_time(self):
        """推进时间，根据选择的调度算法进行进程调度"""
        algorithm = self.scheduler_algorithm.get()  # 获取当前选择的调度算法
        if algorithm == "fcfs":
            result = self.clock.fcfs()  # 执行FCFS调度
        elif algorithm == "rr":
            result = self.clock.rr()  # 执行轮转调度
        elif algorithm == "priority":
            result = self.clock.priority_scheduling()  # 执行优先级调度
        elif algorithm == "sjf":
            result = self.clock.sjf()  # 执行最短作业优先调度
        elif algorithm == "srtf":
            result = self.clock.srtf()  # 执行最短剩余时间优先调度
        else:
            result = "未知调度算法"
        self.log(result)

    def create_process(self):
        """根据输入框内容创建新进程"""
        try:
            pid, priority, burst_time = map(int, self.entry_process.get().split())  # 解析输入
            pcb = Process(pid, priority, burst_time)  # 创建新进程
            self.clock.add_process(pcb)  # 将进程加入时钟的就绪队列
            self.log(f"已创建进程: {pcb}")
            self.entry_process.delete(0, tk.END)  # 清空输入框
        except ValueError:
            self.log("输入格式错误，请输入: PID 优先级 所需时间")
            self.entry_process.delete(0, tk.END)  # 清空输入框


# 主程序启动
if __name__ == "__main__":
    root = tk.Tk()  # 创建主窗口
    app = ProcessManagerApp(root)  # 创建进程管理应用
    root.mainloop()  # 进入主循环，等待用户操作
