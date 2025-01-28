import json
import os
import random
from datetime import datetime, timezone, timedelta

def get_commit_count():
    """Determine how many commits to make based on the day of the week."""
    # Monday, Wednesday, Friday have more commits
    weekday = datetime.now().weekday()
    if weekday in [0, 2, 4]:  # Mon, Wed, Fri
        return random.randint(8, 15)  # High activity
    elif weekday in [1, 3]:  # Tue, Thu
        return random.randint(5, 10)  # Medium activity
    else:  # Weekends
        return random.randint(3, 7)   # Lower activity

def update_activity():
    """Update the activity data file with multiple contributions."""
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    # Create multiple activity files for different types of contributions
    base_files = ['coding', 'documentation', 'testing', 'research']
    current_time = datetime.now(timezone.utc)
    
    commit_count = get_commit_count()
    print(f"Making {commit_count} contributions...")
    
    for i in range(commit_count):
        # Randomly select a contribution type
        activity_type = random.choice(base_files)
        activity_file = os.path.join(data_dir, f'{activity_type}_{i}.json')
        
        # Create activity data with slight time variations
        time_offset = timedelta(minutes=random.randint(1, 59))
        activity_time = (current_time + time_offset).isoformat()
        
        activity_data = {
            "type": activity_type,
            "timestamp": activity_time,
            "details": {
                "files_changed": random.randint(1, 5),
                "lines_added": random.randint(10, 100),
                "lines_removed": random.randint(5, 50),
                "commit_message": f"Update {activity_type} activity #{i+1}"
            }
        }
        
        # Save the activity data
        with open(activity_file, 'w') as f:
            json.dump(activity_data, f, indent=2)
        
        print(f"Created {activity_type} contribution #{i+1}")
    
    # Update summary file
    summary_file = os.path.join(data_dir, 'activity_summary.json')
    if os.path.exists(summary_file):
        with open(summary_file, 'r') as f:
            summary = json.load(f)
    else:
        summary = {
            "total_contributions": 0,
            "streak_days": 0,
            "last_update": "",
            "contribution_types": {}
        }
    
    # Update summary
    summary["total_contributions"] += commit_count
    summary["streak_days"] += 1
    summary["last_update"] = current_time.isoformat()
    
    # Update contribution type counts
    for activity_type in base_files:
        if activity_type not in summary["contribution_types"]:
            summary["contribution_types"][activity_type] = 0
        summary["contribution_types"][activity_type] += sum(1 for _ in range(commit_count) if random.random() < 0.25)
    
    # Save summary
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"Activity updated! Total contributions: {summary['total_contributions']}")

if __name__ == '__main__':
    update_activity()
