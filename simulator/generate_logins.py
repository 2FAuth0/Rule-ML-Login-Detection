import random
import pandas as pd
from datetime import datetime, timedelta
import uuid
from typing import List, Dict

# Constants for simulation configuration

NUM_NORMAL_USERS = 30
NUM_BRUTE_FORCE_ATTACKERS = 10
NUM_EVASIVE_ATTACKERS = 10

# Helper to generate usernames
def generate_username(prefix: str, index: int) -> str:
    return f"{prefix}_user_{index}"

# Simulates a sequence of login attempts for one user or attacker session
def simulate_login_attempts(user_type: str, user_id: str, num_attempts: int,
                            success_rate: float, min_delay: int, max_delay: int,
                            varied_usernames: bool = False) -> List[Dict]:
    logs = []
    last_time = datetime.now()
    session_id = str(uuid.uuid4())

    for attempt in range(num_attempts):
        delay = timedelta(seconds= random.randint(min_delay, max_delay))
        last_time += delay
        success = random.random() < success_rate
        result = "success" if success else "failure"
        username = generate_username(user_type, user_id if not varied_usernames else random.randint(0, NUM_NORMAL_USERS - 1))

        logs.append({
            "timestamp": last_time.isoformat(),
            "username": username,
            "result": result,
            "user_type": user_type,
            "session_id": session_id,
            "attempt_number": attempt + 1,
            "time_since_last": delay.total_seconds()
        })
    return logs

# TODO: Runs the full simulation and aggregates all logs
def generate_login_simulation() -> pd.DataFrame:
    all_logs = []

    # Normal users: mostly 1-3 login attempts per session
    for i in range(NUM_NORMAL_USERS):
        num_attempts = random.choices([1, 2, 3], weights=[0.7, 0.25, 0.05])[0]
        logs = simulate_login_attempts(
            user_type= "normal"
        )
# TODO: Run the simulation and export to CSV