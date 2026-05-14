"""
某班级有5名学生，他们的学号、姓名和英语成绩如下表所示，此数据存储在student_scores.txt文件中，请编写一个程序，完成如下功能：

1，计算每个学生的平均成绩。

2，输出平均成绩最高的学生信息。

3，要求使用面向对象完成此需求，即，创建学生对象用于存储学号、姓名、得分，提供计算平均分方法等。

+------+--------+------+------+------+
| 学号 |  姓名   | 语文  | 数学  | 英语 |
+------+--------+------+------+------+
| 001  | 张三   |  85  |  90  |  78  |
| 002  | 李四   |  92  |  88  |  95  |
| 003  | 王五   |  88  |  92  |  85  |
| 004  | 赵六   |  78  |  85  |  90  |
| 005  | 小明   |  95  |  92  |  88  |
+------+--------+------+------+------+
student_scores.txt文本内容如下

学号,姓名,语文,数学,英语
001,张三,85,90,78
002,李四,92,88,95
003,王五,88,92,85
004,赵六,78,85,90
005,小明,95,92,88
您的答案
"""
def main(): #定义一个函数用于读取文件内容并实例化学生
    stu_class_list = [] #学生类列表
    f = open("student_scores.txt","r",encoding="utf-8")
    title = f.readline(1024)
    title_list = title.strip().split(",")
    print(title_list)
    #这里把标题读了，接下来用循环实例化
    while True:
        stu = f.readline(1024)
        if len(stu) == 0:
            break
        stu_list = stu.strip().split(",")
        print(stu_list)
        Student(stu_list[0],stu_list[1],stu_list[2],stu_list[3],stu_list[4])
        stu_class_list.append(Student(stu_list[0],stu_list[1],stu_list[2],stu_list[3],stu_list[4]))
    #学生类列表整好了，现在比较一下学生平均成绩然后调用最屌学生函数
    for i in stu_class_list:
        print(i.ave_print())
    max_ = stu_class_list[0].ave()
    max_stu = stu_class_list[0]
    for i in stu_class_list:
        if i.ave() > max_:
            max_ = i.ave()
            max_stu = i
    print(max_stu.max_())

class Student:
    def __init__(self,id,name,ch_score,en_score,ma_score):
        self.id = id
        self.name = name
        self.ch = ch_score
        self.en = en_score
        self.ma = ma_score
    def ave(self):
        return (int(self.ch) + int(self.ma) + int(self.en)) / 3
    def ave_print(self):
        return f"学生{self.name}的平均成绩是：{(int(self.ch) + int(self.ma) + int(self.en)) / 3 : .2f}"

    def max_(self):
        return f"最吊学生是{self.name},他的英语成绩是{self.en}，语文成绩是{self.ch}，数学成绩是{self.ma}"
if __name__ == "__main__":
    main()