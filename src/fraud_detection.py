
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report, roc_curve
)

# -----------------------------
# 1. Paths
# -----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "creditcard.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
IMAGE_DIR = os.path.join(BASE_DIR, "images")

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(IMAGE_DIR, exist_ok=True)

# -----------------------------
# 2. Load data
# -----------------------------
df = pd.read_csv(DATA_PATH)

print("\n========== DATASET OVERVIEW ==========")
print("Shape:", df.shape)
print("\nColumns:")
print(df.columns.tolist())
print("\nMissing values:")
print(df.isnull().sum().sum())
print("\nClass distribution:")
print(df["Class"].value_counts())

fraud_count = int((df["Class"] == 1).sum())
total_count = len(df)
fraud_rate = fraud_count / total_count * 100

print(f"\nFraud transactions: {fraud_count:,}")
print(f"Fraud rate: {fraud_rate:.4f}%")

# -----------------------------
# 3. EDA
# -----------------------------
plt.figure(figsize=(7, 5))
sns.countplot(data=df, x="Class")
plt.title("Fraud vs Genuine Transactions")
plt.xlabel("Class (0 = Genuine, 1 = Fraud)")
plt.ylabel("Number of Transactions")
plt.tight_layout()
plt.savefig(os.path.join(IMAGE_DIR, "01_fraud_vs_genuine.png"), dpi=200)
plt.close()

plt.figure(figsize=(8, 5))
sns.boxplot(data=df, x="Class", y="Amount", showfliers=False)
plt.title("Transaction Amount: Fraud vs Genuine")
plt.xlabel("Class")
plt.ylabel("Amount")
plt.tight_layout()
plt.savefig(os.path.join(IMAGE_DIR, "02_amount_by_class.png"), dpi=200)
plt.close()

plt.figure(figsize=(10, 5))
sns.histplot(data=df, x="Time", hue="Class", bins=50, element="step")
plt.title("Transaction Time Distribution")
plt.tight_layout()
plt.savefig(os.path.join(IMAGE_DIR, "03_transaction_time.png"), dpi=200)
plt.close()

plt.figure(figsize=(14, 10))
sns.heatmap(df.corr(), center=0)
plt.title("Correlation Heatmap")
plt.tight_layout()
plt.savefig(os.path.join(IMAGE_DIR, "04_correlation_heatmap.png"), dpi=200)
plt.close()

# -----------------------------
# 4. Prepare data
# -----------------------------
X = df.drop("Class", axis=1)
y = df["Class"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# Scale for Logistic Regression
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# -----------------------------
# 5. Logistic Regression
# -----------------------------
logistic_model = LogisticRegression(
    max_iter=1000,
    class_weight="balanced",
    random_state=42
)
logistic_model.fit(X_train_scaled, y_train)

y_pred_lr = logistic_model.predict(X_test_scaled)
y_prob_lr = logistic_model.predict_proba(X_test_scaled)[:, 1]

# -----------------------------
# 6. Random Forest
# -----------------------------
rf_model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight="balanced",
    n_jobs=-1
)
rf_model.fit(X_train, y_train)

y_pred_rf = rf_model.predict(X_test)
y_prob_rf = rf_model.predict_proba(X_test)[:, 1]

# -----------------------------
# 7. Evaluation
# -----------------------------
def get_metrics(name, y_true, y_pred, y_prob):
    return {
        "Model": name,
        "Accuracy": accuracy_score(y_true, y_pred),
        "Precision": precision_score(y_true, y_pred, zero_division=0),
        "Recall": recall_score(y_true, y_pred, zero_division=0),
        "F1 Score": f1_score(y_true, y_pred, zero_division=0),
        "ROC-AUC": roc_auc_score(y_true, y_prob)
    }

results = pd.DataFrame([
    get_metrics("Logistic Regression", y_test, y_pred_lr, y_prob_lr),
    get_metrics("Random Forest", y_test, y_pred_rf, y_prob_rf)
])

results.to_csv(os.path.join(OUTPUT_DIR, "model_results.csv"), index=False)

print("\n========== MODEL COMPARISON ==========")
print(results.to_string(index=False))

print("\n========== RANDOM FOREST CLASSIFICATION REPORT ==========")
print(classification_report(y_test, y_pred_rf, zero_division=0))

# Confusion matrix for Random Forest
cm = confusion_matrix(y_test, y_pred_rf)
plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt="d")
plt.title("Random Forest - Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.tight_layout()
plt.savefig(os.path.join(IMAGE_DIR, "05_random_forest_confusion_matrix.png"), dpi=200)
plt.close()

# ROC curve
fpr_lr, tpr_lr, _ = roc_curve(y_test, y_prob_lr)
fpr_rf, tpr_rf, _ = roc_curve(y_test, y_prob_rf)

plt.figure(figsize=(8, 6))
plt.plot(fpr_lr, tpr_lr, label="Logistic Regression")
plt.plot(fpr_rf, tpr_rf, label="Random Forest")
plt.plot([0, 1], [0, 1], linestyle="--")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve Comparison")
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(IMAGE_DIR, "06_roc_curve.png"), dpi=200)
plt.close()

# Feature importance
feature_importance = pd.DataFrame({
    "Feature": X.columns,
    "Importance": rf_model.feature_importances_
}).sort_values("Importance", ascending=False)

feature_importance.to_csv(
    os.path.join(OUTPUT_DIR, "feature_importance.csv"),
    index=False
)

plt.figure(figsize=(10, 6))
sns.barplot(
    data=feature_importance.head(10),
    x="Importance",
    y="Feature"
)
plt.title("Top 10 Random Forest Features")
plt.tight_layout()
plt.savefig(os.path.join(IMAGE_DIR, "07_feature_importance.png"), dpi=200)
plt.close()

# Business summary for Power BI
summary = pd.DataFrame({
    "Metric": [
        "Total Transactions",
        "Fraud Transactions",
        "Genuine Transactions",
        "Fraud Rate (%)",
        "Average Transaction Amount",
        "Average Fraud Amount",
        "Average Genuine Amount"
    ],
    "Value": [
        total_count,
        fraud_count,
        int((df["Class"] == 0).sum()),
        fraud_rate,
        df["Amount"].mean(),
        df.loc[df["Class"] == 1, "Amount"].mean(),
        df.loc[df["Class"] == 0, "Amount"].mean()
    ]
})
summary.to_csv(os.path.join(OUTPUT_DIR, "fraud_summary.csv"), index=False)

print("\nProject completed successfully.")
print("Check the 'outputs' and 'images' folders for results.")
