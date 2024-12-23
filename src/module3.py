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
def lfu(page_sequence, frame_size):
    frames = {}
    page_faults = 0
    evicted_pages = []
    frequency = collections.defaultdict(int)  # 页面访问频率

    for page in page_sequence:
        if page not in frames:
            if len(frames) >= frame_size:
                # 淘汰访问频率最低的页面，若有多个，淘汰最早加载的
                least_frequent_page = min(frequency, key=lambda x: (frequency[x], page_sequence.index(x)))
                frames.pop(least_frequent_page)
                evicted_pages.append(least_frequent_page)
            frames[page] = True
            page_faults += 1
        frequency[page] += 1

    return evicted_pages, page_faults

# 读取页面序列
def read_page_sequence(file_path):
    with open(file_path, 'r') as file:
        page_sequence = [int(line.strip()) for line in file.readlines()]
    return page_sequence

def main():
    print("请输入页面调度算法：")
    print("1. FIFO")
    print("2. LRU")
    print("3. LFU")
    choice = input("请选择调度算法（1/2/3）：")

    file_path = input("请输入页面序列文件路径：")
    page_sequence = read_page_sequence(file_path)
    frame_size = int(input("请输入页面框架大小："))

    if choice == '1':
        evicted_pages, page_faults = fifo(page_sequence, frame_size)
    elif choice == '2':
        evicted_pages, page_faults = lru(page_sequence, frame_size)
    elif choice == '3':
        evicted_pages, page_faults = lfu(page_sequence, frame_size)
    else:
        print("无效的选择！")
        return

    print("每次淘汰的页面号：", evicted_pages)
    print("缺页总次数：", page_faults)

if __name__ == "__main__":
    main()
