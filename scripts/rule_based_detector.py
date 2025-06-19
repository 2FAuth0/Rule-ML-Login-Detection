import pandas as pd
from collections import defaultdict
import os

# Config: thresholds for rules and used for tuning
BRUTE_FORCE_ATTEMPT_THRESHOLD = 10
BRUTE_FORCE_TIME_THRESHOLD = 3 # seconds
EVASIVE_DURATION_THRESHOLD = 60 # total time > 1 minutes
EVASIVE_USERNAME_THRESHOLD = 3 # at least 3 distinct usernames in session
LOW_SUCCESS_RATE = 0.1

# Load simulated login data
df = pd.read_csv("data/login_simulation.csv")

# Group by session
sessions = df.groupby("session_id")

# Storage for rule-based predictions
results = []

for session_id, group in sessions:
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

    results.append({
        "session_id": session_id,
        "username_sample": group['username'].iloc[0],
        "num_attempts": attempts,
        "total_time": total_time,
        "success_rate": round(success_rate, 2),
        "distince_usernames": usernames,
        "rule_prediction": flag,
        "rule_reason": reason,
        "true_label": group['label'].iloc[0]
    })

# Save rule-based results
out_df = pd.DataFrame(results)
os.makedirs("results", exist_ok = True)
out_df.to_csv("results/rule_based_flags.csv", index = False)
print("Rule-based detection complete. Output saved to 'results/rule_based_flags.csv'")