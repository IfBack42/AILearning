
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from advanced_simulation import preprocess_data 
import warnings

warnings.filterwarnings('ignore')
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

def sigmoid_weight(progress, k=10, x0=0.5):
    """
    Sigmoid function to transition weights.
    progress: 0.0 (Start) to 1.0 (End)
    k: Steepness of transition
    x0: Midpoint of transition (e.g., 0.5 means Week 5 of 10)
    
    Returns: Weight for Professional Judge (0.0 to 1.0)
    Fan Weight will be 1 - Judge Weight.
    Target: Low Judge Weight at start (High Fan), High Judge Weight at end.
    """
    return 1 / (1 + np.exp(-k * (progress - x0)))

def simulate_dynamic_mechanism(sim_file, raw_file):
    print("Loading data...")
    df_sim = pd.read_csv(sim_file)
    df_raw = preprocess_data(raw_file)
    
    # Standardize Column Names
    df_raw = df_raw.rename(columns={
        'season': 'Season', 
        'week': 'Week', 
        'celebrity': 'Celebrity',
        'avg_judge_score': 'Judge_Score',
        'elim_week': 'Elim_Week'
    })
    
    # Merge Data
    merged = pd.merge(df_sim, df_raw[['Season', 'Week', 'Celebrity', 'Judge_Score', 'Elim_Week']], 
                      on=['Season', 'Week', 'Celebrity'], how='inner')
    
    # Calculate Season Params for Progress
    season_max_weeks = df_raw.groupby('Season')['Week'].max().to_dict()
    
    results = []
    
    # Group by Season/Week to simulate the new ranking logic
    print("Simulating Dynamic Weighting Mechanism...")
    
    for (season, week), group in merged.groupby(['Season', 'Week']):
        if len(group) < 2: continue
        
        # 1. Calculate Progress (0 to 1)
        max_w = season_max_weeks.get(season, 10)
        progress = (week - 1) / (max_w - 1)
        
        # 2. Dynamic Weights
        # Sigmoid transition: Early = Low Judge Weight, Late = High Judge Weight
        judge_weight = sigmoid_weight(progress, k=8, x0=0.6)
        fan_weight = 1.0 - judge_weight
        
        # 3. Normalize Scores (Min-Max Scaling for fair combination)
        # Judge Score (Higher is better)
        j_min, j_max = group['Judge_Score'].min(), group['Judge_Score'].max()
        j_norm = (group['Judge_Score'] - j_min) / (j_max - j_min + 1e-9)
        
        # Fan Vote (Higher is better)
        f_min, f_max = group['Estimated_Fan_Support_Mean'].min(), group['Estimated_Fan_Support_Mean'].max()
        f_norm = (group['Estimated_Fan_Support_Mean'] - f_min) / (f_max - f_min + 1e-9)
        
        # 4. Calculate Combined Score
        group['New_Score'] = judge_weight * j_norm + fan_weight * f_norm
        
        # 5. Determine New Placement
        group['New_Rank'] = group['New_Score'].rank(ascending=False, method='min')
        
        # 6. Reversal Analysis metrics for this week
        # Identify Bottom Performers
        worst_judge = group.loc[group['Judge_Score'].idxmin()]
        worst_fan = group.loc[group['Estimated_Fan_Support_Mean'].idxmin()]
        
        # Check if they would be safe in new system?
        # Simulation: Assume bottom 1 is eliminated (or bottom N based on history)
        # Historical eliminated count
        n_elim = group['Is_Eliminated'].sum()
        
        if n_elim > 0:
            # Eliminated in New System (Bottom K ranks)
            elimuted_new = group.nsmallest(n_elim, 'New_Score')
            eliminated_names_new = elimuted_new['Celebrity'].tolist()
            
            # Metric: Judge Saved? (Worst Judge Score NOT in New Eliminated)
            judge_saved = 1 if worst_judge['Celebrity'] not in eliminated_names_new else 0
            
            # Metric: Fan Saved? (Worst Fan Score NOT in New Eliminated)
            fan_saved = 1 if worst_fan['Celebrity'] not in eliminated_names_new else 0
            
            # Metric: "Controversy" / Conflict
            # Distance between Judge Rank and Fan Rank weighted by current weights differentiation
            rank_diff = abs(group['Judge_Score'].rank(ascending=False) - group['Estimated_Fan_Support_Mean'].rank(ascending=False)).mean()
            
        else:
            judge_saved = np.nan
            fan_saved = np.nan
            rank_diff = 0
            
        # Append simulated week data for overall stats
        for idx, row in group.iterrows():
            results.append({
                'Season': season,
                'Week': week,
                'Celebrity': row['Celebrity'],
                'Progress': progress,
                'Judge_Weight': judge_weight,
                'Fan_Weight': fan_weight,
                'New_Score': row['New_Score'],
                'Judge_Saved_Event': judge_saved,
                'Fan_Saved_Event': fan_saved,
                'Conflict_Score': rank_diff,
                'Industry_Clean': row.get('Industry_Clean') # Need to merge this back if we want regression
            })

    return pd.DataFrame(results)

def analyze_mechanism_performance(df_new):
    print("\nAnalyzing New Mechanism Performance...")
    
    # 1. Plot Weight Transition
    plt.figure(figsize=(8, 5))
    x = np.linspace(0, 1, 100)
    y = sigmoid_weight(x, k=8, x0=0.6)
    plt.plot(x, y, label='Judge Weight', color='blue', linewidth=3)
    plt.plot(x, 1-y, label='Fan Weight', color='orange', linewidth=3, linestyle='--')
    plt.xlabel('Season Progress (0=Start, 1=Final)')
    plt.ylabel('Weight in Scoring')
    plt.title('Proposed Dynamic Weighting Mechanism\nEnsuring Ratings early, Professionalism late')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('dynamic_weight_curve.png')
    print("Saved dynamic_weight_curve.png")
    
    # 2. Reversal Rates Analysis
    avg_j_saved = df_new['Judge_Saved_Event'].mean()
    avg_f_saved = df_new['Fan_Saved_Event'].mean()
    
    print(f"\n--- Reversal Rates (Simulated) ---")
    print(f"Prop. of Weeks worst Judge Score Safe: {avg_j_saved:.2%} (High = Drama/Views)")
    print(f"Prop. of Weeks worst Fan Vote Safe:   {avg_f_saved:.2%} (High = Pro Fairness)")
    
    # 3. Conflict / Ratings Potential
    # Assumption: Higher difference between Judge and Fan weights * Rank diff = More Controversy = More Views
    # In early stage (High Fan Weight), if Judge hates it but Fans love it, it survives -> Controversy.
    
    avg_conflict = df_new.groupby('Week')['Conflict_Score'].mean()
    plt.figure(figsize=(10, 6))
    avg_conflict.plot(marker='o', color='purple')
    plt.title('Expected "Controversy Level" by Week\n(Rank Difference between Judges and Fans)')
    plt.ylabel('Avg Rank Difference')
    plt.xlabel('Week')
    plt.savefig('conflict_profile.png')
    print("Saved conflict_profile.png")
    
    return avg_j_saved, avg_f_saved

def verify_impact_divergence(df_new, raw_file):
    # Retrieve metadata for regression
    df_raw = pd.read_csv(raw_file)
    top_industries = df_raw['celebrity_industry'].value_counts().nlargest(6).index.tolist()
    industry_map = dict(zip(df_raw['celebrity_name'], df_raw['celebrity_industry'].apply(lambda x: x if x in top_industries else 'Other')))
    
    df_new['Industry_Clean'] = df_new['Celebrity'].map(industry_map)
    df_new = pd.get_dummies(df_new, columns=['Industry_Clean'], drop_first=True)
    
    # Regression: New Score ~ Industry factors + Progress
    # We want to see how the coefficients of Industry factors CHANGE over time?
    # Or simply run regression on Early vs Late phase to show the shift.
    
    features = [c for c in df_new.columns if 'Industry_' in c]
    
    print("\n--- Impact Analysis: Early vs Late Phase ---")
    
    # Early Phase (Progress < 0.5)
    early_df = df_new[df_new['Progress'] < 0.4].dropna()
    late_df = df_new[df_new['Progress'] > 0.7].dropna()
    
    def run_reg(data, label):
        if data.empty: return None
        X = data[features]
        y = data['New_Score']
        model = Ridge(alpha=1.0)
        model.fit(X, y)
        coefs = pd.Series(model.coef_, index=features)
        return coefs
        
    coef_early = run_reg(early_df, "Early Stage")
    coef_late = run_reg(late_df, "Late Stage")
    
    if coef_early is not None and coef_late is not None:
        comp_df = pd.DataFrame({'Early Stage (Fan Heavy)': coef_early, 'Late Stage (Judge Heavy)': coef_late})
        print(comp_df)
        
        comp_df.plot(kind='bar', figsize=(10, 6))
        plt.title('Shift in Determinants of Success: Early vs Late')
        plt.ylabel('Impact on Score (Coefficient)')
        plt.tight_layout()
        plt.savefig('impact_shift.png')
        print("Saved impact_shift.png")
    else:
        print("Not enough data for split regression.")

def main():
    sim_file = 'advanced_fan_vote_simulation_optimized.csv'
    raw_file = '2026_MCM_Problem_C_Data.csv'
    
    df_new = simulate_dynamic_mechanism(sim_file, raw_file)
    analyze_mechanism_performance(df_new)
    verify_impact_divergence(df_new, raw_file)

if __name__ == "__main__":
    main()
