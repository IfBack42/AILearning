"""
CART决策树 分类部分
参数：
    criterion（分裂标准）："gini"基尼不纯度（默认值）；"entropy"：信息增益   中小数据集选基尼，大数据集选信息增益
    max_depth（树最大深度）：None不限制深度（易过拟合）；整数3-15层（常用4-8层） 常用max_depth ≈ log₂(特征数量) + 2
    min_samples_split（节点分裂最小样本数）：节点继续分裂所需的最小样本量   小数据集：2-10；大数据集：0.1%-1%总样本量
    min_samples_leaf（叶节点最小样本数：控制叶子节点的最小样本量 分类问题：1-5；回归问题：5-20（需保证叶节点统计显著性）
    max_features（分裂时考虑特征数）：类似随机森林的特征抽样   None用所有特征（决策树默认）；"sqrt"√总特征数（随机森林风格）；"log2"log2(总特征数)

"""
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.tree import plot_tree
import matplotlib.pyplot as plt

#1. 加载数据并查看
data = pd.read_csv('data/train.csv')
#1.1 age列有缺失，用平均值填充
data.loc[:,'Age'].fillna(data['Age'].mean(),inplace=True)
data.info()

#2. 特征选取
x = data[['Pclass','Sex','Age','Fare']]
y = data['Survived']
#2.1 热编码处理
x = pd.get_dummies(x)
x.drop(columns='Sex_female')
print(x.head())
#2.2划分数据集
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2)

#3. 模型训练预测
estimator = DecisionTreeClassifier(max_depth=10)
estimator.fit(x_train,y_train)
pre_result = estimator.predict(x_test)

#4. 模型评估
print(f'分类测试报告：\n{classification_report(y_test,pre_result)}')

#5. 决策树绘制
plt.figure(figsize=(30,20),dpi=250)
plot_tree(estimator,max_depth=10,filled=True)
plt.savefig('./data0/ttnc.png')
plt.show()























