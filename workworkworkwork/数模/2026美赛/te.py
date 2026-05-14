import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 数据
data = {
    'feature': ['age', 'gender', 'dancer_ability', 'dancer_popularity', 'dancer_experience',
               'week_num', 'week_eliminated', 'occupation_Athlete', 'occupation_Comedian',
               'occupation_Entrepreneur', 'occupation_Model', 'occupation_News Anchor',
               'occupation_Other_Occupation', 'occupation_Politician', 'occupation_Racing Driver',
               'occupation_Radio Personality', 'occupation_Singer/Rapper', 'occupation_Social Media Personality',
               'occupation_TV Personality', 'region_group_Midwest', 'region_group_Other_Region',
               'region_group_South', 'region_group_Unknown', 'region_group_West_Coast'],
    'importance_judge_norm': [0.25590705084066656, 0.011364793943975599, 0.03751034178631596,
                             0.029434670835118044, 0.062113529980025145, 0.14381382376658708,
                             0.3451480756765123, 0.010818726763787995, 0.0022995735676145097,
                             0.00025461975726544483, 0.0010486904485877105, 0.00017830963473247768,
                             0.0040719427784919465, 0.0055505810275551185, 0.001204191519887413,
                             0.0008937066697623814, 0.008410549378164536, 0.0014548805706361939,
                             0.026468160871699477, 0.002802749867274181, 0.02230464491749902,
                             0.01297721090288216, 0.006579941459571665, 0.007389233035387158],
    'importance_fan_norm': [0.26127144404202407, 0.007092642797460585, 0.019295736100033888,
                          0.07801576471061684, 0.12931190648252933, 0.1577746675323965,
                          0.19206620241772512, 0.0168606047693817, 0.002266332847017449,
                          0.0016943732130658311, 0.0005953650200846902, 0.00012198654945156086,
                          0.0044607892282765346, 0.010036218473277882, 0.010856530973007494,
                          0.0010093334147097221, 0.0052282389645266075, 0.0005749589661650198,
                          0.04028202058417742, 0.013230452597529958, 0.013678801652701062,
                          0.022388054826623625, 0.00369963153797367, 0.008187942299243434]
}

df = pd.DataFrame(data)

# 设置图形
plt.figure(figsize=(14, 10))

# 设置y轴位置
y_pos = np.arange(len(df['feature']))

# 绘制条形图
plt.barh(y_pos - 0.2, df['importance_judge_norm'], height=0.4,
         label='Judge Importance', alpha=0.8, color='skyblue')
plt.barh(y_pos + 0.2, df['importance_fan_norm'], height=0.4,
         label='Fan Importance', alpha=0.8, color='lightcoral')

# 设置标签和标题
plt.yticks(y_pos, df['feature'])
plt.xlabel('Normalized Importance Score')
plt.ylabel('Features')
plt.title('Feature Importance Comparison: Judge vs Fan (Normalized)')
plt.legend()

# 添加网格线
plt.grid(axis='x', alpha=0.3)

# 调整布局
plt.tight_layout()
plt.show()

# 可选：单独显示前10个最重要的特征（按法官重要性排序）
top_features = df.nlargest(10, 'importance_judge_norm')

plt.figure(figsize=(12, 8))
y_pos_top = np.arange(len(top_features['feature']))

plt.barh(y_pos_top - 0.2, top_features['importance_judge_norm'], height=0.4,
         label='Judge Importance', alpha=0.8, color='skyblue')
plt.barh(y_pos_top + 0.2, top_features['importance_fan_norm'], height=0.4,
         label='Fan Importance', alpha=0.8, color='lightcoral')

plt.yticks(y_pos_top, top_features['feature'],fontsize=14)
plt.xticks(fontsize=14)
plt.xlabel('Normalized Importance Score',fontsize=16)
plt.ylabel('Features',fontsize=16)
plt.title('Top 10 Feature Importance: Judge vs Fan (Normalized)',fontsize=20)
plt.legend()
plt.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.show()