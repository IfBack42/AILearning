import requests

url = "https://passport.17k.com/ck/user/login"

data = {
    "IDToken1": "81A3225C38A74929BCBF502E1C9BDDEE",
    "IDToken2": "5C3594B80CA2939C61B905F1E5DE17A336BE1EF8B95CFF6574F4C4593B1840A1",
    "IDToken3": "",
    "goto": "aHR0cDovL2lkbS5zd3UuZWR1LmNuL2FtL29hdXRoMi9hdXRob3JpemU/c2VydmljZT1pbml0U2VydmljZSZyZXNwb25zZV90eXBlPWNvZGUmY2xpZW50X2lkPTdjMXpva29samw5YmJpaG82eXVvJnNjb3BlPXVpZCtjbit1c2VySWRDb2RlJnJlZGlyZWN0X3VyaT1odHRwcyUzQSUyRiUyRnVhYWFwLnN3dS5lZHUuY24lMkZjYXMlMkZsb2dpbiUzRnNlcnZpY2UlM0RodHRwcyUyNTNBJTI1MkYlMjUyRnNwdnBuLnN3dS5lZHUuY24lMjUyRmF1dGglMjUyRmNhc192YWxpZGF0ZSUyNTNGZW50cnlfaWQlMjUzRDElMjZmZWRlcmFsRW5hYmxlJTNEdHJ1ZSZkZWNpc2lvbj1BbGxvdw==",
    "gotoOnFail": "",
    "SunQueryParamsString": "cmVhbG09LyZzZXJ2aWNlPWluaXRTZXJ2aWNlJg==",
    "encoded": "true",
    "gx_charset": "UTF-8"
}
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
           "referer":"http://idm-swu-edu-cn-s.sangfor.vpn.swu.edu.cn:8118/am/UI/Login?realm=%2F&service=initService&goto=http%3A%2F%2Fidm.swu.edu.cn%2Fam%2Foauth2%2Fauthorize%3Fservice%3DinitService%26response_type%3Dcode%26client_id%3D7c1zokoljl9bbiho6yuo%26scope%3Duid%2Bcn%2BuserIdCode%26redirect_uri%3Dhttps%253A%252F%252Fuaaap.swu.edu.cn%252Fcas%252Flogin%253Fservice%253Dhttps%25253A%25252F%25252Fspvpn.swu.edu.cn%25252Fauth%25252Fcas_validate%25253Fentry_id%25253D1%2526federalEnable%253Dtrue%26decision%3DAllow"
}
session = requests.session()
login_res = session.post(url, data=data,headers=headers)
print(login_res.cookies)
class_choose_url = "http://jw-swu-edu-cn.sangfor.vpn.swu.edu.cn:8118/jwglxt/xsxk/zzxkyzb_cxZzxkYzbIndex.html?gnmkdm=N253512&layout=default"
res = session.get(class_choose_url)
# print(res.content.decode())
