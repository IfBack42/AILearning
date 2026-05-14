from preprocess import preprocess_text
from gensim import corpora, models
import matplotlib.pyplot as plt
import matplotlib
from sklearn.model_selection import train_test_split
import pandas as pd

plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题


def preprocess(n):
    """
    数据预处理函数，与LDAmodel.py保持一致
    """
    # 数据预处理
    all_content = []
    for i in range(1, n + 1):
        with open(f'../reddit/massive_content/reddit_content_{i}.txt', 'r', encoding='utf-8') as f:
            data = f.read()
        raw_comments = [line.strip() for line in data.split('\n') if line.strip()]
        each_text = ' '.join(raw_comments[4:])
        all_content.append(each_text)
    print('-' * 50)
    processed_comments = [preprocess_text(comment) for comment in all_content]
    return processed_comments


def doc_cor(processed_comments):
    """
    构建词典和语料库，与LDAmodel.py保持一致
    """
    # 构建词典
    dictionary = corpora.Dictionary(processed_comments)
    dictionary.filter_extremes(
        no_below=3,  # 保持原设置
        no_above=0.65,  # 保持原设置
        keep_n=2000  # 保持原设置
    )
    print(f"词典大小: {len(dictionary)}")

    # 转换为向量
    corpus = [dictionary.doc2bow(text) for text in processed_comments]
    return corpus, dictionary


def calculate_perplexity(num_topics, corpus, dictionary, passes=25):
    """
    计算给定主题数的困惑度
    """
    lda_model = models.LdaModel(
        corpus,
        num_topics=num_topics,
        id2word=dictionary,
        passes=passes,
        random_state=42
    )

    # 打印主题信息（只在较少主题数时打印，避免输出过多）
    if num_topics <= 10:
        print(f"\n主题数: {num_topics}")
        for idx, topic in lda_model.print_topics(num_words=10):
            print(f"主题 {idx}: {topic}")

    log_perplexity = lda_model.log_perplexity(corpus)
    print(f"主题数 {num_topics} 的对数困惑度: {log_perplexity:.4f}")
    return log_perplexity


def evaluate_topic_numbers(processed_comments, min_topics=5, max_topics=20):
    """
    评估不同主题数的困惑度

    Args:
        processed_comments: 预处理后的评论数据
        min_topics: 最小主题数
        max_topics: 最大主题数
    """
    # 划分数据集
    X_train, X_test = train_test_split(processed_comments, test_size=0.2, random_state=42)

    # 构建训练集词典和语料库
    dictionary_train = corpora.Dictionary(X_train)
    dictionary_train.filter_extremes(no_below=3, no_above=0.65, keep_n=2000)
    corpus_train = [dictionary_train.doc2bow(text) for text in X_train]

    # 将测试集转换为向量形式
    corpus_test = [dictionary_train.doc2bow(text) for text in X_test]

    # 主题范围
    topic_range = range(min_topics, max_topics + 1)

    # 计算训练集和测试集的困惑度
    print("计算训练集困惑度...")
    train_perplexities = [calculate_perplexity(i, corpus_train, dictionary_train) for i in topic_range]

    print("计算测试集困惑度...")
    test_perplexities = [calculate_perplexity(i, corpus_test, dictionary_train) for i in topic_range]

    return topic_range, train_perplexities, test_perplexities


def plot_perplexity(topic_range, train_perplexities, test_perplexities):
    """
    绘制困惑度图表
    """
    # 绘制困惑度折线图
    plt.figure(figsize=(12, 6))
    plt.plot(topic_range, train_perplexities, marker='o', label='训练集', linewidth=2)
    plt.plot(topic_range, test_perplexities, marker='s', label='测试集', linewidth=2)
    plt.xlabel('主题数目')
    plt.ylabel('对数困惑度')
    plt.title('主题数与对数困惑度关系图')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

    # 绘制柱状图对比
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # 训练集柱状图
    ax1.bar(topic_range, train_perplexities, color='skyblue', alpha=0.7)
    ax1.set_xlabel('主题数目')
    ax1.set_ylabel('对数困惑度')
    ax1.set_title('训练集主题-困惑度')
    ax1.grid(True, alpha=0.3)

    # 测试集柱状图
    ax2.bar(topic_range, test_perplexities, color='salmon', alpha=0.7)
    ax2.set_xlabel('主题数目')
    ax2.set_ylabel('对数困惑度')
    ax2.set_title('测试集主题-困惑度')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()

    # 找到测试集最低困惑度对应的主题数
    optimal_topics = topic_range[list(test_perplexities).index(min(test_perplexities))]
    print(f"\n推荐主题数: {optimal_topics} (测试集最低困惑度: {min(test_perplexities):.4f})")

    return optimal_topics


def save_perplexity_results(topic_range, train_perplexities, test_perplexities, filename="perplexity_results.csv"):
    """
    保存困惑度计算结果到CSV文件
    """
    df = pd.DataFrame({
        'num_topics': topic_range,
        'train_perplexity': train_perplexities,
        'test_perplexity': test_perplexities
    })
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"困惑度结果已保存到 {filename}")


if __name__ == '__main__':
    # 读取数据
    n = int(input("总文档数："))

    # 数据预处理
    processed_comments = preprocess(n)

    # 评估不同主题数
    topic_range, train_perplexities, test_perplexities = evaluate_topic_numbers(
        processed_comments,
        min_topics=5,
        max_topics=20
    )

    # 绘制困惑度图表
    optimal_topics = plot_perplexity(topic_range, train_perplexities, test_perplexities)

    # 保存结果
    save_perplexity_results(topic_range, train_perplexities, test_perplexities)

    print(f"\n分析完成！推荐使用 {optimal_topics} 个主题。")
