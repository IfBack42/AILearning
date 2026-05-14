from sklearn.datasets import load_iris                  # sklearn自带数据集
from sklearn.preprocessing import StandardScaler        # 数据标准化
from sklearn.neighbors import KNeighborsClassifier      # 模型
from sklearn.model_selection import train_test_split    # 分割训练集和测试集
from sklearn.metrics import accuracy_score              # 模型评估参数
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1.定义函数加载数据集
def data_load():
    iris_data = load_iris()
    # print(iris_data)
    # print(type(iris_data)) # <class 'sklearn.utils._bunch.Bunch'> 这种数据结构可以使用 .键名 的形式，类似DF对象拿到某个值
    # print(iris_data.keys())
    # print(iris_data.data0[:5])
    # print(iris_data.target[:5])
    # print(iris_data.target_names) # 0,1,2分别是不同品种鸢尾花的名字
    # dict_keys(['data0', 'target', 'frame', 'target_names', 'DESCR', 'feature_names', 'filename', 'data_module'])
    #          特征值👆    标签👆               标签列名称👆            特征列名称👆
    return iris_data

# 2.数据可视化函数
def visual():
    iris_data = load_iris()
    iris_df = pd.DataFrame(data=iris_data.data,columns=iris_data.feature_names)
    iris_df['target'] = iris_data.target
    sns.lmplot(data=iris_df,x='sepal length (cm)',y='sepal width (cm)',hue='target',fit_reg=True)  # seaborn散点图可视化
#                               (如果没有分组的话不同组全是一个颜色)      分组字段👆      拟合回归线👆 （最小二乘法）
    plt.title(label='iris data0',fontsize=15)  # 他有fontsize但是偷偷藏起来不给看到
    plt.tight_layout()  # 紧密布局，防止标题被砍头
    plt.show()

# 3.划分训练集和测试集
def split(iris_data):
    #3.1 加载数据集
    iris_data = iris_data
    #3.2 数据划分                                     特征在前标签在后不能换👇                                            随机种子👇
    x_train,x_test,y_train,y_test= train_test_split(iris_data.data,iris_data.target,test_size=0.2,random_state=3)
    #3.3 打印
    print(f"训练集特征：{x_train},\n个数：{len(x_train)}")
    print(f"训练集标签：{x_test},\n个数：{len(x_test)}")
    print(f"测试集特征：{y_train},\n个数：{len(y_train)}")
    print(f"测试集标签：{y_test},\n个数：{len(y_test)}")

# 4.模型预测
def predict_evaluate(iris_data):
    iris_data = iris_data
    x_train,x_test,y_train,y_test = train_test_split(iris_data.data,iris_data.target,test_size=0.25)
    # 特征工程
    #1.特征提取：源数据4列都是要用的所以不需要筛选
    #2.特征预处理：源数据数据很干净且量纲相同，可以不进行标准化，但是比对一下吧
    transformer = StandardScaler()  # 这里一般只对特征进行标准化，所以只需要训练一次模型参数，测试集标准化直接用训练好的模型，有些神经网络回归才需要对标签进行标准化
    tsd_x_train = transformer.fit_transform(x_train)
    x_train_mean = transformer.mean_
    x_train_sigma = transformer.var_
    print(x_train_mean,x_train_sigma)
    tsd_x_test = transformer.transform(x_test)
    #3.训练模型
        #3.1 创建模型并训练
    KNN_model = KNeighborsClassifier(n_neighbors=5)
    KNN_model.fit(tsd_x_train,y_train)
        #3.2 对测试集进行预测
    result = KNN_model.predict(tsd_x_test)
    print(result,y_test)
        #3.3 对源数据之外的数据进行预测
    my_data = [[7.8,2.1,3.9,1.6]]
    tsd_my_data = transformer.transform(my_data)
    print(KNN_model.predict(tsd_my_data))
    # 查看数据集每种结果概率
    print(f"结果各分类概率：\n{KNN_model.predict_proba(tsd_my_data)}")
    #4.1 基于 训练集特征 和 训练集标签 直接评分 （测试集也行）
    print(f"准确率(正确率)：{KNN_model.score(tsd_x_train,y_train)}") # 这里也需要标准化后的特征
    #4.2 基于 测试集标签 和 预测结果 进行评分 这个更常用
    print(f"准确率(正确率)：{accuracy_score(y_true=y_test,y_pred=result)}")

if __name__ == '__main__':
    iris_data = data_load()
    visual()
    split(iris_data)
    predict_evaluate(iris_data)