"""
有如下信息需要进行存储：学生的姓名 name（字符串类型）
、科目名称 subject（字符串类型）和学科成绩 score（整数类型），教师评语(comment)。
所有文件夹或者文件都存储在 'student_scores' 命名的文件夹中。
每个学生都有根据自己姓名命名的专属文件夹。
在学生姓名文件夹内，创建一个以科目名称命名的文本文件，并将学科成绩，以及老师的评语写入该文件中。
"""

from os import path,mkdir,getcwd,chdir
name = input("学生的名称：")
subject = input("学科：")
score = input("学科成绩：")
comment = input("教师评语：")

print(getcwd())
chdir("../")
print(getcwd())

# 使用listdir 判断老大文件夹是否存在某个学生的专属文件夹，没有则新建
# 再使用该函数判断专属文件夹是否有对应学科文件夹，没有则新建
if not path.exists(f"students_scores/{name}"):
    mkdir(f"students_scores/{name}")
#成功创建专属文件夹，接下来打开文件夹进行接下来的判断
if not path.exists(f"students_scores/{name}/{subject}.txt"):
    with open(f"students_scores/{name}/{subject}.txt","w",encoding = "utf-8") as students_file:
        students_file.write(f"成绩：{score}\n教师评语：{comment}")
else:
    students_file = open(f"students_scores/{name}/{subject}.txt","w",encoding = "utf-8")
    students_file.write(f"成绩：{score}\n教师评语：{comment}")

# student_file = open(f"students_scores/{name}/{subject}.txt", "w", encoding="utf-8")
# student_file.write(f"成绩：{score}\n教师评语：{comment}")
#成功创建学科文件夹，需要在学科文件夹输入成绩及评语
students_file.close()

# 不要问我为什么要用绝对路径，相对路径是个傻逼，不会找自己上级的文件！！！





