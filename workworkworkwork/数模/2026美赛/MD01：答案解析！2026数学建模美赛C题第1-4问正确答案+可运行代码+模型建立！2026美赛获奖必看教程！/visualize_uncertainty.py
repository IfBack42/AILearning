import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from advanced_simulation import simulate_week, preprocess_data # Use existing functions
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore")

# 设置中文字体 (根据系统调整)
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'sans-serif'] 
plt.rcParams['axes.unicode_minus'] = False

def visualize_uncertainty(data_path, results_path, target_season=19, target_week=6):
    print(f"Loading data from {results_path}...")
    try:
        df_results = pd.read_csv(results_path)
    except FileNotFoundError:
        # Fallback to the optimized file if the default is not found
        fallback = 'advanced_fan_vote_simulation_optimized.csv'
        print(f"File {results_path} not found. Trying {fallback}...")
        results_path = fallback
        df_results = pd.read_csv(results_path)
    
    # --- PART 1: Boxplots of 10,000 samples for a specific Week ---
    print(f"\n--- Generating Boxplots for Season {target_season} Week {target_week} ---")
    
    # 1. Get previous week's means as priors (to replicate momentum)
    if target_week > 1:
        prev_week_data = df_results[
            (df_results['Season'] == target_season) & 
            (df_results['Week'] == target_week - 1)
        ]
        # Create a dict {Name: Mean}
        priors = dict(zip(prev_week_data['Celebrity'], prev_week_data['Estimated_Fan_Support_Mean']))
    else:
        priors = {}

    # 2. Load Raw Data for that week to get Judge Scores
    df_raw = preprocess_data(data_path)
    week_group = df_raw[
        (df_raw['season'] == target_season) & 
        (df_raw['week'] == target_week)
    ]
    
    if week_group.empty:
        print(f"No data found for Season {target_season} Week {target_week}")
        return

    # 3. Re-run simulation to get samples (using optimized params)
    # Optimized Params for Percentage Rule (Season 19): Momentum = 100.0
    # Note: We need to modify simulate_week slightly or just copy logic because 
    # the function in advanced_simulation.py returns summary stats, not raw samples.
    # To save tokens, I will implement a lightweight simulation here based on the logic.
    
    contestants = week_group['celebrity'].values
    scores = week_group['avg_judge_score'].values
    elim_week_col = week_group['elim_week'].values
    n_contestants = len(contestants)
    n_simulations = 10000
    momentum_percent = 60.0 # Updated to optimized value
    
    # Prior Vector
    prior_vec = []
    for name in contestants:
        prior_vec.append(priors.get(name, 1.0/n_contestants)) # Default if missing
    prior_vec = np.array(prior_vec)
    
    # Judge Part
    total_judge = scores.sum()
    judge_part = scores / total_judge if total_judge > 0 else np.ones(n_contestants)/n_contestants
    
    # Alpha
    alphas = 1.0 + momentum_percent * prior_vec
    
    # Simulate
    np.random.seed(2026)
    fan_part_batch = np.random.dirichlet(alphas, n_simulations)
    
    # Filter
    total_scores = judge_part + fan_part_batch
    eliminated_mask = (elim_week_col == target_week)
    elim_indices = np.where(eliminated_mask)[0]
    num_elim = len(elim_indices)
    
    if num_elim > 0:
        bottom_k = np.argpartition(total_scores, num_elim, axis=1)[:, :num_elim]
        bottom_sorted = np.sort(bottom_k, axis=1)
        target_sorted = np.sort(elim_indices)
        matches = np.all(bottom_sorted == target_sorted, axis=1)
        valid_samples = fan_part_batch[matches]
    else:
        valid_samples = fan_part_batch

    # 4. Plot Boxplot
    if len(valid_samples) == 0:
        print("No valid samples generated for plotting.")
    else:
        plt.figure(figsize=(14, 8))
        # Prepare data for Seaborn: Flatten to (Name, Vote)
        plot_data = []
        for i, name in enumerate(contestants):
            votes = valid_samples[:, i]
            for v in votes:
                plot_data.append({'Celebrity': name, 'Simulated Fan Vote %': v})
        
        df_plot = pd.DataFrame(plot_data)
        
        sns.boxplot(x='Celebrity', y='Simulated Fan Vote %', data=df_plot, palette="Set3")
        plt.title(f"Distribution of Feasible Fan Votes (Season {target_season}, Week {target_week})\nBased on 10,000 Constraints-Satisfied Simulations", fontsize=14)
        plt.xticks(rotation=45)
        plt.grid(axis='y', linestyle='--', alpha=0.6)
        
        # Highlight eliminated
        elim_names = week_group[week_group['elim_week'] == target_week]['celebrity'].values
        plt.xlabel(f"Contestants (Eliminated: {', '.join(elim_names)})")
        
        plt.tight_layout()
        plt.savefig('fan_vote_boxplot.png')
        print("Saved 'fan_vote_boxplot.png'")

    # --- PART 2: Uncertainty Evolution (Line Plot) ---
    print(f"\n--- Generating Uncertainty Evolution Plot for Season {target_season} ---")
    
    season_data = df_results[df_results['Season'] == target_season].copy()
    
    plt.figure(figsize=(12, 8))
    
    # Pivot for plotting: Index=Week, Columns=Celebrity, Values=CI_Width
    pivot_df = season_data.pivot(index='Week', columns='Celebrity', values='CI_Width')
    
    # Plotlines
    for col in pivot_df.columns:
        # Determine if/when eliminated
        # A simple way is to check the last week they appear in data
        last_week = pivot_df[col].dropna().index.max()
        
        # Plot with markers
        plt.plot(pivot_df.index, pivot_df[col], marker='o', label=col, linewidth=2, alpha=0.8)
        
        # Mark elimination point
        if not np.isnan(last_week):
             plt.plot(last_week, pivot_df.loc[last_week, col], 'rx', markersize=10, markeredgewidth=2)

    plt.title(f"Evolution of Uncertainty (Confidence Interval Width) - Season {target_season}", fontsize=14)
    plt.xlabel("Week", fontsize=12)
    plt.ylabel("95% CI Width of Fan Vote Estimate", fontsize=12)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig('uncertainty_evolution.png')
    print("Saved 'uncertainty_evolution.png'")

if __name__ == "__main__":
    data_path = '2026_MCM_Problem_C_Data.csv'
    results_path = 'advanced_fan_vote_simulation_optimized.csv'
    # Choosing Season 19 as it uses Percentage Rule (better for CI Width visualization)
    visualize_uncertainty(data_path, results_path, target_season=19, target_week=6)
