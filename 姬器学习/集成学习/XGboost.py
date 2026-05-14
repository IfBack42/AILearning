"""
xgboost红酒品质分类案例

xgboost Extrem Gradient Boost概述：
    建模思路与adaboost类似，但是采用函数不同：
    1.在构建树时，使用的特殊的xgboost tree：
        从output输出值，推导familiar相似度，此外相似度的分母为：cover覆盖率+γ正则化参数再计算gain增益，最后比较超参γ和gain值，判断是否分裂
    2.output使用二阶泰勒公式求导，带入损失函数，计算最小梯度时的输出值得到，familiar使用相同公式，引入output计算得到
    3.gain为叶子familiar和+节点familiar
    4.gain - γ 为正值，允许分裂（不剪枝），为负值则不允许分裂（剪枝）
    5.近似贪婪算法：划分区间计算而不是每个节点都要计算，降低计算成本
    6.并行学习：同时条用多个核心计算
    7.加权分位数草图：通过特征权重快速查找分位点，结合近似贪婪算法
    8.稀疏感知分裂查找：在每个树节点中添加一个默认方向，当特征值缺失时，实例会被分类到默认方向，简而言之能够有效处理缺失值
参数介绍：
    n_estimators (num_round)：迭代次数
    learning_rate (eta)：默认0.3
    max_depth：默认6
    gamma：默认0（最小损失减少阈值）
    min_child_weight：叶子节点最小Hessian和     防止过拟合：设为3-5；类别不平衡：增大此值
    reg_alpha (alpha)：L1正则系数
    reg_lambda (lambda)：L2正则系数
    subsample：默认0.3（样本采样比例）     大数据集：0.8-1；小数据集：0.5-0.8
    missing:缺失值默认None ，可设置为其他值
    scale_pos_weight:二分类时，自定义样本权重，手动将少量样本权重增大 ， 多分类时，sample_weight在fit（）时传入
    损失函数objective：
        回归任务	reg:squarederror	连续值预测（默认选择）	直接输出预测值
        二分类	binary:logistic	概率预测（最常用）	输出[0,1]区间概率
                binary:logitraw	未校准的原始分数	输出(-∞,+∞)原始值
        多分类	multi:softmax	直接输出类别标签	需配合num_class参数
                multi:softprob	输出每个类别的概率	输出N维概率向量
        排序任务	rank:pairwise	Learning-to-rank场景	输出排序得分
"""

import joblib # 用于保存训练好的模型，记录参数
import numpy as np
import pandas as pd
from xgboost import XGBClassifier
from collections import Counter # 对于SR对象，效果同SR.value_counts 对于数组，没办法只能用这个
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import StratifiedKFold #分层K折交叉验证，避免某一类别样本过少或缺失，确保每个训练集和测试集中各类别的分布与原始数据集相同
from sklearn.utils import class_weight # 直接在损失函数层面调整样本重要性,处理类别不平衡,平衡样本权重

def preprocessing():
    data = pd.read_csv('./data/红酒品质分类.csv')
    data.info()
    x = data.iloc[:,:-1]
    y = data.iloc[:,-1]
    print(y.value_counts())
    #标签编码，处理标签分布为3 4 5 6的情况，让标签变成0 1 2 3分布
    transfor = LabelEncoder()
    y = pd.DataFrame(transfor.fit_transform(y))
    print(y.value_counts())
    # y = transfor.fit_transform(y)
    # print(Counter(y))
    # 划分数据集
    x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2,random_state=42,stratify=y) # stratify:抽样时参考y标签分布
    #拼接后保存，避免每次都要处理数据
    train = pd.concat([x_train,y_train],axis=1)
    test = pd.concat([x_test,y_test],axis=1)
    train.to_csv('./data/红酒品质分类训练集.csv',index=False)
    test.to_csv('./data/红酒品质分类测试集.csv',index=False)

def model():
    train = pd.read_csv('./data/红酒品质分类训练集.csv')
    test = pd.read_csv('./data/红酒品质分类测试集.csv')
    x_train = train.iloc[:,:-1]
    y_train = train.iloc[:,-1]
    x_test = test.iloc[:,:-1]
    y_test = test.iloc[:,-1]
    #平衡样本权重                                   👇计算权重的模式    👇样本类别，根据哪些类别计算权重 👇传入样本
    # weight = class_weight.compute_class_weight('balanced',classes=np.unique(y_train),y=y_train)
    weight = class_weight.compute_sample_weight('balanced',y=y_train) #compute_class_weight计算类别权重	compute_sample_weight计算每个样本权重
    estimator = XGBClassifier(objective='multi:softmax',max_depth=6,n_estimators=100,learning_rate=0.1)
    #多分类模型，训练时才能传入weight参数
    estimator.fit(x_train,y_train,sample_weight=weight)
    # 单次训练评估
    pre_result = estimator.predict(x_test)
    print(f'一次训练分类评估报告：\n{classification_report(y_test,pre_result)}')
    #保存模型
    joblib.dump(estimator,'./单一XGBoost红酒分类.pkl')

    # 网格儿搜索
    params = {'n_estimators':[80,100,110,120],'max_depth':[4,5,6,7],'learning_rate':[0.1,0.25,0.5,1]}
    #分层K折交叉验证         👇折数     👇是否打乱数据    👇随机种子
    skf = StratifiedKFold(n_splits=5,shuffle=True,random_state=42)
    GS_estimator = GridSearchCV(estimator,param_grid=params,cv=skf)
    GS_estimator.fit(x_train,y_train)
    pre_result2 = GS_estimator.predict(x_test)
    print(f'网格儿搜索模型分类评估报告：\n{classification_report(y_test,pre_result2)}')
    print(f'最优参数组合：{GS_estimator.best_params_}')
    joblib.dump(GS_estimator.best_estimator_,'./网格儿搜索最优XGBoost红酒分类.pkl')




if __name__ == '__main__':
    # preprocessing()
    model()





