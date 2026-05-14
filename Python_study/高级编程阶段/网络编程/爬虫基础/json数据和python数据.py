import json

#1
#读取json数据
with open("test.json","r",encoding="utf-8") as f:
    json_data = f.read()
print(json_data)
#将json数据转化为python数据使用loads
py_data = json.loads(json_data)
print(py_data) #注意True，False，none
#将python数据转化为json数据 中文会被使用ascii码表示，给个参数
j_data = json.dumps(py_data,ensure_ascii=False,indent=4) #intend=表示每一级前方空格数量
print(j_data)
# with open("xxx.json","w",encoding="utf-8") as f: # 报错
#     f.write(py_data)  # 数据写入时只能是字符串格式，不能是字典格式，json数据是字符串

#2使用load dump模块减少文件打开步骤
json.dump(py_data,open("xxx.json","w",encoding="utf-8"),ensure_ascii=False,indent=4)
res = json.load(open("test.json","r",encoding="utf-8"))
print(res)