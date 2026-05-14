"""
基于用户年收入和消费指数进行相似性聚类

"""
import os


os.environ["OMP_NUM_THREADS"] = "1"  # 限制 OpenMP 使用单线程
import matplotlib.pyplot as plt
from sklearn.metrics import calinski_harabasz_score,silhouette_score
from sklearn.cluster import KMeans
import pandas as pd
from sklearn.preprocessing import StandardScaler
import numpy as np
#1. 数据预处理
def preprocessing():
    data = pd.read_csv('./data/customers.csv')
    x = data[['Annual Income (k$)','Spending Score (1-100)']]
    transfer = StandardScaler()
    x = transfer.fit_transform(x)
    # print(x)
    return x

#2. 找最佳质心数
def K(x):
    sse_list = []
    sc_list = []
    for k in range(2,50):
        estimator = KMeans(n_clusters=k,max_iter=100,n_init='auto')
        estimator.fit(x)
        pre_result = estimator.predict(x)
        sse = estimator.inertia_
        sc = silhouette_score(x,pre_result)
        sse_list.append(sse)
        sc_list.append(sc)
    plt.figure(figsize=(20,10),dpi=150)
    plt.plot(range(2,50),sse_list,marker='o')
    plt.xticks(range(0,50,3))
    plt.grid(visible=True)
    plt.show()
    plt.figure(figsize=(20,10),dpi=150)
    plt.plot(range(2,50),sc_list,marker='o')
    plt.xticks(range(0,50,3))
    plt.grid(visible=True)
    plt.show()
#3. 训练模型预测评估
def train_pre(x):
    k = int(input("根据图像选取的K值："))
    estimator = KMeans(n_clusters=k,n_init='auto',max_iter=100)
    estimator.fit(x)
    y_pre = estimator.predict(x)
    print(y_pre)
    #可视化预测结果
    plt.figure(figsize=(5,5),dpi=150)
    plt.scatter(x[y_pre==0,0],x[y_pre==0,1],label='1') # x[y_pre==0,0]含义:x列表筛选,行为y列表等于0的值(Ture,True,False等),列为第一行(0)
    plt.scatter(x[y_pre==1,0],x[y_pre==1,1],label='2')
    plt.scatter(x[y_pre==2,0],x[y_pre==2,1],label='3')
    plt.scatter(x[y_pre==3,0],x[y_pre==3,1],label='4')
    plt.scatter(x[y_pre==4,0],x[y_pre==4,1],label='5')
    center = estimator.cluster_centers_                         # 拿到预测的质心
    plt.scatter(center[:,0],center[:,1],c='black')
    plt.xlabel('Annual Income')
    plt.ylabel('Spending Score')
    plt.title('Clusters of Customers')
    plt.legend()
    plt.show()

if __name__ == '__main__':
    x = preprocessing()
    # K(x)
    train_pre(x)
