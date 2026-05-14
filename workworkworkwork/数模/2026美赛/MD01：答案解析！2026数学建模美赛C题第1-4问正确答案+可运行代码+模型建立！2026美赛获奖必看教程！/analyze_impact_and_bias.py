import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from advanced_simulation import preprocess_data
import warnings

warnings.filterwarnings('ignore')
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

def calculate_ranks_and_metrics(sim_file, raw_file):
    print("Loading data...")
    # Load simulation results (Fan Votes)
    df_sim = pd.read_csv(sim_file)
    
    # Load raw judge scores
    df_raw = preprocess_data(raw_file)
    
    # Merge
    # df_raw has: season, week, celebrity, avg_judge_score
    # df_sim has: Season, Week, Celebrity, Estimated_Fan_Support_Mean, Method, Is_Eliminated
    
    # Standardize columns for merge
    df_raw = df_raw.rename(columns={
        'season': 'Season', 
        'week': 'Week', 
        'celebrity': 'Celebrity',
        'avg_judge_score': 'Judge_Score'
    })
    
    merged = pd.merge(df_sim, df_raw[['Season', 'Week', 'Celebrity', 'Judge_Score']], 
                      on=['Season', 'Week', 'Celebrity'], how='left')
    
    # Drop rows where Judge Score missing (should happen rarely/never with processed data)
    merged = merged.dropna(subset=['Judge_Score'])

    full_stats = []
    
    print("Calculating ranks and correlations...")
    # Iterate by Season-Week groups
    for (season, week), group in merged.groupby(['Season', 'Week']):
        # If single contestant, skip
        if len(group) < 2: continue
        
        # 1. Calculate Component Ranks (1 = Best, N = Worst)
        # Judge Score: Higher is better -> Rank Descending
        group['Judge_Rank_Raw'] = group['Judge_Score'].rank(ascending=False, method='min')
        
        # Fan Vote: Higher is better -> Rank Descending
        group['Fan_Rank_Raw'] = group['Estimated_Fan_Support_Mean'].rank(ascending=False, method='min')
        
        # 2. Calculate Combined Score/Rank based on Rule
        rule = group['Method'].iloc[0]
        
        if rule == 'Percentage':
            # Percentage Rule: %Judge + %Fan
            # Convert Judge Score to %
            total_j = group['Judge_Score'].sum()
            j_pct = group['Judge_Score'] / total_j if total_j > 0 else 0
            
            # Fan % is already in Estimated_Fan_Support_Mean (if sum of weeks ~1)
            # Normalizing fan support just in case
            total_f = group['Estimated_Fan_Support_Mean'].sum()
            f_pct = group['Estimated_Fan_Support_Mean'] / total_f if total_f > 0 else 0
            
            group['Combined_Score'] = j_pct + f_pct
            # Combined Rank: Higher Score is better
            group['Combined_Rank'] = group['Combined_Score'].rank(ascending=False, method='min')
            
        elif rule == 'Rank':
            # Rank Rule: Judge_Rank + Fan_Rank (Lower Sum is better)
            # Need strict ranks for addition (1, 2, 3...)
            j_r = group['Judge_Score'].rank(ascending=False, method='average')
            
            # Fan rank from estimated support
            f_r = group['Estimated_Fan_Support_Mean'].rank(ascending=False, method='average')
            
            group['Combined_Score'] = j_r + f_r
            # Combined Rank: Lower Score is better
            group['Combined_Rank'] = group['Combined_Score'].rank(ascending=True, method='min')

        # 3. Correlation (Fan Bias)
        # Spearman Corr between Combined Rank vs Fan Rank / Judge Rank
        # Since Combined Rank (1=Best) correlates with Fan Rank (1=Best)
        # High corr means Final ~ Fan
        corr_fan, _ = stats.spearmanr(group['Combined_Rank'], group['Fan_Rank_Raw'])
        corr_judge, _ = stats.spearmanr(group['Combined_Rank'], group['Judge_Rank_Raw'])
        
        # 4. Identification of Worst Performers
        # Who was worst by Judge? (Max Rank Number)
        max_j_rank = group['Judge_Rank_Raw'].max()
        worst_judge_celebs = group[group['Judge_Rank_Raw'] == max_j_rank]['Celebrity'].tolist()
        
        # Who was worst by Fan?
        max_f_rank = group['Fan_Rank_Raw'].max()
        worst_fan_celebs = group[group['Fan_Rank_Raw'] == max_f_rank]['Celebrity'].tolist()
        
        # Who was actually eliminated?
        eliminated_celebs = group[group['Is_Eliminated'] == True]['Celebrity'].tolist()
        
        # 5. Reversal Logic
        # "Saved by Fans": Worst Judge Scorer was NOT eliminated
        # (Only counts if someone was eliminated this week)
        judge_saved = 0
        fan_saved = 0
        elim_happened = len(eliminated_celebs) > 0
        
        if elim_happened:
            # Check if ANY of the worst judges were eliminated
            # If the set of eliminated intersects with set of worst judges
            if not set(worst_judge_celebs).intersection(set(eliminated_celebs)):
                judge_saved = 1 # The worst judge scorer survived
            
            # Check if ANY of the worst fan were eliminated
            if not set(worst_fan_celebs).intersection(set(eliminated_celebs)):
                fan_saved = 1 # The worst fan scorer survived
        
        # Append enriched rows for later
        full_stats.append({
            'Season': season,
            'Week': week,
            'Method': rule,
            'Judge_Saved': judge_saved,
            'Fan_Saved': fan_saved,
            'Corr_Fan': corr_fan,
            'Corr_Judge': corr_judge,
            'Elimination_Week': elim_happened
        })
        
        # Append detailed columns to merged dataframe for case study
        # We can't easily append to 'merged' inside loop if we want to update it.
        # Instead, we construct a list of dicts for the new dataframe
    
    stats_df = pd.DataFrame(full_stats)
    return merged, stats_df

def plot_reversal_rates(stats_df):
    print("Plotting Reversal Rates...")
    # Group by Season
    season_stats = stats_df[stats_df['Elimination_Week'] == True].groupby('Season')[['Judge_Saved', 'Fan_Saved']].mean()
    
    plt.figure(figsize=(14, 6))
    
    # Bar plot
    x = season_stats.index
    width = 0.35
    
    plt.bar(x - width/2, season_stats['Judge_Saved'], width, label='Judge Bottom Saved by Fans', color='skyblue', alpha=0.8)
    plt.bar(x + width/2, season_stats['Fan_Saved'], width, label='Fan Bottom Saved by Judges', color='salmon', alpha=0.8)
    
    plt.xlabel('Season')
    plt.ylabel('Frequency of Saving Bottom Performer')
    plt.title('Reversal Rate Analysis: How often does the "Worst" Performer survive?')
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.xticks(x)
    
    plt.savefig('reversal_rates.png')
    print("Saved reversal_rates.png")

def plot_fan_bias(stats_df):
    print("Plotting Fan Bias...")
    # Average Correlation per Season
    season_corr = stats_df.groupby('Season')[['Corr_Fan', 'Corr_Judge']].mean()
    
    plt.figure(figsize=(14, 6))
    plt.plot(season_corr.index, season_corr['Corr_Fan'], marker='o', label='Correlation: Final vs Fan', linewidth=2)
    plt.plot(season_corr.index, season_corr['Corr_Judge'], marker='x', label='Correlation: Final vs Judge', linewidth=2)
    
    plt.xlabel('Season')
    plt.ylabel('Spearman Correlation')
    plt.title('Fan vs Judge Power Dynamic: Who determines the outcome?')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    
    plt.savefig('fan_bias_evolution.png')
    print("Saved fan_bias_evolution.png")

def bobby_bones_case_study(merged_df):
    print("\n--- Case Study: Bobby Bones (Season 27) ---")
    bb_data = merged_df[(merged_df['Season'] == 27) & (merged_df['Celebrity'] == 'Bobby Bones')]
    
    if bb_data.empty:
        print("Bobby Bones data not found!")
        return
        
    # Recalculate ranks in context of the week
    bb_ranks = []
    
    for _, row in bb_data.iterrows():
        week_df = merged_df[(merged_df['Season'] == 27) & (merged_df['Week'] == row['Week'])]
        
        # Judge Rank (among peers that week)
        j_rank = week_df['Judge_Score'].rank(ascending=False, method='min')
        bb_j_rank = j_rank[week_df['Celebrity'] == 'Bobby Bones'].values[0]
        n_contestants = len(week_df)
        
        # Fan Rank
        f_rank = week_df['Estimated_Fan_Support_Mean'].rank(ascending=False, method='min')
        bb_f_rank = f_rank[week_df['Celebrity'] == 'Bobby Bones'].values[0]
        
        bb_ranks.append({
            'Week': row['Week'],
            'Judge_Rank': bb_j_rank,
            'Fan_Rank': bb_f_rank,
            'Judge_Score': row['Judge_Score'],
            'Fan_Vote_Est': row['Estimated_Fan_Support_Mean'],
            'N_Contestants': n_contestants
        })
    
    bb_df = pd.DataFrame(bb_ranks)
    print(bb_df)
    
    # Plotting Bobby Bones
    plt.figure(figsize=(10, 6))
    plt.plot(bb_df['Week'], bb_df['Judge_Rank'], 'r-o', label='Judge Rank', linewidth=2)
    plt.plot(bb_df['Week'], bb_df['Fan_Rank'], 'b-o', label='Fan Rank (Estimated)', linewidth=2)
    plt.plot(bb_df['Week'], bb_df['N_Contestants'], 'k--', label='Number of Contestants', alpha=0.3)
    
    plt.gca().invert_yaxis() # Rank 1 is top
    plt.title('The Bobby Bones Anomaly (Season 27)\nLow Scores but High Fan Support')
    plt.xlabel('Week')
    plt.ylabel('Rank (1 = Best)')
    plt.legend()
    plt.grid(True)
    plt.savefig('bobby_bones_case_study.png')
    print("Saved bobby_bones_case_study.png")


def plot_metrics_by_method(stats_df):
    print("\nAnalyzing Metrics by Method (Rank vs Percentage)...")
    # Filter for elimination weeks only
    elim_stats = stats_df[stats_df['Elimination_Week'] == True]
    
    method_means = elim_stats.groupby('Method')[['Judge_Saved', 'Fan_Saved']].mean()
    print("\nReversal Rates by Method:")
    print(method_means)
    
    plt.figure(figsize=(10, 6))
    x = np.arange(len(method_means))
    width = 0.35
    
    # Note: method_means.index will be ['Percentage', 'Rank']
    plt.bar(x - width/2, method_means['Judge_Saved'], width, label='Judge Bottom SAVED by Fans', color='skyblue', alpha=0.9)
    plt.bar(x + width/2, method_means['Fan_Saved'], width, label='Fan Bottom SAVED by Judges', color='salmon', alpha=0.9)
    
    plt.xticks(x, method_means.index, fontsize=12)
    plt.ylabel('Frequency (Rate)', fontsize=12)
    plt.title('Impact of Voting System on Reversal Rates', fontsize=14)
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    
    plt.savefig('reversal_by_method.png')
    print("Saved reversal_by_method.png")

def main():
    sim_file = 'advanced_fan_vote_simulation_optimized.csv'
    raw_file = '2026_MCM_Problem_C_Data.csv'
    
    merged_df, stats_df = calculate_ranks_and_metrics(sim_file, raw_file)
    
    # Metrics
    avg_judge_saved = stats_df[stats_df['Elimination_Week'] == True]['Judge_Saved'].mean()
    avg_fan_saved = stats_df[stats_df['Elimination_Week'] == True]['Fan_Saved'].mean()
    
    print(f"\nOverall Reversal Analysis:")
    print(f"Percentage of weeks where the WORST Judge Score was SAVED by Fans: {avg_judge_saved:.2%}")
    print(f"Percentage of weeks where the WORST Fan Vote was SAVED by Judges: {avg_fan_saved:.2%}")
    
    plot_reversal_rates(stats_df)
    plot_metrics_by_method(stats_df)
    plot_fan_bias(stats_df)
    bobby_bones_case_study(merged_df)
    plot_metrics_by_method(stats_df)

if __name__ == "__main__":
    main()
