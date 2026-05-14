from jsonpath import jsonpath
import requests
import json
"""
{
  "uid": 10818,
  "title": "深耕医健投资七年，昌发展如何破解产业生态的增长密码？",
  "photo": "https://static-image.xfz.cn/1700020048_905.png",
  "author": {
        "photo": "https://static-image.xfz.cn/15529e",
        "authors": {
                    "name": "xiaojie",
                    "aothor_id":114
                    }
            },
  "is_original": false,
  "article_type": "热点",
  "intro": "深度聚焦医药产业变革，共同寻找行业新的增长曲线",
  "source": "",
  "time": "2023-11-15 11:47:28",
  "keywords": [
                  "动脉网"
              ]
}
"""
js_data = json.load(open("jsonpath_test.json","r",encoding="utf-8"))
#使用jsonpath提取数据
title = jsonpath(js_data,"$.title") #$表示根节点 .表示子节点，跟xpath的/一样， ..和//一样表示子孙节点
print(title)
name = jsonpath(js_data,"$..name") #..和//一样表示子孙节点
print(name)
photo = jsonpath(js_data,"$.author.photo")
print(photo)
time = jsonpath(js_data,"$.time")
print(time)
authors_js = jsonpath(js_data,"$.author[*]") #通配符，返回该节点下面的节点元素
print(authors_js)