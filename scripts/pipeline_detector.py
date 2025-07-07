import pandas as pd
import ast
import joblib
import os
from sklearn.ensemble import RandomForestClassifier

# Load login sessions
df = pd.read_csv("data/login_simulation.csv")
df["keystroke_vector"] = df["keystroke_vector"].apply(ast.literal_eval)

# Load trained ML model
clf = joblib.load("models/keystroke_rf_model.joblib")

# Group by session
grouped = df.groupby("session_id")

results = []

for session_id, group in grouped:
    # Rule-Based Logic
    # WARNING: Must reuse current thresholds as rule_based_detector.py
    flag_rule = 0
    reason = "normal"

    attempts = len(group)
    total_time = group["time_since_last"].sum()
    usernames = group["username"].nunique()
    success_rate = (group["result"] == "success").sum() / attempts if attempts else 0

    vector = group["keystroke_vector"].iloc[0]

    avg_delay = sum(vector) / len(vector) if vector else 0
    std_delay = pd.Series(vector).std() if vector else 0

    # Rule Checks
    if attempts >= 10 and total_time <= 3:
        flag_rule = 1
        reason = "brute_force_pattern"
    elif success_rate < 0.1 and attempts >= 5 and usernames >= 3 and total_time > 60:
        flag_rule = 1
        reason = "evasive_pattern"
    elif std_delay > 0.45:
        flag_rule = 1
        reason = "high_typing_variance"
    elif avg_delay < 0.08:
        flag_rule = 1
        reason = "unrealistic_typing_speed"
    
    # ML Prediction
    feature_names = pd.read_csv("keystroke_ml/processed/keystroke_vectors.csv", nrows = 1).drop(columns = ["label"]).columns.tolist()
    ml_input = pd.DataFrame([vector], columns = feature_names)
    pred_ml = clf.predict(ml_input)[0]

    # Final
    final_flag = 1 if flag_rule == 1 or pred_ml == 1 else 0
    final_reason = "both" if flag_rule == 1 and pred_ml == 1 else ("rule" if flag_rule else "ml" if pred_ml else "none")

    results.append({
        "session_id": session_id,
        "rule_prediction": flag_rule,
        "ml_prediction": pred_ml,
        "final_flag": final_flag,
        "final_reason": final_reason,
        "success_rate": round(success_rate, 3),
        "avg_delay": round(avg_delay, 4),
        "std_delay": round(std_delay, 4),
        "true_label": group["label"].iloc[0]
    })

# Save
os.makedirs("results", exist_ok = True)
pd.DataFrame(results).to_csv("results/pipeline_flags.csv", index = False)
print("Pipeline detection complete. Input saved to results/pipeline_flags.csv")