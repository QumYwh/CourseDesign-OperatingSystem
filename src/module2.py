import tkinter as tk
from tkinter import ttk


class MemoryManagerGUI:
    def __init__(self, master):
        """
        初始化主窗口，并创建内存管理器实例。
        设置窗口标题为"内存管理模拟系统"。
        """
        self.master = master
        self.master.title("内存管理模拟系统")
        self.manager = MemoryManager()  # 创建一个内存管理器实例
        self.create_widgets()  # 创建所有需要的GUI组件

    def create_widgets(self):
        """
        创建并布置GUI的所有控件，包括标签、组合框、按钮、文本输入框以及文本显示框。
        """
        # 主菜单框架
        self.main_frame = tk.Frame(self.master)
        self.main_frame.pack(padx=10, pady=10, fill=tk.X)

        # 内存分配方式的选择标签和下拉列表
        tk.Label(self.main_frame, text="选择内存分配方式：", font=("Arial", 14)).pack(side=tk.LEFT)
        self.allocation_mode = ttk.Combobox(self.main_frame, values=["固定分区方式", "可变分区方式"], state="readonly")
        self.allocation_mode.current(0)  # 默认选择第一个选项
        self.allocation_mode.pack(side=tk.LEFT, padx=5)
        self.allocation_mode.bind("<<ComboboxSelected>>", self.update_mode)  # 绑定选择改变事件

        # 操作按钮框架
        self.operation_frame = tk.Frame(self.master)
        self.operation_frame.pack(padx=10, pady=5, fill=tk.X)

        # 分配空间按钮
        self.allocate_button = tk.Button(self.operation_frame, text="分配空间", state="normal",
                                         command=self.allocate_space)
        self.allocate_button.pack(side=tk.LEFT, padx=5)

        # 释放空间按钮
        self.release_button = tk.Button(self.operation_frame, text="释放空间", state="normal",
                                        command=self.release_space)
        self.release_button.pack(side=tk.LEFT, padx=5)

        # 显示分配表按钮
        self.show_button = tk.Button(self.operation_frame, text="显示分配表", state="normal", command=self.show_table)
        self.show_button.pack(side=tk.LEFT, padx=5)

        # 输入作业名称和大小的框架
        self.entry_frame = tk.Frame(self.master)
        self.entry_frame.pack(padx=10, pady=5, fill=tk.X)

        # 作业名称标签和输入框
        self.job_name_label = tk.Label(self.entry_frame, text="作业名称：")
        self.job_name_label.pack(side=tk.LEFT)
        self.job_name_entry = tk.Entry(self.entry_frame)
        self.job_name_entry.pack(side=tk.LEFT, padx=5)

        # 作业大小标签和输入框
        self.size_label = tk.Label(self.entry_frame, text="作业大小(K)：")
        self.size_label.pack(side=tk.LEFT)
        self.size_entry = tk.Entry(self.entry_frame)
        self.size_entry.pack(side=tk.LEFT, padx=5)

        # 用于显示表格的文本框
        self.text_box = tk.Text(self.master, height=15, width=80, state="disabled")
        self.text_box.pack(padx=10, pady=5)

    def update_mode(self, event):
        """
        根据用户选择的分配模式更新UI状态。
        清空文本框内容，根据所选模式调整作业大小输入框的状态（启用或禁用）。
        """
        mode = self.allocation_mode.get()
        self.text_box.config(state="normal")
        self.text_box.delete(1.0, tk.END)  # 清除文本框内容
        self.text_box.config(state="disabled")

        if mode == "固定分区方式":
            self.setup_fixed_partition_mode()
        elif mode == "可变分区方式":
            self.setup_variable_partition_mode()

    def setup_fixed_partition_mode(self):
        """
        当选择了固定分区分配模式时设置UI状态。
        固定分区分配模式下，作业大小是固定的，所以作业大小输入框被禁用。
        """
        self.allocate_button.config(state="normal")
        self.release_button.config(state="normal")
        self.show_button.config(state="normal")
        self.size_label.config(state="disabled")
        self.size_entry.config(state="disabled")

    def setup_variable_partition_mode(self):
        """
        当选择了可变分区分配模式时设置UI状态。
        可变分区分配模式下，允许用户输入作业大小，因此作业大小输入框被启用。
        """
        self.allocate_button.config(state="normal")
        self.release_button.config(state="normal")
        self.show_button.config(state="normal")
        self.size_label.config(state="normal")
        self.size_entry.config(state="normal")

    def allocate_space(self):
        """
        根据当前选择的分配模式执行分配操作。
        如果是固定分区，则不考虑作业大小直接分配；如果是可变分区，则读取作业大小进行分配。
        分配完成后刷新分配表，并清除输入字段。
        """
        mode = self.allocation_mode.get()
        job_name = self.job_name_entry.get()

        if mode == "固定分区方式":
            self.manager.allocate_fixed(job_name)
        elif mode == "可变分区方式":
            try:
                size = int(self.size_entry.get())
                self.manager.allocate_variable(job_name, size)
            except ValueError:
                self.display_message("请输入有效的作业大小")
                return

        self.show_table()
        self.clear_input_fields()

    def release_space(self):
        """
        根据当前选择的分配模式执行释放操作。
        释放指定作业占用的空间后刷新分配表，并清除输入字段。
        """
        mode = self.allocation_mode.get()
        job_name = self.job_name_entry.get()

        if mode == "固定分区方式":
            self.manager.release_fixed(job_name)
        elif mode == "可变分区方式":
            self.manager.release_variable(job_name)

        self.show_table()
        self.clear_input_fields()

    def show_table(self):
        """
        显示当前的内存分配情况。
        根据当前选择的分配模式更新文本框中的信息。
        """
        mode = self.allocation_mode.get()
        self.text_box.config(state="normal")
        self.text_box.delete(1.0, tk.END)

        if mode == "固定分区方式":
            self.manager.display_fixed_table_gui(self.text_box)
        elif mode == "可变分区方式":
            self.manager.display_variable_table_gui(self.text_box)

        self.text_box.config(state="disabled")

    def clear_input_fields(self):
        """
        清除作业名称和作业大小输入字段的内容。
        """
        self.job_name_entry.delete(0, tk.END)
        self.size_entry.delete(0, tk.END)

    def display_message(self, message):
        """
        在文本框中显示一条消息。
        """
        self.text_box.config(state="normal")
        self.text_box.insert(tk.END, message + "\n")
        self.text_box.config(state="disabled")


class MemoryManager:
    def __init__(self):
        """
        初始化内存管理器，定义总内存大小、操作系统占用的内存大小、用户可用内存大小，
        以及固定分区和可变分区的相关属性。
        """
        self.total_memory = 128  # 总内存大小（以K为单位）
        self.os_memory = 4  # OS占用内存
        self.user_memory = self.total_memory - self.os_memory  # 用户可用内存
        self.fixed_partitions = [16, 16, 16, 16, 16, 16]  # 固定分区，每个分区16K
        self.fixed_allocation = [None] * len(self.fixed_partitions)  # 固定分区分配状态
        self.variable_free = [(self.os_memory, self.user_memory)]  # 可变分区的未分配表
        self.variable_allocated = []  # 可变分区的已分配表


    def display_fixed_table_gui(self, text_box):
        """
        将固定分区的分配情况显示在给定的文本框中。
        """
        text_box.insert(tk.END, "\n固定分区分配情况：\n")
        text_box.insert(tk.END, "分区编号\t大小(K)\t状态\n")
        for i, size in enumerate(self.fixed_partitions):
            status = self.fixed_allocation[i] if self.fixed_allocation[i] else "空闲"
            text_box.insert(tk.END, f"{i + 1}\t\t{size}\t\t{status}\n")

    def allocate_fixed(self, job_name):
        """
        在固定分区模式下为指定作业分配内存。
        遍历分区查找空闲分区，找到后将该分区分配给作业。
        如果没有空闲分区则打印错误信息。
        """
        for i in range(len(self.fixed_allocation)):
            if not self.fixed_allocation[i]:
                self.fixed_allocation[i] = job_name
                print(f"作业 {job_name} 分配到固定分区 {i + 1}")
                return
        print("没有空闲的固定分区可供分配！")

    def release_fixed(self, job_name):
        """
        在固定分区模式下释放指定作业占用的内存。
        查找并释放作业占用的分区，如果找不到则打印错误信息。
        """
        for i in range(len(self.fixed_allocation)):
            if self.fixed_allocation[i] == job_name:
                self.fixed_allocation[i] = None
                print(f"作业 {job_name} 从固定分区 {i + 1} 释放")
                return
        print("未找到该作业！")

    def display_variable_table_gui(self, text_box):
        """
        将可变分区的分配情况显示在给定的文本框中。
        """
        text_box.insert(tk.END, "\n可变分区分配情况：\n")
        text_box.insert(tk.END, "已分配表：\n")
        text_box.insert(tk.END, "起始地址(K)\t大小(K)\t作业\n")
        for start, size, job in self.variable_allocated:
            text_box.insert(tk.END, f"{start}\t\t{size}\t\t{job}\n")
        text_box.insert(tk.END, "\n未分配表：\n")
        text_box.insert(tk.END, "起始地址(K)\t大小(K)\n")
        for start, size in self.variable_free:
            text_box.insert(tk.END, f"{start}\t\t{size}\n")

    def allocate_variable(self, job_name, size):
        """
        在可变分区模式下为指定作业分配内存。
        查找足够的连续空闲空间，将其分配给作业，并更新未分配表。
        如果没有足够的空间则打印错误信息。
        """
        for i, (start, free_size) in enumerate(self.variable_free):
            if free_size >= size:
                # 分配空间
                self.variable_allocated.append((start, size, job_name))
                if free_size > size:
                    # 更新未分配表中的剩余空间
                    self.variable_free[i] = (start + size, free_size - size)
                else:
                    # 如果刚好分配完移除该空闲区
                    self.variable_free.pop(i)
                return
        print("没有足够的可用空间进行分配！")

    def release_variable(self, job_name):
        """
        在可变分区模式下释放指定作业占用的内存。
        查找并释放作业占用的空间，然后合并相邻的空闲区域。
        """
        for i, (start, size, job) in enumerate(self.variable_allocated):
            if job == job_name:
                # 释放空间
                self.variable_allocated.pop(i)
                self.variable_free.append((start, size))
                self.variable_free.sort()  # 按起始地址排序
                self.merge_free_space()  # 合并相邻空闲区域
                return
        print("未找到该作业！")

    def merge_free_space(self):
        """
        合并未分配表中相邻的空闲区域。
        """
        merged = []
        for start, size in sorted(self.variable_free):
            if merged and merged[-1][0] + merged[-1][1] == start:
                # 如果上一个区域的结束地址与当前区域的起始地址相连，合并
                merged[-1] = (merged[-1][0], merged[-1][1] + size)
            else:
                merged.append((start, size))
        self.variable_free = merged


if __name__ == "__main__":
    root = tk.Tk()
    app = MemoryManagerGUI(root)
    root.mainloop()
