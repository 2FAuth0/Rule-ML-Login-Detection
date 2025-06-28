import pandas as pd
import os
# Path to KeyRecs CSV
DATA_PATH = "data/fixed-text.csv"

# 1) Load the dataset
df = pd.read_csv(DATA_PATH)

# 2) Define your unknown users (normal)
known_ids = [f'p{str(i).zfill(3)}' for i in range(1, 11)] 

# 3) Split into known vs. unknown

known = df[df['participant'].isin(known_ids)].copy()
unknown = df[~df['participant'].isin(known_ids)].copy()

# 4) Assign labels: 0 = normal, 1 = attacker
known['label'] = 0
unknown['label'] = 1

# 5) Combine
combined = pd.concat([known, unknown])

# 6) Extract only the keystroke timing columns
feature_cols = combined.columns[4:-1]
X = combined[feature_cols].copy()
X['label'] = combined['label'].values

# 7) Save for use in ML later
os.makedirs("keystroke_ml/processed", exist_ok = True)
X.to_csv("keystroke_ml/processed/keystroke_vectors.csv", index = False)

print(f"Done. Saved {X.shape[0]} samples with {len(feature_cols)} features + label.")