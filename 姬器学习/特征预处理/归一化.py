"""
实际开发中，如果多个特征列因为量纲（单位）问题，导致数值差距过大，模型预测值会偏差
为保证每个特征列对最终预测结果的权重比都是相近的，所以要进行特征预处理的操作
实现方式：归一化、标准化

归一化：采用sklearn.preprocessing.MinMaxScaler类
    x' = (x - min) / (max - min)
    x“ = x' * (mx - mn) * mn
x -> 特征列中每个需要进行计算的值
min -> 该特征列的最小值
max -> 该特征列的最大值
mx -> 区间最大值，默认[0，1],即 mx = 1
mx -> 区间最小值，默认[0，1],即 mn = 0
弊端：
    即使数据再多，也只会受到该列数据的最大最小值影响，可能导致数据不均衡（鲁棒性差wc）
    特别是如果最大值或者最小值为异常值，导致计算结果较差
    所以归一化一般是小数据集，且数据干净的时候使用，开发过程中使用标准化更多
"""
from sklearn.preprocessing import MinMaxScaler

#1.创建归一化对象
transformer = MinMaxScaler(feature_range=(0,1))   #feature_range()参数默认[0,1]

#2. 准备数据集
x_train =[[90,2,10,40],[60,4,15,45],[75,3,13,46]]
x_test = [[22,6,12,43]]

#3.开始归一化
#3.1对训练集进行转换，并训练模型，fit+transform一步到位计算结果
# tsd_x_train = transformer.fit_transform(x_train)
#3.2或者使用两步进行计算：
transformer.fit(x_train)  # 计算训练集的均值和标准差,可以使用特定函数拿到对应值
tsd_x_train = transformer.transform(x_train)  # 用训练集的参数标准化测试集

#4.打印结果
print(tsd_x_train)