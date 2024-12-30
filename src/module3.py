import tkinter as tk
from tkinter import filedialog, messagebox
import collections


# FIFO页面调度算法
def fifo(page_sequence, frame_size):
    frames = []  # 用于存储页面的列表
    page_faults = 0  # 缺页次数
    evicted_pages = []  # 淘汰的页面

    # 遍历页面序列
    for page in page_sequence:
        # 如果页面不在框架中，发生缺页
        if page not in frames:
            if len(frames) < frame_size:  # 如果框架还有空间
                frames.append(page)  # 加载页面
            else:
                evicted_page = frames.pop(0)  # 淘汰最先进入的页面
                evicted_pages.append(evicted_page)  # 记录被淘汰的页面
                frames.append(page)  # 加载新页面
            page_faults += 1  # 增加缺页次数

    return evicted_pages, page_faults  # 返回淘汰的页面和缺页次数


# LRU页面调度算法
def lru(page_sequence, frame_size):
    frames = collections.OrderedDict()  # 有序字典，用于模拟LRU（按访问顺序维护页面）
    page_faults = 0  # 缺页次数
    evicted_pages = []  # 淘汰的页面

    # 遍历页面序列
    for page in page_sequence:
        if page not in frames:
            if len(frames) >= frame_size:  # 如果框架已满
                evicted_page, _ = frames.popitem(last=False)  # 淘汰最久未使用的页面
                evicted_pages.append(evicted_page)  # 记录被淘汰的页面
            frames[page] = True  # 加载页面，标记为最近使用
            page_faults += 1  # 增加缺页次数
        else:
            frames.move_to_end(page)  # 如果页面已存在，更新其为最近使用

    return evicted_pages, page_faults  # 返回淘汰的页面和缺页次数


# LFU 页面调度算法
def lfu(page_sequence, frame_size):
    frames = {}  # 存储页面及其加载顺序
    frequency = collections.defaultdict(int)  # 页面访问频率
    page_faults = 0  # 缺页次数
    evicted_pages = []  # 淘汰的页面

    # 遍历页面序列
    for page in page_sequence:
        if page not in frames:
            # 如果框架已满，淘汰访问频率最低的页面
            if len(frames) >= frame_size:
                least_frequent_page = min(frames, key=lambda x: (frequency[x], frames[x]))  # 找到频率最低的页面
                evicted_pages.append(least_frequent_page)  # 记录淘汰的页面
                frames.pop(least_frequent_page)  # 移除该页面
                del frequency[least_frequent_page]  # 删除该页面的访问频率

            frames[page] = len(frames)  # 记录页面加载顺序
            page_faults += 1  # 增加缺页次数

        # 更新页面的访问频率
        frequency[page] += 1

    return evicted_pages, page_faults  # 返回淘汰的页面和缺页次数


# 读取页面序列
def read_page_sequence(file_path):
    with open(file_path, 'r') as file:
        page_sequence = [int(line.strip()) for line in file.readlines()]  # 从文件中读取页面序列
    return page_sequence


# GUI 主窗口 (GUI Main window)
class PageSchedulingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("页面调度算法")  # 设置窗口标题
        self.root.geometry("700x550")  # 设置窗口大小

        # 标签和输入框 (Labels and Input fields)
        self.algorithm_label = tk.Label(root, text="选择页面调度算法")  # 标签：选择页面调度算法
        self.algorithm_label.pack(pady=10)  # 将标签加入窗口，并设置上下间距

        self.algorithm_var = tk.StringVar()  # 创建字符串变量来保存算法选择
        self.algorithm_var.set("1")  # 默认选择FIFO

        # FIFO、LRU、LFU的单选按钮 (Radio buttons for FIFO, LRU, LFU)
        self.fifo_rb = tk.Radiobutton(root, text="FIFO", variable=self.algorithm_var, value="1", command=self.clear_text)
        self.fifo_rb.pack()  # FIFO按钮

        self.lru_rb = tk.Radiobutton(root, text="LRU", variable=self.algorithm_var, value="2", command=self.clear_text)
        self.lru_rb.pack()  # LRU按钮

        self.lfu_rb = tk.Radiobutton(root, text="LFU", variable=self.algorithm_var, value="3", command=self.clear_text)
        self.lfu_rb.pack()  # LFU按钮

        # 页面框架大小输入框 (Input field for frame size)
        self.frame_size_label = tk.Label(root, text="页面框架大小:")  # 标签：页面框架大小
        self.frame_size_label.pack(pady=5)

        self.frame_size_entry = tk.Entry(root)  # 输入框：框架大小
        self.frame_size_entry.pack()

        # 文件路径显示框和浏览按钮 (File path display field and browse button)
        self.file_label = tk.Label(root, text="选择页面序列文件:")  # 标签：选择页面序列文件
        self.file_label.pack(pady=5)

        self.file_path_entry = tk.Entry(root, width=90)  # 输入框：显示文件路径
        self.file_path_entry.pack(pady=5)

        self.browse_button = tk.Button(root, text="浏览", command=self.load_file)  # 按钮：浏览按钮
        self.browse_button.pack(pady=5)

        # 结果显示框 (Text area to display results)
        self.result_text = tk.Text(root, width=50, height=10)
        self.result_text.pack()

        # 运行按钮 (Run button)
        self.run_button = tk.Button(root, text="运行", command=self.run_algorithm)  # 按钮：运行按钮
        self.run_button.pack(pady=10)

        self.file_path = None  # 文件路径初始值为空

    # 选择文件 (Load file function)
    def load_file(self):
        self.file_path = filedialog.askopenfilename(title="选择页面序列文件", filetypes=[("Text Files", "*.txt")])  # 打开文件选择对话框
        self.file_path_entry.delete(0, tk.END)  # 清空原来的文件路径
        self.file_path_entry.insert(0, self.file_path)  # 显示选择的文件路径

    # 清空文本框 (Clear text area)
    def clear_text(self):
        self.result_text.delete(1.0, tk.END)  # 清空结果显示框中的文本

    # 运行页面调度算法 (Run the page scheduling algorithm)
    def run_algorithm(self):
        if not self.file_path:
            messagebox.showerror("错误", "请先选择页面序列文件")  # 弹出错误提示，文件路径为空
            return

        try:
            page_sequence = read_page_sequence(self.file_path)  # 读取页面序列
            frame_size = int(self.frame_size_entry.get())  # 获取框架大小
            if frame_size <= 0:
                messagebox.showerror("错误", "页面框架大小必须大于0")  # 弹出错误提示，框架大小小于等于0
                return

            # 根据选择的算法运行相应的页面调度算法
            algorithm_choice = self.algorithm_var.get()
            if algorithm_choice == '1':
                evicted_pages, page_faults = fifo(page_sequence, frame_size)  # FIFO算法
            elif algorithm_choice == '2':
                evicted_pages, page_faults = lru(page_sequence, frame_size)  # LRU算法
            elif algorithm_choice == '3':
                evicted_pages, page_faults = lfu(page_sequence, frame_size)  # LFU算法
            else:
                messagebox.showerror("错误", "无效的选择")  # 弹出错误提示，选择无效
                return

            # 显示结果 (Display results)
            result = f"每次淘汰的页面号: {evicted_pages}\n缺页总次数: {page_faults}"
            self.result_text.delete(1.0, tk.END)  # 清空文本框
            self.result_text.insert(tk.END, result)  # 插入结果文本

            # 清空框架大小输入框 (Clear the frame size input)
            self.frame_size_entry.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror("错误", f"发生错误: {str(e)}")  # 弹出错误提示，发生异常


# 创建并运行GUI应用 (Create and run the GUI application)
def main():
    root = tk.Tk()  # 创建主窗口
    app = PageSchedulingApp(root)  # 初始化应用
    root.mainloop()  # 进入主循环


if __name__ == "__main__":
    main()  # 执行主函数
