import requests

#1. post 先给浏览器参数再接收响应
#get请求携带参数 => params
#post请求携带参数 => data0
url = "https://fanyi.baidu.com/sug" #偷一个百度翻译的网址，是一个post模式数据包，返回json格式数据
word = input("输入要翻译成英语的词语")
data = {"kw":word}
print(requests.post(url, data=data).json())
# print(requests.post(url, data0=data0).content.decode()) # 返回数据是json格式，需要使用json解码


