"""
随机森林，集成学习之Bagging思想

集成学习：把多个弱学习器组合成一个强学习器的过程
思想：bagging、boosting：
    bagging：1.有放回的随机抽样 2.平权投票 3.可以并行执行
    boosting：1.每次训练使用全样本 2.加权投票->预测正确降低权重，预测错误增加权重 3.串行执行

随机森林：1.每个弱学习器必须是CART树 2.有放回随机抽样 平权投票 并行执行
参数说明：
    n_estimators(默认100)，森林中决策树的数量一般100-500之间，树越多模型越稳定，但边际效益递减
    criterion(默认"gini")"gini"(基尼系数)或"entropy"(信息熵)
    max_depth(默认None)树的最大深度，通常不设置(完全生长)，或通过交叉验证确定
    min_samples_split(默认2)节点分裂所需的最小样本数，值越大树越保守，防止过拟合
    min_samples_leaf(默认1)叶节点所需的最小样本数，控制叶节点纯度，防止异常值影响
    max_features(默认"sqrt")可选值：整数/浮点数/"auto"/"sqrt"/"log2"，寻找最佳分割时考虑的特征数量，控制特征随机性，典型设置为特征数的平方根
    bootstrap(默认True)是否使用有放回抽样(bootstrap抽样)，True可增加模型多样性
    n_jobs​ (默认None)并行运行的作业数，-1使用所有处理器，加速训练

"""
import  pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV # 网格儿搜索

#1. 加载数据集
data = pd.read_csv('data0/train.csv')
data.info()

#2. 数据预处理
data.loc[:,'Age'].fillna(data.loc[:,'Age'].mean(),inplace=True)

#3. 特征选取
x = data[['Age','Pclass','Sex']]
y = data['Survived']

#4.特征工程
x = pd.get_dummies(x) #热编码创建Sex副本
x.drop(columns=['Sex_female'],inplace=True)
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2,random_state=42)

#5.模型训练之单一决策树
estimator1 = DecisionTreeClassifier(max_depth=None)
estimator1.fit(x_train,y_train)
pre_result1 = estimator1.predict(x_test)
print(f"单一决策树预测结果：\n{classification_report(y_test,pre_result1)}")

#6. 模型训练之随机森林
estimator2 = RandomForestClassifier(max_depth=None)
estimator2.fit(x_train,y_train)
pre_result2 = estimator2.predict(x_test)
print(f"随机森林预测结果：\n{classification_report(y_test,pre_result2)}")

#7. 随机森林之网格搜索
estimator3 = RandomForestClassifier()
#参数准备
params = {'n_estimators':[90,120,150],'max_depth':[4,6,8]}
Grid_Search_estimator = GridSearchCV(estimator=estimator3,param_grid=params,cv=3)
Grid_Search_estimator.fit(x_train,y_train)
pre_result3 = Grid_Search_estimator.predict(x_test)
print(f"网格儿搜索随机森林预测结果：\n{classification_report(y_test,pre_result3)}")
print(f"最佳参数组合（他以为的）：{Grid_Search_estimator.best_params_p}")























