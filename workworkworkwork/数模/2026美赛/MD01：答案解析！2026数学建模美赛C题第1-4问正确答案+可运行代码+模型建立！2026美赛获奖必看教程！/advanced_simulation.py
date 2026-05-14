import pandas as pd
import numpy as np
import scipy.stats as stats
import re
from tqdm import tqdm
import itertools

# 设置随机种子以保证可复现性
np.random.seed(2026)

def preprocess_data(file_path):
    # ...existing code...
    print("正在读取并预处理数据...")
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"找不到文件: {file_path}")
        return pd.DataFrame()

    # 1. 解析淘汰周 (Eliminated/Withdrew Week X)
    def get_elimination_week(res):
        if pd.isna(res): return 999 # 决赛选手或未提及
        res = str(res)
        if 'Eliminated' in res or 'Withdrew' in res or 'Quit' in res:
            match = re.search(r'Week\s*(\d+)', res, re.IGNORECASE)
            if match:
                return int(match.group(1))
        if 'Place' in res: # 决赛周通常是最后一周，这里假设一个较大的数
             return 999 
        return 999 
    
    df['elim_week'] = df['results'].apply(get_elimination_week)
    
    # 2. 识别最大周数和分数列
    score_cols = [c for c in df.columns if 'judge' in c and 'score' in c]
    weeks = set()
    for c in score_cols:
        match = re.search(r'week(\d+)', c)
        if match:
            weeks.add(int(match.group(1)))
    max_week = max(weeks)
    print(f"检测到最大周数为: {max_week}")

    long_data = []
    
    for idx, row in df.iterrows():
        for w in range(1, max_week + 1):
            if w > row['elim_week']:
                continue
                
            cols = [c for c in score_cols if f'week{w}_' in c]
            scores = pd.to_numeric(row[cols], errors='coerce')
            
            if scores.isna().all():
                continue 
                
            avg_score = scores.mean()
            if avg_score == 0 and w != row['elim_week']:
                continue
            
            long_data.append({
                'season': row['season'],
                'week': w,
                'celebrity': row['celebrity_name'],
                'avg_judge_score': avg_score,
                'elim_week': row['elim_week']
            })
            
    return pd.DataFrame(long_data)

def calculate_entropy(rank_matrix):
    # ...existing code...
    n_samples, n_contestants = rank_matrix.shape
    entropies = []
    
    for i in range(n_contestants):
        ranks = rank_matrix[:, i]
        value_counts = pd.Series(ranks).value_counts(normalize=True)
        ent = stats.entropy(value_counts.values)
        entropies.append(ent)
        
    return np.array(entropies)

def simulate_week(season, week, group_df, rule_type, prior_support=None, n_simulations=10000, 
                  momentum_percent=50.0, momentum_rank=0.8):
    """
    对指定的一周进行蒙特卡洛模拟，引入时间相关性（先验知识）。
    prior_support: dict, {celebrity_name: previous_mean_value}
    momentum_percent: Percentage规则下的动量系数
    momentum_rank: Rank规则下的动量系数
    """
    contestants = group_df['celebrity'].values
    scores = group_df['avg_judge_score'].values
    elim_week_col = group_df['elim_week'].values
    n_contestants = len(contestants)
    
    # 1. 确定谁在这一周实际上被淘汰了
    eliminated_mask = (elim_week_col == week)
    eliminated_indices = np.where(eliminated_mask)[0]
    num_eliminated = len(eliminated_indices)
    
    has_prior = False
    prior_vec = None

    if prior_support:
        matched_priors = []
        for name in contestants:
            val = prior_support.get(name)
            if val is None:
                if rule_type == 'Percentage': val = 1.0 / n_contestants
                elif rule_type == 'Rank': val = (n_contestants + 1) / 2 
            matched_priors.append(val)
        prior_vec = np.array(matched_priors)
        has_prior = True

    # --- 准备：计算裁判部分 ---
    if rule_type == 'Percentage':
        total_judge_score = np.sum(scores)
        judge_part = (scores / total_judge_score) if total_judge_score > 0 else (np.ones(n_contestants) / n_contestants)
             
    elif rule_type == 'Rank':
        judge_part = stats.rankdata(-scores, method='average')

    # --- 核心：向量化 10,000 次模拟 ---
    valid_samples_matrix = None
    
    if rule_type == 'Percentage':
        # 1. 确定 Dirichlet 参数 alpha
        if has_prior:
            # 基础 alpha=1 (Uniform) + 动量 * 上周均值
            alphas = 1.0 + momentum_percent * prior_vec
        else:
            alphas = np.ones(n_contestants)
            
        # 2. 生成随机样本
        fan_part_batch = np.random.dirichlet(alphas, n_simulations)
        
        # 3. 计算总分与约束
        total_scores = judge_part + fan_part_batch
        
        if num_eliminated > 0:
            bottom_k_indices = np.argpartition(total_scores, num_eliminated, axis=1)[:, :num_eliminated]
            bottom_k_sorted = np.sort(bottom_k_indices, axis=1)
            target_indices_sorted = np.sort(eliminated_indices)
            matches = np.all(bottom_k_sorted == target_indices_sorted, axis=1)
            valid_samples_matrix = fan_part_batch[matches]
        else:
            valid_samples_matrix = fan_part_batch
        
    elif rule_type == 'Rank':
        # 1. 生成随机用于排序的 Latent Scores
        rand_vals = np.random.rand(n_simulations, n_contestants)
        
        if has_prior:
            # Normalize to 0-1
            max_r = np.max(prior_vec) if len(prior_vec) > 0 else n_contestants
            strength = 1.0 - (prior_vec - 1) / max(max_r, 1)  # 简单归一化
            
            # 施加偏置
            rand_vals += momentum_rank * strength
            
        fan_part_batch = np.argsort(np.argsort(-rand_vals, axis=1), axis=1) + 1
        
        total_scores = judge_part + fan_part_batch
        
        if num_eliminated > 0:
            top_k_indices = np.argpartition(-total_scores, num_eliminated, axis=1)[:, :num_eliminated]
            top_k_sorted = np.sort(top_k_indices, axis=1)
            target_indices_sorted = np.sort(eliminated_indices)
            matches = np.all(top_k_sorted == target_indices_sorted, axis=1)
            valid_samples_matrix = fan_part_batch[matches]
        else:
            valid_samples_matrix = fan_part_batch

    # --- 指标计算与后验更新 ---
    results_list = []
    posterior_means = {} 
    
    num_valid = len(valid_samples_matrix) if valid_samples_matrix is not None else 0
    acceptance_rate = num_valid / n_simulations
    
    if num_valid > 0:
        mean_support = np.mean(valid_samples_matrix, axis=0)
        
        for i, name in enumerate(contestants):
            posterior_means[name] = mean_support[i]
            
        is_validated = False
        if num_eliminated > 0:
            if rule_type == 'Percentage':
                val_total = judge_part + mean_support
                val_bottom_k = np.argsort(val_total)[:num_eliminated]
                is_validated = set(val_bottom_k) == set(eliminated_indices)
            elif rule_type == 'Rank':
                val_total = judge_part + mean_support
                val_top_k = np.argsort(val_total)[-num_eliminated:]
                is_validated = set(val_top_k) == set(eliminated_indices)
        else:
            is_validated = True

        lower_bound = np.percentile(valid_samples_matrix, 2.5, axis=0)
        upper_bound = np.percentile(valid_samples_matrix, 97.5, axis=0)
        ci_width = upper_bound - lower_bound
        
        if rule_type == 'Rank':
            entropies = calculate_entropy(valid_samples_matrix)
        else:
            entropies = [np.nan] * n_contestants
            
        for i, name in enumerate(contestants):
            results_list.append({
                'Season': season,
                'Week': week,
                'Celebrity': name,
                'Is_Eliminated': (i in eliminated_indices),
                'Method': rule_type,
                'Estimated_Fan_Support_Mean': mean_support[i],
                'CI_Width': ci_width[i],
                'Entropy': entropies[i],
                'Acceptance_Rate': acceptance_rate,
                'Validation_By_Mean': is_validated
            })
    else:
        for i, name in enumerate(contestants):
            fallback_val = prior_vec[i] if has_prior else (0.5 if rule_type=='Percentage' else n_contestants/2)
            posterior_means[name] = fallback_val
            results_list.append({
                'Season': season,
                'Week': week,
                'Celebrity': name,
                'Is_Eliminated': (i in eliminated_indices),
                'Method': rule_type,
                'Estimated_Fan_Support_Mean': np.nan,
                'CI_Width': np.nan,
                'Entropy': np.nan,
                'Acceptance_Rate': 0.0,
                'Validation_By_Mean': False
            })
            
    return results_list, posterior_means

def run_simulation_with_params(df_long, momentum_percent, momentum_rank, n_simulations=2000, progress=False):
    all_results = []
    seasons = sorted(df_long['season'].unique())
    iterator = tqdm(seasons, desc="Simulating") if progress else seasons
    
    for season in iterator:
        season_df = df_long[df_long['season'] == season]
        sorted_weeks = sorted(season_df['week'].unique())
        current_priors = {} 
        
        if season <= 2: rule = 'Rank'
        elif season <= 27: rule = 'Percentage'
        else: rule = 'Rank'
        
        for week in sorted_weeks:
            week_group = season_df[season_df['week'] == week]
            week_results, posterior_means = simulate_week(
                season, week, week_group, rule, 
                prior_support=current_priors, 
                n_simulations=n_simulations,
                momentum_percent=momentum_percent,
                momentum_rank=momentum_rank
            )
            all_results.extend(week_results)
            current_priors = posterior_means
            
    return pd.DataFrame(all_results)

def main():
    input_file = '2026_MCM_Problem_C_Data.csv'
    output_file = 'advanced_fan_vote_simulation_optimized.csv'
    
    df_long = preprocess_data(input_file)
    if df_long.empty: return

    # --- 网格搜索部分 ---
    # 细化网格：Percent间隔10，Rank间隔0.1
    possible_percent = list(range(0, 101, 10)) 
    possible_rank = [round(x * 0.1, 1) for x in range(0, 21)]
    
    print("开始网格搜索优化参数 (Grid Search)...")
    print(f"Percentage Candidates: {possible_percent}")
    print(f"Rank Candidates: {possible_rank}")
    
    # 交叉组合
    combinations = list(itertools.product(possible_percent, possible_rank))
    best_score = -1
    best_params = (50.0, 0.8) # 默认
    
    # 使用较少的模拟次数进行搜索，提高速度 (由于网格变密，稍微降低N以控制时间)
    SEARCH_N_SIM = 1000
    
    for p_val, r_val in tqdm(combinations, desc="Grid Searching"):
        res = run_simulation_with_params(df_long, momentum_percent=p_val, momentum_rank=r_val, n_simulations=SEARCH_N_SIM)
        
        # 目标函数：最大化 Validation_By_Mean 的均值
        # 只有存在淘汰的周才有 Validation 结果，非淘汰周 (False) 或者 NaN 应该被正确处理
        # 我们的 simulate_week 逻辑中，如果没有淘汰，Validation_By_Mean 是 True
        # 但我们更关心的是那些有淘汰发生的“关键周”是否验证成功
        
        # 过滤只看有淘汰发生的行 (Is_Eliminated == True 的行对应的 Validation_By_Mean)
        # 或者简单地，计算所有周的 Validation_By_Mean 均值
        
        if not res.empty:
            # 聚合到 weekly level (因为一周内的所有选手 validation 结果是一样的)
            weekly_res = res.drop_duplicates(['Season', 'Week'])
            # 排除非淘汰周 (假设非淘汰周容易通过验证，重点看淘汰周)
            # 通过检查是否有选手 is_eliminated 来判断是否是淘汰周?
            # 我们的 simulate_week 中如果 num_eliminated > 0 才有逻辑
            score = weekly_res['Validation_By_Mean'].mean()
        else:
            score = 0
            
        if score > best_score:
            best_score = score
            best_params = (p_val, r_val)
            
    print(f"\n最优参数已找到！(Target: Maximize Validation Accuracy)")
    print(f"MOMENTUM_PERCENT (For Season 3-27): {best_params[0]}")
    print(f"MOMENTUM_RANK (For Season 1-2, 28+): {best_params[1]}")
    print(f"预计平均接受率: {best_score:.2%}")

    # --- 最终运行 ---
    print("\n使用最优参数运行最终高精度模拟 (N=10,000)...")
    final_results = run_simulation_with_params(
        df_long, 
        momentum_percent=best_params[0], 
        momentum_rank=best_params[1], 
        n_simulations=10000, 
        progress=True
    )
    
    final_results.to_csv(output_file, index=False)
    print(f"结果已保存至: {output_file}")
    
    if not final_results.empty:
        avg_acc = final_results['Acceptance_Rate'].mean()
        print(f"最终平均接受率: {avg_acc:.2%}")

if __name__ == "__main__":
    main()

