a = 10
print(type(a))
b = 9.99
print(type(b))
c = True
print(type(c))
d = 'wocaonima'
print(type(d))
print(isinstance(d, str))  #前面为变量，后面为数据类型，判断是否为真
print(isinstance(d, int))
e = [1, 2, 3]  #列表类型——其实就是他妈的数组，Python确实太无脑了
print(type(e))
f = (1 ,2 ,3) #元组类型，和列表类型相似，但是定义过后不能改
print(type(f))
g = {1 ,1 ,1 ,2, 3, 3, 3,5} # set 集合类型，天生去重
print(g)
print(type(g))
h = {'name':'肖杰','gender':'无','母亲':'无'} # 字典类型，数据查询神器，键值对表示
print(h)
print(type(h))

print(a,end = "\n" , b,end = "\n" , c,end = "\n"  )