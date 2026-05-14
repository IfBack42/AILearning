import pandas as pd

def analyze_results(file_path):
    print(f"Reading file: {file_path}")
    df = pd.read_csv(file_path)
    
    if df.empty:
        print("Dataframe is empty.")
        return

    # 1. Validation By Mean

    # 按独立周计算（因为同一周内所有名人的结果相同）
    # 然而，“Validation_By_Mean”列会在每周为每位名人重复显示。
    # 我们可以取整列的平均值，这实际上会按参赛者数量或独立周数进行加权。
    # 为精确衡量“已验证的周数”，我们采用独立周的计算方式。
    unique_weeks = df.drop_duplicates(['Season', 'Week'])
    val_rate = unique_weeks['Validation_By_Mean'].mean()
    print(f"\nMetric 1: Validation By Mean Accuracy (Per Week)")
    print(f"Overall Accuracy: {val_rate:.2%}")
    
    # 2. CI Width & Entropy
    print(f"\nMetric 2 & 3: Average CI Width and Entropy (By Method)")
    
    grouped = df.groupby('Method')[['CI_Width', 'Entropy']].mean()
    print(grouped)

    
if __name__ == "__main__":
    analyze_results('advanced_fan_vote_simulation_optimized.csv')
