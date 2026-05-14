import time
import re
import requests
from bs4 import BeautifulSoup



def get_paren_html():
    ani_url = "https://dy2018.com/html/dongman/index.html"
    try:
        get_kid_html(ani_url)
    except:
        print("网址貌似出了点问题~")
        exit(250)
    for i in range(2,100):
        time.sleep(0.4)
        ani_url = f"https://dy2018.com/html/dongman/index_{i}.html"
        try:
            get_kid_html(ani_url)
        except:
            print("网址貌似出了点问题~")
            exit(250)


def get_kid_html(url):
    kid_html_res = requests.get(url,headers=headers).content.decode("gbk")
    # print(kid_html_res)
    get_single_ani_url(kid_html_res)


def get_single_ani_url(res):
    pattern = re.compile(r"<tr>.*?<b>.*?<a href=\"(?P<url>.*?)\".*?◎片　　名(?P<name>.*?)\n◎年　　代.*?</tr>",re.S)
    result = pattern.finditer(res)
    if result:
        for i in result:
            single_ani_url = "https://dy2018.com" + i.group("url")
            single_ani_name = i.group("name")
            print(single_ani_url)
            print(single_ani_name)
            get_down_url(single_ani_url)

def get_down_url(single_ani_url):
    time.sleep(0.2)
    down_html_res = requests.get(single_ani_url,headers=headers).content.decode("gbk")
    soup = BeautifulSoup(down_html_res, 'html.parser')
    player_list = soup.find('div', class_='player_list')
    links = player_list.find_all('a')
    for link in links:
        print(f"集数: {link.text}, 下载地址: {link['href']}")

def run():
    get_paren_html()

if __name__ == '__main__':
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"}
    run()