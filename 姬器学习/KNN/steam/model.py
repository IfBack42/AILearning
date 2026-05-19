import math
from collections import Counter


def build_matrix(rows, feature_names):
    """把字典形式的数据转换成 KNN 需要的二维数值矩阵。"""
    return [[float(row[name]) for name in feature_names] for row in rows]


def fit_scaler(matrix):
    """计算训练集每一列特征的均值和标准差，用于后续标准化。"""
    columns = list(zip(*matrix))
    means = [sum(col) / len(col) for col in columns]
    stds = []

    for mean, col in zip(means, columns):
        variance = sum((x - mean) ** 2 for x in col) / len(col)
        std = math.sqrt(variance)
        stds.append(std if std > 1e-12 else 1.0)

    return means, stds


def transform(matrix, means, stds):
    """使用训练集的均值和标准差，对特征矩阵做 Z-score 标准化。"""
    return [[(x - mean) / std for x, mean, std in zip(row, means, stds)] for row in matrix]


def euclidean_squared(a, b):
    """计算两个样本之间的欧氏距离平方，距离越小代表越相似。"""
    return sum((x - y) ** 2 for x, y in zip(a, b))


def knn_predict_one(train_x, train_y, sample, k):
    """预测单个样本：找到最近的 k 个邻居，再用投票决定类别。"""
    distances = []
    for features, label in zip(train_x, train_y):
        distances.append((euclidean_squared(features, sample), label))

    distances.sort(key=lambda item: item[0])
    votes = Counter(label for _, label in distances[:k])
    return votes.most_common(1)[0][0]


def evaluate_knn(train_x, train_y, test_x, test_y, k):
    """用指定 K 值评估 KNN，返回预测结果、准确率、F1 和混淆矩阵。"""
    predictions = [knn_predict_one(train_x, train_y, row, k) for row in test_x]
    labels = sorted(set(train_y) | set(test_y))
    matrix = {actual: Counter() for actual in labels}
    correct = 0

    for actual, pred in zip(test_y, predictions):
        matrix[actual][pred] += 1
        correct += int(actual == pred)

    accuracy = correct / len(test_y)
    metrics = {}
    for label in labels:
        tp = matrix[label][label]
        fp = sum(matrix[other][label] for other in labels if other != label)
        fn = sum(matrix[label][other] for other in labels if other != label)
        precision = tp / (tp + fp) if tp + fp else 0.0
        recall = tp / (tp + fn) if tp + fn else 0.0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
        metrics[label] = {"precision": precision, "recall": recall, "f1": f1}

    macro_f1 = sum(item["f1"] for item in metrics.values()) / len(metrics)
    return predictions, {"accuracy": accuracy, "macro_f1": macro_f1, "by_class": metrics, "matrix": matrix}


def score_predictions(test_y, predictions, labels):
    """根据真实标签和预测标签，计算准确率、每类指标和混淆矩阵。"""
    matrix = {actual: Counter() for actual in labels}
    correct = 0

    for actual, pred in zip(test_y, predictions):
        matrix[actual][pred] += 1
        correct += int(actual == pred)

    accuracy = correct / len(test_y)
    metrics = {}
    for label in labels:
        tp = matrix[label][label]
        fp = sum(matrix[other][label] for other in labels if other != label)
        fn = sum(matrix[label][other] for other in labels if other != label)
        precision = tp / (tp + fp) if tp + fp else 0.0
        recall = tp / (tp + fn) if tp + fn else 0.0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
        metrics[label] = {"precision": precision, "recall": recall, "f1": f1}

    macro_f1 = sum(item["f1"] for item in metrics.values()) / len(metrics)
    return {"accuracy": accuracy, "macro_f1": macro_f1, "by_class": metrics, "matrix": matrix}


def evaluate_knn_for_k_values(train_x, train_y, test_x, test_y, k_values):
    """一次性评估多个 K 值，复用邻居排序来减少重复距离计算。"""
    max_k = max(k_values)
    labels = sorted(set(train_y) | set(test_y))
    predictions_by_k = {k: [] for k in k_values}

    for sample in test_x:
        distances = []
        for features, label in zip(train_x, train_y):
            distances.append((euclidean_squared(features, sample), label))
        distances.sort(key=lambda item: item[0])
        neighbor_labels = [label for _, label in distances[:max_k]]

        for k in k_values:
            votes = Counter(neighbor_labels[:k])
            predictions_by_k[k].append(votes.most_common(1)[0][0])

    results = {}
    for k in k_values:
        results[k] = score_predictions(test_y, predictions_by_k[k], labels)

    return results
