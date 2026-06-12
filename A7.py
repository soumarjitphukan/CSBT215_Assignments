from typing import List, Dict, Set
from functools import reduce


def total_time_per_user(logs: List[Dict]) -> Dict[str, float]:
    users = {log["user"] for log in logs}

    return {
        user: reduce(
            lambda total, log: total + log["duration"] if log["user"] == user else total,
            logs,
            0.0
        )
        for user in users
    }


def most_active_users(logs: List[Dict], k: int) -> List[str]:
    totals = total_time_per_user(logs)

    return [
        user for user, _ in
        sorted(totals.items(), key=lambda x: x[1], reverse=True)[:k]
    ]


def unique_actions(logs: List[Dict]) -> Set[str]:
    return {log["action"] for log in logs}


# Time Complexity
# total_time_per_user: O(n * m)
# n = number of logs, m = number of users
# most_active_users: O(n*m + m log m)
# unique_actions: O(n)

# Space Complexity
# user totals dictionary: O(m)
# unique actions set: O(a)
# where m = number of users, a = number of unique actions


if __name__ == "__main__":
    logs = [
        {"user": "101", "action": "YouTube", "duration": 30.5},
        {"user": "102", "action": "Instagram", "duration": 10},
        {"user": "101", "action": "Google", "duration": 5},
        {"user": "103", "action": "YouTube", "duration": 20},
        {"user": "102", "action": "Google", "duration": 15}
    ]

    print(total_time_per_user(logs))
    print(most_active_users(logs, 2))
    print(unique_actions(logs))