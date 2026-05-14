"""
假设有一个仓库，仓库的容量为10。编写一个 Python 程序来模拟生产者-消费者场景。程序需要使用多线程的方式实现生产者向仓库中放入产品，
消费者从仓库中取出产品，并输出每次操作的结果。

要求：

定义一个全局变量 warehouse 来表示仓库，初始为空列表。
定义一个全局变量 capacity 来表示仓库的容量，初始为10。
定义一个生产者函数 producer()，函数内部实现将产品放入仓库的逻辑。
定义一个消费者函数 consumer()，函数内部实现从仓库中取出产品的逻辑。
使用多线程的方式同时启动多个生产者和消费者线程，并模拟生产者向仓库放入产品，消费者从仓库取出产品的过程。
每次成功放入产品或取出产品后，输出当前操作的结果。

# start_producer(3)  # 启动3个生产者线程
# start_consumer(2)  # 启动2个消费者线程
#
# 如下是运行过程中的打印
# Producer 1: Produced product 1
# Producer 2: Produced product 2
# Producer 1: Produced product 3
# Consumer 1: Consumed product 1
# Consumer 2: Consumed product 2
# Producer 2: Produced product 4
# Producer 3: Produced product 5
# Consumer 1: Consumed product 3
# Producer 1: Produced product 6
# Consumer 2: Consumed product 4
"""
import threading
from time import sleep

warehouse = []
capacity = 10

def producer(i):
    while len(warehouse) < 9:
        j = len(warehouse) + 1
        print(f"Producer {i + 1}:Produced product {j}")
        warehouse.append(f"product {j}")
        sleep(0.5)

def consumer(i):
    sleep(1)
    for j in warehouse:
        warehouse.remove(j)
        print(f"Consumer {i + 1}: Consumed product{j}")
        sleep(0.5)

def start_producer(n):
    for i in range(n):
        producer_thread = threading.Thread(target=producer,args=(i,))
        producer_thread.start()


def start_consumer(n):
    for i in range(n):
        consumer_thread = threading.Thread(target=consumer,args=(i,))
        consumer_thread.start()


if __name__ == '__main__':
    start_consumer(3)
    start_producer(3)