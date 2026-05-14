'''
find()使用方式
字符串变量.find(要搜索的内容)，如果要搜索的内容在字符串中存在，则返回搜索内容的起始位置的下标，找不到则返回-1

index()
字符串变量.index(要搜索的内容)，如果要搜索的内容在字符串中存在，则返回搜索内容的起始位置的下标，找不到则报错
'''
str1 = 'hello world'
print(str1.find('world'))

str2 = 'hello python'
print(str2.index('linux'))