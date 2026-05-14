"""
标准化：采用 sklearn.preprocessing.StandardScaler 类
    x' = (x - mean) / σ(标准差)
    x -> 特征列中每个需要进行计算的值
    mean -> 该列值平均值
应用场景：
    比较适合大数据集的应用场景，受到最大值最小值的影响微乎其微
"""
from sklearn.preprocessing import StandardScaler

#1.创建标准化对象
transformer = StandardScaler()  #这儿就没即把什么范围了

#2.准备数据集
x_train =[[90,2,10,40],[60,4,15,45],[75,3,13,46]]

#3.标准化
#3.1 fit_transform
tsd_x_train = transformer.fit_transform(x_train)
#3.2 或者 fit + transform
# transformer.fit(x_train)
# tsd_x_train = transformer.transform(x_train)

#4.打印！
print(tsd_x_train)

#5.拿到均值和标准差
print(transformer.mean_)  # 均值
print(transformer.var_)  # 标准差