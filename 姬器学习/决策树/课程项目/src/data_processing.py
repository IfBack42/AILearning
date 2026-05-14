# -*- coding: utf-8 -*-
"""数据加载、预处理和训练测试集划分。"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split

from config import RANDOM_STATE


def load_dataset() -> tuple[pd.DataFrame, pd.Series, list[str], np.ndarray]:
    """加载 sklearn 内置乳腺癌数据集。"""
    cancer = load_breast_cancer()
    x = pd.DataFrame(cancer.data, columns=cancer.feature_names)
    y = pd.Series(cancer.target, name="target")
    return x, y, cancer.feature_names.tolist(), cancer.target_names


def preprocess_data(x: pd.DataFrame) -> pd.DataFrame:
    """缺失值处理、异常值检测，并保留原始特征单位。"""
    print("\n========== 数据预处理 ==========")
    print("原始特征维度：", x.shape)
    print("缺失值总数：", int(x.isnull().sum().sum()))

    # 本数据集没有缺失值；保留均值填充流程，让代码适用于一般数值型数据。
    x_filled = x.fillna(x.mean(numeric_only=True))

    # IQR 只用于统计异常值，不删除。决策树对异常值相对不敏感。
    q1 = x_filled.quantile(0.25)
    q3 = x_filled.quantile(0.75)
    iqr = q3 - q1
    outlier_mask = (x_filled < (q1 - 1.5 * iqr)) | (x_filled > (q3 + 1.5 * iqr))
    print("IQR 方法检测到的异常值个数：", int(outlier_mask.sum().sum()))

    print("类别型特征数量：0，无需 One-Hot 编码")
    print("决策树不需要标准化：保留原始特征单位，便于解释切分阈值")
    return x_filled


def split_dataset(
    x: pd.DataFrame,
    y: pd.Series,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """按 7:3 划分训练集和测试集，并保持类别比例一致。"""
    return train_test_split(
        x,
        y,
        test_size=0.3,
        random_state=RANDOM_STATE,
        stratify=y,
    )

