import threading
from time import sleep


def func_a():
    for i in range(5):
        print('任务A')
        sleep(1)


def func_b():
    for i in range(5):
        print('任务B')
        sleep(1)

if __name__ == '__main__':
    func_a_thead = threading.Thread(target=func_a)
    func_b_thead = threading.Thread(target=func_b)
    func_b_thead.daemon = True
    func_a_thead.daemon = True
    func_b_thead.start()
    func_a_thead.start()
    print("主程序结束哥哥")