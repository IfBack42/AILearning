import requests


#2.cookie模拟登录西大
#找到登录后的url
while True:
    url = "https://uaaap.swu.edu.cn/cas/login?service=https%3a%2f%2fjw.swu.edu.cn%2fsso%2fzllogin"
    headers = request_header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 QuarkPC/2.0.7.222","Cookie":"61zqTsrO93nzO_-_uaaap.swu.edu.cn=60FhbuOX9FFiXUXTpNiXihpuIwmNltUhSjsh6EF2uHUqwEDsxfg8d6A5bA0UsSHMtXq1i46USIJgRVFGTsVm4WZa;TWFID=64a0fae093753cca;61zqTsrO93nzO=60jzgzdKwCLhN99sSj3d9kdqyPpiGt0YCSNrB4Gy.8OfsVeYM583n1cQ6Px7tYBWQY4ekZoCi4CLpOsInmuIUl7G;61zqTsrO93nzP=0qsLcSmqq_GAy5whp.hIHPKWoEzmvJob9awMVswde69.7gNYTqzEoWrtQcay2tYsfGPniRLg9_uEtoZyS7I6LF8eji8tM6EJQG0m_842HNI4kqaW7_Uvs7KErqjgsU3NJte2frC5O85fH8cajuwjxrwJefqpyJzUB.dwkKUtjrsI7TMKZ8.EEhG2AKfjMJwvjo.BSsasEFDZQM0cTM1okTEMFgheArJVu4Zg7Zq29H3k5xXeoEFGlpNfPDJPBn477KmU49kg1oH5x90s28bbiA3XDB91QUHnp1eYSaISefkzwXQG3MWJy0IkdetK_K0fqvWwJsiKFG8t2T4VpFJGjxZvRWyTne4_Gg6iR98M2CETmTlRZNzY.lJSs8DgKFXaMaRHP6Tp1gDPP5dWQj8VRJG;JSESSIONID=82CB56EC01D5FD8F9B1C23AED4378C64-n1"}
    data = requests.get(url, headers=headers).content.decode()
    print(data)

