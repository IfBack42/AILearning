str_list = ["xiaojie", "yuhuaichun", "zhangzheng", "shentao", "wanjinxi", "xuhao", "duanjiaqi"]

# 使用lambda表达式作为sort方法的key参数，按照字符串长度排序
str_list.sort(key=lambda x: len(x))

print(str_list)  # 输出排序后的列表

