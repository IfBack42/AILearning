"""
交叉验证：
    把数据分成n份，n折交叉验证（一般4折）
    第一次，把第一份数据作为验证集（测试集），其他作为训练集，训练模型和进行预测，获取第一种划分的准确率
    第二次，把第二份数据作为验证集（测试集），其他作为训练集，训练模型和进行预测，获取第二种划分的准确率
    第三次，把第三份数据作为验证集（测试集），其他作为训练集，训练模型和进行预测，获取第三种划分的准确率
    ...
    计算上述n次准确率的平均值作为模型最终准确率，
    最后找出准确率最高的一次，用全部数据（训练集+测试集）训练模型，再用第n次的测试集进行模型预测，
    以让模型最终验证结果最准确

网格搜索：
    作用：寻找最优超超参组合
    超参:外部输入参数，不同超参组合可能影响模型最终评测结果
    原理：接收超参可能出现的值，然后针对每个值进行交叉验证，获取到最优超参组合

网格搜索+交叉验证都是使用 GridSearchCV API 寻找供参考的最优参数组合
"""
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV,train_test_split  # 网格搜索+交叉验证
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.datasets import load_iris

iris_data = load_iris()

x_train,x_test,y_train,y_test = train_test_split(iris_data.data,iris_data.target,test_size=0.2)

transfer = StandardScaler()

x_train = transfer.fit_transform(x_train)

x_test = transfer.transform(x_test)

estimator = KNeighborsClassifier()

param_dict = {'n_neighbors':[i for i in range(1,11)]}

estimator = GridSearchCV(estimator=estimator,param_grid=param_dict,cv=4)

estimator.fit(x_train,y_train)

print(f"最优评分：{estimator.best_score_}")
print(f"最优超参组合：{estimator.best_params_}")
print(f"最优模型对象：{estimator.best_estimator_}")
print(f"具体交叉验证结果：{estimator.cv_results_}")

estimator = estimator.best_estimator_ # 或者直接从上面得到的最优超参创建新的最优模型

estimator.fit(x_train,y_train)

y_pre= estimator.predict(x_test)

print(f"模型准确率：{accuracy_score(y_test, y_pre)}")