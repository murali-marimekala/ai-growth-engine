# update_index.py
import sys
import os
import json
from pathlib import Path

# Add project root to path
sys.path.insert(0, os.getcwd())

from coach import CareerCoach

def main():
    coach = CareerCoach()
    
    # Get progress summary and AI message
    progress_summary = coach.progress_mgr.get_progress_summary()
    ai_message = coach.ai_coach.get_status_message() or "AI coaching not enabled."
    
    # Parse progress for key stats (simple string parsing)
    lines = progress_summary.split('\n')
    total_hours = next((line.split(': ')[1] for line in lines if 'Total Hours Logged:' in line), '0')
    sessions = next((line.split(': ')[1] for line in lines if 'Sessions Completed:' in line), '0')
    current_streak = next((line.split(': ')[1] for line in lines if 'Current Streak:' in line), '0')
    
    # Get current week
    current_focus = coach.roadmap_mgr.get_current_focus()
    current_week_str = current_focus.get('week', 'Week 1')
    # Parse week number from "Week X: ..."
    import re
    match = re.search(r'Week (\d+)', current_week_str)
    current_week_num = int(match.group(1)) if match else 1
    
    # Get daily progress
    daily_state_file = Path("learning_plan/current_day.json")
    daily_progress = "Not started"
    if daily_state_file.exists():
        with open(daily_state_file, 'r') as f:
            daily_data = json.load(f)
        daily_progress = f"Week {daily_data['week']}, Day {daily_data['day']} ({len(daily_data['completed_days'])} days completed)"
    week_links = ""
    for i in range(1, 4):  # Assuming up to week 3 for now
        week_dir = Path(f"learning_plan/week{i}")
        if week_dir.exists():
            week_links += f'<li><a href="learning_plan/week{i}/index.html">Week {i}: {current_focus.get("week", f"Week {i}") if i == current_week_num else f"Week {i}"}</a></li>\n'
    
    # Generate index.html
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>AI/ML Career Transition Coach</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .progress {{ background: #f0f0f0; padding: 10px; border-radius: 5px; }}
        .ai-message {{ background: #e0f7fa; padding: 10px; border-radius: 5px; margin-top: 20px; }}
        ul {{ list-style-type: none; }}
    </style>
</head>
<body>
    <h1>🚀 AI/ML Career Transition Coach</h1>
    <div class="progress">
        <h2>Your Progress</h2>
        <p>Total Hours Logged: {total_hours}</p>
        <p>Sessions Completed: {sessions}</p>
        <p>Current Streak: {current_streak}</p>
        <p>Daily Learning: {daily_progress}</p>
    </div>
    <div class="ai-message">
        <h2>AI Coaching Message</h2>
        <p>{ai_message}</p>
    </div>
    <h2>Week Overviews</h2>
    <ul>
        {week_links}
    </ul>
</body>
</html>
    """
    
    with open("index.html", "w") as f:
        f.write(html_content)
    
    print("index.html updated successfully.")

if __name__ == "__main__":
    main()