import random
import requests
from urllib.parse import quote,unquote


def func1():
    url = "https://www.baidu.com"
    res_no_header = requests.get(url)
    print(len(res_no_header.content.decode()))
    # 1.上面的是请求的url，.url是响应的url
    print(res_no_header.url)
    # 2.响应状态码
    print(res_no_header.status_code)
    # 3.响应对应的请求头,就是请求头嘛
    print(res_no_header.request.headers)  # **比较重要
    # 4.响应头
    print(res_no_header.headers)  # **比较重要
    # 5.响应对应的编码方式
    print(res_no_header.apparent_encoding)


def func2():
    url = "https://www.baidu.com"
    # 6.用户代理 => 默认请求头为 'User-Agent': 'python-requests/2.32.3'  给皇军暴露了 所以响应可能藏着掖着
    # 所以构建一个请求头让自己看起来像人一点(字典类型)
    request_header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 QuarkPC/2.0.7.222"}
    # 重新发一个带请求头的请求
    res_with_header = requests.get(url, headers=request_header)  # **比较重要
    print(res_with_header.request.headers)
    print(len(res_with_header.content.decode()))


def func3():
    # 7.user-agent池 有限地反反爬
    # 自己创建ua池
    ua_list = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 QuarkPC/2.0.7.222",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"]
    # 随机调用ua值
    ran_agent = {"User-Agent": random.choice(ua_list)}
    print(ran_agent)


def func4():
    # 8.url传参的加密和解密
    # 直接在浏览器输入时：http://www.baidu.com/s?wd=我操&rsv_spt=1&rsv_iqid=0x95e70ca50018723d&issp=1&f=8&rsv_bp=1&rsv_idx=2&ie=utf-8&tn=75144485_3_dg&rsv_enter=1&rsv_dl=tb&rsv_sug3=11&rsv_sug1=9&rsv_sug7=101&rsv_sug2=0&rsv_btype=t&prefixsug=wocao&rsp=5&inputT=3283&rsv_sug4=4716
    # 抓包或者复制粘贴得到的：https://www.baidu.com/s?wd=%E6%88%91%E6%93%8D&rsv_spt=1&rsv_iqid=0x95e70ca50018723d&issp=1&f=8&rsv_bp=1&rsv_idx=2&ie=utf-8&tn=75144485_3_dg&rsv_enter=1&rsv_dl=tb&rsv_sug3=11&rsv_sug1=9&rsv_sug7=101&rsv_sug2=0&rsv_btype=t&prefixsug=wocao&rsp=5&inputT=3283&rsv_sug4=4716
    # 注意wd部分变化，这就是加密解密过程
    # quote => 加密
    # unquote => 解密
    print(quote("我操你妈"))  # => %E6%88%91%E6%93%8D%E4%BD%A0%E5%A6%88
    print(unquote("%E6%88%91%E6%93%8D%E4%BD%A0%E5%A6%88"))  # => 我操你妈


def func5():  #自己设置参数很麻烦，爬到的数据很没有规律，还容易被反爬
    request_header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 QuarkPC/2.0.7.222"}
    # 9.发送带参数的请求
    # 一般的浏览器页面会带有参数https://www.baidu.com/s?wd=wocao&rsv_spt=1&rsv_iqid=0x95e70ca50018723d&issp=1&f=8&rsv_bp=1&rsv_idx=2&ie=utf-8&rqlang=cn&tn=75144485_3_dg&rsv_enter=1&rsv_dl=tb&oq=%25E6%2588%2591%25E6%2593%258D&rsv_btype=t&inputT=5&rsv_t=3a00BXRX94urT3VxBm5wwta%2BLnjWGd27ionIDQAaS%2FjHWCfwe1qsEyrdNhW1q%2FRuk5sd4A&rsv_sug3=12&rsv_sug1=10&rsv_sug7=100&rsv_sug2=0&rsv_pq=d0f3415e0058b37f&rsv_sug4=911&rsv_sug=1
    url_1 = "https://www.baidu.com/s?wd=%E6%98%8E%E6%97%A5%E6%96%B9%E8%88%9F&rsv_spt=1&rsv_iqid=0x89b0234100c0eb45&issp=1&f=8&rsv_bp=1&rsv_idx=2&ie=utf-8&tn=75144485_3_dg&rsv_enter=1&rsv_dl=tb&rsv_sug3=6&rsv_sug1=6&rsv_sug7=101&rsv_sug2=0&rsv_btype=t&inputT=2000&rsv_sug4=2720&rsv_sug=1"
    url_2 = "https://www.baidu.com/s?wd=学习强国"
    # data0 = requests.get(url_1,headers=request_header).content.decode()
    # print(data0)
    # print(len(data0))

    # 所以要通过params携带参数字典
    # ①构建请求参数字典
    url_3 = "https://www.quark.cn/s?"
    kw = {"q": "明日方舟"}
    # ②发送请求的时候带上请求参数的字典
    print(requests.get(url_3, headers=request_header,params=kw).content.decode())

if __name__ == '__main__':
    func5()