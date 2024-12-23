class MemoryManager:
    def __init__(self):
        self.total_memory = 128  # 总内存大小（以K为单位）
        self.os_memory = 4  # OS占用内存
        self.user_memory = self.total_memory - self.os_memory  # 用户可用内存
        self.fixed_partitions = [16, 16, 16, 16, 16, 16]  # 固定分区，每个分区16K
        self.fixed_allocation = [None] * len(self.fixed_partitions)  # 固定分区分配状态
        self.variable_free = [(0, self.user_memory)]  # 可变分区的未分配表
        self.variable_allocated = []  # 可变分区的已分配表

    def display_fixed_table(self):
        print("\n固定分区分配情况：")
        print("分区编号\t大小(K)\t状态")
        for i, size in enumerate(self.fixed_partitions):
            status = self.fixed_allocation[i] if self.fixed_allocation[i] else "空闲"
            print(f"{i + 1}\t\t{size}\t\t{status}")

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

    def display_variable_table(self):
        print("\n可变分区分配情况：")
        print("已分配表：")
        print("起始地址(K)\t大小(K)\t作业")
        for start, size, job in self.variable_allocated:
            print(f"{start}\t\t{size}\t\t{job}")
        print("\n未分配表：")
        print("起始地址(K)\t大小(K)")
        for start, size in self.variable_free:
            print(f"{start}\t\t{size}")

    def allocate_variable(self, job_name, size):
        for i, (start, free_size) in enumerate(self.variable_free):
            if free_size >= size:
                self.variable_allocated.append((start, size, job_name))
                self.variable_free[i] = (start + size, free_size - size)
                if self.variable_free[i][1] == 0:
                    self.variable_free.pop(i)
                print(f"作业 {job_name} 分配成功，占用 {size}K 空间")
                return
        print("没有足够的可用空间进行分配！")

    def release_variable(self, job_name):
        for i, (start, size, job) in enumerate(self.variable_allocated):
            if job == job_name:
                self.variable_allocated.pop(i)
                self.variable_free.append((start, size))
                self.variable_free.sort()
                self.merge_free_space()
                print(f"作业 {job_name} 释放成功，释放 {size}K 空间")
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


def main():
    manager = MemoryManager()

    while True:
        print("\n=== 内存管理程序 ===")
        print("1. 固定分区方式")
        print("2. 可变分区方式")
        print("3. 退出")
        choice = input("请选择操作: ")

        if choice == "1":
            while True:
                print("\n=== 固定分区方式 ===")
                print("1. 分配空间")
                print("2. 释放空间")
                print("3. 显示分配表")
                print("4. 返回主菜单")
                fixed_choice = input("请选择操作: ")

                if fixed_choice == "1":
                    job_name = input("请输入作业名称: ")
                    manager.allocate_fixed(job_name)
                elif fixed_choice == "2":
                    job_name = input("请输入作业名称: ")
                    manager.release_fixed(job_name)
                elif fixed_choice == "3":
                    manager.display_fixed_table()
                elif fixed_choice == "4":
                    break
                else:
                    print("无效的选择！")

        elif choice == "2":
            while True:
                print("\n=== 可变分区方式 ===")
                print("1. 分配空间")
                print("2. 释放空间")
                print("3. 显示分配表")
                print("4. 返回主菜单")
                variable_choice = input("请选择操作: ")

                if variable_choice == "1":
                    job_name = input("请输入作业名称: ")
                    size = int(input("请输入作业大小(K): "))
                    manager.allocate_variable(job_name, size)
                elif variable_choice == "2":
                    job_name = input("请输入作业名称: ")
                    manager.release_variable(job_name)
                elif variable_choice == "3":
                    manager.display_variable_table()
                elif variable_choice == "4":
                    break
                else:
                    print("无效的选择！")

        elif choice == "3":
            print("退出程序！")
            break

        else:
            print("无效的选择！")


if __name__ == "__main__":
    main()
