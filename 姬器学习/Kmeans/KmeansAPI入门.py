"""
Kmeans简介：
    Kmeans属于无监督学习，有特征，无标签，根据样本间的相似性进行划分
    相似性即样本间距离，有：欧氏距离（勾股定理）、曼哈顿距离（城市街区）、切比雪夫距离、闵式距离等
    一般项目初期，还没有进行数据标注时，使用Kmeans聚类较多
"""
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs # 按照高斯分布（正态分布）生成数据集
from sklearn.metrics import calinski_harabasz_score # 评价指标，值越大聚类效果越好

#1. 准备数据集     👇生成样本总数    👇样本特征数   👇样本质心                             👇样本标准差
x,y = make_blobs(n_samples=1000,n_features=2,centers=[[-1,-1],[0,0],[1,1],[2,2]],cluster_std=[0.1,0.3,0.2,0.4],random_state=42)

#2. 画一下数据集分布
plt.figure(figsize=(10,10),dpi=100)
plt.scatter(x[:,0],x[:,1],c=y)
plt.show()

#3. 创建模型对象      👇聚类数量
estimator = KMeans(n_clusters=4)

#4. 模型预测
pre_result = estimator.fit_predict(x)
print(pre_result) # 预测结果是每个样本属于哪个类别

#5.绘制预测结果
plt.figure(figsize=(10,10),dpi=100)
plt.scatter(x[:,0],x[:,1],c=pre_result)
plt.show()