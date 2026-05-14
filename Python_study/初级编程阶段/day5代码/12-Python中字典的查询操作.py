person = {'name':'Tom', 'age':20, 'address':'深圳市宝安区'}
# 常规查询，直接通过字典名称[key]
print(person['name'])

# 1、get(key, 默认值) ：根据字典的key查询对应的值，如果这个值不存在，不报错，则显示默认值信息
print(person.get('mobile', '您要查询的key暂不存在'))

# 2、keys() ：主要功能用于获取字典中的所有的key，然后保存在列表中
print(person.keys())

# 3、values() ：主要功能用于获取字典中所有key对应的value值，然后保存在列表中
print(person.values())

# 4、items() ：主要以[(key,value),(key,value),(key,value)]此结构返回字典中的key:value键值对信息
print(person.items())

# person = {'name':'Tom', 'age':20, 'address':'深圳市宝安区'}
# person.items() => [('name','Tom'),('age',20),('address','深圳市宝安区')]
# for key,value in person.items():
    # 第一次循环时，系统得到列表的第一个元组('name','Tom')，然后把name赋值给key，Tom赋值给value
    # 第二次循环时，系统得到列表的第二个元组('age',20)，然后将age赋值给key，20赋值给value
    # ...

for key,value in person.items():
    # ① 字典中有多少个键值对，则for循环自动循环多少次
    # ② 每次循环时，系统会自动将得到的键值对中的键放入变量key，值放入value中
    print(f'{key} ---- {value}')