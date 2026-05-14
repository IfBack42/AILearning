import requests
import re

#封装一个获取图片地址的函数
def get_pic():
    # 爬取http://192.168.0.11:8999/index.html页面信息，使用content获取数据
    data = requests.get("http://192.168.0.11:8999/index.html").content.decode("utf-8")
    # 信息按行分割方便获取jpg地址
    data_list = data.split("\n")
    # 遍历+字符串操作获取完整地址并塞入列表
    url_list = []
    for i in data_list:
        result = re.match(".*src=\"(.*)\" width.*", i)
        if result:
            print(result.group(1)[1:])
            url = "http://192.168.0.11:8999" + result.group(1)[1:]
            url_list.append(url)
    return url_list

#封装一个保存图片的函数
def save_pic():
    for i in get_pic():
        pic_data = requests.get(i).content
        data_url = re.search(".*images/(.*)",i).group(1)
        with open(f"source/spyder/{data_url}","wb") as f:
            f.write(pic_data)


if __name__ == '__main__':
    save_pic()