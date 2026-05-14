import multiprocessing
import os
import time
my_list = []
def func1():
    for i in range(10):
        my_list.append(i)
        time.sleep(0.5)
        print(my_list[i])
    print(f"func1_data:{my_list}")
    pid_1= os.getpid()
    print(pid_1)

def func2():
    print(f"func2_data:{my_list}")
    pid_2 = os.getpid()
    print(pid_2)
    ppid = os.getppid()
    print(ppid)

if __name__ == '__main__':
    func1_process = multiprocessing.Process(target=func1)
    func2_process = multiprocessing.Process(target=func2)
    func1_process.start()
    func2_process.start()
    pid = os.getpid()
    print(pid)
    print("主进程执行结束")