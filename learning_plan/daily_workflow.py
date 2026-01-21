#!/usr/bin/env python3
"""
Daily Learning Workflow Script
Manages daily AI/ML learning progression with resume capability.
"""

import json
import os
import sys
import webbrowser
from datetime import datetime
from pathlib import Path

class DailyWorkflow:
    def __init__(self, base_dir="learning_plan"):
        self.base_dir = Path(base_dir)
        self.state_file = self.base_dir / "current_day.json"
        self.load_state()

    def load_state(self):
        """Load current progress state."""
        if self.state_file.exists():
            with open(self.state_file, 'r') as f:
                self.state = json.load(f)
        else:
            self.state = {"week": 1, "day": 1, "completed_days": []}

    def save_state(self):
        """Save current progress state."""
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2)

    def get_current_day_path(self):
        """Get path to current day's HTML file."""
        week_dir = self.base_dir / f"week{self.state['week']}"
        day_dir = week_dir / f"day{self.state['day']}"
        html_file = day_dir / "index.html"
        return html_file

    def is_day_completed(self, week, day):
        """Check if a specific day is completed."""
        return f"week{week}_day{day}" in self.state["completed_days"]

    def mark_day_completed(self):
        """Mark current day as completed and advance to next day."""
        day_key = f"week{self.state['week']}_day{self.state['day']}"
        if day_key not in self.state["completed_days"]:
            self.state["completed_days"].append(day_key)

        # Advance to next day
        self.state["day"] += 1
        if self.state["day"] > 7:
            self.state["day"] = 1
            self.state["week"] += 1

        self.save_state()

    def start_day(self):
        """Start the current day's learning session."""
        html_file = self.get_current_day_path()

        if not html_file.exists():
            print(f"Error: Day file not found: {html_file}")
            return

        print(f"🚀 Starting Week {self.state['week']}, Day {self.state['day']}")
        print(f"Opening: {html_file}")
        print("\nInstructions:")
        print("1. Study the topic in the opened page")
        print("2. Work on any mini-projects or exercises")
        print("3. When done, run this script again with --complete to mark as done")
        print("4. Log your session with: python coach.py log <hours> \"<topics>\"")

        # Open in browser
        webbrowser.open(f"file://{html_file.absolute()}")

    def complete_day(self):
        """Mark current day as completed."""
        print(f"✅ Marking Week {self.state['week']}, Day {self.state['day']} as completed")
        self.mark_day_completed()
        print(f"📅 Next: Week {self.state['week']}, Day {self.state['day']}")

    def show_progress(self):
        """Show current progress."""
        print("📊 Daily Learning Progress")
        print(f"Current: Week {self.state['week']}, Day {self.state['day']}")
        print(f"Completed: {len(self.state['completed_days'])} days")
        if self.state["completed_days"]:
            print("Completed days:", ", ".join(self.state["completed_days"][-5:]))  # Show last 5

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Daily AI/ML Learning Workflow")
    parser.add_argument("--complete", action="store_true", help="Mark current day as completed")
    parser.add_argument("--progress", action="store_true", help="Show progress")
    parser.add_argument("--reset", action="store_true", help="Reset to day 1")

    args = parser.parse_args()

    workflow = DailyWorkflow()

    if args.reset:
        workflow.state = {"week": 1, "day": 1, "completed_days": []}
        workflow.save_state()
        print("🔄 Reset to Week 1, Day 1")
        return

    if args.progress:
        workflow.show_progress()
        return

    if args.complete:
        workflow.complete_day()
        return

    # Default: start current day
    workflow.start_day()

if __name__ == "__main__":
    main()