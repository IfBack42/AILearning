import pandas as pd
import numpy as np
import re
from tqdm import tqdm

def preprocess_data(file_path):
    """
    Reads the raw CSV and converts it into a long-format DataFrame 
    suitable for weekly simulation.
    """
    df = pd.read_csv(file_path)
    
    # 1. Parse Elimination/Result Week
    def get_elimination_week(res):
        if pd.isna(res): return 999
        res = str(res)
        if 'Eliminated' in res or 'Withdrew' in res or 'Quit' in res:
            match = re.search(r'Week\s*(\d+)', res, re.IGNORECASE)
            if match:
                return int(match.group(1))
        return 999 
    
    df['elim_week'] = df['results'].apply(get_elimination_week)
    
    # 2. Extract Scores and Convert to Long Format
    # We want columns: Season, Week, Celebrity, AverageScore
    long_data = []
    
    # Identify max week
    score_cols = [c for c in df.columns if 'judge' in c and 'score' in c]
    weeks = set()
    for c in score_cols:
        match = re.search(r'week(\d+)', c)
        if match:
            weeks.add(int(match.group(1)))
    max_week = max(weeks)
    
    for idx, row in df.iterrows():
        for w in range(1, max_week + 1):
            # Check if contestant is still in the competition
            # They participate in the week they get eliminated
            if w > row['elim_week']:
                continue
                
            cols = [c for c in score_cols if f'week{w}_' in c]
            scores = pd.to_numeric(row[cols], errors='coerce')
            
            if scores.isna().all():
                continue # No scores for this week (e.g. didn't dance or N/A)
                
            avg_score = scores.mean()
            if avg_score == 0 and w < row['elim_week']:
                continue # Ignore zero scores unless it's their elimination week might be tricky, usually 0 means didn't dance.
            
            long_data.append({
                'season': row['season'],
                'week': w,
                'celebrity': row['celebrity_name'],
                'avg_judge_score': avg_score,
                'elim_week': row['elim_week']
            })
            
    long_df = pd.DataFrame(long_data)
    return long_df

def simulate_fan_votes(df, rule_type='percent', n_simulations=10000):
    """
    Performs constraint-satisfaction MC simulation.
    
    df: Long-format dataframe
    rule_type: 
        - 'percent': (Season 3-27) Total = %Judge + %Fan. Eliminated = Lowest Total.
        - 'rank_simple': (Seasons 1-2) Total = Rank(Judge) + Rank(Fan). Eliminated = Worst (Highest) Total Rank.
        - 'rank_save': (Season 28+) Total = Rank(Judge) + Rank(Fan). Eliminated is in Bottom 2 (Highest 2 Total Ranks).
    """
    
    # Store results
    simulation_results = []
    
    grouped = df.groupby(['season', 'week'])
    
    print(f"Starting Simulation using {rule_type} rule...")
    
    for (season, week), group in tqdm(grouped):
        # Identify active contestants in this specific week
        contestants = group['celebrity'].values
        scores = group['avg_judge_score'].values
        n_contestants = len(contestants)
        
        # Identify who was ACTUALLY eliminated this week
        eliminated_mask = (group['elim_week'] == week).values
        eliminated_indices = np.where(eliminated_mask)[0]
        
        if len(eliminated_indices) == 0:
            continue
        
        # In double elimination weeks, we might have multiple targets. 
        # Standard code assumes one, but let's be robust:
        # If multiple people eliminated, we need to satisfy constraints for ALL of them?
        # Typically "Bottom N" logic applies. 
        # For simplicity in this script, we focus on the first listed elimination or single elimination.
        target_eliminated_idx = eliminated_indices[0] 
        
        valid_samples_data = []
        
        # --- PRE-CALCULATIONS ---
        if rule_type == 'percent':
            # Percentage Rule: Total = %Judge + %Fan
            total_judge_score = np.sum(scores)
            if total_judge_score == 0:
                judge_shares = np.ones(n_contestants) / n_contestants
            else:
                judge_shares = scores / total_judge_score
                
        elif rule_type.startswith('rank'):
             # Rank Rule: Total = Rank(Judge) + Rank(Fan)
             # Rank 1 is Best. Highest Score = Rank 1.
             from scipy.stats import rankdata
             # Negate scores to rank high scores as 1
             judge_ranks = rankdata(-scores, method='average')
             
        # --- MONTE CARLO LOOP ---
        batch_size = n_simulations
        
        if rule_type == 'percent':
            # Percentage Rule Simulation
            fan_shares_batch = np.random.dirichlet(np.ones(n_contestants), batch_size)
            total_scores = judge_shares + fan_shares_batch
            
            # Constraint: Eliminated person has MIN total score
            sim_eliminated = np.argmin(total_scores, axis=1)
            valid_mask = (sim_eliminated == target_eliminated_idx)
            
            valid_samples_data = fan_shares_batch[valid_mask]
            
        elif rule_type == 'rank_simple':
            # Rank Rule (Simple): Eliminated = Max Total Rank (Worst)
             random_vals = np.random.rand(batch_size, n_contestants)
             fan_ranks_batch = np.argsort(np.argsort(random_vals, axis=1), axis=1) + 1
             
             total_ranks = judge_ranks + fan_ranks_batch
             
             # Constraint: Eliminated person must have MAX total rank
             # We find the index of the max rank sum
             # ties for max: strictly speaking any of them could go home, 
             # but usually tie-breaker is judge score.
             # Simplified: strictly largest sum goes home.
             max_indices = np.argmax(total_ranks, axis=1)
             matches = (max_indices == target_eliminated_idx)
             
             valid_samples_data = fan_ranks_batch[matches]

        elif rule_type == 'rank_save':
             # Rank Rule with Judges' Save (Bottom Two)
             random_vals = np.random.rand(batch_size, n_contestants)
             fan_ranks_batch = np.argsort(np.argsort(random_vals, axis=1), axis=1) + 1
             
             total_ranks = judge_ranks + fan_ranks_batch
             
             # Constraint: Eliminated person must be in the BOTTOM TWO (Highest 2 Ranks)
             # We need to find if target_index is in the top 2 indices of total_ranks
             
             # argsort returns indices that sort the array. 
             # The last two elements of argsort(total_ranks) are the indices of the largest values (Bottom 2)
             sorted_indices = np.argsort(total_ranks, axis=1)
             bottom_two_indices = sorted_indices[:, -2:] 
             
             # Check if target is in bottom_two
             # matches shape: (batch_size,)
             matches = np.any(bottom_two_indices == target_eliminated_idx, axis=1)
             
             valid_samples_data = fan_ranks_batch[matches]

        # --- AGGREGATE RESULTS ---
        if len(valid_samples_data) > 0:
            mean_support = np.mean(valid_samples_data, axis=0)
            std_support = np.std(valid_samples_data, axis=0)
            
            for i, name in enumerate(contestants):
                simulation_results.append({
                    'season': season,
                    'week': week,
                    'celebrity': name,
                    'is_eliminated': (i == target_eliminated_idx),
                    'rule_used': rule_type,
                    'actual_judge_metric': judge_shares[i] if rule_type == 'percent' else judge_ranks[i],
                    'est_fan_support_mean': mean_support[i],
                    'est_fan_support_std': std_support[i],
                    'valid_samples_count': len(valid_samples_data)
                })
        else:
             for i, name in enumerate(contestants):
                simulation_results.append({
                    'season': season,
                    'week': week,
                    'celebrity': name,
                    'is_eliminated': (i == target_eliminated_idx),
                    'rule_used': rule_type,
                    'est_fan_support_mean': np.nan,
                    'est_fan_support_std': np.nan,
                    'valid_samples_count': 0
                })

    return pd.DataFrame(simulation_results)

if __name__ == "__main__":
    file_path = '2026_MCM_Problem_C_Data.csv'
    
    print("Preprocessing data...")
    long_df = preprocess_data(file_path)
    
    # 1. Seasons 1-2: Rank Rule (Simple)
    df_s1_2 = long_df[long_df['season'] <= 2]
    results_1 = simulate_fan_votes(df_s1_2, rule_type='rank_simple', n_simulations=50000)

    # 2. Seasons 3-27: Percentage Rule
    df_s3_27 = long_df[(long_df['season'] >= 3) & (long_df['season'] <= 27)]
    results_2 = simulate_fan_votes(df_s3_27, rule_type='percent', n_simulations=50000)
    
    # 3. Seasons 28+: Rank Rule with Judges' Save
    df_s28_plus = long_df[long_df['season'] >= 28]
    results_3 = simulate_fan_votes(df_s28_plus, rule_type='rank_save', n_simulations=50000)
    
    final_results = pd.concat([results_1, results_2, results_3], ignore_index=True)
    
    output_path = 'simulated_fan_votes.csv'
    final_results.to_csv(output_path, index=False)
    print(f"Simulation complete. Results saved to {output_path}")
    
    # Visualize a snippet
    print(final_results[['season', 'week', 'celebrity', 'rule_used', 'is_eliminated', 'est_fan_support_mean']].head(10))
