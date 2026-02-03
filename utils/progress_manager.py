

import json
import os
from datetime import datetime

PROGRESS_FILE = "data/progress.json"


def _load_all():
    if not os.path.exists(PROGRESS_FILE):
        return {}
    with open(PROGRESS_FILE, "r") as f:
        return json.load(f)


def _save_all(data):
    os.makedirs(os.path.dirname(PROGRESS_FILE), exist_ok=True)
    with open(PROGRESS_FILE, "w") as f:
        json.dump(data, f, indent=4)



# Public API
def load_progress(goal_id):
    """
    Load progress for a specific goal.

    Returns:
    {
        "execution": { milestone: { subtask: bool } },
        "computed": { milestone: percentage },
        "last_updated": timestamp
    }
    """
    data = _load_all()
    return data.get(goal_id, {})


def save_progress(goal_id, execution_matrix, computed_progress):
    """
    Save execution-level progress.

    execution_matrix:
        milestone -> { subtask: bool }

    computed_progress:
        milestone -> percentage (0–100)
    """
    data = _load_all()

    data[goal_id] = {
        "execution": execution_matrix,
        "computed": computed_progress,
        "last_updated": datetime.utcnow().isoformat()
    }

    _save_all(data)



# Backward Compatibility

def load_computed_progress(goal_id):
    """
    Convenience method for legacy code paths.
    Returns milestone -> percentage.
    """
    record = load_progress(goal_id)
    return record.get("computed", {})
