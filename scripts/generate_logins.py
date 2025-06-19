import random
import pandas as pd
from datetime import datetime, timedelta
import uuid
from typing import List, Dict

# Constants for simulation configuration

NUM_NORMAL_USERS = 250
NUM_BRUTE_FORCE_ATTACKERS = 50
NUM_EVASIVE_ATTACKERS = 50

# Helper to generate usernames
def generate_username(prefix: str, index: int) -> str:
    return f"{prefix}_user_{index}"

# Simulates a sequence of login attempts for one user or attacker session
def simulate_login_attempts(user_type: str, user_id: str, outcomes: List[str],
                            min_delay: int, max_delay: int, 
                            varied_usernames: bool = False, 
                            stop_on_success: bool = False) -> List[Dict]:
    logs = []
    last_time = datetime.now()
    session_id = str(uuid.uuid4())

    for attempt, result in enumerate(outcomes):
        delay_secs = random.randint(min_delay, max_delay)
        delay = timedelta(seconds = delay_secs)

        current_time = last_time + delay
        last_time = current_time

        # Determine username
        username = (
            generate_username("normal", random.randint(0, NUM_NORMAL_USERS- 1))
            if varied_usernames
            else generate_username(user_type, user_id)
        )
        

        logs.append({
            "timestamp": current_time.isoformat(),
            "username": username,
            "result": result,
            "user_type": user_type,
            "session_id": session_id,
            "attempt_number": attempt + 1,
            "time_since_last": 0 if attempt == 0 else delay.total_seconds(),
            "label": 0 if user_type == "normal" else 1
        })

        if result == "success" and stop_on_success:
            break

    return logs

# Runs the full simulation and aggregates all logs
def generate_login_simulation() -> pd.DataFrame:
    all_logs = []

    # Normal users: mostly 1-3 login attempts per session
    for i in range(NUM_NORMAL_USERS):
        num_attempts = random.choices([1, 2, 3], weights=[0.7, 0.25, 0.05])[0]
        session_type = random.choices(
            ["one_try", "two_try", "three_try", "give_up"],
            weights = [0.7, 0.2, 0.05, 0.05]
        )[0]
        if session_type == "give_up":
            outcomes = ["failure" , "failure" ,"failure"]
        elif session_type == "three_try":
            outcomes = ["failure" , "failure" ,"success"]
        elif session_type == "two_try":
            outcomes = ["failure" ,"success"]
        else:
            outcomes = ["success"]

        logs = simulate_login_attempts(
            user_type = "normal",
            user_id = str(i),
            outcomes = outcomes,
            min_delay=3,
            max_delay=5,
        )
        all_logs.extend(logs)
    
    # Brute-force attackers: 10-50 rapid fire attempts
    for i in range(NUM_BRUTE_FORCE_ATTACKERS):
        num_attempts = random.randint(10, 50)
        outcomes = ["success" if random.random() < 0.01 else "failure" for _ in range(num_attempts)]
        logs = simulate_login_attempts(
            user_type = "brute_force",
            user_id = str(i),
            outcomes = outcomes,
            min_delay= 0,
            max_delay= 1,
            varied_usernames = True,
            stop_on_success = True
        )
        all_logs.extend(logs)

    # Evasive attackers: 5-20 moderate-paced attempts with username variation
    for i in range(NUM_EVASIVE_ATTACKERS):
        num_attempts = random.randint(5, 20)
        outcomes = ["success" if random.random() < 0.03 else "failure" for _ in range(num_attempts)]
        logs = simulate_login_attempts(
            user_type = "evasive",
            user_id = str(i),
            outcomes = outcomes,
            min_delay = 3,
            max_delay = 15,
            varied_usernames = True,
            stop_on_success = True
        )
        all_logs.extend(logs)
    
    return pd.DataFrame(all_logs)

# Run the simulation and export to CSV
if __name__ == "__main__":
    login_df = generate_login_simulation()
    login_df = login_df.sort_values("timestamp").reset_index(drop = True)
    login_df.to_csv("data/login_simulation.csv", index = False)
    print("Simulation complete. File saved as 'login_simulation.csv'")