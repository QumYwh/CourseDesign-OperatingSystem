import time
import threading
from queue import Queue

# 进程状态
NEW = "新建"
READY = "就绪"
RUNNING = "运行"
WAITING = "等待"
TERMINATED = "终止"

class Process:
    """进程控制块 (PCB)"""
    pid_counter = 0

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
        self.time = 0
        self.ready_queue = []
        self.completed = []
        self.time_slice = 2  # 默认时间片

    def tick(self, scheduler_algorithm, time_unit=1):
        """根据调度算法推进时间，时间推进一个单位"""
        if not self.ready_queue:
            print("无可运行进程，时间未推进.")
            return

        if scheduler_algorithm == 'fcfs':
            self.fcfs(time_unit)
        elif scheduler_algorithm == 'rr':
            self.rr()
        elif scheduler_algorithm == 'priority':
            self.priority_scheduling(time_unit)
        elif scheduler_algorithm == 'sjf':
            self.sjf(time_unit)
        elif scheduler_algorithm == 'srtf':
            self.srtf(time_unit)

    def set_time_slice(self, time_slice):
        """设置时间片"""
        self.time_slice = time_slice

    def add_process(self, process):
        """添加新进程到就绪队列"""
        process.state = READY
        self.ready_queue.append(process)

    def fcfs(self, time_unit):
        """先来先服务调度"""
        process = self.ready_queue[0]
        process.state = RUNNING
        print(f"运行中: {process} (运行 {time_unit} 单位时间)")

        time.sleep(time_unit)
        process.remaining_time -= time_unit

        if process.remaining_time <= 0:
            process.remaining_time = 0
            process.state = TERMINATED
            self.completed.append(self.ready_queue.pop(0))
            print(f"完成: {process}")
        else:
            process.state = READY

    def rr(self):
        """时间片轮转调度"""
        process = self.ready_queue.pop(0)
        process.state = RUNNING
        run_time = min(process.remaining_time, self.time_slice)
        print(f"运行中: {process} (运行 {run_time} 单位时间)")

        time.sleep(run_time)
        process.remaining_time -= run_time

        if process.remaining_time > 0:
            process.state = READY
            self.ready_queue.append(process)
        else:
            process.state = TERMINATED
            self.completed.append(process)
            print(f"完成: {process}")

    def priority_scheduling(self, time_unit):
        """优先级调度"""
        self.ready_queue.sort(key=lambda p: p.priority)
        self.fcfs(time_unit)

    def sjf(self, time_unit):
        """短作业优先调度"""
        self.ready_queue.sort(key=lambda p: p.burst_time)
        self.fcfs(time_unit)

    def srtf(self, time_unit):
        """最短剩余时间优先调度"""
        self.ready_queue.sort(key=lambda p: p.remaining_time)
        process = self.ready_queue[0]
        process.state = RUNNING
        print(f"运行中: {process} (运行 {time_unit} 单位时间)")

        time.sleep(time_unit)
        process.remaining_time -= time_unit

        if process.remaining_time <= 0:
            process.remaining_time = 0
            process.state = TERMINATED
            self.completed.append(self.ready_queue.pop(0))
            print(f"完成: {process}")
        else:
            process.state = READY

clock = Clock()

def main():
    print("欢迎使用进程管理模拟系统！")

    while True:  # 外层循环用于选择调度算法
        scheduler_algorithm = input("请选择调度算法 (FCFS/RR/Priority/SJF/SRTF): ").strip().lower()
        if scheduler_algorithm not in ['fcfs', 'rr', 'priority', 'sjf', 'srtf']:
            print("未知调度算法，请选择有效的算法.")
            continue

        if scheduler_algorithm == 'rr':
            try:
                time_slice = int(input("请输入时间片大小: ").strip())
                clock.set_time_slice(time_slice)
                print(f"时间片已设置为 {time_slice}.")
            except ValueError:
                print("时间片无效，默认为 2.")

        while True:  # 内层循环用于处理命令
            print("\n命令列表：")
            print("1. 创建 - 创建新进程")
            print("2. 推进 - 推进模拟时间")
            print("3. 返回 - 返回调度算法选择")
            print("0. 退出 - 退出程序")
            command = input("请输入命令编号：").strip()

            if command == '1':
                try:
                    pid, priority, burst_time = map(int, input("请输入PID, 优先级, 和所需CPU时间（用空格分隔）: ").split())
                    pcb = Process(pid, priority, burst_time)
                    clock.add_process(pcb)
                    print(f"已创建进程 PID: {pid}")
                except ValueError:
                    print("输入无效，请重新尝试.")
            elif command == '2':
                time_unit = 1 if scheduler_algorithm != 'rr' else clock.time_slice
                clock.tick(scheduler_algorithm, time_unit)
            elif command == '3':
                print("返回调度算法选择...")
                break  # 退出内层循环，返回到外层循环重新选择调度算法
            elif command == '0':
                print("感谢使用进程管理模拟系统！再见！")
                return  # 退出整个程序
            else:
                print("未知命令，请选择有效的命令编号.")

if __name__ == "__main__":
    main()
