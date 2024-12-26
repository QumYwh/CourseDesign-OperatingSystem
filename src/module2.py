import tkinter as tk
from tkinter import ttk


class MemoryManagerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("内存管理模拟系统")

        self.manager = MemoryManager()

        self.create_widgets()

    def create_widgets(self):
        # Frame for the main menu
        self.main_frame = tk.Frame(self.master)
        self.main_frame.pack(padx=10, pady=10, fill=tk.X)

        tk.Label(self.main_frame, text="选择内存分配方式：", font=("Arial", 14)).pack(side=tk.LEFT)

        self.allocation_mode = ttk.Combobox(self.main_frame, values=["固定分区方式", "可变分区方式"], state="readonly")
        self.allocation_mode.current(0)
        self.allocation_mode.pack(side=tk.LEFT, padx=5)
        self.allocation_mode.bind("<<ComboboxSelected>>", self.update_mode)

        # Create a frame for operation buttons
        self.operation_frame = tk.Frame(self.master)
        self.operation_frame.pack(padx=10, pady=5, fill=tk.X)

        self.allocate_button = tk.Button(self.operation_frame, text="分配空间", state="normal",
                                         command=self.allocate_space)
        self.allocate_button.pack(side=tk.LEFT, padx=5)

        self.release_button = tk.Button(self.operation_frame, text="释放空间", state="normal",
                                        command=self.release_space)
        self.release_button.pack(side=tk.LEFT, padx=5)

        self.show_button = tk.Button(self.operation_frame, text="显示分配表", state="normal", command=self.show_table)
        self.show_button.pack(side=tk.LEFT, padx=5)

        # Entry for job name and size (if applicable)
        self.entry_frame = tk.Frame(self.master)
        self.entry_frame.pack(padx=10, pady=5, fill=tk.X)

        self.job_name_label = tk.Label(self.entry_frame, text="作业名称：")
        self.job_name_label.pack(side=tk.LEFT)
        self.job_name_entry = tk.Entry(self.entry_frame)
        self.job_name_entry.pack(side=tk.LEFT, padx=5)

        self.size_label = tk.Label(self.entry_frame, text="作业大小(K)：")
        self.size_label.pack(side=tk.LEFT)
        self.size_entry = tk.Entry(self.entry_frame)
        self.size_entry.pack(side=tk.LEFT, padx=5)

        # Text box to display tables
        self.text_box = tk.Text(self.master, height=15, width=80, state="disabled")
        self.text_box.pack(padx=10, pady=5)

    def update_mode(self, event):
        """Update UI based on selected allocation mode"""
        mode = self.allocation_mode.get()
        self.text_box.config(state="normal")
        self.text_box.delete(1.0, tk.END)  # Clear text box when changing modes
        self.text_box.config(state="disabled")

        if mode == "固定分区方式":
            self.setup_fixed_partition_mode()
        elif mode == "可变分区方式":
            self.setup_variable_partition_mode()

    def setup_fixed_partition_mode(self):
        """Setup UI for fixed partition allocation"""
        self.allocate_button.config(state="normal")
        self.release_button.config(state="normal")
        self.show_button.config(state="normal")
        self.size_label.config(state="disabled")
        self.size_entry.config(state="disabled")

    def setup_variable_partition_mode(self):
        """Setup UI for variable partition allocation"""
        self.allocate_button.config(state="normal")
        self.release_button.config(state="normal")
        self.show_button.config(state="normal")
        self.size_label.config(state="normal")
        self.size_entry.config(state="normal")

    def allocate_space(self):
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
        mode = self.allocation_mode.get()
        job_name = self.job_name_entry.get()

        if mode == "固定分区方式":
            self.manager.release_fixed(job_name)
        elif mode == "可变分区方式":
            self.manager.release_variable(job_name)

        self.show_table()
        self.clear_input_fields()

    def show_table(self):
        mode = self.allocation_mode.get()
        self.text_box.config(state="normal")
        self.text_box.delete(1.0, tk.END)

        if mode == "固定分区方式":
            self.manager.display_fixed_table_gui(self.text_box)
        elif mode == "可变分区方式":
            self.manager.display_variable_table_gui(self.text_box)

        self.text_box.config(state="disabled")

    def clear_input_fields(self):
        """Clear the job name and job size input fields"""
        self.job_name_entry.delete(0, tk.END)
        self.size_entry.delete(0, tk.END)

    def display_message(self, message):
        """Displays a message in the text box"""
        self.text_box.config(state="normal")
        self.text_box.insert(tk.END, message + "\n")
        self.text_box.config(state="disabled")


class MemoryManager:
    def __init__(self):
        self.total_memory = 128  # 总内存大小（以K为单位）
        self.os_memory = 4  # OS占用内存
        self.user_memory = self.total_memory - self.os_memory  # 用户可用内存
        self.fixed_partitions = [16, 16, 16, 16, 16, 16]  # 固定分区，每个分区16K
        self.fixed_allocation = [None] * len(self.fixed_partitions)  # 固定分区分配状态
        self.variable_free = [(4, self.user_memory - 4)]  # 可变分区的未分配表，4K 起始地址
        self.variable_allocated = []  # 可变分区的已分配表

    def display_fixed_table_gui(self, text_box):
        """Display fixed partition table in the text box"""
        text_box.insert(tk.END, "\n固定分区分配情况：\n")
        text_box.insert(tk.END, "分区编号\t大小(K)\t状态\n")
        for i, size in enumerate(self.fixed_partitions):
            status = self.fixed_allocation[i] if self.fixed_allocation[i] else "空闲"
            text_box.insert(tk.END, f"{i + 1}\t\t{size}\t\t{status}\n")

    def allocate_fixed(self, job_name):
        for i in range(len(self.fixed_allocation)):
            if not self.fixed_allocation[i]:
                self.fixed_allocation[i] = job_name
                print(f"作业 {job_name} 分配到固定分区 {i + 1}")
                return
        print("没有空闲的固定分区可供分配！")

    def release_fixed(self, job_name):
        for i in range(len(self.fixed_allocation)):
            if self.fixed_allocation[i] == job_name:
                self.fixed_allocation[i] = None
                print(f"作业 {job_name} 从固定分区 {i + 1} 释放")
                return
        print("未找到该作业！")

    def display_variable_table_gui(self, text_box):
        """Display variable partition table in the text box"""
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
        for i, (start, free_size) in enumerate(self.variable_free):
            if free_size >= size:
                self.variable_allocated.append((start, size, job_name))
                self.variable_free[i] = (start + size, free_size - size)
                if self.variable_free[i][1] == 0:
                    self.variable_free.pop(i)
                return
        print("没有足够的可用空间进行分配！")

    def release_variable(self, job_name):
        for i, (start, size, job) in enumerate(self.variable_allocated):
            if job == job_name:
                self.variable_allocated.pop(i)
                self.variable_free.append((start, size))
                self.variable_free.sort()
                self.merge_free_space()
                return
        print("未找到该作业！")

    def merge_free_space(self):
        merged = []
        for start, size in sorted(self.variable_free):
            if merged and merged[-1][0] + merged[-1][1] == start:
                merged[-1] = (merged[-1][0], merged[-1][1] + size)
            else:
                merged.append((start, size))
        self.variable_free = merged


if __name__ == "__main__":
    root = tk.Tk()
    app = MemoryManagerGUI(root)
    root.mainloop()
