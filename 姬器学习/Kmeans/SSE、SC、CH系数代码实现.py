"""
聚类算法评估指标：SSE、CH、SC：
    一般优先选择SC值
    1.SSE+肘部法
        SSE：所有簇的所有样本到该簇质心的 误差平方和
            SSE越小，簇内样本越聚集，内聚程度越高，
            随着K值增加，SSE会逐渐减小，根据图像，SSE值下降变缓的时候为最佳K值
    2.SC轮廓系数：
        考虑簇内 -> 越小越好
        考虑簇外 ->越大越好
    3.CH轮廓系数：
        考虑簇内 -> 越小越好
        考虑簇外 ->越大越好
        考虑k值 -> 越小越好，样本内聚程度越高
"""
import os
os.environ["OMP_NUM_THREADS"] = "1"  # 限制 OpenMP 使用单线程
from sklearn.cluster import KMeans
from sklearn.metrics import calinski_harabasz_score,silhouette_score #SSE
from sklearn.datasets import make_blobs # 按照高斯分布（正态分布）生成数据集
import matplotlib.pyplot as plt

def SSE():
    #1. 生成数据集 x接收二维特征，y接收簇的位置
    x,y = make_blobs(n_samples=1000,n_features=2,centers=[[-1,-1],[0,0],[1,1],[2,2]],cluster_std=[0.1,0.4,0.2,0.5])
    #2.定义SSE列表记录值
    SSE_list = []
    #3.循环训练Kmean，计算不同K值时SSE值
    for k in range(1,100):
        estimator = KMeans(n_clusters=k,max_iter=100)
        estimator.fit(x) #训练时只需要传入特征，不需要传入标签
        sse_value = estimator.inertia_ #SSE
        SSE_list.append(sse_value)
    print(SSE_list)
    plt.figure(figsize=(20,10),dpi=100)
    plt.plot(range(1,100),SSE_list,marker='o')
    plt.xticks(range(0,100,3))
    plt.xlabel('K',fontsize=20)
    plt.ylabel('SSE',fontsize=20)
    plt.grid()
    plt.show()

def SC():
    #1. 生成数据集 x接收二维特征，y接收簇的位置
    x,y = make_blobs(n_samples=1000,n_features=2,centers=[[-1,-1],[0,0],[1,1],[2,2]],cluster_std=[0.1,0.4,0.2,0.3])
    #2.定义SC列表记录值
    SC_list = []
    #3.循环训练Kmean，计算不同K值时SC值
    for k in range(2,100):
        estimator = KMeans(n_clusters=k,max_iter=100,n_init='auto')
        estimator.fit(x) #训练时只需要传入特征，不需要传入标签
        pre_result = estimator.predict(x)
        sc_value = silhouette_score(x,pre_result)
        SC_list.append(sc_value)
    plt.figure(figsize=(20,10),dpi=100)
    plt.plot(range(2,100),SC_list,marker='o')
    plt.xticks(range(0,100,3))
    plt.xlabel('K',fontsize=20)
    plt.ylabel('SSE',fontsize=20)
    plt.grid()
    plt.show()

def CH():
    #1. 生成数据集 x接收二维特征，y接收簇的位置
    x,y = make_blobs(n_samples=1000,n_features=2,centers=[[-1,-1],[0,0],[1,1],[2,2]],cluster_std=[0.1,0.4,0.2,0.3])
    #2.定义CH列表记录值
    CH_list = []
    #3.循环训练Kmean，计算不同K值时CH值
    for k in range(2,100):
        estimator = KMeans(n_clusters=k,max_iter=100)
        estimator.fit(x) #训练时只需要传入特征，不需要传入标签
        pre_result = estimator.predict(x)
        CH_value = calinski_harabasz_score(x,pre_result)
        CH_list.append(CH_value)
    plt.figure(figsize=(20,10),dpi=100)
    plt.plot(range(2,100),CH_list,marker='o')
    plt.xticks(range(0,100,3))
    plt.xlabel('K',fontsize=20)
    plt.ylabel('CH',fontsize=20)
    plt.grid()
    plt.show()

if __name__ == '__main__':
    # SSE()
    SC()
    # CH()