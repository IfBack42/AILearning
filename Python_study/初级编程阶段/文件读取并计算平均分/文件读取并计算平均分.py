"""我们需要从一个包含学生考试成绩的源文本文件中提取并计算平均分，
并将结果写入另一个目标文件目标average_score.txt。
源文件score.txt内容如下

75
82
90
85
92
78
80
88
91
79
87
93
83
89
77
81
"""
import os
f = open("score.txt","r")
list_ = []
sum_ = 0
while True:
    line = f.readline()
    if len(line) == 0:
        break
    line = line.replace("\n","")
    list_.append(line)
    print(line)
    sum_ += int(line)

print(list_)
ave = sum_ / len(list_)
print(ave)
ave = str(ave)
f.close()
f = open("average_score.txt","w")
f.write(ave)
f.close()
# os.remove("average_score.txt")