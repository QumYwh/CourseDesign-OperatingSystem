import tkinter as tk
from tkinter import filedialog, messagebox


# 读取磁道请求序列文件并返回其中的整数列表
def read_track_sequence(file_path):
    try:
        with open(file_path, 'r') as file:  # 打开文件
            return [int(line.strip()) for line in file.readlines()]  # 读取每行并转换为整数
    except Exception as e:
        messagebox.showerror("错误", f"无法读取文件: {e}")  # 如果出现异常，弹出错误对话框
        return []


# 先来先服务算法（FCFS）
def fcfs(service_sequence, current_position):
    total_head_movement = 0  # 初始化总磁头移动距离
    service_order = []  # 存储服务的顺序

    # 遍历磁道请求序列
    for track in service_sequence:
        total_head_movement += abs(track - current_position)  # 计算磁头从当前磁道位置到目标磁道的移动距离
        current_position = track  # 更新当前磁头位置
        service_order.append(track)  # 将当前磁道加入服务顺序

    return service_order, total_head_movement  # 返回服务顺序和总移动道数


# 最短寻道优先算法（SSTF）
def sstf(service_sequence, current_position):
    total_head_movement = 0  # 初始化总磁头移动距离
    service_order = []  # 存储服务顺序
    remaining_tracks = service_sequence.copy()  # 创建磁道请求序列的副本

    # 循环处理每个磁道请求，选择距离当前磁头位置最近的磁道
    while remaining_tracks:
        closest_track = min(remaining_tracks, key=lambda x: abs(x - current_position))  # 找到最近的磁道
        total_head_movement += abs(closest_track - current_position)  # 更新总移动道数
        current_position = closest_track  # 更新磁头位置
        service_order.append(closest_track)  # 将该磁道添加到服务顺序
        remaining_tracks.remove(closest_track)  # 从剩余请求中移除已处理的磁道

    return service_order, total_head_movement  # 返回服务顺序和总移动道数


# 电梯算法（SCAN）
def scan(service_sequence, current_position, direction='right'):
    total_head_movement = 0  # 初始化总磁头移动距离
    service_order = []  # 存储服务顺序

    service_sequence.sort()  # 对磁道请求进行排序

    # 根据方向决定磁头扫描的顺序
    if direction == 'right':
        # 磁头向右扫描
        service_sequence = [track for track in service_sequence if track >= current_position] + \
                           [track for track in service_sequence if track < current_position][::-1]
    else:
        # 磁头向左扫描
        service_sequence = [track for track in service_sequence if track <= current_position][::-1] + \
                           [track for track in service_sequence if track > current_position]

    # 遍历扫描后的磁道顺序
    for track in service_sequence:
        total_head_movement += abs(track - current_position)  # 更新总移动道数
        current_position = track  # 更新磁头位置
        service_order.append(track)  # 将该磁道加入服务顺序

    return service_order, total_head_movement  # 返回服务顺序和总移动道数


# 计算按钮点击事件的处理函数
def calculate():
    file_path = file_path_entry.get()  # 获取文件路径
    direction = direction_var.get()  # 获取SCAN算法的扫描方向
    try:
        current_position = int(current_position_entry.get())  # 获取当前磁头位置
    except ValueError:
        messagebox.showwarning("警告", "请输入有效的当前磁头位置！")  # 如果输入无效，弹出警告
        return

    if not file_path:
        messagebox.showwarning("警告", "请提供磁道请求序列文件路径！")  # 如果没有提供文件路径，弹出警告
        return

    # 读取磁道请求序列
    track_sequence = read_track_sequence(file_path)

    if not track_sequence:
        return  # 如果磁道请求序列为空，直接返回

    # 获取选择的调度算法
    algorithm = algorithm_var.get()

    # 根据选择的算法计算服务顺序和总移动道数
    if algorithm == "FCFS":
        service_order, total_head_movement = fcfs(track_sequence, current_position)
    elif algorithm == "SSTF":
        service_order, total_head_movement = sstf(track_sequence, current_position)
    elif algorithm == "SCAN":
        service_order, total_head_movement = scan(track_sequence, current_position, direction)
    else:
        messagebox.showwarning("警告", "请选择一个调度算法！")  # 如果没有选择算法，弹出警告
        return

    # 显示计算结果
    result_label.config(text=f"服务顺序: {service_order}\n总移动道数: {total_head_movement}")

    # 只清空当前磁头位置输入框
    current_position_entry.delete(0, tk.END)


# 选择文件按钮的点击事件处理函数
def browse_file():
    # 弹出文件选择对话框
    file_path = filedialog.askopenfilename(title="选择磁道请求序列文件")
    # 清空文件路径输入框并插入选中的文件路径
    file_path_entry.delete(0, tk.END)
    file_path_entry.insert(0, file_path)


# 创建主窗口
root = tk.Tk()
root.title("磁盘调度算法")

# 设置窗口大小和允许缩放
root.geometry("700x500")  # 初始大小
root.resizable(True, True)  # 允许水平和垂直方向上的窗口缩放

# 文件路径输入框
file_frame = tk.Frame(root)
file_frame.pack(pady=10, fill=tk.X)

tk.Label(file_frame, text="磁道请求文件:").pack(side=tk.LEFT)  # 标签
file_path_entry = tk.Entry(file_frame, width=40)  # 文件路径输入框
file_path_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
browse_button = tk.Button(file_frame, text="浏览", command=browse_file)  # 浏览按钮
browse_button.pack(side=tk.LEFT)

# 当前磁头位置输入框
current_position_frame = tk.Frame(root)
current_position_frame.pack(pady=10, fill=tk.X)

tk.Label(current_position_frame, text="当前磁头位置:").pack(side=tk.LEFT)
current_position_entry = tk.Entry(current_position_frame, width=10)  # 当前磁头位置输入框
current_position_entry.pack(side=tk.LEFT, padx=5)

# 算法选择
algorithm_var = tk.StringVar()
algorithm_var.set("FCFS")  # 默认选择FCFS

algorithm_frame = tk.Frame(root)
algorithm_frame.pack(pady=10, fill=tk.X)

tk.Label(algorithm_frame, text="选择调度算法:").pack(anchor=tk.W)

# 单选按钮，用于选择调度算法
algorithms = ["FCFS", "SSTF", "SCAN"]
for algo in algorithms:
    tk.Radiobutton(algorithm_frame, text=algo, variable=algorithm_var, value=algo).pack(anchor=tk.W)

# SCAN方向选择
direction_var = tk.StringVar()
direction_var.set("right")  # 默认扫描方向向右

direction_frame = tk.Frame(root)
direction_frame.pack(pady=10, fill=tk.X)

tk.Label(direction_frame, text="SCAN方向:").pack(anchor=tk.W)

tk.Radiobutton(direction_frame, text="向右", variable=direction_var, value="right").pack(anchor=tk.W)
tk.Radiobutton(direction_frame, text="向左", variable=direction_var, value="left").pack(anchor=tk.W)

# 计算按钮
calculate_button = tk.Button(root, text="计算", command=calculate)
calculate_button.pack(pady=10)

# 结果显示标签
result_label = tk.Label(root, text="", justify=tk.LEFT)
result_label.pack(pady=10, fill=tk.X)

# 启动Tkinter主循环
root.mainloop()
