import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import re

# 设置包含中文字符的字体，防止乱码 (根据系统可能需要调整，这里尝试通用设置)
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'sans-serif'] 
plt.rcParams['axes.unicode_minus'] = False

def analyze_and_plot(file_path):
    # 1. 读取数据
    print(f"正在读取文件: {file_path}")
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"读取文件失败: {e}")
        return

    # 2. 数据预处理
    # 找出所有包含分数的列
    score_columns = [col for col in df.columns if 'judge' in col and 'score' in col]
    
    # 将 'N/A' 替换为 NaN，并将列转换为数值型
    for col in score_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # 识别最大的周数
    weeks = set()
    for col in score_columns:
        match = re.search(r'week(\d+)', col)
        if match:
            weeks.add(int(match.group(1)))
    max_week = max(weeks)
    print(f"检测到最大周数为: {max_week}")

    # 提取淘汰信息
    # 假设 'results' 列包含 "Eliminated Week X" 或 "Withdrew Week X"
    def get_elimination_week(result_str):
        if pd.isna(result_str):
            return None
        match = re.search(r'(?:Eliminated|Withdrew|Quit).*Week\s*(\d+)', str(result_str), re.IGNORECASE)
        if match:
            return int(match.group(1))
        return None

    df['elimination_week'] = df['results'].apply(get_elimination_week)

    # 计算每个选手每周的平均分
    processed_data = []

    for index, row in df.iterrows():
        player_name = row['celebrity_name']
        season = row['season']
        
        player_scores = {'season': season, 'name': player_name}
        
        for w in range(1, max_week + 1):
            week_cols = [c for c in score_columns if f'week{w}_' in c]
            scores = row[week_cols]
            
            if scores.isnull().all():
                avg_score = np.nan
            else:
                avg_score = scores.mean()
            
            if avg_score == 0:
                avg_score = np.nan
                
            player_scores[f'week_{w}'] = avg_score
            
        processed_data.append(player_scores)

    df_processed = pd.DataFrame(processed_data)

    # 3. 按 Season 分组绘图
    output_dir = 'season_plots_v2'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"创建输出目录: {output_dir}")

    seasons = sorted(df_processed['season'].unique())
    
    print(f"共发现 {len(seasons)} 个赛季。开始绘图...")

    for season in seasons:
        season_df = df_processed[df_processed['season'] == season]
        
        # 获取该赛季的淘汰数据
        season_eliminations = df[df['season'] == season]['elimination_week'].value_counts().sort_index()
        
        # 创建两个子图：上图为折线图，下图为淘汰人数柱状图
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True, gridspec_kw={'height_ratios': [3, 1]})
        
        # --- 绘制折线图 (ax1) ---
        week_nums = range(1, max_week + 1)
        # 为图例收集句柄和标签
        lines = []
        labels = []
        
        for idx, row in season_df.iterrows():
            scores = [row[f'week_{w}'] for w in week_nums]
            if not all(np.isnan(s) for s in scores):
                line, = ax1.plot(week_nums, scores, marker='o', label=row['name'])
                lines.append(line)
                labels.append(row['name'])

        ax1.set_title(f'Season {season} - Weekly Average Scores & Eliminations')
        ax1.set_ylabel('Average Score')
        ax1.grid(True, linestyle='--', alpha=0.7)
        # 将图例放在图外，避免遮挡
        ax1.legend(bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0., fontsize='small')

        # --- 绘制淘汰柱状图 (ax2) ---
        # 准备数据：确保包含所有周，即使没有人淘汰也是0
        elim_counts = [season_eliminations.get(w, 0) for w in week_nums]
        
        bars = ax2.bar(week_nums, elim_counts, color='salmon', alpha=0.7, label='Eliminated Count')
        ax2.set_ylabel('Eliminations')
        ax2.set_xlabel('Week')
        ax2.set_xticks(week_nums)
        ax2.set_ylim(0, max(elim_counts) + 1 if elim_counts else 1) # 稍微留点空间
        ax2.grid(True, axis='y', linestyle='--', alpha=0.5)
        
        # 在柱子上标具体的数字
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax2.text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(height)}',
                        ha='center', va='bottom')

        plt.tight_layout()
        
        # 保存图片
        save_path = os.path.join(output_dir, f'season_{season}_analysis.png')
        plt.savefig(save_path, bbox_inches='tight') # bbox_inches='tight' 防止图例被截断
        plt.close()
        print(f"已保存 Season {season} 的图表至 {save_path}")

    print("所有分析图表绘制完成！")

if __name__ == "__main__":
    file_path = '2026_MCM_Problem_C_Data.csv'
    analyze_and_plot(file_path)
