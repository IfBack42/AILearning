import re
str1 = "wocaonimaxiaojie"
result1 = re.match(r".*(xiaojie)",str1)
print(result1.group())          #match:从头开始匹配，返回Match对象，需要group提取

str2 = "111大哥真送吗"
result2 = re.match(r"(\d)\1\1",str2)
print(result2.group())

str3 = "hello xiaojie,hello yuhuaichun"
result3 = re.findall(r"hello (xiaojie|yuhuaichun)",str3)
if result3:
    for i in result3:           #findall:查找整个字符串，返回找到内容的列表，遍历就行
        print(i)

#多用命名而不是直接group（1）这种，?P<>也不麻烦
str4 = "<book></book>"
pattern = r"<(?P<mark>\w+)></(?P=mark)>"
result4 = re.search(pattern,str4)
print(result4.group())          #search:查找整个字符串，找到一个对象就收手，需要提取

list1 = ["xiaojie","zhangzheng","yuhuiachun","zhengchao"]
str5 = str(list1)
result5 = re.finditer("(xiaojie|zhengchao)",str5)
if result5:                     #finditer:查找整个字符串，返回可遍历对象，需要提取
    for i in result5:
        print(i.group())

str6 = "1914295436@qq.com, go@126.com, hentai123@163.com"
result6 = re.finditer(r"\w+@(qq|126|163)\.com",str6)
if result6:
    for i in result6:
        print(i.group())

str7 = "xiaojie:fw, yuhuaichun:gou"
result7 = re.split(":",str7)
print(result7)
str8 = "abc123wocaonima"           #split:根据法则切割为列表
result8 = re.split("123",str8)
print(result8)

#预加载，先把正则表达式赋值给变量
pattern_ = re.compile(r"\d+")
#然后后面直接可以用pattern_充当表达式
# xxx = patern_.findall(#需要匹配的内容)





