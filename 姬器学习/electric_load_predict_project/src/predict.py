"""
核心问题：递归预测中的  特征构建效率
    在时序递归预测中，主要性能瓶颈在于特征构建。每次预测都需要：
    1.获取历史数据（特别是最近几小时/天的数据）
    2.计算各种统计特征（均值、滞后值等）
    3.添加时间特征（小时、月份等）
    我试过动态更新df对象，效率及其低下，因为每次预测后都需要进行复杂的特征操作获取特征，
    反而使用字典存储数据，只需要简单查询，效率高很多

递归字典方案:
    1.逐步递归（在线学习）
    2.实时更新字典
    3.动态查询最新数据
    4.实时预测/流式数据
"""
import os

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime
import joblib
from utils.common import preprocessing, calculate_weekday
from utils.log import Logger
from sklearn.metrics import mean_squared_error,mean_absolute_error,mean_absolute_percentage_error


class PowerLoadPredict:
    def __init__(self, estimator, history_data_file):
        # 配置日志
        self._log_filename = "predict" + datetime.datetime.now().strftime('%Y%m%d') + '.log'
        self._logger = Logger(log_file_name=self._log_filename, root_path='../log', loger_name='IFback').get_logger()
        self._logger.info(f'{"=" * 20}初始化了PowerLoadPredict类{"=" * 20}')
        # 配置预测模型
        self._estimator = estimator
        # 获取历史数据并转换为高效字典
        self._data_source = preprocessing(history_data_file)
        self._history_dict = self._data_source.set_index('time')['power_load'].to_dict()
        # 存储预测结果
        self.predictions = []


    def _get_time_features(self, time_str):
        """这段热编码是真他妈巧妙，工业级优化，适用于字典不能使用get_dummy时，收藏了"""
        dt = datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
        # 小时特征 (24维度)
        hour_features = [1 if dt.hour == i else 0 for i in range(24)]
        # 月份特征 (12维度)
        month_features = [1 if dt.month == i else 0 for i in range(1, 13)]
        # 周特征
        weekday = calculate_weekday(time_str[:10])
        is_holiday = 1 if weekday in ['星期六', '星期天'] else 0
        return hour_features + month_features + [is_holiday]


    def _get_history_features(self, time_str):
        """高效获取历史负荷特征"""
        dt = datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S') # strptime字符串转换datetime
        # 获取前1小时、2小时、3小时的负荷
        prev_1h = (dt - datetime.timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S')
        prev_2h = (dt - datetime.timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S')
        prev_3h = (dt - datetime.timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S')
        # 获取昨日同时刻、前日同时刻、大前日同时刻负荷
        prev_day = (dt - datetime.timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
        prev_2day = (dt - datetime.timedelta(days=2)).strftime('%Y-%m-%d %H:%M:%S')
        prev_3day = (dt - datetime.timedelta(days=3)).strftime('%Y-%m-%d %H:%M:%S')
        return [
            self._history_dict.get(prev_1h),
            self._history_dict.get(prev_2h),
            self._history_dict.get(prev_3h),
            self._history_dict.get(prev_day),
            self._history_dict.get(prev_2day),
            self._history_dict.get(prev_3day)
        ]


    def predict(self, start_time, end_time):
        """递归预测指定时间范围内的负荷"""
        # 生成预测时间序列
        start_dt = pd.to_datetime(start_time)
        end_dt = pd.to_datetime(end_time)
        pred_times = pd.date_range(start=start_dt, end=end_dt, freq='H')
        # 清空之前的预测结果
        self.predictions = []
        for time in pred_times:
            time_str = time.strftime('%Y-%m-%d %H:%M:%S')
            self._logger.info(f"开始预测时间点: {time_str}")
            # 构建特征向量
            time_features = self._get_time_features(time_str)
            history_features = self._get_history_features(time_str)
            features = np.array([time_features + history_features])
            # 模型预测
            prediction = self._estimator.predict(features)[0]
            # 记录预测结果
            self.predictions.append({
                'time': time_str,
                'prediction': prediction,
                'true_value': self._history_dict.get(time_str, None)
            })
            # 将预测值加入历史字典（用于后续预测）
            self._history_dict[time_str] = prediction

        return pd.DataFrame(self.predictions)


    def evaluate(self):
        """评估预测结果"""
        results = pd.DataFrame(self.predictions)
        #可视化
        fig,ax = plt.subplots(figsize=(20,10),dpi=150)
        ax.plot(results['time'],results['prediction'],label='prediction')
        ax.plot(results['time'],results['true_value'],label='true_value')
        ax.set_xlabel('time',fontsize=20)
        ax.set_ylabel('load',fontsize=20)
        ax.set_xticks(results['time'][::6])
        ax.legend()
        ax.set_title('power_load_predict&conpare',fontsize=25)
        plt.xticks(rotation=15)
        plt.grid(visible=True,alpha=0.5)
        plt.show()
        #评估系数
        results = results.dropna()
        pre_result = results["prediction"]
        y_test = results["true_value"]
        self._logger.info(f'预测结果：\n{pre_result}')
        self._logger.info(f'均方误差：{mean_squared_error(y_test,pre_result)}')
        self._logger.info(f'均方根误差：{np.sqrt(mean_squared_error(y_test,pre_result))}')
        self._logger.info(f'平均绝对误差：{mean_absolute_error(y_test,pre_result)}')
        self._logger.info(f'平均绝对百分比误差：{mean_absolute_percentage_error(y_test,pre_result)}')


# 使用示例
if __name__ == '__main__':
    # 1. 加载模型
    estimator = joblib.load('../model/xgb_IFback.pt')
    # 2. 初始化预测器
    predictor = PowerLoadPredict(estimator, '../data/train.csv')
    # 3. 进行预测
    predictions = predictor.predict('2015-08-01 00:00:00', '2015-08-03 23:00:00')
    print(predictions)
    filename = '../data/' + "prediction" + pd.to_datetime(datetime.datetime.now()).strftime('%Y%m%d%H%M%S') + '.csv'
    pd.DataFrame(predictions).to_csv(filename)
    print(f'预测结果已保存至：{filename}')
        # 4. 评估结果（提供测试数据）
    predictor.evaluate()
