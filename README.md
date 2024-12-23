# CourseDesign-OperatingSystem
fosu操作系统期末课程设计
要求实现操作系统的四个管理模块（语言不限）。

1、进程管理模块设计
要求设计一个允许多个进程并发运行的进程管理模拟系统。该系统包括有简单的进程控制、进程调度算法可任意选择。每个进程用一个PCB表示，其内容根据具体情况设置。各进程之间有一定的同步关系（可选）。系统在运行过程中应能显示或打印各进程的状态及有关参数的变化情况，以便观察诸进程的运行过程及系统的管理过程。
输入：创建一个进程；或模拟时间进度。
输出：当前全部进程的状态。

2、存贮器管理模块设计
设计一个模拟计算机分配内存的管理程序，实现以下两种分配方式：固定分区方式、可变分区方式。设共有128K空间，其中前4K被OS占用，可分配的作业空间从4K地址开始。要求用菜单形式实现程序。主菜单选择：固定分区，或可变分区方式。每种分配方式再细分为：分配空间、释放空间、返回主菜单。固定分区表用一个表格的形式显示分配情况；可变分区表用已分配表、未分配表分别显示。
输入：菜单上选择某项操作，输入对应数据。
输出：内存分配的情况（包括已分配分区以及未分配分区）

3、虚拟存储器管理模块设计
设计虚拟存储器管理模块，实现三种页面调度算法：FIFO、最近最少使用调度算法（LRU）、最近最不常用调度算法（LFU）。
输入：页面序列从指定的文本文件（TXT文件）中取出。
输出：第一行：每次淘汰的页面号，第二行：缺页总次数。

4、文件管理模块设计
实现三种磁盘调度算法：先来先服务、最短寻道优先、电梯算法。
输入：磁道服务顺序从指定的文本文件（TXT文件）中取出。
输出：第一行：磁道的服务顺序；第二行：显示移动总道数。