"""
根据如下说明，编写代码完成相关需求
1、
2、
选择课程装饰器：choose_course
为『成绩录入功能』新增选择课程的拓展功能，达到可以录入不同学科的成绩
2.1可以重复输入要录入的学科名，然后就可以进入该门学科的『成绩录入功能』，录入结束后，可以进入下一门学科成绩录入
2.2当输入学科名为q时，结束所有录入工作
2.3将学科成绩保存在字典中并返回给外界，例如：{'math': [90, 80, 50, 70], 'english': [70, 50, 55, 90]}
3、
处理成绩装饰器：deal_fail
可以将所有录入的成绩按60分为分水岭，转换为 "通过" | "不通过"进行存储
3.1，如果只对原功能装饰，结果还为list返回给外界，例如：["通过", "通过", "不通过", "通过"]
3.2，如果对已被选择课程装饰器装饰了的原功能再装饰，结果就为dict返回给外界，
例如：{'math': ["通过", "通过", "不通过", "通过"],'english': ["通过", "不通过", "不通过", "通过"]}
"""

def choose_course(fn):  #定义第一个修饰器
    def inner():
        dict_ = {}
        while True:
            project = input("科目：（输入p结束）")
            if project == "p":
                break
            print(f"请录入{project}成绩：")
            dict_[project] = fn()
        return dict_
    return inner

def deal_fail(fn):  #定义第二个修饰器，修饰被第一个修饰器修饰的函数
    def inner():
        dict__ = fn()
        for i in dict__.values():
            n = 0
            for j in i:
                if eval(j) >= 60:
                    i[n] = "通过"
                else:
                    i[n] = "不通过"
                n += 1
        return dict__
    return inner
@deal_fail
@choose_course  # 先执行下面的修饰器，再执行上面的
def entry_grade():
    list_ = []
    while True:
        grade = input("录入成绩：（输入0结束）")
        if grade == "0":
            break
        list_.append(grade)
    return list_


print(entry_grade())