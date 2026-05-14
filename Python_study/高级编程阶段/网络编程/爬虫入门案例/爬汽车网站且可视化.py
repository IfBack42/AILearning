"""
请爬取地址为：https://web.phb123.com/hangye/qiche/pinpai/ ,
请求爬取汽车品牌销量排行榜2023中前100的数据并保存到cars.csv,
按照品牌以及全年销量，取前15名进行柱状图绘制，注意按照销量来展示图形，并生成保存资源，html命名为cars_top15.html并用于展示。
"""

# 回顾发现，下次千万不要把爬到的数据分开再一条一条匹配，连续挨着的两个一样的标签处理起来很麻烦的
# 直接把正则表达式拉长一点，然后分组匹配就能匹配挨着的了
import re,requests,csv
from pyecharts import options as opts
from pyecharts.charts import Bar


rank_list = []
brand_list = []
crude_sales_list = []
crude_type_list = []
type_list = []
month_sales_list = []
year_sales_list = []

def get_data():
    global rank_list,crude_sales_list,crude_type_list
    data = requests.get("https://web.phb123.com/hangye/qiche/pinpai/").content.decode("utf-8")
    data_list = data.split("\n")
    for line in data_list:
        print(line)
        rank = re.match(r".*<td><span class=\".*\">(.+)</span></td>",line)
        if rank:
            rank_list.append(rank.group(1))

        brand = re.match(r".*<td><a href=\".*\" title=\".*\" target=\"_blank\">(.*)</a></td>",line)
        if brand:
            crude_type_list.append(brand.group(1))

        sales = re.match(r".*<td>(\d*)</td>",line)
        if sales: #月销量和黏销量还没清洗
            crude_sales_list.append(sales.group(1))


def sales_clear(sales_list):
    global month_sales_list,year_sales_list
    i,j,n = 0,1,0
    while n < len(sales_list):
        month_sales = sales_list[i]
        year_sales = sales_list[j]
        month_sales_list.append(month_sales)
        year_sales_list.append(year_sales)
        i += 2
        j += 2
        n += 2

def type_clear(mode_list):
    global brand_list,type_list
    i,j,n = 0,1,0
    while n < len(mode_list):
        brand = mode_list[i]
        type = mode_list[j]
        brand_list.append(brand)
        type_list.append(type)
        i += 2
        j += 2
        n += 2

def switch_csv_list_mode():
    global rank_list,brand_list,month_sales_list,year_sales_list,type_list
    csv_data = [("排名", "品牌", "1月销量", "全年销量", "最佳车型")]
    csv_list = list(zip(rank_list,brand_list,month_sales_list,year_sales_list,type_list))
    for i in csv_list:
        csv_data.append(i)
    return csv_data

def csv_make(data):
    filename = "../../../cars.csv"
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)
    print(f"数据已成功写入 {filename}")

def column_make(is_realtime_sort: bool = False):
    # 柱状图数据
    x_data = brand_list
    y_data = year_sales_list

    # 创建 Bar 实例
    bar = (
        Bar()
        .add_xaxis(x_data)
        .add_yaxis("汽车销量", y_data)
        .set_global_opts(
            title_opts=opts.TitleOpts(title="汽车销量"),
            xaxis_opts=opts.AxisOpts(name="品牌"),
            yaxis_opts=opts.AxisOpts(name="销量"),
        )

    )
    # 渲染生成柱状图（默认为 HTML 文件）
    bar.render("cars_top15.html")

if __name__ == '__main__':
    get_data()
    print(rank_list)
    sales_clear(crude_sales_list)
    type_clear(crude_type_list)
    print(month_sales_list)
    print(year_sales_list)
    print(brand_list)
    print(type_list)
    print(switch_csv_list_mode())
    csv_make(switch_csv_list_mode())
    column_make()

#参考答案
"""
# complete code
import requests
import re
from pyecharts.charts import Bar


def crawl_parse_data(url):
    """"""
    用于爬取汽车数据
    url: 爬取的地址
    return: 返回爬取的数据的title以及数据
    """"""
    # 1. 先爬取页面数据
    response = requests.get(url)
    # 如果没有爬取到则直接返回空，表示数据爬取失败
    if response.status_code != 200:
        return
        # 2. 对数据进行分割，并且去除前后的空白字符，方便后续处理
    text_list = [line.strip() for line in response.text.split('\n')]
    print(text_list)
    #  提取tbody数据
    tbody = text_list[text_list.index('<table class="table-ui">') + 1:text_list.index('</table>')]
    print(tbody)
    # 3. 提取字段的标题
    titles = [re.search(r'<th.*>(.+)</th>', line).group(1)  for line in tbody[1:6] ]

    # 4. 解析提取数据
    data0 = []
    for line in tbody[6:]:
        if line.startswith('<td'):
            data0.append((re.search(r'<td.*>.+title="([^\"]+)', line) or re.search(r'<td.*>(\d+)<.*/td>', line)).group(1))
    #  列表推导式写法
    # data0 = [(re.search(r'<td.*>.+title="([^\"]+)',line) or re.search(r'<td.*>(.+)</td>',line)).group(1) for line in [6:] if line.startswith('<td')]

    # 把数据转化成二维数组，方便我们后面使用
    start = 0
    sep = 5
    data_frame = []
    while start < len(data0):
        data_frame.append(data0[start:start + sep])
        start += sep

    return titles, data_frame


# 存储数据到csv文件
def write_csv(fname, titles, data0):
    # 打开文件用于写入文件
    f = open(fname, 'w', encoding='utf8')

    # 写入titles
    f.write("\t".join(titles) + '\n')
    # 写入数据
    for d_line in data0:
        f.write("\t".join(d_line) + '\n')
    # 关闭文件
    f.close()


# 定义绘制bar的图
def draw_bar(data0, html_name):
    c = (
        Bar()
            .add_xaxis(
            [d[0] for d in data0]
        )
            .add_yaxis("2023汽车排名前15", [d[1] for d in data0])
            .render(html_name)

    )


url = "https://mip.phb123.com/hangye/qiche/pinpai/"
csv_file_name = 'cars.csv'
html_name = 'cars_top15.html'

# 爬取数据
titles, car_data = crawl_parse_data(url)

# 数据写入到csv文件
write_csv(csv_file_name, titles, car_data)

# 提取top15数据
# 保留品牌与年销量 注意要把销量转化成整数
top15 = [[d[1], int(d[-2])] for d in car_data[:15]]

# 根据销售量排序,用于后面的绘图使用
top15.sort(key=lambda x: x[1], reverse=True)

# 生成绘制的html文档
draw_bar(top15, html_name)"""