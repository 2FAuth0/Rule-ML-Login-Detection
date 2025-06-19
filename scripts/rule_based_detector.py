import pandas as pd
from collections import defaultdict
import os

# Config: thresholds for rules
BRUTE_FORCE_ATTEMPT_THRESHOLD = 10
BRUTE_FORCE_TIME_THRESHOLD = 10 # seconds
EVASIVE_DURATION_THRESHOLD = 120 # total time > 2 minutes
EVASIVE_USERNAME_THRESHOLD = 3 # at least 3 distinct usernames in session

# Load simulated login data
df = pd.read_csv("data/login_simulation.csv")

# Group by session
sessions = df.groupby("session_id")