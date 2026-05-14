'''
要求上传一张图片，通过Python代码获取图片的名称以及图片的后缀名（.jpg/.png/.gif）
hlw.png
rfind = right find，代表从右开始查询第一个出现的搜索字符
'''
filename = input('请输入要上传文件的名称：')
# 判断文件名称是否包含.点号
index = filename.rfind('.')
# 获取文件的名称
print(filename[:index])
# 获取文件的后缀名
print(filename[index:])