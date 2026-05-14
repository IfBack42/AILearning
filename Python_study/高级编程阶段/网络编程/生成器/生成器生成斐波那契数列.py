import memory_profiler as mem
start = mem.memory_usage()
print(start)
#生成器生成斐波那契是递推
def fib(max):
    n = 1
    m = 2
    for i in range(max): #想了半天上一位数跟循环次数i的关系，他妈发现没关系，直接糙俩变量来记录
        if i < 2:
            yield 1
        else:
            yield m
            n, m = m, m + n

f = fib(40)
for i in f:
    print(i)
end = mem.memory_usage()
print(end)