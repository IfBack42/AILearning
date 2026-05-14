import requests

url = "https://movie.douban.com/j/search_subjects?"

data = {
    "type" : "movie",
    "tag" : "热门",
    "page_limit" : "50",
    "page_start" : "0",
}

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"}

res = requests.get(url, params=data, headers=headers)
print(res.json())
print(res.url)
