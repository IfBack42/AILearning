"""
我们需要统计一个源文本文件中每个单词出现的次数，并将结果写入另一个目标文件。
源文件input.txt内容如下：

As your report on White Pollution indicates, regulations on the use of plastic bags have not been implemented effectively in some areas.
I am writing this letter to express my concern over the abuse of plastic bags and make some suggestions.
目标文件output.txt展示结果如下：

As: 1
your: 1
report: 1
on: 2
White: 1
Pollution: 1
indicates,: 1
regulations: 1
the: 2
use: 1
of: 2
plastic: 2
bags: 2
have: 1
not: 1
been: 1
implemented: 1
effectively: 1
in: 1
some: 2
areas.: 1
I: 1
am: 1
writing: 1
this: 1
letter: 1
to: 1
express: 1
my: 1
concern: 1
over: 1
abuse: 1
and: 1
make: 1
suggestions.: 1
"""

f = open("input.txt", "r")
content = []
while True:
    line = f.readline(1024)
    line = line.split()
    content += line
    if len(line) == 0:
        break
print(content)
f.close()
f = open("output.txt", "w")
for i in content:
    f.write(f"{i}: {content.count(i)}\n")
f.close()