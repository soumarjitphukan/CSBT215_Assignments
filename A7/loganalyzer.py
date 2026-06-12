from typing import List, Dict, Set
from functools import reduce

def total_time_per_user(logs: List[Dict[str, any]]) -> Dict[str, float]:
    def accumulator(acc: Dict[str, float], log: Dict[str, any]) -> Dict[str, float]:
        user = log['user']
        acc[user] = acc.get(user, 0.0) + log['duration']
        return acc
    return reduce(accumulator, logs, {})

def most_active_users(logs: List[Dict[str, any]], k: int) -> List[str]:
    totals = total_time_per_user(logs)
    return sorted(totals, key=lambda u: totals[u], reverse=True)[:k]

def unique_actions(logs: List[Dict[str, any]]) -> Set[str]:
    return {log['action'] for log in logs}


if __name__ == "__main__":
    
    logs = [
        {"user": "CSB23001", "action": "VS Code",      "duration": 45.5},
        {"user": "CSB23002", "action": "YouTube",      "duration": 120.0},
        {"user": "CSB23001", "action": "LeetCode",     "duration": 30.0},
        {"user": "CSB23003", "action": "YouTube",      "duration": 90.0},
        {"user": "CSB23002", "action": "Instagram",    "duration": 15.0},
        {"user": "CSB23001", "action": "VS Code",      "duration": 20.0},
        {"user": "CSB23004", "action": "ChatGPT",      "duration": 5.0},
    ]

    print("Total time per user:")
    print(total_time_per_user(logs))
    print()

    print("Top 3 most active users:")
    print(most_active_users(logs, 3))
    print()

    print("All unique actions:")
    print(unique_actions(logs))


# Time Complexity
# total_time_per_user: O(n * m)
# n = number of logs, m = number of users
# most_active_users: O(n*m + m log m)
# unique_actions: O(n)

# Space Complexity
# user totals dictionary: O(m)
# unique actions set: O(a)
# where m = number of users, a = number of unique actions    