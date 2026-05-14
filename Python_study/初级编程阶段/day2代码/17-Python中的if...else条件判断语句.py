'''
if...else...基本语法
if 条件判断:
    如果以上条件为True，则执行缩进代码
else:
    如果条件判断为False，则自动else中的缩进代码
'''
age = int(input('请输入您的年龄：'))
if age >= 18:
    print('已成年，可以正常上网！')
else:
    print('您还未成年，回家好好学习，天天向上！')