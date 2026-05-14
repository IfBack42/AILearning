from bs4 import BeautifulSoup

html = """ 
<tr>
    <th class="xiaojie">zhanshen</th>
    <th class="yuhuaichun">shabi</th>
    <th class="gou">1145</th>
    <th class="shentao">niubi</th>
</tr>"""

#假如爬到这么个html页面
#1.初始化BeautifulSoup对象 => 使对象成为解析树，甚至修复错误闭合，为后续操作做准备
page = BeautifulSoup(html,"html.parser")

#2.查找操作，主要用find 和 find_all
#find("标签名",attrs={"属性":"值"})
tr = page.find("tr")
print(tr)

#3.找到后的标签可以进一步查找
th = tr.find("th",attrs={"class":"xiaojie"})
print(th)

#4.最小的标签内容使用text获取
print(th.text)
#也能获取标签属性
print(th.get("class"))

#5.find_all使用
th_list = page.find_all("th")
print(th_list)

