"""
GBDT梯度提升树泰塔尼克号预测
GBDT回归算法思路： 损失函数为均方误差
    1.初始化预测值：求观测值的平均值（其实是负梯度最小时的预测值）作为第一个弱学习器的预测值
    2.计算每个样本的残差（伪残差），并搭建回归决策树进行残差拟合，若叶子节点有多个结果，求平均值为输出结果（仍然是负梯度最小）
    3.补充回归决策树的搭建：划分样本，使用残差平方和最小处作为根节点，具体为每个样本残差拟合值减去平均拟合值，平方求和以此类推
    4.更新模型：第二个弱学习器的预测值 = 上一个弱学习器的预测值 + 学习率 * 回归决策树拟合的残差
    5.最终输出：F（X） = F0（x） + 学习率 * Σ hi（x） （对残差的拟合）
GBDT分类算法思路大致和回归相似，不同点： 损失函数为对数损失LogLoss
    1.初始化：计算对数几率F0：ln（odd），初始概率p0：sigmoid（F0）
    2.计算伪残差（依赖每次弱学习器计算的当前概率）： 真实标签（0，1） - 当前概率（p0）
    3.拟合伪残差：回归树
    4.计算叶子输出：这里比回归复杂，使用分子残差和除以分母概率方差进行加权修正
    5.更新模型：Fm（x） = Fm-1（x） + 学习率 * 拟合残差（这里更新的是对数几率而不是直接更新概率）
    6.计算当前概率：sigmoid（Fm），重复2-6步骤。
    7.最终输出：所有弱学习器的对数概率之和 使用sigmoid映射为概率
GBDT参数介绍：
    n_estimators	弱学习器数量（默认100）
    learning_rate	学习率（默认0.1）
    subsample	样本采样率（默认1.0）:	可防过拟合：噪音多场景（如用户行为预测）选0.6~0.8；数据纯净场景（如实验室数据）可选1.0
    loss损失函数	deviance（对数损失）、exponential（指数损失）、ls（均方误差）、huber（鲁棒损失）、quantile（分位数回归）
        数据干净、无异常值 	        均方误差（ls）	        默认参数即可
        存在离群点 （如金融数据）	    Huber损失（huber）	    alpha调至0.9~0.95
        需要预测区间（如医疗预后）	    分位数损失（quantile）	alpha=0.5中位数，alpha=0.9上限
        二分类概率预测（如CTR预估）	对数损失（deviance）	    配合calibration=True提升概率校准
        多分类任务	                对数损失（多分类扩展） 	需设置n_classes

"""
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV

#1. 数据加载
data = pd.read_csv('./data0/train.csv')
data.info()

#2. 数据预处理
data.loc[:,'Age'].fillna(data['Age'].mean(),inplace=True)

#3. 特征工程
#3.1 特征选取
x = data[['Sex','Pclass','Age']]
y = data['Survived']
#3.2 热编码处理
x = pd.get_dummies(x)
x = x.drop(columns=['Sex_female'])
print(x)
#3.3 划分数据集
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2,random_state=42)

#4. 模型训练
#4.1 单一决策树
estimator1 = DecisionTreeClassifier(max_depth=4)
estimator1.fit(x_train,y_train)
pre_result1 = estimator1.predict(x_test)
print(f"单一决策树分类评估报告：\n{classification_report(y_test,pre_result1)}")

#4.2 GBDT
estimator2 = GradientBoostingClassifier(n_estimators=100,max_depth=4)
estimator2.fit(x_train,y_train)
pre_result2 = estimator2.predict(x_test)
print(f"GBDT分类评估报告：\n{classification_report(y_test,pre_result2)}")

#4.3 网格儿搜索交叉验证
params = {'n_estimators':[90,120,150],'learning_rate':[0.1,1.0,0.5],'max_depth':[4,6,8]}
estimator3 = GridSearchCV(estimator=GradientBoostingClassifier(),param_grid=params,cv=4)
estimator3.fit(x_train,y_train)
pre_result3 = estimator3.predict(x_test)
print(f"GBDT分类评估报告(网格儿)：\n{classification_report(y_test,pre_result3)}")
print(f'最佳参数组合：{estimator3.best_params_}')


















