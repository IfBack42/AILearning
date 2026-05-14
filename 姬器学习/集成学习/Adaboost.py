"""
Adabboost葡萄酒预测
Adaboost属于boosting思想，即：串行执行，每次使用全部样本，最后加权投票
    原理：
    1.默认样本权重为1/n，使用全部样本特征，使用单层决策树（第一个弱分类器）进行训练，保留基尼值最小特征作为树桩，再根据预测结果调整样本权重
    2.样本调整权重后，将权重归一化，再对数据集进行重构，新数据集中，上次预测错误的样本具有更高权重，预测正确样本具有更低权重
    3.重复1，2过程，结束后，所有树桩进行加权投票
参数介绍：
    base_estimator：基学习器(弱分类器/回归器)，默认为决策树
    n_estimators：弱学习器的最大迭代次数，默认50，通常需要与learning_rate一起调参
    learning_rate：学习率，范围(0,1]，默认1。较小的值需要更多的弱学习器来达到相同拟合效果。工程引入，乘在模型权重前，公式本身没有
    algorithm：提升算法，可选'SAMME'或'SAMME.R'(默认)。SAMME.R使用预测概率，通常收敛更快；SAMME使用分类结果，适用性更广
    loss（回归特有）：损失函数，可选'linear'(默认)、'square'或'exponential'，对应不同误差计算方式
    其他max_depth，min_samples_leaf什么什么的和决策树相同

"""
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import AdaBoostClassifier
from sklearn.preprocessing import LabelEncoder #标签编码器，用于将多分类标签进行处理，类似热编码，不用关心标签数值关系，因为树模型不影响
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report

#1. 准备数据
data = pd.read_csv('./data/wine0501.csv')

#2. 数据预处理
data.info()
print(data[['Alcohol','Hue']].head(50))
# print(data['Class label'].unique())


#3. 特征工程 树模型对量纲要求不大，特征间差距实在太小可以使用标准化提高训练速度
# data = data.loc[data['Class label'] != 1]  # 数据集问题，只选两个种类进行预测正确率会高一些
x = data[['Alcohol','Hue']]
y = data['Class label']
transfer = LabelEncoder()
y = transfer.fit_transform(y)
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2)

#4.1 单一决策树模型训练
estimator1 = DecisionTreeClassifier(max_depth=4)
estimator1.fit(x_train,y_train)
pre_result1 = estimator1.predict(x_test)
print(f'单一决策树预测结果：{pre_result1}')
print(f'单一决策树正确率：{accuracy_score(y_true=y_test,y_pred=pre_result1)}')
print(f'单一决策树分类评估报告：\n{classification_report(y_test,pre_result1)}')

#4.2 Adaboost模型训练
estimator2 = AdaBoostClassifier(estimator=DecisionTreeClassifier(max_depth=4),n_estimators=200,learning_rate=1,algorithm='SAMME')
estimator2.fit(x_train,y_train)
pre_result2 = estimator2.predict(x_test)
print(f'Adaboost预测结果：{pre_result2}')
print(f'Adaboost正确率：{accuracy_score(y_true=y_test,y_pred=pre_result2)}')
print(f'Adaboost分类评估报告：\n{classification_report(y_test,pre_result2)}')




















