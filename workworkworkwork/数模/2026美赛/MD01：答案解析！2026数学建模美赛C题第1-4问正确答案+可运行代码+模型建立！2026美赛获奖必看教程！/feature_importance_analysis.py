
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
import warnings

# 忽略警告
warnings.filterwarnings("ignore")

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

def load_and_merge_data(raw_file, sim_file):
    print("Loading data...")
    df_raw = pd.read_csv(raw_file)
    df_sim = pd.read_csv(sim_file)
    
    # --- 预处理原始数据（元数据） ---
    # 需要将宽表 'weekX_judgeY' 转换为长表格式以获取 'Judge Score'
    # 实际上，我们在模拟脚本逻辑中已经有了预处理后的长表
    # 这里再次复用逻辑来拆解原始文件，以包含元数据的长表格式
    
    # 1. 清洗行业字段
    top_industries = df_raw['celebrity_industry'].value_counts().nlargest(6).index.tolist()
    df_raw['Industry_Clean'] = df_raw['celebrity_industry'].apply(lambda x: x if x in top_industries else 'Other')
    
    # 2. 提取专业舞伴（保留前15位最常见舞伴，其余归为 'Other'）
    top_pros = df_raw['ballroom_partner'].value_counts().nlargest(15).index.tolist()
    df_raw['Pro_Partner_Clean'] = df_raw['ballroom_partner'].apply(lambda x: x if x in top_pros else 'Other_Pro')
    
    # 3. 年龄处理
    df_raw['Age'] =  pd.to_numeric(df_raw['celebrity_age_during_season'], errors='coerce')
    
    meta_cols = ['season', 'celebrity_name', 'Industry_Clean', 'Pro_Partner_Clean', 'Age']
    metadata = df_raw[meta_cols].rename(columns={
        'season': 'Season', 
        'celebrity_name': 'Celebrity'
    })
    
    # --- 合并模拟结果（长表格式） ---
    # df_sim 包含 [赛季,周数, 名人姓名, 估算粉丝支持均值, 规则方法]
    merged = pd.merge(df_sim, metadata, on=['Season', 'Celebrity'], how='left')
    
    # --- 将裁判评分添加到长表中 ---
    # 我们需要读取每行的裁判评分
    # 干净的方法是重新解析原始文件，或直接在此处读取分数。
    
    # 辅助函数：从原始数据获取裁判评分
    score_lookup = {}
    total_contestants_per_season = df_raw.groupby('season').size()
    
    # 构建查找字典：(赛季, 名人) -> {周数: 分数}
    for idx, row in df_raw.iterrows():
        s = row['season']
        c = row['celebrity_name']
        scores = {}
        for w in range(1, 12): # 第1-11周
            # 计算裁判平均分
            col_prefix = f"week{w}_judge"
            cols = [col for col in df_raw.columns if col.startswith(col_prefix) and 'score' in col]
            vals = pd.to_numeric(row[cols], errors='coerce')
            if not vals.isna().all():
                scores[w] = vals.mean()
        score_lookup[(s, c)] = scores
        
    def get_score(row):
        key = (row['Season'], row['Celebrity'])
        if key in score_lookup:
            return score_lookup[key].get(row['Week'], np.nan)
        return np.nan

    merged['Judge_Score'] = merged.apply(get_score, axis=1)
    
    # 移除没有裁判评分的行（意味着可能已被淘汰或数据缺失）
    merged = merged.dropna(subset=['Judge_Score'])
    
    # --- 特征工程 ---
    
    # 1. 每周排名（因变量 1）
    # 计算该名人在当周的排名
    ranking_groups = merged.groupby(['Season', 'Week'])
    
    def calc_ranks(g):
        g['Judge_Rank'] = g['Judge_Score'].rank(ascending=False) # 1为最好
        g['Fan_Rank'] = g['Estimated_Fan_Support_Mean'].rank(ascending=False) # 1为最好
        g['Total_Score_Proxy'] = g['Judge_Rank'] + g['Fan_Rank'] # 整体表现的简单替代指标
        g['Overall_Rank_Weekly'] = g['Total_Score_Proxy'].rank(ascending=True) # 1为最好
        
        # 2. 比赛进度变量（剩余选手比例）
        # 比例 = 当前人数 / 初始人数
        n_current = len(g)
        s = g['Season'].iloc[0]
        n_start = total_contestants_per_season.get(s, n_current)
        g['Progress_Remaining_Ratio'] = n_current / n_start
        
        # 3. 标准化回归目标的得分（每周Z-score）
        g['Judge_Score_Std'] = (g['Judge_Score'] - g['Judge_Score'].mean()) / (g['Judge_Score'].std() + 1e-9)
        g['Fan_Vote_Std'] = (g['Estimated_Fan_Support_Mean'] - g['Estimated_Fan_Support_Mean'].mean()) / (g['Estimated_Fan_Support_Mean'].std() + 1e-9)
        
        # 4. 反转排名以用于回归目标（越高越好）
        # 归一化排名得分：0（最差）到 1（最好）
        g['Overall_Performance_Score'] = 1.0 - (g['Overall_Rank_Weekly'] - 1) / (len(g) - 1 + 1e-9)
        
        return g

    enriched_df = ranking_groups.apply(calc_ranks).reset_index(drop=True)
    
    return enriched_df

def run_regression_analysis(df):
    print("Running Regression Models...")
    
    # 特征
    # 数值型：年龄，进度比例
    # 类别型：行业，专业舞伴
    
    # 目标变量
    targets = {
        'Judge Preference (Score)': 'Judge_Score_Std',
        'Fan Preference (Vote)': 'Fan_Vote_Std',
        'Overall Performance (Rank)': 'Overall_Performance_Score'
    }
    
    feature_cols = ['Age', 'Progress_Remaining_Ratio', 'Industry_Clean', 'Pro_Partner_Clean']
    
    # 预处理流水线
    numeric_features = ['Age', 'Progress_Remaining_Ratio']
    categorical_features = ['Industry_Clean', 'Pro_Partner_Clean']
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_features),
            ('cat', OneHotEncoder(drop='first', handle_unknown='ignore'), categorical_features)
        ])
    
    # 权重存储
    results = {}
    
    for name, target_col in targets.items():
        print(f"Training model for: {name}")
        
        # 丢弃缺失值
        model_data = df.dropna(subset=[target_col] + numeric_features).copy()
        
        X = model_data[feature_cols]
        y = model_data[target_col]
        
        # 岭回归（比简单线性回归更好地处理多重共线性）
        model = Pipeline(steps=[('preprocessor', preprocessor),
                                ('classifier', Ridge(alpha=1.0))])
        
        model.fit(X, y)
        
        # 提取系数
        regressor = model.named_steps['classifier']
        encoder = model.named_steps['preprocessor'].named_transformers_['cat']
        encoded_cols = encoder.get_feature_names_out(categorical_features)
        all_feature_names = numeric_features + list(encoded_cols)
        
        coefs = pd.Series(regressor.coef_, index=all_feature_names)
        results[name] = coefs
        
    return pd.DataFrame(results)

def plot_feature_importance(coef_df):
    print("Plotting Feature Weights...")
    
    # 筛选最重要的特征（按各模型系数绝对值之和排序）
    coef_df['Abs_Sum'] = coef_df.abs().sum(axis=1)
    top_features = coef_df.sort_values('Abs_Sum', ascending=False) # 取全部或前20个
    top_features = top_features.drop(columns=['Abs_Sum'])
    
    if len(top_features) > 20:
        top_features = top_features.head(20)
    
    # 绘图
    top_features.plot(kind='barh', figsize=(12, 10), width=0.8)
    plt.title('Impact of Factors on Performance (Judge vs Fan vs Overall)\nRegression Coefficients (Standardized)', fontsize=16)
    plt.xlabel('Coefficient Value (Positive = Beneficial)', fontsize=12)
    plt.axvline(0, color='black', linewidth=0.8, linestyle='--')
    plt.grid(axis='x', linestyle='--', alpha=0.5)
    plt.legend(title='Target Variable')
    plt.tight_layout()
    plt.gca().invert_yaxis() # 最重要的特征排在顶部
    
    plt.savefig('feature_importance_comparison.png')
    print("Saved feature_importance_comparison.png")
    
    # 打印具体观察结果
    print("\nFeature Analysis Summary:")
    print(top_features)

def main():
    raw_file = '2026_MCM_Problem_C_Data.csv'
    sim_file = 'advanced_fan_vote_simulation_optimized.csv'
    
    df = load_and_merge_data(raw_file, sim_file)
    coef_df = run_regression_analysis(df)
    plot_feature_importance(coef_df)

if __name__ == "__main__":
    main()
