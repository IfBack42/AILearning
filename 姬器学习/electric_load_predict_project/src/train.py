import os
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
from utils.common import preprocessing,feature_engineering
from utils.log import Logger
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split,GridSearchCV
from sklearn.metrics import mean_squared_error,mean_absolute_error,mean_absolute_percentage_error
import joblib
plt.rcParams["font.sans-serif"] = ["SimSun"]
plt.rcParams["axes.unicode_minus"] = False

#1. 定义电力负荷模型类，配置日志，获取数据
class power_load_prepare():
    #1.1 初始化属性信息
    def __init__(self):
        #1.2 配置日志对象
        logfile_name = "train" + datetime.datetime.now().strftime('%Y%m%d') + '.log'
        self.loggeeer = Logger('../log',logfile_name,'IFback').get_logger()
        self.loggeeer.info(f'{"="*20}初始化了power_load_prepare类{"="*20}')
        self.data_source = preprocessing('../data/train.csv')
        self.ana_data,self.train_data = feature_engineering(self.data_source)


    def data_analysis(self):
        self.loggeeer.info("查看了数据分布")
        #1.查看数据整体情况 2.整体负荷分布趋势 3.平均一天各小时分布趋势 4.平均每年各月分布趋势 5.平均每周各天分布趋势
        # 拿到各个字段的平均值 👇
        mean_hour = self.ana_data.groupby('hour', as_index=False)['power_load'].mean()
        mean_week = self.ana_data.groupby('week', as_index=False)['power_load'].mean()
        mean_week = mean_week.sort_values('week', key=lambda x: x.map({
            '星期一': 0, '星期二': 1, '星期三': 2,'星期四': 3, '星期五': 4, '星期六': 5, '星期日': 6
        }))
        mean_holiday = self.ana_data.groupby('is_holiday', as_index=False)['power_load'].mean()
        mean_month = self.ana_data.groupby('month', as_index=False)['power_load'].mean()

        # 可视化 👇
        fig, ax = plt.subplots(ncols=1, nrows=5, figsize=(20, 40))  # 如果是多行多列，ax相应变动，如ax[1,2]，就不只是单维
        ax[0].hist(self.ana_data['power_load'],bins=100) #x（必需）：输入数据（一维数组或列表）。bins：直方图的柱子数量或边界值。range：数据的取值范围（元组 (min, max)）。density：是否归一化为概率密度（默认为 False）。color：柱子颜色（如 'blue', '#FF5733'）。alpha：透明度（0~1）。label：图例标签。histtype：直方图类型（如 'bar', 'step', 'stepfilled'）。
        ax[1].plot(mean_hour.iloc[:,0],mean_hour.iloc[:,1])
        ax[2].plot(mean_week.iloc[:,0],mean_week.iloc[:,1])
        ax[3].plot(mean_month.iloc[:,0],mean_month.iloc[:,1])
        ax[4].bar(['工作日','周末'],mean_holiday['power_load'])
        ax[0].set_title('total_power_load',fontsize=25)
        ax[0].set_ylabel('frequency',fontsize=25)
        ax[1].set_title('mean_hour',fontsize=45)
        ax[1].set_xlabel('hour',fontsize=25)
        ax[2].set_title('mean_week',fontsize=45)
        ax[2].set_xlabel('week',fontsize=25)
        ax[3].set_title('mean_month',fontsize=45)
        ax[3].set_xlabel('month',fontsize=25)
        ax[4].set_title('holiday',fontsize=25)
        plt.savefig('../data/fig/analysis.png')
        plt.show()


    def model_train(self):
        self.loggeeer.info("模型开始GS训练")
        # 1.数据集切分 2.网格儿搜索交叉验证
        train_data = self.train_data.copy()
        x_train,x_test,y_train,y_test = train_test_split(train_data.iloc[:,1:-1],train_data.iloc[:,0],test_size=0.2)
        estimator = XGBRegressor()
        params = {'n_estimators':[80,100,130,150],'max_depth':[4,5,6,7],'learning_rate':[0.1,0.2,0.3,0.5]}
        GS = GridSearchCV(estimator=estimator,param_grid=params,cv=4)
        time_start = time.time()
        GS.fit(x_train,y_train)
        time_end = time.time()
        self.loggeeer.info(f'模型最优参数组合：{GS.best_params_}')
        self.loggeeer.info(f'GS训练用时：{time_end-time_start}')


    def model_test(self):
        self.loggeeer.info('开始模型预测')
        # 1.数据集切分 2.模型训练 3.模型评估 4.模型保存
        train_data = self.train_data.copy()
        print(train_data.columns)
        x_train,x_test,y_train,y_test = train_test_split(train_data.iloc[:,1:],train_data.iloc[:,0],test_size=0.2)
        estimator = XGBRegressor(learning_rate=0.2,max_depth=4,n_estimators=150)
        estimator.fit(x_train,y_train)
        pre_result = estimator.predict(x_test)
        self.loggeeer.info(f'预测结果：{pre_result}')
        self.loggeeer.info(f'均方误差：{mean_squared_error(y_test,pre_result)}')
        self.loggeeer.info(f'均方根误差：{np.sqrt(mean_squared_error(y_test,pre_result))}')
        self.loggeeer.info(f'平均绝对误差：{mean_absolute_error(y_test,pre_result)}')
        self.loggeeer.info(f'平均绝对百分比误差：{mean_absolute_percentage_error(y_test,pre_result)}')
        filename = '../model/xgb_IFback.pt'
        joblib.dump(estimator,filename)
        self.loggeeer.info(f'模型已保存至：{filename}')


if __name__ == '__main__':
    power_load_prepare().data_analysis()
    # power_load_prepare().model_test()

