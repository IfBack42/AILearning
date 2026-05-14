'''
字典的新增操作与修改操作语法基本是一致的
字典名称[key] = value
如果字典中没有这个key，则表示新增操作
如果字典中存在这个key，则表示更新操作
'''
person = {'name':'孙悟空', 'age':600, 'address':'花果山'}
# 修改address值为东土大唐
person['address'] = '东土大唐'
print(person)