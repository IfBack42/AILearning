name_list = ["xiaojie", "yuhuaichun", "zengkun", "duanjiaqi", "xiaojie"]
fw_list = ["pengjinghang", "zhengchang", "wanjinxi", "heigou"]
sb_list = ["duanjiaqi", "ribenren", "zuosiqi"]
big_list = [["zhenchao","pengjinghang","heigou","wanjingxi"],["duanjiaqi","jiangyundi","zhangshiyue"],["zenkun","xiaojie",["yuhuaicun"]]]

# print(big_list[1,1][1,1])   这种不存在
print(big_list[1][1])

sb_list.extend(fw_list) # 合并列表在左边那个
sb_list.extend("zhanshenxiaojie") # 插入的是字符串的话会分开

name_list.append("zhishangtuan" ) # 列表末尾增加且只能增加一个元素

sb_list.insert(2,"wudidehuangsihao") # 在指定序列插入

print(sb_list)

for i in name_list:
    print(i)

print(name_list[0])
print(name_list[1])
print(name_list[2])
print(name_list[3])
print(name_list)

print(name_list.count("xiaojie")) # 统计傻逼出现次数


if "xiaojie" in name_list:  # in 和 not in 判断列表是否包含某元素，返回值为bool
    print("滚出去！")
if "shentao" not in name_list:
    print("我涛哥")