import jieba
import sys
import matplotlib.pyplot as plt
from wordcloud import WordCloud

text = open('test.txt', 'r', encoding='utf-8').read()
print(type(text))
wordlist = jieba.cut(text, cut_all = True)
wl_space_split = " ".join(wordlist)
print(wl_space_split)

my_wordcloud = WordCloud().generate(wl_space_split)
plt.imshow(my_wordcloud)
plt.axis("off")
plt.show()

import jieba
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# 读取文本文件
text = open('test.txt', 'r', encoding='utf-8').read()

# 使用jieba进行中文分词
wordlist = jieba.cut(text, cut_all=True)
wl_space_split = " ".join(wordlist)

# 指定中文字体路径（根据你的系统修改）
font_path = 'C:/Windows/Fonts/simhei.ttf'  # Windows系统中的黑体字体路径
# 如果是macOS，可以使用：'/System/Library/Fonts/PingFang.ttc'
# 如果是Linux，需要手动指定一个中文字体路径
"""
# 读取mask/color图片  
d = path.dirname(__file__)
nana_coloring = imread(path.join(d, "1.jpg"))

"""
# 生成词云图
my_wordcloud = WordCloud(
    font_path=font_path,  # 指定中文字体
    background_color='white',  # 背景颜色
    width=800,  # 图片宽度
    height=600  # 图片高度
).generate(wl_space_split)
"""
my_wordcloud = WordCloud(background_color='white',  # 背景颜色  
                         mask=nana_coloring,  # 设置背景图片  
                         max_words=2000,  # 设置最大现实的字数  
                         stopwords=STOPWORDS,  # 设置停用词  
                         max_font_size=200,  # 设置字体最大值  
                         random_state=30,  # 设置有多少种随机生成状态，即有多少种配色方案    
                         ).generate(wl_space_split) 
"""
# 显示词云图
plt.imshow(my_wordcloud)
plt.axis("off")
plt.show()

