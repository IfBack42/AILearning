import time
def time_co(fn):
    def inner():
        x1 = time.time()
        fn()
        x2 = time.time()
        print(x2 - x1)
    return inner

@time_co
def func():
    list_ = []
    for i in range(1000000):
        list_.append(i)
    print(list_)
func()