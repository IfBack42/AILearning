from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import numpy as np
import matplotlib.pyplot as plt

# 存储读取语料 一行预料为一个文档
corpus = []
for line in open('result.txt', 'r', encoding="utf-8").readlines():
    corpus.append(line.strip())

# 将文本中的词语转换为词频矩阵
vectorizer = CountVectorizer() #这个方法同时完成了两个任务：一是生成词汇表，二是统计词频并生成词频矩阵。它返回的是一个稀疏矩阵，表示词频矩阵。
# 计算个词语出现的次数
X = vectorizer.fit_transform(corpus)
"""
存储形式：X是一个稀疏矩阵（sparse matrix），通常以压缩稀疏行（Compressed Sparse Row, CSR）格式存储。
用途：稀疏矩阵用于高效存储和处理大部分元素为零的矩阵。
在文本处理中，词频矩阵通常有很多零值（因为每个文档只包含词汇表中的一部分词），因此使用稀疏矩阵可以节省内存和计算资源。
"""
# 获取词袋中所有文本关键词
word = vectorizer.get_feature_names_out()
for i in word:
    print(i,end=' ')
# 查看词频结果
print("\n")
print(X.toarray())
"""
存储形式：X.toarray()将稀疏矩阵转换为密集矩阵（dense matrix），即一个完整的二维数组，包含所有元素（包括零值）。
用途：密集矩阵更直观，适合调试和查看矩阵内容，但会占用更多内存，尤其是当矩阵很大时。
输出形式：打印X.toarray()会显示完整的矩阵内容，包括所有零值。"""


#计算TF-IDF值
transformer = TfidfTransformer()
print(transformer)
tfidf = transformer.fit_transform(X) #将词频矩阵X统计成TF-IDF值
#查看数据结构
print(tfidf.toarray())        #tfidf[i][j]表示i类文本中的tf-idf权重
print(transformer.get_feature_names_out())
weight = tfidf.toarray()

# 第三步 KMeans聚类

clf = KMeans(n_clusters=3)
s = clf.fit(weight)
y_pred = clf.fit_predict(weight)
print(clf)
print(clf.cluster_centers_)  # 类簇中心
print(clf.inertia_)  # 距离:用来评估簇的个数是否合适 越小说明簇分的越好
print(y_pred)  # 预测类标

# 第四步 降维处理

pca = PCA(n_components=2)  # 降低成两维绘图
newData = pca.fit_transform(weight)
print(newData)
x = [n[0] for n in newData]
y = [n[1] for n in newData]

# 第五步 可视化


plt.scatter(x, y, c=y_pred, s=100, marker='s')
plt.title("Kmeans")
plt.xlabel("x")
plt.ylabel("y")
plt.show()
