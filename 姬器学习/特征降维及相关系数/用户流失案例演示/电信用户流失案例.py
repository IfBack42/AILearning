"""
项目:
    基于 SHAP 可解释性的用户流失特征降维研究.

运行:
    python main.py

输出:
    outputs/metrics.csv                 模型评估指标
    outputs/selected_features.csv       Lasso筛选出的特征
    outputs/feature_count_compare.png   特征数量对比图
    outputs/shap_summary.png            SHAP全局解释图
    outputs/shap_bar.png                SHAP特征重要性柱状图
    outputs/umap_churn.png              UMAP二维可视化图
    outputs/correlation_heatmap.png     数值特征相关系数热力图
"""

from pathlib import Path
import warnings
import subprocess
import sys

import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np
import pandas as pd
import seaborn as sns
import shap
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.manifold import TSNE
from xgboost import XGBClassifier


warnings.filterwarnings("ignore")

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "WA_Fn-UseC_-Telco-Customer-Churn.csv"
OUTPUT_DIR = BASE_DIR / "outputs"
RANDOM_STATE = 42


def make_output_dir():
    OUTPUT_DIR.mkdir(exist_ok=True)


def setup_plot_style():
    font_candidates = [
        "Microsoft YaHei",
        "SimHei",
        "SimSun",
        "Noto Sans CJK SC",
        "Arial Unicode MS",
    ]
    installed_fonts = {font.name for font in font_manager.fontManager.ttflist}
    chinese_font = next((font for font in font_candidates if font in installed_fonts), "Arial")

    sns.set_theme(
        style="whitegrid",
        rc={
            "font.sans-serif": [chinese_font, "Arial"],
            "font.family": "sans-serif",
            "axes.unicode_minus": False,
        },
    )
    plt.rcParams["font.sans-serif"] = [chinese_font, "Arial"]
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["axes.unicode_minus"] = False
    print(f"Matplotlib中文字体: {chinese_font}")


def make_one_hot_encoder():
    """兼容新版和旧版 scikit-learn 的 OneHotEncoder 参数名."""
    try:
        return OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    except TypeError:
        return OneHotEncoder(handle_unknown="ignore", sparse=False)


def load_and_clean_data():
    df = pd.read_csv(DATA_PATH)

    # customerID只是用户编号, 不代表用户行为, 建模时应删除.
    df = df.drop(columns=["customerID"])

    # TotalCharges原始数据里有空字符串, 需要转成数值, 无法转换的变成缺失值.
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    df = df.dropna().reset_index(drop=True)

    # 目标变量: Yes表示流失, No表示未流失.
    df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})
    return df


def save_correlation_heatmap(df):
    numeric_df = df[["tenure", "MonthlyCharges", "TotalCharges", "SeniorCitizen", "Churn"]]
    corr = numeric_df.corr()

    plt.figure(figsize=(8, 6))
    sns.heatmap(corr, annot=True, cmap="RdBu_r", center=0, fmt=".2f")
    plt.title("数值特征相关系数热力图")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "correlation_heatmap.png", dpi=180)
    plt.close()


def build_preprocessor(x):
    numeric_features = x.select_dtypes(include=["int64", "float64"]).columns.tolist()
    categorical_features = x.select_dtypes(include=["object"]).columns.tolist()

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numeric_features),
            ("cat", make_one_hot_encoder(), categorical_features),
        ]
    )
    return preprocessor, numeric_features, categorical_features


def get_feature_names(preprocessor, numeric_features, categorical_features):
    cat_encoder = preprocessor.named_transformers_["cat"]
    cat_names = cat_encoder.get_feature_names_out(categorical_features).tolist()
    return numeric_features + cat_names


def evaluate_model(model, x_test, y_test, model_name):
    pred = model.predict(x_test)
    return {
        "model": model_name,
        "accuracy": accuracy_score(y_test, pred),
        "precision": precision_score(y_test, pred),
        "recall": recall_score(y_test, pred),
        "f1": f1_score(y_test, pred),
    }


def train_xgboost(x_train, y_train):
    return XGBClassifier(
        n_estimators=160,
        max_depth=3,
        learning_rate=0.05,
        subsample=0.9,
        colsample_bytree=0.9,
        eval_metric="logloss",
        base_score=0.5,
        random_state=RANDOM_STATE,
    ).fit(x_train, y_train)


def select_features_by_lasso(x_train, y_train, feature_names):
    lasso = LogisticRegression(
        penalty="l1",
        solver="liblinear",
        C=0.08,
        class_weight="balanced",
        max_iter=5000,
        random_state=RANDOM_STATE,
    )
    lasso.fit(x_train, y_train)

    coef_abs = np.abs(lasso.coef_[0])
    selected_mask = coef_abs > 1e-6

    # 如果正则化过强导致筛得太少, 就保留系数绝对值最大的前10个特征.
    if selected_mask.sum() < 8:
        top_k = min(10, len(feature_names))
        top_indices = np.argsort(coef_abs)[-top_k:]
        selected_mask = np.zeros_like(coef_abs, dtype=bool)
        selected_mask[top_indices] = True

    importance_df = pd.DataFrame(
        {
            "feature": feature_names,
            "lasso_abs_coef": coef_abs,
            "selected": selected_mask,
        }
    ).sort_values("lasso_abs_coef", ascending=False)
    importance_df.to_csv(OUTPUT_DIR / "selected_features.csv", index=False, encoding="utf-8-sig")
    return selected_mask, importance_df


def save_feature_count_plot(original_count, selected_count):
    plt.figure(figsize=(6, 4))
    bars = plt.bar(["原始特征", "Lasso筛选后"], [original_count, selected_count], color=["#4C78A8", "#F58518"])
    plt.title("特征选择前后维度对比")
    plt.ylabel("特征数量")
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height, str(int(height)), ha="center", va="bottom")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "feature_count_compare.png", dpi=180)
    plt.close()


def save_shap_plots(model, x_test_selected, selected_feature_names):
    # SHAP图用于汇报展示, 取一部分测试集样本可以明显加快运行速度.
    sample_size = min(180, x_test_selected.shape[0])
    x_test_sample = x_test_selected[:sample_size]
    x_test_df = pd.DataFrame(x_test_sample, columns=selected_feature_names)

    background_size = min(80, x_test_selected.shape[0])
    background_df = pd.DataFrame(x_test_selected[:background_size], columns=selected_feature_names)

    def predict_churn_probability(data):
        return model.predict_proba(np.asarray(data))[:, 1]

    masker = shap.maskers.Independent(background_df)
    explainer = shap.Explainer(predict_churn_probability, masker, algorithm="permutation")
    explanation = explainer(
        x_test_df,
        max_evals=2 * len(selected_feature_names) + 1,
        batch_size=50,
    )
    shap_values = explanation.values

    plt.figure()
    shap.summary_plot(shap_values, x_test_df, show=False, max_display=15)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "shap_summary.png", dpi=180, bbox_inches="tight")
    plt.close()

    plt.figure()
    shap.summary_plot(shap_values, x_test_df, plot_type="bar", show=False, max_display=15)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "shap_bar.png", dpi=180, bbox_inches="tight")
    plt.close()


def can_import_umap(timeout_seconds=20):
    try:
        subprocess.run(
            [sys.executable, "-c", "import umap"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=timeout_seconds,
            check=True,
        )
        return True
    except (subprocess.SubprocessError, TimeoutError):
        return False


def save_umap_plot(x_selected, y):
    sample_size = min(2500, x_selected.shape[0])
    rng = np.random.default_rng(RANDOM_STATE)
    sample_indices = rng.choice(x_selected.shape[0], size=sample_size, replace=False)
    x_sample = x_selected[sample_indices]
    y_sample = y[sample_indices]

    method_name = "UMAP"
    if can_import_umap():
        import umap

        reducer = umap.UMAP(n_components=2, n_neighbors=20, min_dist=0.1, random_state=RANDOM_STATE)
        embedding = reducer.fit_transform(x_sample)
    else:
        # 当前机器若UMAP导入异常, 用t-SNE兜底生成二维非线性降维图, 保证项目能完整运行.
        method_name = "t-SNE兜底"
        reducer = TSNE(n_components=2, perplexity=35, learning_rate="auto", init="pca", random_state=RANDOM_STATE)
        embedding = reducer.fit_transform(x_sample)

    plot_df = pd.DataFrame(
        {
            "UMAP1": embedding[:, 0],
            "UMAP2": embedding[:, 1],
            "Churn": np.where(y_sample == 1, "流失", "未流失"),
        }
    )

    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=plot_df, x="UMAP1", y="UMAP2", hue="Churn", alpha=0.75, s=22)
    plt.title(f"{method_name}用户流失二维可视化")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "umap_churn.png", dpi=180)
    plt.close()


def main():
    make_output_dir()
    setup_plot_style()

    df = load_and_clean_data()
    save_correlation_heatmap(df)

    x = df.drop(columns=["Churn"])
    y = df["Churn"]

    x_train_raw, x_test_raw, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.2,
        stratify=y,
        random_state=RANDOM_STATE,
    )

    preprocessor, numeric_features, categorical_features = build_preprocessor(x)
    preprocess_pipeline = Pipeline([("preprocessor", preprocessor)])

    x_train = preprocess_pipeline.fit_transform(x_train_raw)
    x_test = preprocess_pipeline.transform(x_test_raw)
    feature_names = get_feature_names(preprocessor, numeric_features, categorical_features)

    full_model = train_xgboost(x_train, y_train)
    full_metrics = evaluate_model(full_model, x_test, y_test, "XGBoost_全部特征")

    selected_mask, selected_df = select_features_by_lasso(x_train, y_train, feature_names)
    selected_feature_names = np.array(feature_names)[selected_mask].tolist()

    x_train_selected = x_train[:, selected_mask]
    x_test_selected = x_test[:, selected_mask]

    selected_model = train_xgboost(x_train_selected, y_train)
    selected_metrics = evaluate_model(selected_model, x_test_selected, y_test, "XGBoost_Lasso特征选择")

    metrics_df = pd.DataFrame([full_metrics, selected_metrics])
    metrics_df.to_csv(OUTPUT_DIR / "metrics.csv", index=False, encoding="utf-8-sig")

    save_feature_count_plot(len(feature_names), len(selected_feature_names))
    save_shap_plots(selected_model, x_test_selected, selected_feature_names)

    x_all = preprocess_pipeline.transform(x)
    x_all_selected = x_all[:, selected_mask]
    save_umap_plot(x_all_selected, y.to_numpy())

    reduction_ratio = 1 - len(selected_feature_names) / len(feature_names)
    print("项目运行完成")
    print(f"清洗后样本数: {len(df)}")
    print(f"One-Hot后原始特征数: {len(feature_names)}")
    print(f"Lasso筛选后特征数: {len(selected_feature_names)}")
    print(f"降维比例: {reduction_ratio:.2%}")
    print("\n模型指标:")
    print(metrics_df.round(4))
    print("\nLasso筛选出的核心特征:")
    print(selected_df[selected_df["selected"]][["feature", "lasso_abs_coef"]].head(20).to_string(index=False))
    print(f"\n所有结果已保存到: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
