import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# 加载数据
df = pd.read_csv('./data/df_long.csv')

# 计算淘汰周的行业分布
eliminated_industries = df[df['is_eliminated'] == True]['celebrity_industry'].value_counts()

plt.figure(figsize=(14, 7))
sns.barplot(
    x=eliminated_industries.index,
    y=eliminated_industries.values,
    palette='coolwarm'
)
plt.title('Professional Distribution', fontsize=22, pad=20)
plt.xlabel('Industry', fontsize=18, labelpad=10)
plt.ylabel('Count', fontsize=18, labelpad=10)
plt.grid(True, linestyle='--', alpha=0.7)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.savefig('./data/industry_elimination.png', dpi=300)
plt.show()


# 首先对数据进行处理，计算每个赛季每周期间被淘汰的选手数
elimination_counts = df[df['is_eliminated'] == True].groupby(['season', 'week_num']).size().unstack(fill_value=0)

# 创建堆叠条形图
plt.figure(figsize=(16, 8))
elimination_counts.plot(kind='bar', stacked=True, colormap='tab20b', ax=plt.gca())
plt.xticks(fontsize=19,rotation=45)
plt.yticks(fontsize=19)
plt.title('Elimination Flow Across Seasons', fontsize=25, pad=20)
plt.xlabel('Week Number', fontsize=22, labelpad=10)
plt.ylabel('Number of Eliminations', fontsize=22, labelpad=10)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(title='Season', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('./data/elimination_flow_stacked_bar.png', dpi=300)
plt.show()




# 争议选手列表
controversial = ['Adam Rippon', "John O'Hurley",'Reginald VelJohnson','Evander Holyfield','Eric Roberts']

# 创建争议案例图
plt.figure(figsize=(14, 8))
for name in controversial:
    player_data = df[df['celebrity_name'] == name]
    sns.lineplot(
        data=player_data,
        x='week_num',
        y='J',
        label=name,
        linewidth=2.5,
        alpha=0.8,
        err_style=None,  # 禁用误差带
        estimator=None,  # 禁用聚合
    )

plt.title('J Score Trends of Controversial Cases', fontsize=24, pad=20)
plt.xlabel('Week Number', fontsize=20, labelpad=10)
plt.ylabel('J Score', fontsize=20, labelpad=10)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(title='Controversial Celebrities', loc='best')
plt.tight_layout()
plt.xticks(fontsize=19)
plt.yticks(fontsize=19)
plt.savefig('./data/controversial_cases.png', dpi=300)
plt.show()


key_players = ['Jerry Rice', 'Bobby Bones', 'Meryl Davis', 'John O\'Hurley', 'Adam Rippon']

plt.figure(figsize=(14, 8))


for name in key_players:
    player_data = df[df['celebrity_name'] == name]
    sns.lineplot(
        data=player_data,
        x='week_num',
        y='J',
        label=name,
        linewidth=2.5,
        alpha=0.8,
        err_style=None,  # 禁用误差带
        estimator=None,  # 禁用聚合
    )

plt.title('J Score Trends of Key Competitors', fontsize=24)
plt.xlabel('Week Number', fontsize=20, labelpad=10)
plt.ylabel('J Score', fontsize=20, labelpad=10)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(title='Key Competitors', loc='best')
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.tight_layout()
plt.savefig('./data/key_players_j.png', dpi=300, facecolor='white')
plt.show()

# 提取J值
j_data = df[df['J'] > 0]['J']

# 创建J分布图
plt.figure(figsize=(10, 6))

# 绘制J值分布
sns.histplot(
    j_data,
    bins=30,
    kde=True,
    color='#1f77b4',
    edgecolor='black',
    alpha=0.7
)

# 添加均值和中位数线
mean_j = j_data.mean()
median_j = j_data.median()

# 使用与前面图表一致的颜色
plt.axvline(mean_j, color='#FF6B6B', linestyle='--', linewidth=2, label=f'Mean: {mean_j:.2f}')
plt.axvline(median_j, color='#4ECDC4', linestyle='-.', linewidth=2, label=f'Median: {median_j:.2f}')

# 设置标题和标签
plt.title('Distribution of Judge Scores (J)', fontsize=20, pad=20)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.xlabel('Judge Score (J)', fontsize=18, labelpad=10)
plt.ylabel('Frequency', fontsize=18, labelpad=10)
plt.legend(fontsize=18)
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.savefig('./data/j_distribution.png', bbox_inches='tight', dpi=300)
plt.show()


