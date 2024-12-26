import tkinter as tk
from tkinter import filedialog, messagebox
import collections


# FIFO页面调度算法
def fifo(page_sequence, frame_size):
    frames = []
    page_faults = 0
    evicted_pages = []

    for page in page_sequence:
        if page not in frames:
            if len(frames) < frame_size:
                frames.append(page)
            else:
                evicted_page = frames.pop(0)  # 淘汰最先进入的页面
                evicted_pages.append(evicted_page)
                frames.append(page)
            page_faults += 1

    return evicted_pages, page_faults


# LRU页面调度算法
def lru(page_sequence, frame_size):
    frames = collections.OrderedDict()  # 有序字典，用于模拟LRU
    page_faults = 0
    evicted_pages = []

    for page in page_sequence:
        if page not in frames:
            if len(frames) >= frame_size:
                evicted_page, _ = frames.popitem(last=False)  # 淘汰最久未使用的页面
                evicted_pages.append(evicted_page)
            frames[page] = True
            page_faults += 1
        else:
            frames.move_to_end(page)  # 将页面移动到字典末尾，表示最近使用

    return evicted_pages, page_faults


# LFU页面调度算法
# 优化后的 LFU 页面调度算法
def lfu(page_sequence, frame_size):
    frames = {}  # 存储页面及其访问频率
    frequency = collections.defaultdict(int)  # 页面访问频率
    page_faults = 0
    evicted_pages = []

    for page in page_sequence:
        if page not in frames:
            # 如果框架已满，淘汰访问频率最低的页面
            if len(frames) >= frame_size:
                # 找出频率最低的页面，如果频率相同，淘汰最早加载的页面
                least_frequent_page = min(frames, key=lambda x: (frequency[x], frames[x]))
                evicted_pages.append(least_frequent_page)
                frames.pop(least_frequent_page)
                del frequency[least_frequent_page]

            # 加载新页面
            frames[page] = len(frames)  # 记录页面加载顺序（用于处理频率相同时的优先级）
            page_faults += 1

        # 更新访问频率
        frequency[page] += 1

    return evicted_pages, page_faults


# 读取页面序列
def read_page_sequence(file_path):
    with open(file_path, 'r') as file:
        page_sequence = [int(line.strip()) for line in file.readlines()]
    return page_sequence


# GUI 主窗口
class PageSchedulingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("页面调度算法")
        self.root.geometry("400x450")

        # 标签和输入框
        self.algorithm_label = tk.Label(root, text="选择页面调度算法")
        self.algorithm_label.pack(pady=10)

        self.algorithm_var = tk.StringVar()
        self.algorithm_var.set("1")  # 默认选择FIFO

        self.fifo_rb = tk.Radiobutton(root, text="FIFO", variable=self.algorithm_var, value="1",
                                      command=self.clear_text)
        self.fifo_rb.pack()

        self.lru_rb = tk.Radiobutton(root, text="LRU", variable=self.algorithm_var, value="2", command=self.clear_text)
        self.lru_rb.pack()

        self.lfu_rb = tk.Radiobutton(root, text="LFU", variable=self.algorithm_var, value="3", command=self.clear_text)
        self.lfu_rb.pack()

        self.frame_size_label = tk.Label(root, text="页面框架大小:")
        self.frame_size_label.pack(pady=5)

        self.frame_size_entry = tk.Entry(root)
        self.frame_size_entry.pack()

        self.file_button = tk.Button(root, text="选择页面序列文件", command=self.load_file)
        self.file_button.pack(pady=10)

        self.result_text = tk.Text(root, width=50, height=10)
        self.result_text.pack()

        self.run_button = tk.Button(root, text="运行", command=self.run_algorithm)
        self.run_button.pack(pady=10)

        self.file_path = None

    # 选择文件
    def load_file(self):
        self.file_path = filedialog.askopenfilename(title="选择页面序列文件", filetypes=[("Text Files", "*.txt")])

    # 清空文本框
    def clear_text(self):
        self.result_text.delete(1.0, tk.END)

    # 运行页面调度算法
    def run_algorithm(self):
        if not self.file_path:
            messagebox.showerror("错误", "请先选择页面序列文件")
            return

        try:
            page_sequence = read_page_sequence(self.file_path)
            frame_size = int(self.frame_size_entry.get())
            if frame_size <= 0:
                messagebox.showerror("错误", "页面框架大小必须大于0")
                return

            algorithm_choice = self.algorithm_var.get()
            if algorithm_choice == '1':
                evicted_pages, page_faults = fifo(page_sequence, frame_size)
            elif algorithm_choice == '2':
                evicted_pages, page_faults = lru(page_sequence, frame_size)
            elif algorithm_choice == '3':
                evicted_pages, page_faults = lfu(page_sequence, frame_size)
            else:
                messagebox.showerror("错误", "无效的选择")
                return

            result = f"每次淘汰的页面号: {evicted_pages}\n缺页总次数: {page_faults}"
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, result)

            # 清空框架大小输入框
            self.frame_size_entry.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror("错误", f"发生错误: {str(e)}")


# 创建并运行GUI应用
def main():
    root = tk.Tk()
    app = PageSchedulingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
