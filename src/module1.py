from collections import deque

class PCB:
    def __init__(self, pid, priority, burst_time):
        self.pid = pid  # 进程ID
        self.priority = priority  # 优先级
        self.burst_time = burst_time  # 所需CPU时间
        self.remaining_time = burst_time  # 剩余CPU时间
        self.state = '就绪'  # 状态: '就绪', '运行', '等待', '终止'
        self.waiting_for = None  # 如果有等待资源，则设置为资源名称

    def __repr__(self):
        return f"进程(pid={self.pid}, 状态={self.state}, 剩余时间={self.remaining_time})"

class Scheduler:
    def __init__(self, algorithm='fcfs'):
        self.algorithm = algorithm.lower()
        self.ready_queue = deque()  # 就绪队列

    def add_process(self, pcb):
        if self.algorithm == 'priority':
            self.ready_queue = deque(sorted(list(self.ready_queue) + [pcb], key=lambda x: x.priority))
        else:
            self.ready_queue.append(pcb)

    def get_next_process(self):
        if self.ready_queue:
            if self.algorithm in ['sjf', 'srtf']:
                # 按最短作业或剩余时间排序
                self.ready_queue = deque(sorted(self.ready_queue, key=lambda x: x.remaining_time))
            return self.ready_queue.popleft()
        return None

class Clock:
    def __init__(self, scheduler):
        self.time = 0
        self.scheduler = scheduler

    def tick(self):
        self.time += 1
        print(f"时间 {self.time}:")
        next_pcb = self.scheduler.get_next_process()
        if next_pcb:
            next_pcb.state = '运行'
            next_pcb.remaining_time -= 1
            if next_pcb.remaining_time <= 0:
                next_pcb.state = '终止'
                print(f"进程 {next_pcb.pid} 已终止.")
            else:
                self.scheduler.add_process(next_pcb)
        self.print_status()

    def print_status(self):
        print("当前所有进程状态:")
        for pcb in self.scheduler.ready_queue:
            print(pcb)
        print()

def main():
    print("欢迎使用进程管理模拟系统！")
    scheduler_algorithm = input("请选择调度算法 (FCFS/RR/Priority/SJF/SRTF): ").strip().lower()
    scheduler = Scheduler(algorithm=scheduler_algorithm)
    clock = Clock(scheduler)

    while True:
        print("\n命令列表：")
        print("1. 创建 - 创建新进程")
        print("2. 推进 - 推进模拟时间")
        print("3. 退出 - 退出程序")
        command = input("请输入命令编号：").strip()

        if command == '1':
            try:
                pid, priority, burst_time = map(int, input("请输入PID, 优先级, 和所需CPU时间（用空格分隔）: ").split())
                pcb = PCB(pid, priority, burst_time)
                scheduler.add_process(pcb)
                print(f"已创建进程 PID: {pid}")
            except ValueError:
                print("输入无效，请重新尝试.")
        elif command == '2':
            clock.tick()
        elif command == '3':
            print("感谢使用进程管理模拟系统！再见！")
            break
        else:
            print("未知命令，请选择有效的命令编号.")

if __name__ == '__main__':
    main()