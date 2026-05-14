def xioajie(fn):
    def inner(x1,x2):
        print("张正wcnm")
        fn(x1,x2)
    return inner
@xioajie
def zhangzheng(x1,x2):
   print(x1,x2)
zhangzheng(1,2)


