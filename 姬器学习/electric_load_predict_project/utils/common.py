import numpy as np
import pandas as pd
from datetime import datetime
def preprocessing(file_dir):
    data = pd.read_csv(file_dir)
    # data.info()
    data['time'] = pd.to_datetime(data['time']) # 自动识别常见日期格式 将字符串时间 → datetime64[ns] 类型
    data.sort_values('time',ascending=True,inplace=True) # 按时间排序（需要 datetime 类型）
    data['time'] = data['time'].dt.strftime('%Y-%m-%d %H:%M:%S') # 将 datetime 格式化回字符串
    # print(data.head())
    data.drop_duplicates(inplace=True) # 删除 DataFrame 中的重复行
    # print(data.head())
    return data

def calculate_weekday(target_date_str):
    # 基准日：2013-09-02（星期一）
    base_date = datetime(2013, 9, 2)
    target_date = datetime.strptime(target_date_str, "%Y-%m-%d")

    # 计算天数差
    delta = (target_date - base_date).days

    # 计算星期几（星期一为0，星期日为6）
    weekday = (delta % 7 + 0) % 7  # 0=Monday, 1=Tuesday, ..., 6=Sunday

    weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    return weekdays[weekday]

def feature_engineering(data_source):
    # 先处理通用的数据anadata 👇
    ana_data = data_source.copy()
    ana_data['hour'] = ana_data['time'].str[11:13]  # 可以直接访问每个元素的str，不需要apply和map逐行操作
    ana_data['week'] = ana_data['time'].str[0:10].apply(
        lambda x: calculate_weekday(x))  # common定义了一个计算星期的函数，使用apply加给数据
    # ana_data['week'] = ana_data['time'].str[0:10].apply(lambda x : pd.to_datetime(x).weekday()) #或者用weekday更方便
    ana_data['is_holiday'] = ana_data['week'].apply(lambda x: 1 if x in ['星期六', '星期天'] else 0)
    ana_data['month'] = ana_data['time'].str[5:7]
    # ana_data.info()
    # print(ana_data)

    # 再处理用来训练的数据 👇
    dummy_data = pd.get_dummies(ana_data[['hour','is_holiday','month']]) # 热编码老朋友了,拿一下这三个字段的dummy
    past_1h = ana_data['power_load'].shift(1).rename('past_1h')           # 拿到前1小时的负荷
    past_2h = ana_data['power_load'].shift(2).rename('past_2h') # 拿到前2小时的负荷
    past_3h = ana_data['power_load'].shift(3).rename('past_3h') # 拿到前3小时的负荷
    past_hour = pd.concat([past_1h,past_2h,past_3h],axis=1)
    yesterday1 = ana_data['power_load'].shift(24).rename('yesterday1')
    yesterday2 = ana_data['power_load'].shift(48).rename('yesterday2')
    yesterday3 = ana_data['power_load'].shift(72).rename('yesterday3')
    train_data = pd.concat([ana_data['power_load'],dummy_data,past_hour,yesterday1,yesterday2,yesterday3],axis=1)
    train_data.dropna(inplace=True)
    # train_data.info()
    # print(train_data)
    return ana_data,train_data



if __name__ == '__main__':
    preprocessing('../data/test.csv').info()