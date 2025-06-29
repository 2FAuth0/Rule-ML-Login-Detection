import pandas as pd
from collections import defaultdict
import os
import ast

# Config: thresholds for rules and used for tuning
BRUTE_FORCE_ATTEMPT_THRESHOLD = 10
BRUTE_FORCE_TIME_THRESHOLD = 3 # seconds
EVASIVE_DURATION_THRESHOLD = 60 # total time > 1 minutes
EVASIVE_USERNAME_THRESHOLD = 3 # at least 3 distinct usernames in session
LOW_SUCCESS_RATE = 0.1
HIGH_VARIANCE_THRESOLD = 0.45
LOW_TYPING_TIME_THRESHOLD = 0.08

# Load simulated login data
df = pd.read_csv("data/login_simulation.csv")

# Parse stringified vectors into real lists
df["keystroke_vector"] = df["keystroke_vector"].apply(ast.literal_eval)

# Group by session
sessions = df.groupby("session_id")

# Storage for rule-based predictions
results = []

for session_id, group in sessions:
    # Extract All keystroke vectors in the session
    vectors = group["keystroke_vector"].tolist()
    flat_vector = [v for session in vectors for v in session]
    
    if flat_vector:
        avg_delay = sum(flat_vector) / len(flat_vector)
        std_delay = pd.Series(flat_vector).std()
    else:
        avg_delay = 0
        std_delay = 0
    
    usernames = group['username'].nunique()
    attempts = len(group)
    total_time = group['time_since_last'].sum()
    success_count = (group['result'] == "success").sum()
    failure_count = (group['result'] == "failure").sum()
    success_rate = success_count / attempts if attempts else 0
    user_type = group['user_type'].iloc[0] # for sanity check or eval

    flag = 0
    reason = "normal"

    # Rule 1: Brute force - many fast attempts
    if attempts >= BRUTE_FORCE_ATTEMPT_THRESHOLD and total_time <= BRUTE_FORCE_TIME_THRESHOLD:
        flag = 1
        reason = "brute_force_pattern"

    # Rule 2: Evasive - low succuss, spread out, multiple usernames
    elif success_rate < LOW_SUCCESS_RATE and attempts >= 5:
        flag = 1
        reason = "evasive_pattern"

    # Rule 3: suspiciously low success rate but not clearly attack
    elif success_rate < LOW_SUCCESS_RATE and attempts >= 5:
        flag = 1
        reason = "generic_low_success"

    # Rule 4: High variance in typing
    if std_delay > HIGH_VARIANCE_THRESOLD:
        flag = 1
        reason = "high_typing_variance"
    
    # Rule 5: Unrealistically fast typing
    elif avg_delay < LOW_SUCCESS_RATE:
        flag = 1
        reason = "unrealistic_typing_speed"

    results.append({
        "session_id": session_id,
        "username_sample": group['username'].iloc[0],
        "num_attempts": attempts,
        "total_time": total_time,
        "success_rate": round(success_rate, 2),
        "distince_usernames": usernames,
        "rule_prediction": flag,
        "rule_reason": reason,
        "avg_keystroke_delay": round(avg_delay, 4),
        "std_keystroke_delay": round(std_delay, 4),
        "true_label": group['label'].iloc[0]
    })

# Save rule-based results
out_df = pd.DataFrame(results)
os.makedirs("results", exist_ok = True)
out_df.to_csv("results/rule_based_flags.csv", index = False)
print("Rule-based detection complete. Output saved to 'results/rule_based_flags.csv'")