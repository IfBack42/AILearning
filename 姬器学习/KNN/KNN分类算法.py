"""
基于欧氏距离计算每个训练集距离测试集的距离
对应维度差值的平方和开放
按照距离值找到距离最小的K个样本值
投票选取票数最多的测试集标签作为测试集的标签
如果标签数一致，选取最近的标签结果（最简单模型，奥卡姆剃刀原理）
"""
from sklearn.neighbors import KNeighborsClassifier

#1.创建模型对象 estimator->评估器
estimator = KNeighborsClassifier(n_neighbors=2)

#2.准备数据集（x_train,y_train）
x_train = [[1],[2],[3],[4]]
y_train = [0,0,0,1]

#3.准备测试集（y_test）
x_test = [[5]]

#4.模型训练(1.训练集特征，2.训练集标签)
estimator.fit(x_train,y_train)

#5.模型预测并输出
#传入测试集特征，获取测试集标签
y_test = estimator.predict(x_test)
print(y_test)