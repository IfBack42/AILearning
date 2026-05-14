import requests
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 QuarkPC/2.4.5.292',
}
# url = "https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts+dSST.csv"
# url = "https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts+dSST.txt"
url = 'https://data.giss.nasa.gov/pub/gistemp/SBBX.ERSSTv5.gz'
with open('./海洋.csv', 'a', encoding='utf-8') as f:
    for i in range(1,10000):
        data = requests.get(headers=headers,url=url).content.decode('utf-8')
        f.write(data)