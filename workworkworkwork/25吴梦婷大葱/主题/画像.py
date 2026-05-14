import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import csv
from collections import defaultdict
import os
import warnings

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 忽略特定警告
warnings.filterwarnings("ignore", message="KMeans is known to have a memory leak on Windows with MKL")


def load_topic_probabilities(file_path):
    """
    从CSV文件加载主题概率分布数据
    """
    topic_probs = []
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            # 跳过空行
            if not row:
                continue
            # 解析每个主题的概率分布
            doc_topic_probs = []
            for item in row:
                if item.strip():
                    # 解析 (主题ID, 概率) 格式
                    item = item.strip().strip('()')
                    parts = item.split(',')
                    if len(parts) == 2:
                        topic_id = int(parts[0])
                        prob = float(parts[1])
                        doc_topic_probs.append((topic_id, prob))
            topic_probs.append(doc_topic_probs)
    return topic_probs


def aggregate_user_preferences(topic_probs, user_mapping):
    """
    根据用户映射关系聚合用户主题偏好向量

    Args:
        topic_probs: 每条评论的主题概率分布
        user_mapping: 每条评论对应的用户ID列表
    """
    user_topics = defaultdict(list)

    # 将每条评论的主题分布按用户分组
    for i, user_id in enumerate(user_mapping):
        if i < len(topic_probs):
            user_topics[user_id].append(topic_probs[i])

    # 计算每个用户的平均主题偏好向量
    user_preferences = {}
    for user_id, docs in user_topics.items():
        # 初始化主题向量（修改为9个主题）
        avg_topic_vector = np.zeros(9)
        doc_count = len(docs)

        # 累加所有评论的主题分布
        for doc_topics in docs:
            topic_vector = np.zeros(9)
            for topic_id, prob in doc_topics:
                topic_vector[topic_id] = prob
            avg_topic_vector += topic_vector

        # 计算平均值
        if doc_count > 0:
            avg_topic_vector /= doc_count

        user_preferences[user_id] = avg_topic_vector

    return user_preferences


def cluster_users(user_preferences, n_clusters=5):
    """
    对用户主题偏好进行聚类

    Args:
        user_preferences: 用户主题偏好向量字典
        n_clusters: 聚类数量
    """
    # 提取用户ID和偏好向量
    user_ids = list(user_preferences.keys())
    preference_vectors = np.array(list(user_preferences.values()))

    # 标准化数据
    scaler = StandardScaler()
    scaled_preferences = scaler.fit_transform(preference_vectors)

    # K-means聚类，显式设置n_init参数以避免警告
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    cluster_labels = kmeans.fit_predict(scaled_preferences)

    # 返回用户ID、聚类标签和偏好向量
    return user_ids, cluster_labels, preference_vectors, kmeans


def plot_radar_chart(user_preferences, cluster_labels, user_ids, n_clusters, topic_names=None):
    """
    绘制用户聚类的雷达图

    Args:
        user_preferences: 用户主题偏好向量
        cluster_labels: 聚类标签
        user_ids: 用户ID列表
        n_clusters: 聚类数量
        topic_names: 主题名称列表（可选）
    """
    # 计算每个聚类的平均主题偏好
    cluster_preferences = defaultdict(list)
    for i, label in enumerate(cluster_labels):
        cluster_preferences[label].append(list(user_preferences.values())[i])

    cluster_averages = {}
    for cluster_id, preferences in cluster_preferences.items():
        cluster_averages[cluster_id] = np.mean(preferences, axis=0)

    # 创建雷达图
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(projection='polar'))

    # 设置角度
    num_topics = len(list(cluster_averages.values())[0])
    angles = np.linspace(0, 2 * np.pi, num_topics, endpoint=False)
    angles = np.concatenate((angles, [angles[0]]))  # 闭合图形

    # 设置主题标签
    if topic_names is None:
        topic_names = [f'主题{i + 1}' for i in range(num_topics)]
    else:
        # 确保标签数量与主题数量一致
        topic_names = topic_names[:num_topics] + [f'主题{i + 1}' for i in range(len(topic_names), num_topics)]

    # 为每个聚类绘制雷达图
    colors = ['red', 'blue', 'green', 'orange', 'purple']
    for i, (cluster_id, avg_prefs) in enumerate(cluster_averages.items()):
        # 闭合数据
        data = np.concatenate((avg_prefs, [avg_prefs[0]]))

        # 绘制线条
        ax.plot(angles, data, 'o-', linewidth=2, label=f'聚类 {cluster_id}', color=colors[i % len(colors)])
        # 填充区域
        ax.fill(angles, data, alpha=0.25, color=colors[i % len(colors)])

    # 设置标签
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(topic_names)
    ax.set_ylim(0, np.max(list(cluster_averages.values())) * 1.1)

    # 添加图例和标题
    plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
    plt.title('用户主题偏好聚类雷达图', size=16, color='black', y=1.1)

    # 调整布局
    plt.tight_layout()

    # 保存图像
    plt.savefig('user_cluster_radar_chart.png', dpi=300, bbox_inches='tight')
    plt.show()


def analyze_user_clusters(topic_prob_file, user_mapping, n_clusters=4):
    """
    完整的用户聚类分析流程
    """
    # 加载主题概率分布
    print("加载主题概率分布...")
    topic_probs = load_topic_probabilities(topic_prob_file)
    print(f"加载了 {len(topic_probs)} 条评论的主题分布")

    # 聚合用户偏好
    print("聚合用户主题偏好...")
    user_preferences = aggregate_user_preferences(topic_probs, user_mapping)
    print(f"识别出 {len(user_preferences)} 个用户")

    # 用户聚类
    print("进行用户聚类...")
    user_ids, cluster_labels, preference_vectors, kmeans_model = cluster_users(user_preferences, n_clusters)
    print(f"完成 {n_clusters} 个聚类")

    # 显示聚类结果
    print("\n聚类结果:")
    for i in range(n_clusters):
        users_in_cluster = [user_ids[j] for j, label in enumerate(cluster_labels) if label == i]
        print(f"聚类 {i}: {len(users_in_cluster)} 个用户")

    # 定义主题名称（根据你的图片）
    topic_names = [
        "游戏体验评价",
        "历史文化探讨",
        "视觉表现评价",
        "社区规范管理",
        "角色培养策略",
        "叙事内容鉴赏",
        "修真文化解读",
        "游戏内容体验",
        "情感记忆分享"
    ]

    # 绘制雷达图
    print("生成雷达图...")
    plot_radar_chart(
        user_preferences,
        cluster_labels,
        user_ids,
        n_clusters,
        topic_names=topic_names  # 使用你提供的命名
    )

    return user_ids, cluster_labels, preference_vectors



# 示例用法
if __name__ == "__main__":
    # 设置环境变量以避免Windows内存泄漏警告
    os.environ['OMP_NUM_THREADS'] = '1'

    # 如果topic_probability文件存在，则进行分析
    topic_prob_file = "./topic_probability.csv"
    if os.path.exists(topic_prob_file):
        # 加载主题概率分布以确定评论数量
        topic_probs = load_topic_probabilities(topic_prob_file)
        num_comments = len(topic_probs)
        print(f"检测到 {num_comments} 条评论")

        # 每一行代表一个用户，所以用户ID就是0到num_comments-1
        user_mapping = list(range(num_comments))

        # 执行分析
        user_ids, cluster_labels, preference_vectors = analyze_user_clusters(
            topic_prob_file,
            user_mapping,
            n_clusters=4  # 可以根据需要调整聚类数
        )

        # 保存聚类结果
        cluster_results = pd.DataFrame({
            'user_id': user_ids,
            'cluster': cluster_labels
        })
        cluster_results.to_csv('user_clusters.csv', index=False, encoding='utf-8-sig')
        print("聚类结果已保存到 user_clusters.csv")
    else:
        print(f"未找到主题概率文件: {topic_prob_file}")
        print("请先运行 LDAmodel.py 生成主题概率分布文件")
