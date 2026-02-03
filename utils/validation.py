

from datetime import date


def validate_goal_input(goal, hours_per_day, deadline):
    """
    Validate initial goal and constraint inputs.
    Returns a list of error messages (empty if valid).
    """
    errors = []

    
    # Goal Validation
    
    if not goal or goal.strip() == "":
        errors.append("Goal cannot be empty.")

    elif len(goal.strip()) < 10:
        errors.append(
            "Goal description is too short. Please provide more context."
        )

   
    # Time Commitment Validation
   
    if hours_per_day <= 0:
        errors.append("Hours per day must be greater than 0.")

    elif hours_per_day > 16:
        errors.append(
            "Hours per day seems unrealistically high. Please enter a realistic value."
        )

    
    # Deadline Validation
    
    if deadline < date.today():
        errors.append("Deadline cannot be in the past.")

    elif (deadline - date.today()).days < 3:
        errors.append(
            "Deadline is very close. ACHIEVIT works best with at least a few days to plan."
        )

    return errors
