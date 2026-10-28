import pandas as pd
import numpy as np
import json
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import sys

try:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

print("=" * 70)
print("[INFO] SMART CAMPUS - TRAINING ML MODEL ON INDIAN ENGINEERING PLACEMENT DATASET 2026")
print("=" * 70)

DATASET_FILE = "indian_engineering_placement_2026.csv"

# 1. Load dataset
df = pd.read_csv(DATASET_FILE)
print(f"Loaded dataset '{DATASET_FILE}': {df.shape[0]} rows, {df.shape[1]} columns")

# 2. Define Features & Target
feature_cols = [
    "CGPA",
    "Attendance_Percentage",
    "Aptitude_Score",
    "DSA_Problems_Solved",
    "Projects_Count",
    "Internships_Count",
    "Certifications_Count",
    "Communication_Score"
]

X = df[feature_cols]
# Binary Target: 1 = Placed, 0 = Not Placed
y = df["Placement_Status"].apply(lambda status: 1 if str(status).strip().lower() == "placed" else 0)

print(f"Target distribution:\n{y.value_counts()}")

# 3. Train-Test Split (80% Train, 20% Test)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

print(f"Train samples: {len(X_train)}, Test samples: {len(X_test)}")

# 4. Train Random Forest Classifier
rf_model = RandomForestClassifier(
    n_estimators=100,
    max_depth=12,
    min_samples_split=4,
    random_state=42
)
rf_model.fit(X_train, y_train)

# 5. Evaluate Model
y_pred_train = rf_model.predict(X_train)
y_pred_test = rf_model.predict(X_test)

train_acc = accuracy_score(y_train, y_pred_train)
test_acc = accuracy_score(y_test, y_pred_test)

cm = confusion_matrix(y_test, y_pred_test)
cr = classification_report(y_test, y_pred_test, output_dict=True)

feature_importances = dict(
    zip(feature_cols, [round(float(val), 4) for val in rf_model.feature_importances_])
)
# Sort feature importances descending
sorted_feature_importances = dict(
    sorted(feature_importances.items(), key=lambda item: item[1], reverse=True)
)

print("\n--- Model Evaluation Results ---")
print(f"[OK] Training Accuracy: {train_acc * 100:.2f}%")
print(f"[OK] Testing Accuracy : {test_acc * 100:.2f}%")
print(f"\nConfusion Matrix:\n{cm}")
print(f"\nClassification Report:\n{classification_report(y_test, y_pred_test, target_names=['Not Placed', 'Placed'])}")

print("Feature Importances:")
for feat, imp in sorted_feature_importances.items():
    print(f"  - {feat:25s}: {imp * 100:.2f}%")

# 6. Save Model & Metadata
model_filename = "placement_model.pkl"
joblib.dump(rf_model, model_filename)
print(f"\n[SAVED] Model successfully saved to: {model_filename}")

metadata = {
    "model_name": "Random Forest Classifier",
    "dataset_source": "Indian Engineering Placement Dataset 2026 (Vishwajeet Chandole)",
    "n_estimators": 100,
    "max_depth": 12,
    "total_records": len(df),
    "train_records": len(X_train),
    "test_records": len(X_test),
    "train_accuracy": round(train_acc * 100, 2),
    "test_accuracy": round(test_acc * 100, 2),
    "confusion_matrix": cm.tolist(),
    "feature_importances": sorted_feature_importances,
    "feature_names": feature_cols,
    "classification_report": {
        "Not Placed": {
            "precision": round(cr["0"]["precision"] * 100, 2),
            "recall": round(cr["0"]["recall"] * 100, 2),
            "f1_score": round(cr["0"]["f1-score"] * 100, 2),
            "support": cr["0"]["support"]
        },
        "Placed": {
            "precision": round(cr["1"]["precision"] * 100, 2),
            "recall": round(cr["1"]["recall"] * 100, 2),
            "f1_score": round(cr["1"]["f1-score"] * 100, 2),
            "support": cr["1"]["support"]
        }
    }
}

with open("model_metadata.json", "w", encoding="utf-8") as f:
    json.dump(metadata, f, indent=4)

print("[SAVED] Model metadata saved to: model_metadata.json")

# 7. Sample Prediction Verification
# [CGPA, Attendance_Percentage, Aptitude_Score, DSA_Problems_Solved, Projects_Count, Internships_Count, Certifications_Count, Communication_Score]
sample_student = [[8.5, 88.0, 75.0, 220, 3, 2, 4, 80.0]]
sample_df = pd.DataFrame(sample_student, columns=feature_cols)
prob = rf_model.predict_proba(sample_df)[0][1]
pred = rf_model.predict(sample_df)[0]
print("\n--- Sample Prediction Verification ---")
print(f"Input: {sample_student[0]}")
print(f"Predicted Class: {'Placed' if pred == 1 else 'Not Placed'}")
print(f"Placement Probability: {prob * 100:.2f}%")
print("=" * 70)
