from pyquery import PyQuery
#主要是对数据进行修改调整功能很强大，让数据整齐方便操作

html1 = """
    <li><a href="https://www.baiadu.com"><a/></li>
"""

#初始化
# p = PyQuery(html1)
# print(p)
# print(type(p))

#pyquery对象直接（css选择器）提取内容
# a = p("a") # 也可以 p("li")("a") => 链式操作
#a也是pyquery对象，可以进一步提取
# print(a)

#a = p("li a") # 后代选择器
# print(a)

html2 = """
<ul>
    <li class = "aaa"><a href="https://www.baiadu.com">百度</a></li>
    <li class = "bbb" id ="米哈游"><a href="https://www.hoyomix.com">米哈游</a></li>
    <li class = "bbb"><a href="https://www.genshen.com">原神</a></li>
    <li class = "bbb"><a href="https://www.zzz.com">绝区零</a></li>
    <li class = "bbb"><a href="https://www.mrfz.com">明日方舟</a></li>
</ul>
"""
p = PyQuery(html2)
# a = p(".bbb") # .xxx 点叉叉叉表示类选择器
# a = p(".bbb a") #提取bbb类标签里面的a标签
# print(a)

# a = p("#米哈游 a") # #xxx 井号叉叉叉表示id选择器
# print(a)
# href = p("#米哈游 a").attr("href") #.attr("xxxx")表示提取属性
# text = p("#米哈游 a").text() #.text()表示提取文本
# print(href)

# a = p("li a").attr("href") #不能同时拿所有符合的标签
# print(a) #默认拿到第一个标签属性
#多个标签拿属性
# iter = p("li a").items() #先拿到所有标签，再在循环里边逐个提取属性
# for i in iter:
#     href = i.attr("href")
#     print(href)

div = """
    <div><span>我操你妈</span></div>
"""
# div = PyQuery(div)
# print(div("span").html())  #html表示这个标签下的所有html内容，不能跨标签
# print(div("span").text())  #text表示这个标签下的文本内容，直接到最里边提取文本
# print(div("div").html())
# print(div("div").text())

#pyquery还能修改html内容结构

html3 = """
<html>
    <div class="aaa">哒哒哒</div>
    <div class="bbb">呀呀呀</div>
</html>
"""
# p2 = PyQuery(html3) #div.aaa表示选中属性为aaa的div标签
# p2("div.aaa").after("""<div class="ccc">啦啦啦</div>\n    """) #after表示在某个标签后面添加
# print(p2)
# p2("div.aaa").append("""<span>牛逼</span>""") #apppend表示在内部添加内容
# print(p2)
# p2("div.aaa").attr("class","zzz") #attr后面一个值表示替换，和字典操作一样
# print(p2)
# p2("div.aaa").attr("id","222") #和字典一样也可以添加属性,不过好像只能操作一次
# print(p2)
# p2("div.aaa").remove_attr("class") #删掉属性
# print(p2)
# p2("div#222").remove() #删掉标签
# print(p2)


#总结：
    #1.PyQuery初始化选择器
    #2.items()提取内容不止一个，返回生成器用于遍历
    #3. .attr("属性名")用于获取属性信息
    #4. .text()用于获取内容文本