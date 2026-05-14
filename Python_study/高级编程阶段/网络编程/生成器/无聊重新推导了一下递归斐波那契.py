import memory_profiler as mem
import time
start_time = time.time()
start = mem.memory_usage()
print(start)
#递归函数反复调用自身到后面次数非常恐怖
#不过递归函数返回值也会及时销毁没用的数据
def func(max):
    if max <= 2:
        return 1
    else:
        return func(max -1) + func(max - 2)

print(func(35))
end = mem.memory_usage()
end_time = time.time()
print(end_time-start_time)
print(end)