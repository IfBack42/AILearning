import os
import moviepy.editor as mp
from jsonpath import jsonpath
import requests
import json
import re
from lxml import etree

def video_get(video_url,audio_url,title):
    # 创建bilidown目录如果不存在
    if not os.path.exists("bilidown"):
        os.makedirs("bilidown")
        
    vi_res = requests.get(video_url,headers=headers).content
    with open("bilidown/video.mp4","wb") as f:
        f.write(vi_res)
    so_res = requests.get(audio_url,headers=headers).content
    with open("bilidown/audio.mp4", "wb") as f:
        f.write(so_res)
    
    # 使用moviepy合并音视频
    video_clip = mp.VideoFileClip("bilidown/video.mp4")
    audio_clip = mp.AudioFileClip("bilidown/audio.mp4")
    final_clip = video_clip.set_audio(audio_clip)
    title = "bilidown/" + re.sub(r'[<>:"/\\|?*\x00-\x1F]', '_', title) + ".mp4"
    final_clip.write_videofile(title, codec="libx264", audio_codec="aac")
    
    print(f"已下载视频：{title}")
    os.remove("bilidown/video.mp4")
    os.remove("bilidown/audio.mp4")

def referer_get(html_res):
    et = etree.HTML(html_res)
    referer = et.xpath("/html/head/meta[@itemprop='url']/@content")[0] # 拿到防盗链
    global headers
    headers["Referer"] = referer

#拿一下存音视频地址的json
def json_get(et):
    # 尝试多种方式获取播放信息
    scripts = et.xpath("//script/text()")
    play_info_json = None
    
    # 查找包含播放信息的脚本
    for script in scripts:
        if "window.__playinfo__" in script:
            # 提取JSON部分
            match = re.search(r"window\.__playinfo__\s*=\s*({.*?});", script, re.DOTALL)
            if match:
                play_info_json = match.group(1)
                break
    
    if not play_info_json:
        # 如果没找到，尝试另一种方式
        for script in scripts:
            if "__playinfo__" in script and "data" in script:
                try:
                    # 尝试直接解析整个脚本作为JSON
                    play_info_json = script
                    json.loads(play_info_json)  # 测试是否能解析
                    break
                except:
                    play_info_json = None
                    continue
    
    if not play_info_json:
        raise Exception("无法从页面中提取播放信息")
    
    # json.dump(play_info_json,open("url.json","w",encoding="utf-8"),ensure_ascii=False,indent=4) #测试json是否拿到
    url_js_data = json.loads(play_info_json) #拿到json，交给下一个函数用jsonpath拿音视频url
    return url_js_data

def v_s_url_get(url_js_data):
    # 更新JSON路径以适配B站新的数据结构
    try:
        video_url = jsonpath(url_js_data,"$.data.dash.video[0].baseUrl")[0]
        audio_url = jsonpath(url_js_data,"$.data.dash.audio[0].baseUrl")[0]
    except:
        # 尝试备用路径
        video_url = jsonpath(url_js_data,"$.data.dash.video[0].base_url")[0]
        audio_url = jsonpath(url_js_data,"$.data.dash.audio[0].base_url")[0]
    # print(video_url)
    # print(audio_url)
    return video_url,audio_url

def judge_url(page,html_url):
    # 拿到页数后根据页数修改url然后传给视频下载函数
    to_replace = re.search(r".*?(&p=\d)", html_url)
    if to_replace: #如果传的url是带p参数的，就给去掉然后从0开始下载
        html_url = html_url.replace(to_replace.group(1),"")
    for i in range(1,page + 1):
        if i == 1:
            print(html_url)
            single_html_get(html_url)
        else:
            new_html_url = html_url + f"&p={i}"
            print(new_html_url)
            single_html_get(new_html_url)

def single_title_get(et):
    title = et.xpath("/html/head/title/text()")[0]  # 拿一下视频标题
    # 替换文件名中的特殊字符
    return re.sub(r'[<>:"/\\|?*\x00-\x1F]', '_', title)

def mul_ulr_get(html_url):
    html_res = requests.get(html_url, headers=headers).content.decode("utf-8")  # 拿html
    et = etree.HTML(html_res)  # 初始化然后拿页数
    try:
        page_text = et.xpath("//div[@class='rcmd-tab']//div[@class='amt']/text()")[0]
        page = int(page_text.split("/")[1].rstrip("）"))
    except:
        # 如果找不到分页信息，默认为1页
        page = 1
    judge_url(page, html_url)

#先拿html，然后从里面拿防盗链和音频视频的url
def single_html_get(html_url):
    html_res = requests.get(html_url,headers=headers).content.decode("utf-8")
    et = etree.HTML(html_res)
    referer_get(html_res)
    title = single_title_get(et)
    json_data = json_get(et)
    video_url, audio_url = v_s_url_get(json_data)
    video_get(video_url,audio_url,title)

def choose():
    print("_" * 20)
    print("下载分p视频还是单个视频？")
    print("_" * 20)
    global flag
    flag = input("单个视频 => 1\n分集视频 => 2\n:")
    if flag == "1" :
        html_url = input("复制粘贴视频地址(氪金视频不彳亍)：")
        single_html_get(html_url)
    elif flag == "2":
        html_url = input("复制粘贴视频地址(氪金视频不彳亍)：")
        mul_ulr_get(html_url)
    else:
        print("啥呢？")

if __name__ == '__main__':
    flag = ""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 SLBrowser/9.0.5.12181 SLBChan/112 SLBVPV/64-bit",
        "Referer": "https://www.bilibili.com/"
    }
    # test()
    choose()