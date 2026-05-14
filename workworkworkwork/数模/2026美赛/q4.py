import pandas as pd
import numpy as np
import scipy.stats as stats
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'Microsoft YaHei', 'DejaVu Sans']  # 中文字体
plt.rcParams['axes.unicode_minus'] = False  # 使用ASCII减号替代unicode减号

# ==================== 1. 数据加载与预处理 ====================
def load_and_preprocess_data():
    """加载并预处理数据，确保与上传文件匹配"""
    df_long = pd.read_csv('./data/df_long.csv')
    fan_votes = pd.read_csv('task1_estimated_votes.csv')

    # 合并数据
    df = pd.merge(
        df_long,
        fan_votes[['season', 'week_num', 'celebrity_name', 'estimated_p']],
        on=['season', 'week_num', 'celebrity_name'],
        how='inner'
    )

    # 标准化（按赛季+周）
    df['normalized_j'] = df.groupby(['season', 'week_num'])['J'].transform(
        lambda x: (x - x.mean()) / (x.std() + 1e-6)
    )
    df['normalized_p'] = df.groupby(['season', 'week_num'])['estimated_p'].transform(
        lambda x: (x - x.mean()) / (x.std() + 1e-6)
    )

    # 创建选手特征
    df = create_athlete_features_optimized(df)

    # 计算舞者指标
    df = calculate_dancer_metrics_optimized(df)

    # 严格处理缺失值
    required_cols = ['normalized_j', 'normalized_p', 'age', 'dancer_ability', 'dancer_popularity', 'dancer_experience']
    df = df.dropna(subset=required_cols)

    print(f"✅ 预处理完成: {df.shape[0]} 行, {df.shape[1]} 列")
    print(f" - 裁判评分: 均值={df['normalized_j'].mean():.4f}, 标准差={df['normalized_j'].std():.4f}")
    print(f" - 粉丝投票: 均值={df['normalized_p'].mean():.4f}, 标准差={df['normalized_p'].std():.4f}")

    return df

# ==================== 2. 选手特征工程 ====================
def create_athlete_features_optimized(df):
    """严格过滤小样本类别，避免系数爆炸"""
    df['age'] = pd.to_numeric(df['celebrity_age_during_season'], errors='coerce')

    # 职业处理：仅保留≥30样本的类别
    occ_counts = df['celebrity_industry'].value_counts()
    valid_occupations = occ_counts[occ_counts >= 30].index.tolist()
    df['occupation'] = df['celebrity_industry'].apply(
        lambda x: x if x in valid_occupations else 'Other_Occupation'
    )

    # 地区分组
    west_coast = ['California', 'Oregon', 'Washington']
    east_coast = ['New York', 'New Jersey', 'Massachusetts', 'Maine', 'Virginia']
    south = ['Texas', 'Florida', 'Alabama', 'Louisiana', 'South Carolina', 'Kentucky']
    midwest = ['Illinois', 'Ohio', 'Michigan', 'Delaware']

    def map_region(state):
        if pd.isna(state):
            return 'Unknown'
        if state in west_coast:
            return 'West_Coast'
        if state in east_coast:
            return 'East_Coast'
        if state in south:
            return 'South'
        if state in midwest:
            return 'Midwest'
        return 'Other_Region'

    df['region_group'] = df['celebrity_homestate'].apply(map_region)

    # 性别简化处理
    df['gender'] = df['celebrity_name'].str[-1].isin(['a', 'e', 'y']).astype(int)

    # 淘汰信息
    df['is_eliminated'] = df['results'].str.contains('Eliminated', na=False)
    df['week_eliminated'] = df['results'].str.extract(r'Eliminated Week (\d+)')[0].fillna(0).astype(int)

    keep_cols = ['season', 'week_num', 'celebrity_name', 'ballroom_partner', 'age',
                 'occupation', 'region_group', 'gender', 'normalized_j', 'normalized_p',
                 'is_eliminated', 'week_eliminated']

    return df[keep_cols]

# ==================== 3. 舞者指标计算 ====================
def calculate_dancer_metrics_optimized(df):
    """舞者经验改用总参赛周数（核心修正）"""
    for col in ['dancer_ability', 'dancer_popularity', 'dancer_experience']:
        df[col] = np.nan

    for dancer, group in df.groupby('ballroom_partner'):
        if len(group) < 3:
            continue

        # 舞者能力（α=0.9）
        season_j = group.groupby('season')['normalized_j'].mean()
        weights_j = 0.9 ** (season_j.index - season_j.index.min()).to_series()
        if weights_j.sum() > 0:
            df.loc[df['ballroom_partner'] == dancer, 'dancer_ability'] = (
                (season_j * weights_j).sum() / weights_j.sum()
            )

        # 舞者人气（β=0.95）
        season_p = group.groupby('season')['normalized_p'].mean()
        weights_p = 0.95 ** (season_p.index - season_p.index.min()).to_series()
        if weights_p.sum() > 0:
            df.loc[df['ballroom_partner'] == dancer, 'dancer_popularity'] = (
                (season_p * weights_p).sum() / weights_p.sum()
            )

        # 舞者经验：总参赛周数（关键修正！）
        df.loc[df['ballroom_partner'] == dancer, 'dancer_experience'] = len(group)

    # 填充缺失值
    for col in ['dancer_ability', 'dancer_popularity', 'dancer_experience']:
        df[col] = df[col].fillna(df[col].median())

    return df

# ==================== 4. DSI计算 ====================
def calculate_dual_standard_index(df):
    """计算双重标准指数（DSI）并返回包含选手DSI的DataFrame"""
    # 仅保留样本量≥30的类别
    occ_counts = df['occupation'].value_counts()
    valid_occupations = occ_counts[occ_counts >= 30].index.tolist()
    df_valid = df[df['occupation'].isin(valid_occupations)]

    # 准备特征
    features = ['age', 'occupation', 'region_group', 'gender', 'dancer_ability',
                'dancer_popularity', 'dancer_experience', 'week_num', 'week_eliminated']
    X = df_valid[features].copy()
    X = pd.get_dummies(X, columns=['occupation', 'region_group'], drop_first=True)

    # 标准化数值特征
    numeric_cols = ['age', 'dancer_ability', 'dancer_popularity', 'dancer_experience',
                    'week_num', 'week_eliminated', 'gender']
    scaler = StandardScaler()
    X[numeric_cols] = scaler.fit_transform(X[numeric_cols])

    # 训练模型
    X_train, X_test, yj_train, yj_test, yp_train, yp_test = train_test_split(
        X, df_valid['normalized_j'], df_valid['normalized_p'],
        test_size=0.2, random_state=42
    )

    # 线性回归
    lr_j = LinearRegression().fit(X_train, yj_train)
    lr_p = LinearRegression().fit(X_train, yp_train)

    # 提取系数
    coefs_j = pd.Series(lr_j.coef_, index=X.columns)
    coefs_p = pd.Series(lr_p.coef_, index=X.columns)

    # 创建DSI列
    df_valid['DSI'] = 0.5  # 默认值

    # 计算每个选手的DSI
    for idx, row in df_valid.iterrows():
        # 为每个特征计算DSI
        dsi_values = []
        for feat in X.columns:
            beta_j = coefs_j.get(feat, 0)
            alpha_p = coefs_p.get(feat, 0)

            if abs(beta_j) < 0.01 and abs(alpha_p) < 0.01:
                continue

            sign_opposite = 1.0 if beta_j * alpha_p < 0 else 0.0
            mag_diff = abs(abs(beta_j) - abs(alpha_p)) / (abs(beta_j) + abs(alpha_p) + 1e-8)
            dsi = 0.7 * sign_opposite + 0.3 * mag_diff
            dsi_values.append(dsi)

        # 取平均DSI
        df_valid.at[idx, 'DSI'] = np.mean(dsi_values)

    # 合并回原始DataFrame
    df = pd.merge(df, df_valid[['celebrity_name', 'DSI']], on='celebrity_name', how='left')
    df['DSI'] = df['DSI'].fillna(0.5)  # 填充默认值

    return df

# ==================== 5. 新系统评分计算 ====================
def calculate_dynamic_weights(df):
    """计算双重动态权重"""
    # 计算比赛进度
    df['season_max_weeks'] = df.groupby('season')['week_num'].transform('max')
    df['progress'] = (df['week_num'] - 1) / (df['season_max_weeks'] - 1)

    # 计算比赛进度权重
    k = 8  # 陡峭度参数
    x0 = 0.6  # 拐点位置
    df['w_progress'] = 1 / (1 + np.exp(-k * (df['progress'] - x0)))

    # 计算特征权重
    c = 5  # 调整参数
    df['w_feature'] = 1 / (1 + np.exp(-c * (1 - df['DSI'])))

    # 计算综合权重
    df['w_j'] = df['w_progress'] * df['w_feature'] + (1 - df['w_progress']) * (1 - df['w_feature'])
    df['w_p'] = 1 - df['w_j']

    # 计算综合得分
    df['combined_score'] = df['w_j'] * df['normalized_j'] + df['w_p'] * df['normalized_p']

    return df

# ==================== 6. 淘汰机制实现 ====================
def simulate_elimination(df):
    """模拟淘汰机制"""
    results = []

    for (season, week), group in df.groupby(['season', 'week_num']):
        if not group['is_eliminated'].any():
            continue

        n_elim = group['is_eliminated'].sum()

        # 计算综合得分
        group = group.sort_values('combined_score')

        # 找出最危险的2名选手
        bottom_two = group.head(2)

        # 裁判选择淘汰者（裁判评分更低者）
        if len(bottom_two) >= 2:
            # 选择裁判评分更低的选手
            eliminated = bottom_two.iloc[0] if bottom_two['normalized_j'].iloc[0] < bottom_two['normalized_j'].iloc[1] else bottom_two.iloc[1]
        else:
            eliminated = bottom_two.iloc[0]

        results.append({
            'season': season,
            'week': week,
            'actual_eliminated': group[group['is_eliminated']]['celebrity_name'].tolist(),
            'simulated_eliminated': eliminated['celebrity_name'],
            'is_correct': eliminated['celebrity_name'] in group[group['is_eliminated']]['celebrity_name'].tolist()
        })

    return pd.DataFrame(results)

# ==================== 7. 评估与可视化 ====================
def evaluate_system(elimination_results):
    """评估新系统性能并生成可视化"""
    # 计算淘汰预测准确率
    correct_count = elimination_results['is_correct'].sum()
    total_weeks = len(elimination_results)

    print(f"\n✅ 淘汰预测准确率: {correct_count}/{total_weeks} ({correct_count / total_weeks:.2%})")

    # 按季度分析准确率
    season_accuracy = elimination_results.groupby('season')['is_correct'].mean().reset_index()
    season_accuracy.columns = ['season', 'accuracy']

    # 可视化结果
    plt.figure(figsize=(12, 6))
    sns.barplot(x='season', y='accuracy', data=season_accuracy)
    plt.title('淘汰预测准确率按季度')
    plt.xlabel('季度')
    plt.ylabel('准确率')
    plt.savefig('elimination_accuracy.png')

    print("\n✅ 淘汰预测准确率已保存至: elimination_accuracy.png")

    return season_accuracy

# ==================== 8. 主函数 ====================
def main():
    print("=" * 70)
    print("🎯 问题四：动态权重平衡系统 - 机制优化设计")
    print("=" * 70)

    # 加载数据
    df = load_and_preprocess_data()

    # 计算DSI
    df = calculate_dual_standard_index(df)

    # 计算动态权重
    df = calculate_dynamic_weights(df)

    # 模拟淘汰机制
    elimination_results = simulate_elimination(df)

    # 评估系统
    season_accuracy = evaluate_system(elimination_results)

    # 保存结果
    df.to_csv('dynamic_weight_system_results.csv', index=False)
    elimination_results.to_csv('elimination_simulation_results.csv', index=False)
    season_accuracy.to_csv('season_accuracy.csv', index=False)

    print("\n" + "=" * 70)
    print("✅ 问题四分析完成！结果已保存至CSV文件和可视化图表")
    print("=" * 70)

if __name__ == "__main__":
    main()