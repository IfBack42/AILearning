import memory_profiler as mem
import time
start = time.time()
#获取程序开始前的内存信息
# start_mem = mem.memory_usage()
# print(start_mem)
# test_list = [i * i for i in range(10000000)]
test_list = (i * i for i in range(1000000))
# print(next(test_list))
#获取程序结束前的内存信息
# end_mem = mem.memory_usage()
end = time.time()
print(f"{end-start}")
# print(end_mem)