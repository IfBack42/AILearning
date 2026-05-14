import re,requests

country_list = []
gdp_list = []
def get_gdp():
    global country_list
    global gdp_list
    #获取页面信息，存入列表，方便后续匹配
    gdp_data = requests.get("http://192.168.0.11:8999/gdp.html").content.decode("utf-8")
    data_list = gdp_data.split("\n")
    for line in data_list:
        result = re.match('.*<a href=""><font>(.*)</font></a>', line)
        if result:
            country_list.append(result.group(1))

        result = re.match(r'.*<font>\$(.*)<font>亿', line)
        if result:
            gdp_list.append(result.group(1))
if __name__ == '__main__':
    get_gdp()
    print(country_list)
    print(gdp_list)
    total_data = list(zip(country_list,gdp_list))
    print(total_data)




