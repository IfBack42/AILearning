from lxml import etree
# etree性能比bs4好，bs4唯一的优点是对脏数据有一定修复能力
xml = """
<book>
    <id>1</id>
    <name>野花遍地香</name>
    <price>1.23</price>
    <nick>臭豆腐</nick>
    <nicks>
        <nick id="10086">周大强</nick>
        <nick id="10010">周芷若</nick>
        <nick class="jay">周杰伦</nick>
        <nick class="jolin">蔡依林</nick>
    </nicks>
    <div>
        <nick>惹了</nick>
    </div>
    <author>
        <nick id="10086">周大强</nick>
        <nick id="10010">周芷若</nick>
        <nick class="jay">周杰伦</nick>
        <nick class="jolin">蔡依林</nick>
    </author>
    <partner>
        <nick id="ppc">胖胖陈</nick>
        <nick id="ppbc">胖胖不陈</nick>
    </partner>
</book>
"""
# 首先使用etree功能初始化，对数据进行解析
et = etree.XML(xml)#这一篇是xml格式，使用XML功能
# result = et.xpath("/book")  # /表示根节点，范围最大的那个
# result = et.xpath("/book/name") #表示book节点下的name节点，/表示儿子
# result = et.xpath("/book/name/text()")[0] #/text()表示提取节点中的文本，返回列表，用【】取出来纯字符串
# result = et.xpath("/book//nick/text()") #//表示子孙后代，中间不管有多少级，全部提取
# result = et.xpath("/book/*/nick/text()")  # *表示通配符，谁都行，仅跳过一级
# result = et.xpath("/book/author/nick[@class='jay']/text()") #[]表示属性筛选，@属性名=值 和bs4find(xml，attrs={'':''})差不多
# result = et.xpath("/book/partner/nick/@id") #属性放在节点后面表示提取属性的内容，放在里面表示筛选
# print(result)

html = """
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <title>Title</title>
</head>
<body>
    <ul>
        <li><a href="http://www.baidu.com">百度</a></li>
        <li><a href="http://www.google.com">谷歌</a></li>
        <li><a href="http://www.sogou.com">搜狗</a></li>
    </ul>
    <ol>
        <li><a href="feiji">飞机</a></li>
        <li><a href="dapao">大炮</a></li>
        <li><a href="huoche">火车</a></li>
    </ol>
    <div class="job">李嘉诚</div>
    <div class="common">胡辣汤</div>
</body>
</html>
"""
et2 = etree.HTML(html)
# li_list = et2.xpath("/html/body/ul/li[2]/a/text()") #[]可以直接在节点里面选择第几个，xml也一样
# print(li_list)

li_list = et2.xpath("//li")
for i in li_list: # ./表示当前节点，上一级提取的是li节点，所以当前节点写作 ./ 而不是 /li
    print(i.xpath("./a/@href")[0],i.xpath("./a/text()")[0])
