'''
案例:
    商品评论情感分析, 演示: 朴素贝叶斯 分类问题.

贝叶斯介绍:
    它属于机器学习的算法的一种, 主要采用 概率来划分 分类.
'''

# 导包
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import jieba
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB


# 1. 读取数据.
data = pd.read_csv('./data/书籍评价.csv', encoding='gbk')
# print(data.head())

# 2. 数据预处理.
# 2.1 增加1列 labels充当标签列, 即: 0 -> 差评, 1 -> 好评.
data['labels'] = np.where(data['评价'] == '差评', 0, 1)
print(data.head())

# 2.2 把上述的 labels 充当: y列(标签列)
y = data['labels']
print(y)

# 2.3 演示切词.
# print(jieba.lcut('好好学习, 我爱你你爱我, 蜜雪冰城甜蜜蜜!'))

# 2.4 对用户录入的 内容进行切词, 然后去重, 并放到1个列表中.
# jieba.lcut(line)处理后的内容: [[第1条评论的切词1, 切词2......], [第2条评论的切词1, 切词2......], [第3条评论的切词1, 切词2......]]
# comment_list的格式: ['第1条评论切词1, 切词2, 切词3...',    '第2条评论切词1, 切词2, 切词3...',    '第3条评论切词1, 切词2, 切词3...']
comment_list = [','.join(jieba.lcut(line)) for line in data['内容']]
print(comment_list)

# 2.5 把上述切词后的内容, 无效词给过滤掉, 例如: , 的 等之类的, 都是无效词.
# 读取 停用词文件, 获取到所有的停用词(对区分 好评 和 差评 没有帮助的词 -> 停用词)
with open('./data/stopwords.txt', 'r', encoding='utf-8') as f:
    # 一次读取所有行, 格式: ['行1\n', '行2\n', '行3\n'...]
    lines = f.readlines()
    # 删除上述每行后的\n, 然后把所有数据放到1个列表中.
    stopword_list = [line.strip() for line in lines]
    # 对上述列表中的停用词进行去重.
    stopword_list = list(set(stopword_list))
    # print(len(stopword_list))       # 1711
    print(stopword_list)

# 3. 向量化处理, 把切词后的内容, 无效词给过滤掉, 例如: , 的 等之类的, 都是无效词.
# 参1: 停用词列表
transfer = CountVectorizer(stop_words=stopword_list)
# 具体的向量化过程, 然后转成列表, 就可以知道: 共多少个切词, 每个语句中都出现了哪些切词.
# 例如: []
x = transfer.fit_transform(comment_list).toarray()
# print(x.shape)  # (13, 37) => 13个评论, 37个切词(13个评论全部切词后, 删除无效词后, 共剩下37个切词)
print(x)

# 查看上述37个切词的总的内容.
# print(transfer.get_feature_names_out())

# 4. 切分训练集 和 测试集, 共12条评论, 我们让前10条当训练集, 后3条当测试集.
x_train = x[:10]
y_train = y[:10]
x_test = x[10:]
y_test = y[10:]

# 5. 创建模型对象(贝叶斯), 进行训练.
estimator = MultinomialNB()
estimator.fit(x_train, y_train)

# 6. 模型预测.
y_predict = estimator.predict(x_test)
print(f'预测值: {y_predict}')

# 7. 模型评估.
print(f'模型准确率: {estimator.score(x_test, y_test)}')  # 1