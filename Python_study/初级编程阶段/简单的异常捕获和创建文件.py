"""
按照要求实现如下逻辑：

尝试开启python.txt的文本文件，从中逐行读取数据。
如果python.txt文件不存在，则在异常处理逻辑代码块中创建此文件，
并向文件中写入"开启文件失败，执行except中的代码"
"""
content = []
try:
    f = open("python.txt","r",encoding="utf-8")
    while True:
        line = f.readline(1024)
        if len(line) == 0:
            f.close()
            break
        content.append(line)
except:
    with open("python.txt","w",encoding="utf-8") as file:
        file.write("开启文件失败，执行except中的代码")
    file.close()
print(content)