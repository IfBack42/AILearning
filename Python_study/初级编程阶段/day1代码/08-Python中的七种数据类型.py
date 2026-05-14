'''
Python中一共有7种数据类型
① 基本数据类型
数值类型（int整数类型/float浮点类型），定义时直接写数字即可，不需要添加任何符号
布尔类型（只有两个值，要么为真True，要么为假False），注意Python中的布尔值必须首字母大写bool
字符串类型（在Python中通过一对引号引起来的内容就称之为字符串 => 文本信息）str

② 容器类型/数据序列
列表类型 => list，[1, 2, 3] => 数据可以发生改变
元组类型 => tuple，(1, 2, 3) => 数据一旦定义，其值就不能发生改变了
集合类型 => set，{1, 1, 2, 3} => {1, 2, 3}天生去重 => 类似select distinct 列名称
字典类型 => dict，{key:value键值对} => {'name':'张三', 'age':23, 'address':'深圳市宝安区'}，查询神器
'''
# ① 数值类型（整型数据）
a = 10
print(type(a))

# ① 数值类型（浮点类型数据，带小数点）
b = 9.99
print(type(b))

# ② 布尔类型
c = True
print(type(c))

# ③ 字符串类型
d = 'hello'
print(isinstance(d, str))  # 扩展：可以通过isinstance()函数判断一个判断是否为某种类型，返回结果True或False

# ④ 列表类型，一个变量同时保存多个元素
e = [1, 2, 3, 4, 5]
print(type(e))

# ⑤ 元组类型，功能与列表类似，但是其值一旦定义，就无法改变了
f = (1, 2, 3, 4, 5)
print(type(f))

# ⑥ 集合类型，set类型，天生去重
g = {1, 1, 3, 5, 7}
print(g)
print(type(g))

# ⑦ 字典类型，查询神器
h = {'name':'张三', 'age':23, 'address':'深圳市宝安区'}
print(type(h))