# FCFS: 先来先服务
def fcfs(service_sequence):
    total_head_movement = 0
    current_position = 0
    service_order = []

    for track in service_sequence:
        total_head_movement += abs(track - current_position)
        current_position = track
        service_order.append(track)

    return service_order, total_head_movement


# SSTF: 最短寻道优先
def sstf(service_sequence):
    total_head_movement = 0
    current_position = 0
    service_order = []
    remaining_tracks = service_sequence.copy()

    while remaining_tracks:
        # 找到距离当前磁头最近的磁道
        closest_track = min(remaining_tracks, key=lambda x: abs(x - current_position))
        total_head_movement += abs(closest_track - current_position)
        current_position = closest_track
        service_order.append(closest_track)
        remaining_tracks.remove(closest_track)

    return service_order, total_head_movement


# SCAN: 电梯算法
def scan(service_sequence, disk_size, direction='right'):
    total_head_movement = 0
    current_position = 0
    service_order = []

    # 排序服务请求
    service_sequence.sort()

    if direction == 'right':
        # 磁头向右扫描
        service_sequence = [track for track in service_sequence if track >= current_position] + \
                           [track for track in service_sequence if track < current_position][::-1]
    else:
        # 磁头向左扫描
        service_sequence = [track for track in service_sequence if track <= current_position][::-1] + \
                           [track for track in service_sequence if track > current_position]

    for track in service_sequence:
        total_head_movement += abs(track - current_position)
        current_position = track
        service_order.append(track)

    return service_order, total_head_movement


# 读取磁道请求序列
def read_track_sequence(file_path):
    with open(file_path, 'r') as file:
        track_sequence = [int(line.strip()) for line in file.readlines()]
    return track_sequence


def main():
    print("请输入磁盘调度算法：")
    print("1. 先来先服务 (FCFS)")
    print("2. 最短寻道优先 (SSTF)")
    print("3. 电梯算法 (SCAN)")

    choice = input("请选择调度算法（1/2/3）：")

    file_path = input("请输入磁道请求序列文件路径：")
    track_sequence = read_track_sequence(file_path)
    disk_size = int(input("请输入磁盘的总磁道数："))
    direction = 'right'

    if choice == '1':
        service_order, total_head_movement = fcfs(track_sequence)
    elif choice == '2':
        service_order, total_head_movement = sstf(track_sequence)
    elif choice == '3':
        # 电梯算法需要知道磁头初始方向
        direction = input("请输入磁头初始方向（left/right）：").strip().lower()
        service_order, total_head_movement = scan(track_sequence, disk_size, direction)
    else:
        print("无效的选择！")
        return

    print("磁道的服务顺序：", service_order)
    print("移动的总道数：", total_head_movement)


if __name__ == "__main__":
    main()
